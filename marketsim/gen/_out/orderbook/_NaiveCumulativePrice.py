from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._out._iorderbook import IOrderBook
from marketsim.gen._out._iobservable import IObservablefloat
from marketsim import registry
from marketsim import context
@registry.expose(["Asset", "NaiveCumulativePrice"])
class NaiveCumulativePrice_IOrderBookIObservableFloat(Observablefloat):
    """   by taking into account prices only for the best order
    
      Negative *depth* correponds to will buy assets
      Positive *depth* correponds to will sell assets
    """ 
    def __init__(self, book = None, depth = None):
        from marketsim import _
        from marketsim import rtti
        from marketsim.gen._out.orderbook._oftrader import OfTrader_IAccount as _orderbook_OfTrader_IAccount
        from marketsim.gen._out._const import const_Float as _const_Float
        from marketsim import event
        from marketsim.gen._out._observable import Observablefloat
        Observablefloat.__init__(self)
        self.book = book if book is not None else _orderbook_OfTrader_IAccount()
        self.depth = depth if depth is not None else _const_Float(1.0)
        rtti.check_fields(self)
        self.impl = self.getImpl()
        event.subscribe(self.impl, _(self).fire, self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'book' : IOrderBook,
        'depth' : IObservablefloat
    }
    def __repr__(self):
        return "NaiveCumulativePrice(%(book)s, %(depth)s)" % self.__dict__
    
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
        from marketsim.gen._out.ops._less import Less_IObservableFloatFloat as _ops_Less_IObservableFloatFloat
        from marketsim.gen._out.ops._greater import Greater_IObservableFloatFloat as _ops_Greater_IObservableFloatFloat
        from marketsim.gen._out.ops._condition import Condition_IObservableBooleanIObservableFloatFloat as _ops_Condition_IObservableBooleanIObservableFloatFloat
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim.gen._out.orderbook._bestprice import BestPrice_IOrderQueue as _orderbook_BestPrice_IOrderQueue
        from marketsim.gen._out.orderbook._bids import Bids_IOrderBook as _orderbook_Bids_IOrderBook
        from marketsim.gen._out.orderbook._asks import Asks_IOrderBook as _orderbook_Asks_IOrderBook
        from marketsim.gen._out.ops._mul import Mul_IObservableFloatIObservableFloat as _ops_Mul_IObservableFloatIObservableFloat
        from marketsim.gen._out.ops._condition import Condition_IObservableBooleanIObservableFloatIObservableFloat as _ops_Condition_IObservableBooleanIObservableFloatIObservableFloat
        return _ops_Condition_IObservableBooleanIObservableFloatIObservableFloat(_ops_Less_IObservableFloatFloat(self.depth,_constant_Float(0.0)),_ops_Mul_IObservableFloatIObservableFloat(self.depth,_orderbook_BestPrice_IOrderQueue(_orderbook_Asks_IOrderBook(self.book))),_ops_Condition_IObservableBooleanIObservableFloatFloat(_ops_Greater_IObservableFloatFloat(self.depth,_constant_Float(0.0)),_ops_Mul_IObservableFloatIObservableFloat(self.depth,_orderbook_BestPrice_IOrderQueue(_orderbook_Bids_IOrderBook(self.book))),_constant_Float(0.0)))
    
from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._out._ifunction import IFunctionfloat
from marketsim.gen._out._iorderbook import IOrderBook
from marketsim import registry
from marketsim import context
@registry.expose(["Asset", "NaiveCumulativePrice"])
class NaiveCumulativePrice_IOrderBookFloat(Observablefloat):
    """   by taking into account prices only for the best order
    
      Negative *depth* correponds to will buy assets
      Positive *depth* correponds to will sell assets
    """ 
    def __init__(self, book = None, depth = None):
        from marketsim import _
        from marketsim import rtti
        from marketsim.gen._out.orderbook._oftrader import OfTrader_IAccount as _orderbook_OfTrader_IAccount
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim import event
        from marketsim.gen._out._observable import Observablefloat
        Observablefloat.__init__(self)
        self.book = book if book is not None else _orderbook_OfTrader_IAccount()
        self.depth = depth if depth is not None else _constant_Float(1.0)
        rtti.check_fields(self)
        self.impl = self.getImpl()
        event.subscribe(self.impl, _(self).fire, self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'book' : IOrderBook,
        'depth' : IFunctionfloat
    }
    def __repr__(self):
        return "NaiveCumulativePrice(%(book)s, %(depth)s)" % self.__dict__
    
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
        from marketsim.gen._out.ops._greater import Greater_FloatFloat as _ops_Greater_FloatFloat
        from marketsim.gen._out.ops._mul import Mul_FloatIObservableFloat as _ops_Mul_FloatIObservableFloat
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        from marketsim.gen._out.orderbook._bestprice import BestPrice_IOrderQueue as _orderbook_BestPrice_IOrderQueue
        from marketsim.gen._out.orderbook._bids import Bids_IOrderBook as _orderbook_Bids_IOrderBook
        from marketsim.gen._out.ops._condition import Condition_BooleanIObservableFloatIObservableFloat as _ops_Condition_BooleanIObservableFloatIObservableFloat
        from marketsim.gen._out.orderbook._asks import Asks_IOrderBook as _orderbook_Asks_IOrderBook
        from marketsim.gen._out.ops._less import Less_FloatFloat as _ops_Less_FloatFloat
        from marketsim.gen._out.ops._condition import Condition_BooleanIObservableFloatFloat as _ops_Condition_BooleanIObservableFloatFloat
        return _ops_Condition_BooleanIObservableFloatIObservableFloat(_ops_Less_FloatFloat(self.depth,_constant_Float(0.0)),_ops_Mul_FloatIObservableFloat(self.depth,_orderbook_BestPrice_IOrderQueue(_orderbook_Asks_IOrderBook(self.book))),_ops_Condition_BooleanIObservableFloatFloat(_ops_Greater_FloatFloat(self.depth,_constant_Float(0.0)),_ops_Mul_FloatIObservableFloat(self.depth,_orderbook_BestPrice_IOrderQueue(_orderbook_Bids_IOrderBook(self.book))),_constant_Float(0.0)))
    
def NaiveCumulativePrice(book = None,depth = None): 
    from marketsim.gen._out._iorderbook import IOrderBook
    from marketsim.gen._out._iobservable import IObservablefloat
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim import rtti
    if book is None or rtti.can_be_casted(book, IOrderBook):
        if depth is None or rtti.can_be_casted(depth, IObservablefloat):
            return NaiveCumulativePrice_IOrderBookIObservableFloat(book,depth)
    if book is None or rtti.can_be_casted(book, IOrderBook):
        if depth is None or rtti.can_be_casted(depth, IFunctionfloat):
            return NaiveCumulativePrice_IOrderBookFloat(book,depth)
    raise Exception('Cannot find suitable overload for NaiveCumulativePrice('+str(book) +':'+ str(type(book))+','+str(depth) +':'+ str(type(depth))+')')
