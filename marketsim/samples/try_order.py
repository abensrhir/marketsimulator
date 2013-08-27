import sys
sys.path.append(r'../..')

from marketsim import (Side, mathutils, parts, signal, strategy, observable, ops, order, scheduler)
from common import expose, InterlacingSide

@expose("Various Orders", __name__)
def Orders(ctx):

    const = ops.constant
    linear_signal = signal.RandomWalk(initialValue=20, 
                                      deltaDistr=const(-.1), 
                                      label="20-0.1t")
    
    midPrice = observable.MidPrice(ctx.book_A)

    return [
        ctx.makeTrader_A(strategy.LiquidityProvider(volumeDistr=const(25)), "liquidity"),
        
        ctx.makeTrader_A(strategy.Signal(
                            order.factory.side.Market(volume = const(1)),
                            linear_signal), 
                         "signalmarket"), 
  
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.StopLoss(
                                const(0.1),
                                order.factory.Market(
                                    side = parts.side.Signal(linear_signal), 
                                    volume = const(1)))), 
                         "signalstoploss"), 
   
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.Limit(
                                side = parts.side.Signal(linear_signal), 
                                price = midPrice, 
                                volume = const(1))), 
                         "signallimit"), 
    
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.Limit(
                                side = InterlacingSide(), 
                                price = midPrice, 
                                volume = const(1)),
                            scheduler.Timer(const(1))), 
                         "noiselimitmarket"), 
    
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.WithExpiry(
                                const(100), 
                                order.factory.Limit(
                                    side = InterlacingSide(), 
                                    price = midPrice, 
                                    volume = const(1))),
                            scheduler.Timer(const(1))), 
                         "noiselimitexpiry"), 
   
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.Iceberg(
                                const(1),
                                order.factory.Limit(
                                    side = InterlacingSide(),
                                    price = midPrice, 
                                    volume = const(10))),
                            scheduler.Timer(const(10))), 
                         "noiseiceberglimit"), 
   
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.FixedBudget(
                                side = parts.side.Signal(linear_signal), 
                                budget = const(450))), 
                         "signalfixedbudget"), 
             
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.Iceberg(
                                const(1),
                                order.factory.Peg(
                                    order._limit.Price_Factory(
                                        side = InterlacingSide(),
                                        volume = const(10)))),
                            scheduler.Timer(const(10))), 
                         "icebergpeg"), 
   
        ctx.makeTrader_A(strategy.Generic(
                                order.factory.Peg(
                                    order.meta._iceberg.Price_Factory(
                                        const(1),
                                        order._limit.Price_Factory(
                                            side = InterlacingSide(),
                                            volume = const(10)))),
                            scheduler.Timer(const(10))), 
                         "pegiceberg"), 
   
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.Peg(
                                order._limit.Price_Factory(
                                    side = InterlacingSide(),
                                    volume = const(10))),
                            scheduler.Timer(const(10))), 
                         "noise_peg"), 
  
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.WithExpiry(
                                ops.constant(10),
                                order.factory.Peg(
                                    order.meta._iceberg.Price_Factory(
                                        const(1),
                                        order._limit.Price_Factory(
                                            side = InterlacingSide(),
                                            volume = const(10))))),
                            scheduler.Timer(const(10))), 
                         "pegicebergwithexpiry"), 
   
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.WithExpiry(
                                ops.constant(0.1),
                                order.factory.Iceberg(
                                    const(1),
                                    order.factory.Peg(
                                        order._limit.Price_Factory(
                                            side = InterlacingSide(),
                                            volume = const(10))))),
                            scheduler.Timer(const(10))), 
                         "icebergpeg"), 
   
        ctx.makeTrader_A(strategy.Generic(
                            order.factory.WithExpiry(
                                ops.constant(0.1),
                                order.factory.Peg(
                                    order._limit.Price_Factory(
                                        side = InterlacingSide(),
                                        volume = const(10)))),
                            scheduler.Timer(const(10))), 
                         "noise_pegexpiry"), 
    ]    
