from marketsim import registry
from marketsim.gen._out._ifunction import IFunctionbool
from marketsim import context
@registry.expose(["Basic", "false"])
class false_(IFunctionbool):
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
        return "False" % self.__dict__
    
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
        from marketsim.gen._out._observablefalse import observableFalse_ as _observableFalse_
        return _observableFalse_()
    
def false(): 
    from marketsim import rtti
    return false_()
    raise Exception('Cannot find suitable overload for false('++')')
