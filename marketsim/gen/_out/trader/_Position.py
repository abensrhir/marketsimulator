from marketsim.ops._all import Observable
from marketsim import Volume
from marketsim import IAccount
from marketsim.gen._intrinsic.trader.props import Position_Impl
from marketsim import registry
@registry.expose(["Trader", "Position"])
class Position_IAccount(Observable[Volume],Position_Impl):
    """   It is negative if trader has sold more assets than has bought and
      positive otherwise
    """ 
    def __init__(self, trader = None):
        from marketsim import types
        from marketsim.ops._all import Observable
        from marketsim import rtti
        from marketsim import Volume
        from marketsim import event
        from marketsim.gen._out.trader._singleproxy import SingleProxy_ as _trader_SingleProxy
        Observable[Volume].__init__(self)
        self.trader = trader if trader is not None else _trader_SingleProxy()
        if isinstance(trader, types.IEvent):
            event.subscribe(self.trader, self.fire, self)
        rtti.check_fields(self)
        Position_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'trader' : IAccount
    }
    def __repr__(self):
        return "Position(%(trader)s)" % self.__dict__
    
def Position(trader = None): 
    from marketsim import IAccount
    from marketsim import rtti
    if trader is None or rtti.can_be_casted(trader, IAccount):
        return Position_IAccount(trader)
    raise Exception('Cannot find suitable overload for Position('+str(trader)+')')
