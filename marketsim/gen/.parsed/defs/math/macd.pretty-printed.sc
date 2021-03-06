@category = "MACD"

package math.macd() {
    // defined at defs\math\macd.sc: 4.5
    /** Moving average convergence/divergence
     */
    @label = "MACD_{%(fast)s}^{%(slow)s}(%(x)s)"
    def MACD(/** source */ x = const(1.0),
             /** long period */ slow = 26.0,
             /** short period */ fast = 12.0) = x~>EW_Avg(2.0/(fast+1))-x~>EW_Avg(2.0/(slow+1))
    
    // defined at defs\math\macd.sc: 14.5
    /** Moving average convergence/divergence signal
     */
    @label = "Signal^{%(timeframe)s}_{%(step)s}(MACD_{%(fast)s}^{%(slow)s}(%(x)s))"
    @method = "macd_Signal"
    def Signal(/** source */ x = const(1.0),
               /** long period */ slow = 26.0,
               /** short period */ fast = 12.0,
               /** signal period */ timeframe = 9.0,
               /** discretization step */ step = 1.0) = x~>MACD(slow,fast)~>OnEveryDt(step)~>EW_Avg(2/(timeframe+1))
    
    // defined at defs\math\macd.sc: 27.5
    /** Moving average convergence/divergence histogram
     */
    @label = "Histogram^{%(timeframe)s}_{%(step)s}(MACD_{%(fast)s}^{%(slow)s}(%(x)s))"
    @method = "macd_Histogram"
    def Histogram(/** source */ x = const(1.0),
                  /** long period */ slow = 26.0,
                  /** short period */ fast = 12.0,
                  /** signal period */ timeframe = 9.0,
                  /** discretization step */ step = 1.0) = x~>MACD(slow,fast)-x~>macd_Signal(slow,fast,timeframe,step)
}
