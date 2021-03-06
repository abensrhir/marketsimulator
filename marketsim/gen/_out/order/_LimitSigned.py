from marketsim.gen._out._observable import ObservableIOrder
from marketsim.gen._out._iorder import IOrder
from marketsim.gen._out._iobservable import IObservableIOrder
from marketsim.gen._out._ifunction import IFunctionfloat
from marketsim import registry
@registry.expose(["Order", "LimitSigned"])
class LimitSigned_FloatFloat(ObservableIOrder,IObservableIOrder):
    """ 
      Limit orders ask to buy or sell some asset at price better than some limit price.
      If a limit order is not competely fulfilled
      it remains in an order book waiting to be matched with another order.
    """ 
    def __init__(self, signedVolume = None, price = None):
        from marketsim.gen._out._iorder import IOrder
        from marketsim.gen._out._observable import ObservableIOrder
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import rtti
        ObservableIOrder.__init__(self)
        self.signedVolume = signedVolume if signedVolume is not None else _constant_Float(1.0)
        
        self.price = price if price is not None else _constant_Float(100.0)
        
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'signedVolume' : IFunctionfloat,
        'price' : IFunctionfloat
    }
    def __repr__(self):
        return "LimitSigned(%(signedVolume)s, %(price)s)" % self.__dict__
    
    def __call__(self, *args, **kwargs):
        from marketsim.gen._out._side import Side
        from marketsim.gen._intrinsic.order.limit import Order_Impl
        signedVolume = self.signedVolume()
        if signedVolume is None: return None
        side = Side.Buy if signedVolume > 0 else Side.Sell
        volume = abs(signedVolume)
        if abs(volume) < 1: return None
        volume = int(volume)
        price = self.price()
        if price is None: return None
        
        return Order_Impl(side, price, volume)
    
def LimitSigned(signedVolume = None,price = None): 
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if signedVolume is None or rtti.can_be_casted(signedVolume, IFunctionfloat):
        if price is None or rtti.can_be_casted(price, IFunctionfloat):
            return LimitSigned_FloatFloat(signedVolume,price)
    raise Exception('Cannot find suitable overload for LimitSigned('+str(signedVolume) +':'+ str(type(signedVolume))+','+str(price) +':'+ str(type(price))+')')
