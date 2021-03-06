class String(object):
    @property
    def Graph(self):
        from marketsim.gen._out.veusz._graph import Graph
        return Graph(self)
    
    def Quote(self, start = None,end = None):
        from marketsim.gen._out.observable._quote import Quote
        return Quote(self,start,end)
    
    def Local(self, tickSize = None,_digitsToShow = None,timeseries = None):
        from marketsim.gen._out.orderbook._local import Local
        return Local(self,tickSize,_digitsToShow,timeseries)
    
    pass
