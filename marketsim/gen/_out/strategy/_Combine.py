from marketsim import registry
from marketsim.gen._out._isingleassetstrategy import ISingleAssetStrategy
from marketsim.gen._intrinsic.strategy.combine import _Combine_Impl
@registry.expose(["Strategy", "Combine"])
class Combine_ISingleAssetStrategyISingleAssetStrategy(ISingleAssetStrategy,_Combine_Impl):
    """   Can be considered as a particular case of Array strategy
    """ 
    def __init__(self, A = None, B = None):
        from marketsim.gen._out.strategy._noise import Noise_IEventSideIObservableIOrder as _strategy_Noise_IEventSideIObservableIOrder
        from marketsim import rtti
        self.A = A if A is not None else _strategy_Noise_IEventSideIObservableIOrder()
        self.B = B if B is not None else _strategy_Noise_IEventSideIObservableIOrder()
        rtti.check_fields(self)
        _Combine_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'A' : ISingleAssetStrategy,
        'B' : ISingleAssetStrategy
    }
    def __repr__(self):
        return "Combine(%(A)s, %(B)s)" % self.__dict__
    
def Combine(A = None,B = None): 
    from marketsim.gen._out._isingleassetstrategy import ISingleAssetStrategy
    from marketsim import rtti
    if A is None or rtti.can_be_casted(A, ISingleAssetStrategy):
        if B is None or rtti.can_be_casted(B, ISingleAssetStrategy):
            return Combine_ISingleAssetStrategyISingleAssetStrategy(A,B)
    raise Exception('Cannot find suitable overload for Combine('+str(A) +':'+ str(type(A))+','+str(B) +':'+ str(type(B))+')')
