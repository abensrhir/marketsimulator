from marketsim.gen._out._observable import ObservableIOrder
from marketsim.gen._out._iorder import IOrder
from marketsim.gen._out._iobservable import IObservableIOrder
from marketsim.gen._out._ifunction import IFunctionfloat
from marketsim import registry
@registry.expose(["Order", "StopLoss"])
class StopLoss_FloatIObservableIOrder(ObservableIOrder,IObservableIOrder):
    """ 
      StopLoss order is initialised by an underlying order and a maximal acceptable loss factor.
      It keeps track of position and balance change induced by trades of the underlying order and
      if losses from keeping the position exceed certain limit (given by maximum loss factor),
      the meta order clears its position.
    """ 
    def __init__(self, maxloss = None, proto = None):
        from marketsim.gen._out.order._limit import Limit_SideFloatFloat as _order_Limit_SideFloatFloat
        from marketsim.gen._out._iorder import IOrder
        from marketsim import rtti
        from marketsim.gen._out._observable import ObservableIOrder
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import event
        ObservableIOrder.__init__(self)
        self.maxloss = maxloss if maxloss is not None else _constant_Float(0.1)
        
        self.proto = proto if proto is not None else _order_Limit_SideFloatFloat()
        event.subscribe(self.proto, self.fire, self)
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'maxloss' : IFunctionfloat,
        'proto' : IObservableIOrder
    }
    def __repr__(self):
        return "StopLoss(%(maxloss)s, %(proto)s)" % self.__dict__
    
    def __call__(self, *args, **kwargs):
        from marketsim.gen._intrinsic.order.meta.stoploss import Order_Impl
        maxloss = self.maxloss()
        if maxloss is None: return None
        
        proto = self.proto()
        if proto is None: return None
        
        return Order_Impl(maxloss, proto)
    
def StopLoss(maxloss = None,proto = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim.gen._out._iorder import IOrder
    from marketsim.gen._out._iobservable import IObservableIOrder
    from marketsim import rtti
    if maxloss is None or rtti.can_be_casted(maxloss, IFunctionfloat):
        if proto is None or rtti.can_be_casted(proto, IObservableIOrder):
            return StopLoss_FloatIObservableIOrder(maxloss,proto)
    raise Exception('Cannot find suitable overload for StopLoss('+str(maxloss) +':'+ str(type(maxloss))+','+str(proto) +':'+ str(type(proto))+')')
