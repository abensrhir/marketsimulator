from marketsim import registry
from marketsim.gen._out._iorderqueue import IOrderQueue
from marketsim.gen._intrinsic.orderbook.proxy import _Bids_Impl
from marketsim.gen._out._iorderbook import IOrderBook
@registry.expose(["Asset", "Bids"])
class Bids_IOrderBook(IOrderQueue,_Bids_Impl):
    """ 
    """ 
    def __init__(self, book = None):
        from marketsim.gen._out.orderbook._oftrader import OfTrader_IAccount as _orderbook_OfTrader_IAccount
        from marketsim import rtti
        self.book = book if book is not None else _orderbook_OfTrader_IAccount()
        rtti.check_fields(self)
        _Bids_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'book' : IOrderBook
    }
    def __repr__(self):
        return "Bids(%(book)s)" % self.__dict__
    
def Bids(book = None): 
    from marketsim.gen._out._iorderbook import IOrderBook
    from marketsim import rtti
    if book is None or rtti.can_be_casted(book, IOrderBook):
        return Bids_IOrderBook(book)
    raise Exception('Cannot find suitable overload for Bids('+str(book) +':'+ str(type(book))+')')
