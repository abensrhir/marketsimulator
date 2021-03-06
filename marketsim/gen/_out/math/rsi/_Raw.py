from marketsim import registry
from marketsim.gen._out._ifunction import IFunctionfloat
from marketsim.gen._out._iobservable import IObservablefloat
from marketsim import context
@registry.expose(["RSI", "Raw"])
class Raw_IObservableFloatFloatFloat(IFunctionfloat):
    """ 
    """ 
    def __init__(self, source = None, timeframe = None, alpha = None):
        from marketsim.gen._out._const import const_Float as _const_Float
        from marketsim import rtti
        self.source = source if source is not None else _const_Float(1.0)
        self.timeframe = timeframe if timeframe is not None else 10.0
        self.alpha = alpha if alpha is not None else 0.015
        rtti.check_fields(self)
        self.impl = self.getImpl()
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'source' : IObservablefloat,
        'timeframe' : float,
        'alpha' : float
    }
    def __repr__(self):
        return "RSIRaw_{%(timeframe)s}^{%(alpha)s}(%(source)s)" % self.__dict__
    
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
        from marketsim.gen._out.ops._div import Div_FloatFloat as _ops_Div_FloatFloat
        from marketsim.gen._out.math.EW._avg import Avg_IObservableFloatFloat as _math_EW_Avg_IObservableFloatFloat
        from marketsim.gen._out.math._upmovements import UpMovements_IObservableFloatFloat as _math_UpMovements_IObservableFloatFloat
        from marketsim.gen._out.math._downmovements import DownMovements_IObservableFloatFloat as _math_DownMovements_IObservableFloatFloat
        return _ops_Div_FloatFloat(_math_EW_Avg_IObservableFloatFloat(_math_UpMovements_IObservableFloatFloat(self.source,self.timeframe),self.alpha),_math_EW_Avg_IObservableFloatFloat(_math_DownMovements_IObservableFloatFloat(self.source,self.timeframe),self.alpha))
    
def Raw(source = None,timeframe = None,alpha = None): 
    from marketsim.gen._out._iobservable import IObservablefloat
    from marketsim import rtti
    if source is None or rtti.can_be_casted(source, IObservablefloat):
        if timeframe is None or rtti.can_be_casted(timeframe, float):
            if alpha is None or rtti.can_be_casted(alpha, float):
                return Raw_IObservableFloatFloatFloat(source,timeframe,alpha)
    raise Exception('Cannot find suitable overload for Raw('+str(source) +':'+ str(type(source))+','+str(timeframe) +':'+ str(type(timeframe))+','+str(alpha) +':'+ str(type(alpha))+')')
