from marketsim import scheduler
from _basic import TwoSides

class _Noise_Impl(TwoSides):
    
    def __init__( self, trader, params):
        self._params = params
        self._orderFactoryT = params.orderFactoryT
        self._eventGen = scheduler.Timer(params.creationIntervalDistr)
    
        TwoSides.__init__(self, trader)
        
    def _orderFunc(self):
        return (self._params.sideDistr(), (int(self._params.volumeDistr()),)) 

