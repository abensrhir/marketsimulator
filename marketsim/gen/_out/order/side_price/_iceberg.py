def Iceberg(proto = None,lotSize = None): 
    from marketsim.gen._out._ifunction import IFunctionIObservableIOrderIFunctionSideIFunctionfloat
    from marketsim.gen._out._ifunction import IFunctionfloat
    from marketsim.gen._out.order._curried._sideprice_iceberg import sideprice_Iceberg_SideFloatIObservableIOrderFloat as _order__curried_sideprice_Iceberg_SideFloatIObservableIOrderFloat
    from marketsim import rtti
    if proto is None or rtti.can_be_casted(proto, IFunctionIObservableIOrderIFunctionSideIFunctionfloat):
        if lotSize is None or rtti.can_be_casted(lotSize, IFunctionfloat):
            return _order__curried_sideprice_Iceberg_SideFloatIObservableIOrderFloat(proto,lotSize)
    raise Exception('Cannot find suitable overload for Iceberg('+str(proto) +':'+ str(type(proto))+','+str(lotSize) +':'+ str(type(lotSize))+')')
