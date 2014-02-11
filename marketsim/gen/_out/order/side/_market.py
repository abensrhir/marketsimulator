def Market(volume = None): 
    from marketsim import IFunction
    from marketsim import float
    from marketsim.gen._out.order._curried._side_market import side_Market_IFunctionFloat as _order__curried_side_Market
    from marketsim import rtti
    if volume is None or rtti.can_be_casted(volume, IFunction[float]):
        return _order__curried_side_Market(volume)
    raise Exception('Cannot find suitable overload for Market('+str(volume)+')')
