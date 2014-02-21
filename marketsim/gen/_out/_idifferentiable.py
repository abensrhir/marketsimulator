from marketsim.gen._out._ifunction import IFunctionfloat
class IDifferentiable(IFunctionfloat):
    @property
    def Derivative(self):
        from marketsim.gen._out.math._derivative import Derivative
        return Derivative(self)
    
    pass
