from marketsim.gen._out._ifunction import IFunctionIFunctionlistOffloatlistOffloat
from marketsim.gen._out._ifunction import IFunctionIFunctionfloatIFunctionfloat
from marketsim.gen._out._isingleassetstrategy import ISingleAssetStrategy
from marketsim.gen._intrinsic.strategy.multiarmed_bandit import _MultiarmedBandit2_Impl
from marketsim.gen._out._ifunction import IFunctionIAccountISingleAssetStrategy
from marketsim import listOf
from marketsim import registry
from marketsim.gen._out._ifunction import IFunctionIFunctionfloatIAccount
@registry.expose(["Strategy", "MultiArmedBandit"])
class MultiArmedBandit_ListISingleAssetStrategyISingleAssetStrategyIAccountIAccountFloatFloatFloatListFloatListFloat(ISingleAssetStrategy,_MultiarmedBandit2_Impl):
    """  In some moments of time the efficiency of the strategies is evaluated
     These efficiencies are mapped into weights using *weight* and *normilizer*
     functions per every strategy and *corrector* for the whole collection of weights
     These weights are used to choose randomly a strategy to run for the next quant of time.
     All other strategies are suspended
    """ 
    def __init__(self, strategies = None, account = None, weight = None, normalizer = None, corrector = None):
        from marketsim import rtti
        from marketsim.gen._out.strategy.weight.trader._trader_traderefficiencytrend import trader_TraderEfficiencyTrend_Float as _strategy_weight_trader_trader_TraderEfficiencyTrend_Float
        from marketsim.gen._out.strategy._noise import Noise_IEventSideIObservableIOrder as _strategy_Noise_IEventSideIObservableIOrder
        from marketsim.gen._out.strategy.account.inner._inner_virtualmarket import inner_VirtualMarket_ as _strategy_account_inner_inner_VirtualMarket_
        from marketsim.gen._out.strategy.weight.f._f_atanpow import f_AtanPow_Float as _strategy_weight_f_f_AtanPow_Float
        from marketsim.gen._out.strategy.weight.array._array_identityl import array_IdentityL_ as _strategy_weight_array_array_IdentityL_
        self.strategies = strategies if strategies is not None else [_strategy_Noise_IEventSideIObservableIOrder()]
        self.account = account if account is not None else _strategy_account_inner_inner_VirtualMarket_()
        self.weight = weight if weight is not None else _strategy_weight_trader_trader_TraderEfficiencyTrend_Float()
        self.normalizer = normalizer if normalizer is not None else _strategy_weight_f_f_AtanPow_Float()
        self.corrector = corrector if corrector is not None else _strategy_weight_array_array_IdentityL_()
        rtti.check_fields(self)
        _MultiarmedBandit2_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'strategies' : listOf(ISingleAssetStrategy),
        'account' : IFunctionIAccountISingleAssetStrategy,
        'weight' : IFunctionIFunctionfloatIAccount,
        'normalizer' : IFunctionIFunctionfloatIFunctionfloat,
        'corrector' : IFunctionIFunctionlistOffloatlistOffloat
    }
    def __repr__(self):
        return "MultiArmedBandit(%(strategies)s, %(account)s, %(weight)s, %(normalizer)s, %(corrector)s)" % self.__dict__
    
def MultiArmedBandit(strategies = None,account = None,weight = None,normalizer = None,corrector = None): 
    from marketsim.gen._out._ifunction import IFunctionIFunctionfloatIAccount
    from marketsim.gen._out._ifunction import IFunctionIFunctionfloatIFunctionfloat
    from marketsim import rtti
    from marketsim.gen._out._ifunction import IFunctionIAccountISingleAssetStrategy
    from marketsim.gen._out._isingleassetstrategy import ISingleAssetStrategy
    from marketsim import listOf
    from marketsim.gen._out._ifunction import IFunctionIFunctionlistOffloatlistOffloat
    if strategies is None or rtti.can_be_casted(strategies, listOf(ISingleAssetStrategy)):
        if account is None or rtti.can_be_casted(account, IFunctionIAccountISingleAssetStrategy):
            if weight is None or rtti.can_be_casted(weight, IFunctionIFunctionfloatIAccount):
                if normalizer is None or rtti.can_be_casted(normalizer, IFunctionIFunctionfloatIFunctionfloat):
                    if corrector is None or rtti.can_be_casted(corrector, IFunctionIFunctionlistOffloatlistOffloat):
                        return MultiArmedBandit_ListISingleAssetStrategyISingleAssetStrategyIAccountIAccountFloatFloatFloatListFloatListFloat(strategies,account,weight,normalizer,corrector)
    raise Exception('Cannot find suitable overload for MultiArmedBandit('+str(strategies) +':'+ str(type(strategies))+','+str(account) +':'+ str(type(account))+','+str(weight) +':'+ str(type(weight))+','+str(normalizer) +':'+ str(type(normalizer))+','+str(corrector) +':'+ str(type(corrector))+')')
