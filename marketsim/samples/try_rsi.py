import sys
sys.path.append(r'../..')

from marketsim._pub import (event, order, math, strategy, orderbook, observable, constant, trader)
from common import expose, Constant

@expose("Relative strength index", __name__)
def RSI(ctx):

    const = constant
    linear_signal = math.RandomWalk(initialValue=20,
                                      deltaDistr=const(-.1), 
                                      name="20-0.1t")
    
    one = const(1)
    
    threshold = 30
    
    demo = ctx.addGraph('demo')
    myVolume = lambda: [(trader.Position(), demo)]

    alpha = 1./14
    
    myRsiBis = lambda: [(orderbook.OfTrader().RSI(1, alpha).OnEveryDt(1), demo)]
    
    return [
        ctx.makeTrader_A(
                strategy.LiquidityProvider(
                        event.Every(constant(1.)),
                        order.side_price.Limit(volume=const(4))),
                "liquidity"),
        
        ctx.makeTrader_A(strategy.Signal(event.Every(constant(1.)),
                                         order.side.Market(),
                                         linear_signal), 
                         "signal", 
                         [(linear_signal, ctx.amount_graph)]),
    
        ctx.makeTrader_A(strategy.RSI_linear(
                                         order.signedVolume.MarketSigned(),
                                         alpha = alpha,
                                         timeframe = 1),
                         "rsi_linear",
                         myVolume()),

        ctx.makeTrader_A(strategy.RSIbis(event.Every(constant(1.)),
                                         order.side.Market(one),
                                         alpha = alpha,
                                         timeframe = 1,
                                         threshold=threshold),
                         "rsi_bis",
                         myVolume() + myRsiBis()), 
    ]
