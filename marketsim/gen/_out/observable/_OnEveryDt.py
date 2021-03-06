from marketsim import registry
from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._intrinsic.observable.on_every_dt import _OnEveryDt_Impl
from marketsim.gen._out._ifunction import IFunctionfloat
@registry.expose(["Basic", "OnEveryDt"])
class OnEveryDt_FloatFloat(Observablefloat,_OnEveryDt_Impl):
    """ 
    """ 
    def __init__(self, x = None, dt = None):
        from marketsim.gen._out._observable import Observablefloat
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import rtti
        Observablefloat.__init__(self)
        self.x = x if x is not None else _constant_Float(1.0)
        
        self.dt = dt if dt is not None else 1.0
        
        rtti.check_fields(self)
        _OnEveryDt_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'x' : IFunctionfloat,
        'dt' : float
    }
    def __repr__(self):
        return "[%(x)s]_dt=%(dt)s" % self.__dict__
    
def OnEveryDt(x = None,dt = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if x is None or rtti.can_be_casted(x, IFunctionfloat):
        if dt is None or rtti.can_be_casted(dt, float):
            return OnEveryDt_FloatFloat(x,dt)
    raise Exception('Cannot find suitable overload for OnEveryDt('+str(x) +':'+ str(type(x))+','+str(dt) +':'+ str(type(dt))+')')
