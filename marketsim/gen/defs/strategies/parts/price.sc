@category = "Price function"
package strategy.price
{
    /**
     *  Price function for a liquidity provider strategy
     */
    def LiquidityProvider(
            /** side of orders to create */
            side         = .side.Sell() : IFunction[Side],
            /** initial price which is taken if orderBook is empty */
            initialValue = 100.0,
            /** defines multipliers for current asset price when price of
             order to create is calculated*/
            priceDistr   = math.random.lognormvariate(0., .1),
            /** asset in question */
            book = orderbook.OfTrader())

        = book~>Queue(side)~>SafeSidePrice(initialValue) * priceDistr
}