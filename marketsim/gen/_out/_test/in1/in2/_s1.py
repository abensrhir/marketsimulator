from marketsim import registry
from marketsim import context
@registry.expose(["internal tests", "S1"])
class S1_String(str):
    """ 
    """ 
    def __init__(self, y = None):
        from marketsim import rtti
        self.y = y if y is not None else "abc"
        rtti.check_fields(self)
        self.impl = self.getImpl()
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'y' : str
    }
    def __repr__(self):
        return "S1(%(y)s)" % self.__dict__
    
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
        return self.y
    
def S1(y = None): 
    from marketsim import rtti
    if y is None or rtti.can_be_casted(y, str):
        return S1_String(y)
    raise Exception('Cannot find suitable overload for S1('+str(y) +':'+ str(type(y))+')')
