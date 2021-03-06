from marketsim import registry
from marketsim.gen._out._iaccount import IAccount
from marketsim.gen._intrinsic.strategy.account import _VirtualMarket_Impl
from marketsim.gen._out._isingleassetstrategy import ISingleAssetStrategy
@registry.expose(["Strategy", "VirtualMarket"])
class VirtualMarket_ISingleAssetStrategy(IAccount,_VirtualMarket_Impl):
    """   how it would be traded by sending request.evalMarketOrder
      (note: orders sent by a strategy wrapped into an adaptive strategy may not come to the market
      but we want evaluate in any case would it be profitable or not)
    """ 
    def __init__(self, inner = None):
        from marketsim.gen._out.strategy._noise import Noise_IEventSideIObservableIOrder as _strategy_Noise_IEventSideIObservableIOrder
        from marketsim import rtti
        self.inner = inner if inner is not None else _strategy_Noise_IEventSideIObservableIOrder()
        rtti.check_fields(self)
        _VirtualMarket_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'inner' : ISingleAssetStrategy
    }
    def __repr__(self):
        return "VirtualMarket(%(inner)s)" % self.__dict__
    
def VirtualMarket(inner = None): 
    from marketsim.gen._out._isingleassetstrategy import ISingleAssetStrategy
    from marketsim import rtti
    if inner is None or rtti.can_be_casted(inner, ISingleAssetStrategy):
        return VirtualMarket_ISingleAssetStrategy(inner)
    raise Exception('Cannot find suitable overload for VirtualMarket('+str(inner) +':'+ str(type(inner))+')')
def virtualMarket(): 
    from marketsim.gen._out.strategy.account.inner._inner_virtualmarket import inner_VirtualMarket_ as _strategy_account_inner_inner_VirtualMarket_
    from marketsim import rtti
    return _strategy_account_inner_inner_VirtualMarket_()
    raise Exception('Cannot find suitable overload for virtualMarket('++')')
