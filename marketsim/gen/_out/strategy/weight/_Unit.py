def unit(): 
    from marketsim.gen._out.strategy.weight.trader._trader_unit import trader_Unit_ as _strategy_weight_trader_trader_Unit_
    from marketsim import rtti
    return _strategy_weight_trader_trader_Unit_()
    raise Exception('Cannot find suitable overload for unit('++')')
from marketsim import registry
from marketsim.gen._out._ifunction import IFunctionfloat
from marketsim.gen._out._iaccount import IAccount
from marketsim import context
@registry.expose(["Strategy", "Unit"])
class Unit_IAccount(IFunctionfloat):
    """ 
    """ 
    def __init__(self, trader = None):
        from marketsim.gen._out.trader._singleproxy import SingleProxy_ as _trader_SingleProxy_
        from marketsim import rtti
        self.trader = trader if trader is not None else _trader_SingleProxy_()
        rtti.check_fields(self)
        self.impl = self.getImpl()
    
    @property
    def label(self):
        return repr(self)
    
    _properties = {
        'trader' : IAccount
    }
    def __repr__(self):
        return "Unit(%(trader)s)" % self.__dict__
    
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
        from marketsim.gen._out._constant import constant_Float as _constant_Float
        return _constant_Float(1.0)
    
def Unit(trader = None): 
    from marketsim.gen._out._iaccount import IAccount
    from marketsim import rtti
    if trader is None or rtti.can_be_casted(trader, IAccount):
        return Unit_IAccount(trader)
    raise Exception('Cannot find suitable overload for Unit('+str(trader) +':'+ str(type(trader))+')')
