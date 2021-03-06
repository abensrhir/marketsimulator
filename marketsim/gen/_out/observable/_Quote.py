from marketsim import registry
from marketsim.gen._out._observable import Observablefloat
from marketsim.gen._intrinsic.observable.quote import Quote_Impl
@registry.expose(["Basic", "Quote"])
class Quote_StringStringString(Observablefloat,Quote_Impl):
    """   and follows the price in scale 1 model unit of time = 1 real day
    """ 
    def __init__(self, ticker = None, start = None, end = None):
        from marketsim.gen._out._observable import Observablefloat
        from marketsim import rtti
        Observablefloat.__init__(self)
        self.ticker = ticker if ticker is not None else "^GSPC"
        
        self.start = start if start is not None else "2001-1-1"
        
        self.end = end if end is not None else "2010-1-1"
        
        rtti.check_fields(self)
        Quote_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'ticker' : str,
        'start' : str,
        'end' : str
    }
    def __repr__(self):
        return "%(ticker)s" % self.__dict__
    
def Quote(ticker = None,start = None,end = None): 
    from marketsim import rtti
    if ticker is None or rtti.can_be_casted(ticker, str):
        if start is None or rtti.can_be_casted(start, str):
            if end is None or rtti.can_be_casted(end, str):
                return Quote_StringStringString(ticker,start,end)
    raise Exception('Cannot find suitable overload for Quote('+str(ticker) +':'+ str(type(ticker))+','+str(start) +':'+ str(type(start))+','+str(end) +':'+ str(type(end))+')')
