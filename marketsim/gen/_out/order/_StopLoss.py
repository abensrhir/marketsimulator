from marketsim import Order
from marketsim.ops._all import Observable
from marketsim import IFunction
from marketsim import IOrderGenerator
from marketsim import registry
from marketsim import float
@registry.expose(["Order", "StopLoss"])
class StopLoss_IFunctionFloatIOrderGenerator(Observable[Order],IOrderGenerator):
    """ 
      StopLoss order is initialised by an underlying order and a maximal acceptable loss factor.
      It keeps track of position and balance change induced by trades of the underlying order and
      if losses from keeping the position exceed certain limit (given by maximum loss factor),
      the meta order clears its position.
    """ 
    def __init__(self, maxloss = None, proto = None):
        from marketsim import types
        from marketsim.ops._all import Observable
        from marketsim import rtti
        from marketsim.gen._out.order._limit import Limit_SideIFunctionFloatIFunctionFloat as _order_Limit
        from marketsim import event
        from marketsim.gen._out._constant import constant_Float as _constant
        from marketsim import Order
        Observable[Order].__init__(self)
        self.maxloss = maxloss if maxloss is not None else _constant(0.1)
        if isinstance(maxloss, types.IEvent):
            event.subscribe(self.maxloss, self.fire, self)
        self.proto = proto if proto is not None else _order_Limit()
        if isinstance(proto, types.IEvent):
            event.subscribe(self.proto, self.fire, self)
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'maxloss' : IFunction[float],
        'proto' : IOrderGenerator
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
    from marketsim import IFunction
    from marketsim import float
    from marketsim import IOrderGenerator
    from marketsim import rtti
    if maxloss is None or rtti.can_be_casted(maxloss, IFunction[float]):
        if proto is None or rtti.can_be_casted(proto, IOrderGenerator):
            return StopLoss_IFunctionFloatIOrderGenerator(maxloss,proto)
    raise Exception('Cannot find suitable overload for StopLoss('+str(maxloss)+','+str(proto)+')')
