from marketsim import registry
from marketsim import float
from marketsim import float
from marketsim.ops._all import Observable
from marketsim import IAccount
from marketsim import context
@registry.expose(["Trader", "Efficiency"])
class Efficiency_Optional__IAccount_(Observable[float]):
    """ 
    """ 
    def __init__(self, trader = None):
        from marketsim import float
        from marketsim import float
        from marketsim.ops._all import Observable
        from marketsim.gen._out.trader._SingleProxy import SingleProxy as _trader_SingleProxy
        from marketsim import rtti
        from marketsim import _
        from marketsim import event
        Observable[float].__init__(self)
        self.trader = trader if trader is not None else _trader_SingleProxy()
        rtti.check_fields(self)
        self.impl = self.getImpl()
        event.subscribe(self.impl, _(self).fire, self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'trader' : IAccount
    }
    def __repr__(self):
        return "Efficiency(%(trader)s)" % self.__dict__
    
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
        from marketsim.gen._out.observable._Float import Float as _observable_Float
        from marketsim.gen._out.ops._Add import Add as _ops_Add
        from marketsim.gen._out.trader._Balance import Balance as _trader_Balance
        from marketsim.gen._out.orderbook._CumulativePrice import CumulativePrice as _orderbook_CumulativePrice
        from marketsim.gen._out.orderbook._OfTrader import OfTrader as _orderbook_OfTrader
        from marketsim.gen._out.trader._Position import Position as _trader_Position
        return _observable_Float(_ops_Add(_trader_Balance(self.trader),_orderbook_CumulativePrice(_orderbook_OfTrader(self.trader),_trader_Position(self.trader))))
    
Efficiency = Efficiency_Optional__IAccount_
