from marketsim import registry
from marketsim.gen._out._ifunction import IFunctionfloat
from marketsim.gen._out._iorderbook import IOrderBook
from marketsim import context
@registry.expose(["Asset", "WeightedPrice"])
class WeightedPrice_IOrderBookFloat(IFunctionfloat):
    """ 
    """ 
    def __init__(self, book = None, alpha = None):
        from marketsim.gen._out.orderbook._oftrader import OfTrader_IAccount as _orderbook_OfTrader_IAccount
        from marketsim import rtti
        self.book = book if book is not None else _orderbook_OfTrader_IAccount()
        self.alpha = alpha if alpha is not None else 0.15
        rtti.check_fields(self)
        self.impl = self.getImpl()
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'book' : IOrderBook,
        'alpha' : float
    }
    def __repr__(self):
        return "[Bid^{%(book)s}]_{%(alpha)s}" % self.__dict__
    
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
        from marketsim.gen._out.orderbook._weightedprice import WeightedPrice_IOrderQueueFloat as _orderbook_WeightedPrice_IOrderQueueFloat
        from marketsim.gen._out.orderbook._bids import Bids_IOrderBook as _orderbook_Bids_IOrderBook
        return _orderbook_WeightedPrice_IOrderQueueFloat(_orderbook_Bids_IOrderBook(self.book),self.alpha)
    
def WeightedPrice(book = None,alpha = None): 
    from marketsim.gen._out._iorderbook import IOrderBook
    from marketsim import rtti
    if book is None or rtti.can_be_casted(book, IOrderBook):
        if alpha is None or rtti.can_be_casted(alpha, float):
            return WeightedPrice_IOrderBookFloat(book,alpha)
    raise Exception('Cannot find suitable overload for WeightedPrice('+str(book) +':'+ str(type(book))+','+str(alpha) +':'+ str(type(alpha))+')')
