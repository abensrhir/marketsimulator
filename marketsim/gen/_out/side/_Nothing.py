from marketsim import registry
from marketsim.gen._out._ifunction import IFunctionSide
from marketsim import context
@registry.expose(["Side", "Nothing"])
class Nothing_(IFunctionSide):
    """ 
    """ 
    def __init__(self):
        from marketsim import rtti
        
        rtti.check_fields(self)
        self.impl = self.getImpl()
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        
    }
    def __repr__(self):
        return "Nothing" % self.__dict__
    
    def bind(self, ctx):
        self._ctx = ctx.clone()
    
    _internals = ['impl']
    def __call__(self, *args, **kwargs):
        return self.impl()
    
    def reset(self):
        self.impl = self.getImpl()
        ctx = getattr(self, '_ctx', None)
        if ctx: context.bind(self.impl, ctx)
    
    def getImpl(self):
        from marketsim.gen._out.side._observablenothing import observableNothing_ as _side_observableNothing_
        return _side_observableNothing_()
    
def Nothing(): 
    from marketsim import rtti
    return Nothing_()
    raise Exception('Cannot find suitable overload for Nothing('++')')
