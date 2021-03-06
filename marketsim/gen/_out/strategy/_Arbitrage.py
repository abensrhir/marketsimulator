from marketsim import registry
from marketsim.gen._out._imultiassetstrategy import IMultiAssetStrategy
from marketsim.gen._intrinsic.strategy.arbitrage import _Arbitrage_Impl
@registry.expose(["Strategy", "Arbitrage"])
class Arbitrage_(IMultiAssetStrategy,_Arbitrage_Impl):
    """  It believes that these assets represent a single asset traded on different venues
     Once an ask at one venue becomes lower than a bid at another venue
     it sends market sell and buy orders in order to exploit this arbitrage possibility
    """ 
    def __init__(self):
        from marketsim import rtti
        
        rtti.check_fields(self)
        _Arbitrage_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        
    }
    def __repr__(self):
        return "Arbitrage" % self.__dict__
    
def Arbitrage(): 
    from marketsim import rtti
    return Arbitrage_()
    raise Exception('Cannot find suitable overload for Arbitrage('++')')
