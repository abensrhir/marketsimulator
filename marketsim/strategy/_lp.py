import random
from _basic import Strategy
from _one_side import OneSide
from _generic import Generic
from _array import StrategyArray
from _wrap import merge, wrapper, wrapper2
from _lp_side import LiquidityProviderSide, LiquidityProviderSideEx
from marketsim import order, orderbook, scheduler, mathutils, types, registry, bind, meta, trader
from marketsim.types import *

def merge_dict(d, **kwargs):
    ret = d.copy()
    for k in kwargs:
        ret[k] = kwargs[k]
    return ret


class _LiquidityProvider_Impl(Strategy):
    def __init__(self):
        Strategy.__init__(self, None)
        props = { k : getattr(self, k) for k in self._properties.iterkeys() }
        sp = merge_dict(props, side=Side.Sell)
        bp = merge_dict(props, side=Side.Buy) 
        self._sell = LiquidityProviderSide(**sp)
        self._buy = LiquidityProviderSide(**bp)

    _internals = ['_sell', '_buy']
        
        
    def reset(self):
        self._sell.reset()
        self._buy.reset()
    
    def suspend(self, s):
        Strategy.suspend(self, s)
        self._sell.suspend(s)
        self._buy.suspend(s)
        
    @property
    def suspended(self):
        assert self._sell.suspended == self._suspended
        assert self._buy.suspended == self._suspended
        return Strategy.suspended(self)
    
    def dispose(self):
        self._sell.dispose()
        self._buy.dispose()

exec wrapper2('LiquidityProvider',
             """ Liquidity provider is a combination of two LiquidityProviderSide traders 
                 with the same parameters but different trading sides. 
                 
                 It has followng parameters:

                 |orderFactory| 
                     order factory function (default: order.Limit.T)
                     
                 |initialValue| 
                     initial price which is taken if orderBook is empty (default: 100)
                     
                 |creationIntervalDistr|
                     defines intervals of time between order creation 
                     (default: exponential distribution with |lambda| = 1)
                     
                 |priceDistr|
                     defines multipliers for current asset price when price of
                     order to create is calculated (default: log normal distribution with 
                     |mu| = 0 and |sigma| = 0.1)
                     
                 |volumeDistr| 
                     defines volumes of orders to create 
                     (default: exponential distribution with |lambda| = 1)
            """,  
            [('orderFactoryT',          'order.LimitFactory',                   'Side -> (Price, Volume) -> IOrder'),
             ('defaultValue',           '100',                                  'Price'),
             ('creationIntervalDistr',  'mathutils.rnd.expovariate(1.)',        '() -> TimeInterval'),
             ('priceDistr',             'mathutils.rnd.lognormvariate(0., .1)', '() -> float'),
             ('volumeDistr',            'mathutils.rnd.expovariate(.1)',        '() -> Volume')])


def LiquidityProviderEx    (orderFactory            = order.LimitFactory, 
                            defaultValue            = 100., 
                            creationIntervalDistr   = mathutils.rnd.expovariate(1.), 
                            priceDistr              = mathutils.rnd.lognormvariate(0., .1), 
                            volumeDistr             = mathutils.rnd.expovariate(1.)):

    orderBook = orderbook.OfTrader()

    def create(side):
        return LiquidityProviderSideEx(side, 
                                       orderFactory, 
                                       defaultValue, 
                                       creationIntervalDistr, 
                                       priceDistr, 
                                       volumeDistr)

    r = StrategyArray([
            create(Side.Sell),
            create(Side.Buy)
        ])
    
    r._alias = ["Generic", 'LiquidityProvider']
    
    return r

class _Canceller_Impl(object):
    """ Randomly cancels created orders in specific moments of time    
    """
    
    def choiceFunc(self, N):
        return random.randint(0, N-1)

    def _wakeUp_impl(self, _):
        # if we have orders to cancel
        while self._elements <> []:
            # choose an order
            N = len(self._elements)
            idx = self.choiceFunc(N)
            e = self._elements[idx]
            # if the order is invalid
            if e.empty or e.cancelled:
                # put the last order instead of it and repeat the procedure
                if e <> self._elements[-1]:
                    self._elements[idx] = self._elements[-1]
                # it converges since every time we pops an element from the queue
                self._elements.pop()
            else:
                # if order is valid, cancel it
                self._book.process(order.Cancel(e))
                return

    def __init__(self):

        # orders created by trader
        self._elements = []
        self.wakeUp = bind.Method(self, '_wakeUp_impl')
        self._eventGen = scheduler.Timer(self.cancellationIntervalDistr)
        myTrader = trader.SASM_Proxy()
        # start listening its orders sent
        myTrader.on_order_sent += bind.Method(self, 'process')
        self._book = orderbook.OfTrader(myTrader)
        self._eventGen += self.wakeUp
    
    _internals = ['_eventGen']
        
    def dispose(self):
        self._eventGen -= self.wakeUp
        
    def reset(self):
        self._eventGen.schedule()

    def process(self, order):
        """ Puts 'order' to future cancellation list
        """
        self._elements.append(order)

exec wrapper2("Canceller",
             "",
             [('cancellationIntervalDistr', 'mathutils.rnd.expovariate(1.)',    '() -> TimeInterval')])
