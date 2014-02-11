from marketsim import registry
from marketsim import float
from marketsim import listOf
from marketsim import IFunction
@registry.expose(["Strategy", "array_ChooseTheBest"])
class array_ChooseTheBest_(IFunction[listOf(float), listOf(float)]):
    """   having 1 at the index of the maximal element and 0 are at the rest
    """ 
    def __init__(self):
        from marketsim import rtti
        
        rtti.check_fields(self)
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        
    }
    def __repr__(self):
        return "array_ChooseTheBest" % self.__dict__
    
    def __call__(self, array = None):
        from marketsim.gen._out.strategy.weight._choosethebest import ChooseTheBest_ListFloat as _strategy_weight_ChooseTheBest
        array = array if array is not None else []
        
        return _strategy_weight_ChooseTheBest(array)
    
def array_ChooseTheBest(): 
    from marketsim import rtti
    return array_ChooseTheBest_()
    raise Exception('Cannot find suitable overload for array_ChooseTheBest('++')')
