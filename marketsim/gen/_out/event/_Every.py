from marketsim import registry
from marketsim.gen._out._ievent import IEvent
from marketsim.gen._intrinsic.event import _Every_Impl
from marketsim.gen._out._ifunction import IFunctionfloat
@registry.expose(["Event", "Every"])
class Every_Float(IEvent,_Every_Impl):
    """ 
    """ 
    def __init__(self, intervalFunc = None):
        from marketsim.gen._out.math.random._expovariate import expovariate_Float as _math_random_expovariate_Float
        from marketsim import rtti
        self.intervalFunc = intervalFunc if intervalFunc is not None else _math_random_expovariate_Float(1.0)
        rtti.check_fields(self)
        _Every_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'intervalFunc' : IFunctionfloat
    }
    def __repr__(self):
        return "Every(%(intervalFunc)s)" % self.__dict__
    
def Every(intervalFunc = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if intervalFunc is None or rtti.can_be_casted(intervalFunc, IFunctionfloat):
        return Every_Float(intervalFunc)
    raise Exception('Cannot find suitable overload for Every('+str(intervalFunc) +':'+ str(type(intervalFunc))+')')
