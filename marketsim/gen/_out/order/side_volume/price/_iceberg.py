def Iceberg(proto = None,lotSize = None): 
    from marketsim.gen._out._ifunction import IFunctionIFunctionIObservableIOrderIFunctionfloatIFunctionSideIFunctionfloat
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim.gen._out.order._curried._sidevolume_price_iceberg import sidevolume_price_Iceberg_SideFloatFloatIObservableIOrderFloat as _order__curried_sidevolume_price_Iceberg_SideFloatFloatIObservableIOrderFloat
    from marketsim import rtti
    if proto is None or rtti.can_be_casted(proto, IFunctionIFunctionIObservableIOrderIFunctionfloatIFunctionSideIFunctionfloat):
        if lotSize is None or rtti.can_be_casted(lotSize, IFunctionfloat):
            return _order__curried_sidevolume_price_Iceberg_SideFloatFloatIObservableIOrderFloat(proto,lotSize)
    raise Exception('Cannot find suitable overload for Iceberg('+str(proto) +':'+ str(type(proto))+','+str(lotSize) +':'+ str(type(lotSize))+')')
