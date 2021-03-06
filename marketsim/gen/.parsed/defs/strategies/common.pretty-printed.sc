@category = "Strategy"

package strategy() {
    // defined at defs\strategies\common.sc: 4.5
    /** Generic strategy that wakes up on events given by *eventGen*,
     *  creates an order via *orderFactory* and sends the order to the market using its trader
     */
    @python.intrinsic("strategy.generic._Generic_Impl")
    def Generic(/** order factory function*/ orderFactory = order.Limit(),
                /** Event source making the strategy to wake up*/ eventGen = event.Every()) : ISingleAssetStrategy
    
    // defined at defs\strategies\common.sc: 14.5
    /** Creates a strategy combining two strategies
     *  Can be considered as a particular case of Array strategy
     */
    @python.intrinsic("strategy.combine._Combine_Impl")
    def Combine(A = Noise(),
                B = Noise()) : ISingleAssetStrategy
    
    // defined at defs\strategies\common.sc: 22.5
    /** Creates a strategy combining an array of strategies
     */
    @python.intrinsic("strategy.combine._Array_Impl")
    def Array(/** strategies to combine */ strategies = [Noise()]) : ISingleAssetStrategy
    
    // defined at defs\strategies\common.sc: 29.5
    /** Strategy that listens to all orders sent by a trader to the market
     *  and in some moments of time it randomly chooses an order and cancels it
     *  Note: a similar effect can be obtained using order.WithExpiry meta orders
     */
    @python.intrinsic("strategy.canceller._Canceller_Impl")
    def Canceller(/** intervals between order cancellations */ cancellationIntervalDistr = math.random.expovariate(1.0)) : ISingleAssetStrategy
    
    // defined at defs\strategies\common.sc: 38.5
    /** Empty strategy doing nothing
     */
    @python.intrinsic("strategy.basic._Empty_Impl")
    def Empty() : ISingleAssetStrategy
    
    // defined at defs\strategies\common.sc: 44.5
    /** Strategy for a multi asset trader.
     * It believes that these assets represent a single asset traded on different venues
     * Once an ask at one venue becomes lower than a bid at another venue
     * it sends market sell and buy orders in order to exploit this arbitrage possibility
     */
    @python.intrinsic("strategy.arbitrage._Arbitrage_Impl")
    def Arbitrage() : IMultiAssetStrategy
}
