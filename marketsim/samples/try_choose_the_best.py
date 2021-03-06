import sys
sys.path.append(r'../..')

from marketsim._pub import (math, order, strategy, orderbook,
                            event, observable, constant, trader)

from common import expose

@expose("Choose-The-Best", __name__)
def ChooseTheBest(ctx):

    ctx.volumeStep = 30
    
    slow_alpha = 0.015
    fast_alpha = 0.15

    linear_signal = math.RandomWalk(initialValue=200,
                                      deltaDistr=constant(-1),
                                      name="200-t")
    
    demo = ctx.addGraph('demo')
    myVolume = lambda: [(trader.Position(), demo)]
    myAverage = lambda alpha: [(orderbook.OfTrader().MidPrice.EW_Avg(alpha).OnEveryDt(1), demo)]
    
    def cross(alpha1, alpha2):
        return strategy.CrossingAverages(
                    event.Every(constant(1.)),
                    order.side.Market(volume = constant(1.)),
                    alpha1, alpha2)
        
    def strategies():
        return [cross(slow_alpha, fast_alpha), cross(fast_alpha, slow_alpha)]
        
    return [
        ctx.makeTrader_A(
            strategy.LiquidityProvider(
                orderFactory = order.side_price.Limit(volume=constant(45))),
                         "liquidity"),

        ctx.makeTrader_A(strategy.Signal(event.Every(constant(1.)),
                                         order.side.Market(volume = constant(20)),
                                         linear_signal), 
                        "signal", 
                        [(linear_signal, ctx.amount_graph)]),
            
        ctx.makeTrader_A(cross(slow_alpha, fast_alpha), 
                        'avg+', 
                        myAverage(slow_alpha) + myAverage(fast_alpha) + myVolume()),
 
        ctx.makeTrader_A(cross(fast_alpha, slow_alpha), 
                         'avg-',
                         myVolume()),

        ctx.makeTrader_A(strategy.ChooseTheBest(
                                    strategies(), 
                                    strategy.account.virtualMarket()),
                         'best virt',
                         myVolume()),

        ctx.makeTrader_A(strategy.ChooseTheBest(
                                    strategies(), 
                                    strategy.account.real()),
                         'best real',
                         myVolume()),
    ]
