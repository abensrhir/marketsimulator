from marketsim import registry
from marketsim.gen._out._ievent import IEvent
from marketsim.gen._intrinsic.event import _After_Impl
from marketsim.gen._out._ifunction import IFunctionfloat
@registry.expose(["Event", "After"])
class After_Float(IEvent,_After_Impl):
    """ 
    """ 
    def __init__(self, delay = None):
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import rtti
        self.delay = delay if delay is not None else _constant_Float(10.0)
        rtti.check_fields(self)
        _After_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'delay' : IFunctionfloat
    }
    def __repr__(self):
        return "After(%(delay)s)" % self.__dict__
    
def After(delay = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if delay is None or rtti.can_be_casted(delay, IFunctionfloat):
        return After_Float(delay)
    raise Exception('Cannot find suitable overload for After('+str(delay) +':'+ str(type(delay))+')')
