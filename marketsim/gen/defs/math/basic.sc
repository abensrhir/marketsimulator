@category = "Basic"
package math

@category = "Log/Pow"
package {

    /**
     *  Square of *x*
     */
    @python.observable
    @label = "{%(x)s}^2"
    def Sqr(x = constant(1.)) = x*x

    /** Exponent of *x*
      *
      */
    @python.mathops("exp")
    @label = "e^{%(x)s}"
    def Exp(x = constant(1.)) => Float

    /** Natural logarithm of *x* (to base e)
     *
     */
    @python.mathops("log")
    @label = "log(%(x)s)"
    def Log(x = constant(1.)) => Float

    /** Square root of *x*
     *
     */
    @python.mathops("sqrt")
    @label = "\\sqrt{%(x)s}"
    def Sqrt(x = constant(1.)) => Float

    /** Return *x* raised to the power *y*.
      *
      * Exceptional cases follow Annex F of the C99 standard as far as possible.
      * In particular, ``pow(1.0, x)`` and ``pow(x, 0.0)`` always return 1.0,
      * even when *x* is a zero or a NaN.
      * If both *x* and *y* are finite, *x* is negative, and *y* is not an integer then
      * ``pow(x, y)`` is undefined, and raises ``ValueError``.
      */
    @python.mathops("pow")
    @label = "%(base)s^{%(power)s}"
    def Pow(base = constant(1.), power = constant(1.)) => Float
}

package {
    /**
     * Function returning minimum of two functions *x* and *y*.
     * If *x* or/and *y* are observables, *Min* is also observable
     */
    @python.observable
    @label = "min{%(x)s, %(y)s}"
    def Min(x = constant(1.), y = constant(1.)) = if x < y then x else y

    /**
     * Function returning maximum of two functions *x* and *y*.
     * If *x* or/and *y* are observables, *Min* is also observable
     */
    @python.observable
    @label = "max{%(x)s, %(y)s}"
    def Max(x = constant(1.), y = constant(1.)) = if x > y then x else y

    /**
     * Function returning first derivative on time of *x*
     * *x* should provide *derivative* member
     */
    @python.intrinsic("observable.derivative._Derivative_Impl")
    @label = "\\frac{d%(x)s}{dt}"
    def Derivative(x = math.EW.Avg() : IDifferentiable) => Float
}

@category = "Trigonometric"
package {
    /** Arc tangent of x, in radians.
     *
     */
    @python.mathops("atan")
    def Atan(x = constant(0.)) => Float

}

