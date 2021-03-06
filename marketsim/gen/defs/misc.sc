@category = "Basic"
package {
    /**
     *  Function always returning *x*
     */
    @label = "C=%(x)s"
    def constant(x = 1.0) = const(x) : IFunction[Float]

    /**
     *  Trivial observable always returning *x*
     */
    @python.intrinsic.observable("_constant._Constant_Impl")
    @label = "C=%(x)s"
    @trivialObservable = "true"
    def const(x = 1.0) : IObservable[Float]

    /**
     *  Function always returning *x*
     */
    @label = "C=%(x)s"
    def constant(x = 1) = const(x) : IFunction[Int]

    /**
     *  Trivial observable always returning *x*
     */
    @python.intrinsic.observable("_constant._Constant_Impl")
    @label = "C=%(x)s"
    @trivialObservable = "true"
    def const(x = 1) : IObservable[Int]

    /**
     *  Function always returning *True*
     */
    @label = "True"
    def true() = observableTrue() : IFunction[Boolean]

    /**
     *  Function always returning *False*
     */
    @label = "False"
    def false() = observableFalse() : IFunction[Boolean]

    /**
     *  Trivial observable always returning *True*
     */
    @python.intrinsic.observable("_constant._True_Impl")
    @label = "True"
    def observableTrue() : IObservable[Boolean]

    /**
     *  Trivial observable always returning *False*
     */
    @python.intrinsic.observable("_constant._False_Impl")
    @label = "False"
    def observableFalse() : IObservable[Boolean]

    /**
     *  Trivial observable always returning *undefined* or *None* value
     */
    @python.intrinsic("_constant._Null_Impl")
    def null() => Float

    /**
     *  Returns *x* if defined and *elsePart* otherwise
     */
    @python.observable
    @label = "If def(%(x)s) else %(elsePart)s"
    def IfDefined(
             x = constant(1.),
             /** function to take values from when *x* is undefined */
             elsePart = constant(1.)) =

        if x <> null() then x else elsePart

}


