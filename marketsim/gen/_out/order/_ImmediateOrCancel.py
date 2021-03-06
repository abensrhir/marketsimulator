from marketsim import registry
from marketsim.gen._out._iorder import IOrder
from marketsim.gen._out._observable import ObservableIOrder
from marketsim.gen._out._iobservable import IObservableIOrder
@registry.expose(["Order", "ImmediateOrCancel"])
class ImmediateOrCancel_IObservableIOrder(ObservableIOrder,IObservableIOrder):
    """ 
      Immediate-Or-Cancel order sends an underlying order to the market and
      immediately sends a cancel request for it.
      It allows to combine market and limit order behaviour:
      the order is either executed immediately
      at price equal or better than given one
      either it is cancelled (and consequently never stored in the order queue).
    """ 
    def __init__(self, proto = None):
        from marketsim.gen._out.order._limit import Limit_SideFloatFloat as _order_Limit_SideFloatFloat
        from marketsim.gen._out._iorder import IOrder
        from marketsim import rtti
        from marketsim.gen._out._observable import ObservableIOrder
        from marketsim import event
        ObservableIOrder.__init__(self)
        self.proto = proto if proto is not None else _order_Limit_SideFloatFloat()
        event.subscribe(self.proto, self.fire, self)
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'proto' : IObservableIOrder
    }
    def __repr__(self):
        return "ImmediateOrCancel(%(proto)s)" % self.__dict__
    
    def __call__(self, *args, **kwargs):
        from marketsim.gen._intrinsic.order.meta.ioc import Order_Impl
        proto = self.proto()
        if proto is None: return None
        
        return Order_Impl(proto)
    
def ImmediateOrCancel(proto = None): 
    from marketsim.gen._out._iorder import IOrder
    from marketsim.gen._out._iobservable import IObservableIOrder
    from marketsim import rtti
    if proto is None or rtti.can_be_casted(proto, IObservableIOrder):
        return ImmediateOrCancel_IObservableIOrder(proto)
    raise Exception('Cannot find suitable overload for ImmediateOrCancel('+str(proto) +':'+ str(type(proto))+')')
