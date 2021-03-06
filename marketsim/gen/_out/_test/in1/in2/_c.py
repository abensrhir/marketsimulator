from marketsim.gen._out._ifunction import IFunctionICandleStick
from marketsim import context

class C_ICandleStickInt(int):
    """ 
    """ 
    def __init__(self, x , p = None):
        from marketsim import rtti
        self.x = x
        self.p = p if p is not None else 12
        rtti.check_fields(self)
        self.impl = self.getImpl()
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'x' : IFunctionICandleStick,
        'p' : int
    }
    def __repr__(self):
        return "C(%(x)s, %(p)s)" % self.__dict__
    
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
        return self.p
    
def C(x = None,p = None): 
    from marketsim.gen._out._ifunction import IFunctionICandleStick
    from marketsim import rtti
    if x is None or rtti.can_be_casted(x, IFunctionICandleStick):
        if p is None or rtti.can_be_casted(p, int):
            return C_ICandleStickInt(x,p)
    raise Exception('Cannot find suitable overload for C('+str(x) +':'+ str(type(x))+','+str(p) +':'+ str(type(p))+')')
