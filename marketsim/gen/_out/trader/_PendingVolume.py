from marketsim import registry
from marketsim.gen._out._observable import Observableint
from marketsim.gen._intrinsic.trader.props import PendingVolume_Impl
from marketsim.gen._out._iaccount import IAccount
@registry.expose(["Trader", "PendingVolume"])
class PendingVolume_IAccount(Observableint,PendingVolume_Impl):
    """ 
    """ 
    def __init__(self, trader = None):
        from marketsim.gen._out._observable import Observableint
        from marketsim.gen._out.trader._singleproxy import SingleProxy_ as _trader_SingleProxy_
        from marketsim import rtti
        Observableint.__init__(self)
        self.trader = trader if trader is not None else _trader_SingleProxy_()
        
        rtti.check_fields(self)
        PendingVolume_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'trader' : IAccount
    }
    def __repr__(self):
        return "PendingVolume(%(trader)s)" % self.__dict__
    
def PendingVolume(trader = None): 
    from marketsim.gen._out._iaccount import IAccount
    from marketsim import rtti
    if trader is None or rtti.can_be_casted(trader, IAccount):
        return PendingVolume_IAccount(trader)
    raise Exception('Cannot find suitable overload for PendingVolume('+str(trader) +':'+ str(type(trader))+')')
