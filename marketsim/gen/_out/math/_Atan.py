from marketsim import registry
from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._out._ifunction import IFunctionfloat
@registry.expose(["Trigonometric", "Atan"])
class Atan_Float(Observablefloat):
    """ 
    """ 
    def __init__(self, x = None):
        from marketsim.gen._out._observable import Observablefloat
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import rtti
        Observablefloat.__init__(self)
        self.x = x if x is not None else _constant_Float(0.0)
        
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'x' : IFunctionfloat
    }
    def __repr__(self):
        return "Atan(%(x)s)" % self.__dict__
    
    def __call__(self, *args, **kwargs):
        import math
        x = self.x()
        if x is None: return None
        return math.atan(x)
    
def Atan(x = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if x is None or rtti.can_be_casted(x, IFunctionfloat):
        return Atan_Float(x)
    raise Exception('Cannot find suitable overload for Atan('+str(x) +':'+ str(type(x))+')')
