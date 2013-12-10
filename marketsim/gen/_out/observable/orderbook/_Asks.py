from marketsim import registry
from marketsim.ops._function import Function
from marketsim.gen._intrinsic.orderbook.queue import _Asks_Impl
from marketsim import IOrderBook
@registry.expose(["Queue's", "Asks"])
class Asks(Function[float], _Asks_Impl):
    """ 
    """ 
    def __init__(self, book = None):
        from marketsim.gen._out.observable.orderbook._OfTrader import OfTrader
        self.book = book if book is not None else OfTrader()
        _Asks_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'book' : IOrderBook
    }
    def __repr__(self):
        return "Asks" % self.__dict__
    
