@category = "Volume function"
package strategy.position
{
    /**
     * Position function for desired position strategy
     */
    def DesiredPosition(
             /** observable desired position */ desiredPosition = const(1.),
             /** trader in question */          trader          = trader.SingleProxy())

        =   desiredPosition - trader~>Position - trader~>PendingVolume

    /**
     * Position function for Bollinger bands strategy with linear scaling
     */
    def Bollinger_linear(
                /** alpha parameter for exponentially weighted moving everage and variance */
                alpha   = 0.15,
                /** observable scaling function that maps relative deviation to desired position */
                k       = const(0.5),
                /** trader in question */
                trader  = trader.SingleProxy())

        = DesiredPosition(
                    trader~>Orderbook~>MidPrice~>EW_RelStdDev(alpha)~>OnEveryDt(1.0) * k,
                    trader)

    /**
     *  Position function for Relative Strength Index strategy with linear scaling
     */
    def RSI_linear(
            /** alpha parameter for exponentially moving averages of up movements and down movements */
            alpha = 1./14.,
            /** observable scaling function that maps RSI deviation from 50 to the desired position */
            k = const(-0.04),
            /** lag for calculating up and down movements */
            timeframe = 1.,
            /** trader in question */
            trader = trader.SingleProxy())

        = DesiredPosition(
                (50. - trader~>Orderbook~>RSI(timeframe, alpha))~>OnEveryDt(1.0) * k,
                trader)
}