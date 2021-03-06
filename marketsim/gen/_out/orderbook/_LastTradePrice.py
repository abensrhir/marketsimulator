from marketsim import registry
from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._intrinsic.orderbook.last_trade import _LastTradePrice_Impl
from marketsim.gen._out._iorderqueue import IOrderQueue
@registry.expose(["Asset", "LastTradePrice"])
class LastTradePrice_IOrderQueue(Observablefloat,_LastTradePrice_Impl):
    """   Returns None if there haven't been any trades
    """ 
    def __init__(self, queue = None):
        from marketsim.gen._out._observable import Observablefloat
        from marketsim.gen._out.orderbook._asks import Asks_IOrderBook as _orderbook_Asks_IOrderBook
        from marketsim import rtti
        Observablefloat.__init__(self)
        self.queue = queue if queue is not None else _orderbook_Asks_IOrderBook()
        
        rtti.check_fields(self)
        _LastTradePrice_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'queue' : IOrderQueue
    }
    def __repr__(self):
        return "LastTradePrice(%(queue)s)" % self.__dict__
    
def LastTradePrice(queue = None): 
    from marketsim.gen._out._iorderqueue import IOrderQueue
    from marketsim import rtti
    if queue is None or rtti.can_be_casted(queue, IOrderQueue):
        return LastTradePrice_IOrderQueue(queue)
    raise Exception('Cannot find suitable overload for LastTradePrice('+str(queue) +':'+ str(type(queue))+')')
