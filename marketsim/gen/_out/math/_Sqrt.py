from marketsim import registry
from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._out._ifunction import IFunctionfloat
@registry.expose(["Log/Pow", "Sqrt"])
class Sqrt_Float(Observablefloat):
    """ 
    """ 
    def __init__(self, x = None):
        from marketsim.gen._out._observable import Observablefloat
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import rtti
        Observablefloat.__init__(self)
        self.x = x if x is not None else _constant_Float(1.0)
        
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'x' : IFunctionfloat
    }
    def __repr__(self):
        return "\\sqrt{%(x)s}" % self.__dict__
    
    def __call__(self, *args, **kwargs):
        import math
        x = self.x()
        if x is None: return None
        return math.sqrt(x)
    
def Sqrt(x = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if x is None or rtti.can_be_casted(x, IFunctionfloat):
        return Sqrt_Float(x)
    raise Exception('Cannot find suitable overload for Sqrt('+str(x) +':'+ str(type(x))+')')
