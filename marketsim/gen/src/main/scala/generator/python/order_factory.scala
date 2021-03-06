package generator.python

import predef._
import predef.ImportFrom
import scala.Some

object order_factory
        extends gen.PythonGenerator
        with    Typed.BeforeTyping
{
    case class Parameter(p : Typed.Parameter)
            extends base.Parameter
            with    base.SubscribeParameter
    {
        def check_none_aux(name : String) : Code = name match {
            case "volume" =>
                s"if abs($name) < 1: return None" |
                s"$name = int($name)"
            case "signedVolume" =>
                s"side = "||| Typed.topLevel.Side.asCode |||".Buy if signedVolume > 0 else Side.Sell" |
                s"volume = abs(signedVolume)" |
                check_none_aux("volume")

            case _ => ""
        }

        def nullable =
            s"$name = self.$name()" |
            s"if $name is None: return None" |
            check_none_aux(name)

        override def call = name
    }

    abstract class FactoryBase
        extends base.Printer
        with    base.DocString
        with    base.Alias
        with    base.DecoratedName
    {
        def factoryName = f.name

        def raw_params = f.parameters

        // only for curried factories
        def curried : List[Typed.Parameter] = Nil

        def prefix = ""

        def interface = Typed.topLevel.IOrderGenerator

        override def body = super.body | call
    }

    class Factory(val args  : List[String],
                  val f     : Typed.Function)
            extends FactoryBase
            with    base.BaseClass_Observable
            with    base.IntrinsicEx
    {
        if (args.length != 1)
            throw new Exception(s"Annotation $factoryName should have 1 arguments in" +
                    " form (...Order_Impl or ...Factory_Impl)" + "\r\n" + "In function " + f)

        val impl_module = implementation_module

        val is_factory_intrinsic = implementation_class match {
            case "Order_Impl" => false
            case "Factory_Impl" => true
            case _ => throw new Exception("Implementation class should be either Order_Impl or Factory_Impl" +
                    "\r\n" + "In function " + f)
        }

        def mkParam(p : Typed.Parameter) = order_factory.Parameter(p)
        type Parameter = order_factory.Parameter

        def impl = TypesBound.ImplementationClass(implementation_class, implementation_module)

        override def observableBase =
            if (is_factory_intrinsic)
                impl
            else
                super.observableBase

        override def base_class_list = interface :: super.base_class_list

        def nullable_fields = join_fields({ _.nullable}, crlf)

        override def call = if (is_factory_intrinsic) "" else super.call

        override def call_fields : Code = if (factoryName endsWith "Signed") {
            val original_f = f.parent getFunction (factoryName replace ("Signed", ""))
            val original = gen.generationUnit(original_f.head).get.asInstanceOf[Factory]
            original.call_fields
        }  else
            super.call_fields

        override def call_body = nullable_fields |
                "return "||| impl.asCode |||s"($call_fields)"
    }

    def paramTypesInPython(curried: List[Typed.Parameter]) = {
        if (curried.length == 1)
            curried(0).ty
        else
            TypesBound.Tuple(curried map { _.ty })
    }

    def curriedTypes(curried : List[Typed.Parameter]) = {
        val curr_types = TypesBound.Tuple(curried map { _.ty })

        curr_types.asCode
    }

    def curriedTypesAsList(curried : List[Typed.Parameter]) : Code = curried match {
        case Nil => predef.stop
        case x :: Nil => x.ty.asCode
        case x :: y => x.ty.asCode ||| "," ||| curriedTypesAsList(y)
    }

    def generatePython(/** arguments of the annotation */ args  : List[String])
                      (/** function to process         */ f     : Typed.Function) =
    {
        new Factory(args, f)
    }

    def extract(names : List[String], parameters : List[AST.Parameter])
        : Option[(List[AST.Parameter], List[AST.Parameter])] = names match
    {
        case Nil =>
            Some((Nil, parameters))

        case n :: tl =>

            val (curried, rest_0) = parameters partition { _.name == n}

            if (curried.length == 1) {
                extract(tl, rest_0) match {
                    case Some((c_1, r_1)) => Some((curried(0) :: c_1, r_1))
                    case None             => None
                }
            }
            else
                None
    }

    def locate(path : List[String], n : NameTable.Scope) : NameTable.Scope  =
        path match  {
            case Nil => n
            case x :: xs => locate(xs, n getPackageOrCreate x)
        }

    def beforeTyping(/** arguments of the annotation */ args  : List[String])
                    (/** function to process         */ f     : AST.FunDef,
                                                        scope : NameTable.Scope)
    {
        def hasProto(parameters : List[AST.Parameter]) = parameters exists { _.name == "proto" }

        def createParam(name : String, ty : AST.Type = AST.float_function_t) =
            AST.Parameter(name, Some(ty), None, Nil)

        val sideParam = createParam("side", AST.side_function_t)
        val volumeParam = createParam("volume")
        val signedVolumeParam = createParam("signedVolume")
        val priceParam = createParam("price")



        val factorySigned = extract("side" :: "volume" :: Nil, f.parameters) map {
            case (sv, rest) => ()
                val fc =
                    f.copy(
                        name = f.name + "Signed",
                        parameters =
                                AST.Parameter(
                                    "signedVolume",
                                    Some(AST.float_function_t),
                                    sv(1).initializer,
                                    "signed volume" :: Nil) ::
                                rest,
                        ty = f.ty map scope.fullyQualifyType)

                locate("signed" :: Nil, scope) add AST.FunAlias(
                    f.name, "" :: "order" :: fc.name :: Nil)

                scope add fc

                fc
        }

        def partialFactory(curried  : List[AST.Parameter],
                           base_    : AST.FunDef = f) =
        {
            //println(s"partial factory $curried for $base_")
            val base = base_
            val prefix = (curried map { _.name } mkString "") + "_"
            val prefixed = prefix + base.name

            val orig_path = base.name split "_"
            val (orig_scope, brief_name_arr) = orig_path.splitAt(orig_path.length - 1)
            val u_prefix = curried map { _.name } mkString "_"
            val alias = u_prefix :: orig_scope.toList
            val brief_name = brief_name_arr(0)

            def addPrefix(e : Option[AST.Expr]) = {
                val call = e.get.asInstanceOf[AST.FunCall]
                def insertPrefix(in : List[String]): List[String] = {
                    in match {
                        case "" :: "order" :: tl =>
                            "" :: "order" :: insertPrefix(tl)
                        case last :: Nil =>
                            alias :+ last
                        case "price" :: tl if (curried find { _.name == "price" }).nonEmpty =>
                            ((curried map { _.name } filter { _ != "price"}  mkString "_") :: "price" :: tl) filter { _ != "" }
                        case tl =>
                            u_prefix :: tl
                    }
                }

                Some(call.copy(name = insertPrefix(call.name)))
            }

            lazy val withAdjustedProto = base.parameters map {
                case x if x.name == "proto" => x.copy(initializer = addPrefix(x.initializer))
                case x => x
            }

            val ty = Some(AST.FunctionType(curried map { _.ty.get }, base.ty.get))

            (extract(curried map { _.name }, base.parameters) match {
                case Some((cr, rest)) =>
                    Some(base.copy(
                        name = prefixed,
                        parameters = rest,
                        decorators =
                                AST.Annotation(
                                    order_factory_curried.name.split('.').toList,
                                    base.name :: Nil) :: Nil,
                        ty = ty map scope.fullyQualifyType))
                case _ =>
                    if (hasProto(base.parameters)){
                        Some(base.copy(
                            name = prefixed,
                            parameters = withAdjustedProto,
                            decorators =
                                    AST.Annotation(
                                        order_factory_on_proto.name.split('.').toList,
                                        base.name :: Nil) :: Nil,
                            ty = ty map scope.fullyQualifyType))
                    }
                    else
                        None
            }) map  { fc =>
                locate(alias, scope) add AST.FunAlias(
                    brief_name, "" :: "order" :: "_curried" :: prefixed :: Nil)

                val curried = scope getPackageOrCreate "_curried"

                if (!(curried.functions contains fc.name))
                    curried add fc

                fc
            }
        }

        val signedVolumeFactory = factorySigned flatMap { partialFactory(signedVolumeParam :: Nil, _) }
        val priceFactory = partialFactory(priceParam :: Nil)
        val sideFactory = partialFactory(sideParam :: Nil)
        val volumeFactory = partialFactory(volumeParam :: Nil)
        val sidePriceFactory = partialFactory(sideParam :: priceParam :: Nil)
        val sideVolumeFactory = partialFactory(sideParam :: volumeParam :: Nil)
        val side_priceFactory = priceFactory flatMap { partialFactory(sideParam :: Nil, _) }
        val volume_priceFactory = priceFactory flatMap { partialFactory(volumeParam :: Nil, _) }
        val sideVolume_priceFactory = priceFactory flatMap { partialFactory(sideParam :: volumeParam :: Nil, _) }
    }

    val name = "python.order.factory"
}
