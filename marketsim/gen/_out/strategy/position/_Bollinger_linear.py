from marketsim import registry
from marketsim import Volume
from marketsim import Volume
from marketsim.ops._all import Observable
from marketsim import float
from marketsim import IObservable
from marketsim import float
from marketsim import ISingleAssetTrader
from marketsim import context
@registry.expose(["Volume function", "Bollinger_linear"])
class Bollinger_linear_Optional__Float___Optional__IObservable__Float____Optional__ISingleAssetTrader_(Observable[Volume]):
    """ 
    """ 
    def __init__(self, alpha = None, k = None, trader = None):
        from marketsim import Volume
        from marketsim import Volume
        from marketsim.ops._all import Observable
        from marketsim.gen._out._const import const as _const
        from marketsim.gen._out.trader._SingleProxy import SingleProxy as _trader_SingleProxy
        from marketsim import rtti
        from marketsim import _
        from marketsim import event
        Observable[Volume].__init__(self)
        self.alpha = alpha if alpha is not None else 0.15
        self.k = k if k is not None else _const(0.5)
        self.trader = trader if trader is not None else _trader_SingleProxy()
        rtti.check_fields(self)
        self.impl = self.getImpl()
        event.subscribe(self.impl, _(self).fire, self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'alpha' : float,
        'k' : IObservable[float],
        'trader' : ISingleAssetTrader
    }
    def __repr__(self):
        return "Bollinger_linear(%(alpha)s, %(k)s, %(trader)s)" % self.__dict__
    
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
        from marketsim.gen._out.strategy.position._DesiredPosition import DesiredPosition as _strategy_position_DesiredPosition
        from marketsim.gen._out.observable._OnEveryDt import OnEveryDt as _observable_OnEveryDt
        from marketsim.gen._out.ops._Mul import Mul as _ops_Mul
        from marketsim.gen._out.math.EW._RelStdDev import RelStdDev as _math_EW_RelStdDev
        from marketsim.gen._out.orderbook._MidPrice import MidPrice as _orderbook_MidPrice
        from marketsim.gen._out.orderbook._OfTrader import OfTrader as _orderbook_OfTrader
        return _strategy_position_DesiredPosition(_observable_OnEveryDt(1.0,_ops_Mul(_math_EW_RelStdDev(_orderbook_MidPrice(_orderbook_OfTrader(self.trader)),self.alpha),self.k)),self.trader)
    
Bollinger_linear = Bollinger_linear_Optional__Float___Optional__IObservable__Float____Optional__ISingleAssetTrader_
