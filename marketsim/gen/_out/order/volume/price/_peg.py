def Peg(proto = None): 
    from marketsim.gen._out._ifunction import IFunctionIFunctionIObservableIOrderIFunctionfloatIFunctionfloat
    from marketsim.gen._out.order._curried._volume_price_peg import volume_price_Peg_FloatFloatIObservableIOrder as _order__curried_volume_price_Peg_FloatFloatIObservableIOrder
    from marketsim import rtti
    if proto is None or rtti.can_be_casted(proto, IFunctionIFunctionIObservableIOrderIFunctionfloatIFunctionfloat):
        return _order__curried_volume_price_Peg_FloatFloatIObservableIOrder(proto)
    raise Exception('Cannot find suitable overload for Peg('+str(proto) +':'+ str(type(proto))+')')
