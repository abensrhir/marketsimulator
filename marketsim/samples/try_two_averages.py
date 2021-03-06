import sys
sys.path.append(r'../..')

from marketsim._pub import (strategy, trader, orderbook, constant, order, event, math)

const = constant

from common import expose

@expose("Two Averages", __name__)
def TwoAverages(ctx):

    ctx.volumeStep = 30
    
    alpha_slow = 0.015
    alpha_fast = 0.15

    linear_signal = math.RandomWalk(initialValue=200,
                                      deltaDistr=const(-1), 
                                      name="200-t")
    
    demo = ctx.addGraph('demo')
    myVolume = lambda: [(trader.Position(), demo)]

    return [
        ctx.makeTrader_A(
                strategy.LiquidityProvider(
                    event.Every(constant(1.)),
                    order.side_price.Limit(volume=const(10))),
                "liquidity"),

        ctx.makeTrader_A(strategy.Signal(event.Every(constant(1.)),
                                         order.side.Market(volume = const(3)),
                                         linear_signal), 
                        "signal", 
                        [(linear_signal, ctx.amount_graph)]),
            
        ctx.makeTrader_A(strategy.CrossingAverages(
                            event.Every(constant(1.)),
                            order.side.Market(volume = const(1.)),
                            alpha_slow, 
                            alpha_fast),
                         'avg_ex+',
                         myVolume()),

        ctx.makeTrader_A(strategy.CrossingAverages(
                            event.Every(constant(1.)),
                            order.side.Market(volume = const(1.)),
                            alpha_fast, 
                            alpha_slow),
                         'avg_ex-',
                         myVolume()),
    ]
