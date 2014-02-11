from marketsim import IDifferentiable
from marketsim import registry
from marketsim.gen._intrinsic.observable.derivative import _Derivative_Impl
from marketsim.ops._function import Function
from marketsim import float
@registry.expose(["Basic", "Derivative"])
class Derivative_IDifferentiable(Function[float],_Derivative_Impl):
    """  *x* should provide *derivative* member
    """ 
    def __init__(self, x = None):
        from marketsim.gen._out.math.EW._avg import Avg_IObservableFloatFloat as _math_EW_Avg
        from marketsim import rtti
        self.x = x if x is not None else _math_EW_Avg()
        rtti.check_fields(self)
        _Derivative_Impl.__init__(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'x' : IDifferentiable
    }
    def __repr__(self):
        return "\\frac{d%(x)s}{dt}" % self.__dict__
    
def Derivative(x = None): 
    from marketsim import IDifferentiable
    from marketsim import rtti
    if x is None or rtti.can_be_casted(x, IDifferentiable):
        return Derivative_IDifferentiable(x)
    raise Exception('Cannot find suitable overload for Derivative('+str(x)+')')
