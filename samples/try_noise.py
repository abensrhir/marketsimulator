import sys
sys.path.append(r'..')

from marketsim import (strategy, trader, orderbook, order, mathutils,
                       scheduler, observable, veusz, registry)

from common import run 

def Noise(graph, world, books):

    book_A = books['Asset A']

    price_graph = graph("Price")
     
    assetPrice = observable.Price(book_A)
    
    avg = observable.avg
    
    
    lp_A = trader.SASM(book_A, 
                       strategy.LiquidityProvider(
                            volumeDistr=mathutils.constant(1),
                            orderFactoryT=order.WithExpiryFactory(
                                expirationDistr=mathutils.constant(10))))
    noise_trader = trader.SASM(book_A, strategy.Noise(), "noise")
    
    price_graph += [assetPrice,
                    avg(assetPrice)]
    
    eff_graph = graph("efficiency")
    eff_graph += [observable.Efficiency(noise_trader),
                  observable.PnL(noise_trader)]
    
    return [lp_A, noise_trader], [price_graph, eff_graph]


if __name__ == '__main__':    
    run("noise_trader", Noise)
