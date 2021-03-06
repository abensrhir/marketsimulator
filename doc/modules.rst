**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none
    
Compound modules are shown in notation of a special domain specific language (to be developed)

.. code-block:: haskell

	MACD(x, slow, fast) ::= EWMA(x, 2./(fast+1)) - EWMA(x, 2./(slow+1))

Currently they are implemented using a Python subset:

.. code-block:: python

	class MACD(ops.Function[float]):
	    
	    def getImpl(self):
	        return EWMA(self.source, 2./(self.fast+1)) - EWMA(self.source, 2./(self.slow+1))
	    
	    @property
	    def label(self):
	        return 'MACD_{%s}^{%s}(%s)' % (self.fast, self.slow, self.source.label)
	    
	_wrap.function(MACD, ['Statistics', 'MACD', 'Convergence/Divergence'], 
	               """ Moving average convergence/divergence
	               """, 
	               [
	                    ('source', 'MidPrice()', 'types.IObservable[float]'), 
	                    ('fast',   '12',         'types.positive'),
	                    ('slow',   '26',         'types.positive'),
	               ], globals())    


Basic modules
--------------

Normally they return None if one of the operands is None

- ``Constant[T]``/``None[T]`` functions
- ``Identity`` function
- Arithmetic operations (+,-,*,/,%)
- Comparisons (<, <=, >, >=, ==, !=)
- Conditional branching (``if condition then trueBranch else falseBranch``)
- Math module functions (``Exp``, ``Pow``, ``Log``, ``Atan`` etc.)
- Random distrubutions (``uniform``, ``lognormvariate``, ``expovariate`` etc.)
- ``Derivative`` of a differentiable function
- ``Quotes``: downloads external historical data
- ``Lagged``: returns function values with some lag
- ``CurrentTime``: current model time

.. code-block:: haskell

	Max(x,y) ::= if x > y then x else y
	Min(x,y) ::= if x < y then x else y
	Sqr(x) ::= x*x


Statistics
----------

- average (Mean): cumulative (``CMA``), moving (``MA``), exponentially weighted (``EWMA``)
- variance (Variance): cumulative, moving, exponentially weighted
- moving minimum/maximum

Variances could be implemented via Mean but it looses precision 

.. code-block:: haskell

	Var(x) ::= Mean(Sqr(x)) - Sqr(Mean(x)) 

Standard deviation 

.. code-block:: haskell

	StdDev(x) ::= Sqrt(Variance(x))

Relative strength index

.. code-block:: haskell

	Ups(x, dt, alpha) ::= EWMA(max(0, x - Lagged(x, dt)), alpha)
	Downs(x, dt, alpha) ::= EWMA(max(0, Lagged(x, dt) - x), alpha)
	RSI(x, dt, alpha) ::= 100 - 100 / (1 + Ups(x,dt,alpha)/Downs(x,dt,alpha))

Moving average convergence/divergence

.. code-block:: haskell

	MACD(x, slow, fast) ::= EWMA(x, 2./(fast+1)) - EWMA(x, 2./(slow+1))
	MACD_signal(x, slow, fast, timeframe) ::= EWMA(MACD(x, slow, fast), 2/(timeframe+1))
	MACD_histogram(x, slow, fast, timeframe) ::= MACD(x,slow,fast) - MACD_signal(x,slow, fast, timeframe)

Bollinger bands

.. code-block:: haskell

	Bollinger_Hi(x) ::= Mean(x) + 2*StdDev(x)
	Bollinger_Lo(x) ::= Mean(x) - 2*StdDev(x)


Order book functions and observables
--------------------------------

- ``TickSize(orderbook)``
- ``Asks(orderbook)``/``Bids(orderbook)``: return asks or bids queue of the ``orderbook``
- ``BestPrice(orderqueue)``: current price at the ``orderqueue``
- ``LastTradePrice(orderqueue)``: price of the last trade
- ``LastTradeVolume(orderqueue)``: volume of the last trade
- ``PriceAtVolume(orderqueue, volume)``: price of order at the given depth
- ``CumulativePrice(volume)``: sum of the best order prices with total volume less than ``volume``

Price of last trades weighted by their volumes

.. code-block:: haskell

    WeightedPrice(queue, alpha) ::= EWMA(LastTradePrice(queue)*LastTradeVolume(queue), alpha) / 
                                    EWMA(LastTradeVolume(queue), alpha)
    
Mid-price

.. code-block:: haskell

    MidPrice(orderbook) ::= (BestPrice(Asks(orderbook)) + BestPrice(Bids(orderbook))) / 2
    
Spread

.. code-block:: haskell

    Spread(orderbook) ::= BestPrice(Asks(orderbook)) - BestPrice(Bids(orderbook))

Trader functions and observables
-------------------------------------

- ``Position(trader)``
- ``Balance(trader)``
- ``PendingVolume(trader)``: cumulative volume of orders sent by the ``trader`` but haven't been matched

.. code-block:: haskell

    Efficiency(trader) ::= Balance(trader) + CumulativePrice(Orderbook(trader), Position(trader))
    EfficiencyTrend(trader, alpha) ::= Derivative(EWMA(Efficiency(trader), alpha))

Strategy parts
--------------

Price for a liquidity provider

.. code-block:: haskell
    
    NotNone(x, defaultValue) ::= if x == None then defaultValue else x
    LiquidityProviderPrice(orderqueue, priceDistr, defaultValue) ::=
        priceDistr * (NotNone(BestPrice(orderqueue), 
                         NotNone(LastTradePrice(orderqueue), 
                             defaultValue))
                             
Side for a noise strategy

.. code-block:: haskell

    NoiseSide() ::= if uniform(0,1) > 0.5 then Side.Sell else Side.Buy
    
    
Side for a signal value strategy

.. code-block:: haskell

    SignalSide(x, threshold) ::= if  x > threshold then Side.Buy else 
                                 if -x > threshold then Side.Sell else
                                    None 
    
Side for a trend follower

.. code-block:: haskell

    TrendFollowerSide(price, alpha) ::= SignalSide(Derivative(EWMA(price, alpha)), 0)
    
Side for crossing averages strategy

.. code-block:: haskell

    TwoAveragesSide(price, alpha1, alpha2) ::= SignalSide(EWMA(price, alpha1) - EWMA(price, alpha2), 0)

Side for fundamental value strategy

.. code-block:: haskell

    FundamentalValueSide(orderbook, fv) ::= if BestPrice(Asks(orderbook)) < fv then Side.Buy else 
                                            if BestPrice(Bids(orderbook)) > fv then Side.Sell else
                                               Nothing

Side for mean reverting strategy

.. code-block:: haskell

    MeanRevertingSide(orderbook, alpha) ::= FundamentalValueSide(orderbook, EWMA(MidPrice(orderbook), alpha))

Side for dependency trading strategy

.. code-block:: haskell

    DependencySide(orderbook, otherOrderbook) ::= FundamentalValueSide(orderbook, MidPrice(otherOrderbook))

Signed volume for a desired position strategy

.. code-block:: haskell

    DesiredPositionVolume(x, trader) ::= x - (Position(trader) + PendingVolume(trader))
    
Signed volume for a RSI strategy

.. code-block:: haskell

    RSI_Volume(trader, alpha, k, lag) ::= 
        price = MidPrice(Orderbook(trader)) in 
        DesiredPositionVolume(k * (50 - RSI(price, lag, alpha)), trader)
        
Signed volume for Bollinger band strategy

.. code-block:: haskell

    BollingerVolume(trader, alpha, k) ::= 
        price = MidPrice(Orderbook(trader)) in 
        DesiredPositionVolume((price - EWMA(price, alpha)) / StdDevEW(price, alpha) * k, trader)

Order factories
---------------

Base orders:

- ``Market`` order 
- ``Limit`` order 

Meta orders:

- ``Iceberg(lotSize, orderFactory)`` creates an order using ``orderFactory`` and sends it consequetively splitting on portions of ``lotSize``
- ``FloatingPrice(priceFunc, orderFactory)`` creates an order with price controlled by priceFunc
- ``Peg(orderFactory)`` creates an order that tries to keep its price the best. Implemented via ``FloatingPrice`` and ``Maximum``/``Minimum``
- ``ImmediateOrCancel(orderFactory)`` creates a (limit-like) order with an immediate cancellation request
- ``WithExpiry(expiry, orderFactory)`` creates limit-like orders that are cancelled after ``expiry``
- ``StopLoss(maxLoss, orderFactory)`` sends an order and if losses from keeping its position are higher than ``maxLoss`` liquidates it

It should be noted that meta orders can be combined in quite wide range. For example, 

.. code-block:: haskell

    WithExpiry(expiry = const(10.),
        factory = Iceberg(lotSize = const(1),
            factory = Peg(
                factory = Limit(volume = const(10))))),

creates limit orders with volume 10, price is taken as the best price (Peg order), sends them in portions of ``lotSize = 1`` and cancels them after ``expiry = 10`` units of time.
	
Strategies
----------

- ``Generic(eventGen, orderFactory)`` wakes up at moments of time given by ``eventGen``	and asks ``orderFactory`` to create an order

A crossing averages strategy that sends market orders with exponentially distributed volume sizes in even intervals of time could be written as:

.. code-block:: haskell

    Generic(event.Every(constant(1.)),
            order.factory.Market(
                side = parts.side.TwoAverages(MidPrice(orderbook.OfTrader()), alpha1, alpha2),
                volume = rnd.Expovariate(1.)
           ))

- ``Array(strategies)`` aggregates an array of strategies
- ``Suspendable(strategy, predicate)`` passes orders issued by ``strategy`` only if ``predicate`` is true

In order to estimate trade impact of a strategy there are two classes:
- ``VirtualMarket`` for every order sent by the strategy it tries to estimate at what price it would be executed
- ``ActuallyTraded`` tracks actual trades done on orders issued by the strategy

A strategy that wraps another ``strategy`` and passes its orders only if it is considered as "effective" can be implemented in the following way:

.. code-block:: haskell

    Suspendable(strategy, Derivative(EWMA(Efficiency(VirtualMarket(strategy))), alpha) >= 0)

A strategy that provide liquidity using historical data serves as a good example of composing strategies, meta order factories and observables

.. code-block:: python

	class MarketData(types.ISingleAssetStrategy):
	    
	    def getImpl(self):
	        quotes = observable.Quote(self.ticker, self.start, self.end) 
	        return Array([
	                Generic(
	                    order.factory.Iceberg(
	                        ops.constant(self.volume),
	                        order.factory.FloatingPrice(
	                            ops.constant(sign*self.delta) + quotes,
	                            order.factory.price.Limit(
	                                side = const(side),
	                                volume = const(self.volume * 1000000)))),
	                    event.After(ops.constant(0)))\
	                    for side, sign in {Side.Buy : -1, Side.Sell : 1}.iteritems()
	            ])
	            
	_wrap.strategy(MarketData, ['Market data'],
	             """ A Strategy that allows to drive the asset price based on historical market data
	             by creating large volume orders for the given price.
	 
	             Every time step of 1 in the simulation corresponds to a 1 day in the market data.
	 
	             At each time step the previous Limit Buy/Sell orders are cancelled and new ones
	             are created based on the next price of the market data.
	 
	             |ticker|
	                Ticker of the asset
	 
	             |start|
	                Start date in DD-MM-YYYY format
	 
	             |end|
	                End date in DD-MM-YYYY format
	 
	             |delta|
	                Price difference between orders placed and underlying quotes
	 
	             |volume|
	                Volume of Buy/Sell orders. Should be large compared to the volumes of other traders.
	             """,
	              [ ('ticker','"^GSPC"',  'str'),
	                ('start', '"2001-1-1"', 'str'),
	                ('end',   '"2010-1-1"', 'str'),
	                ('delta', '1', 'positive'),
	                ('volume','1000', 'Volume')], globals())
