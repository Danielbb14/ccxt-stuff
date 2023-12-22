import ccxt
import time

def get_exchange_prices(exchanges, symbol='SOL/USDT'):
    prices = {}
    start_time = time.time()

    for exchange_id in exchanges:
        try:
            exchange = getattr(ccxt, exchange_id)()
            
            # Fetch ticker for price
            ticker = exchange.fetch_ticker(symbol)
            prices[exchange_id] = {
                'price': ticker['last']
            }
        except ccxt.NetworkError as e:
            print(f"Network error for {exchange_id}: {str(e)}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error for {exchange_id}: {str(e)}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")
    return prices

def find_arbitrage_opportunity(prices):
    lowest_exchange = min(prices, key=lambda x: prices[x]['price'])
    highest_exchange = max(prices, key=lambda x: prices[x]['price'])

    return lowest_exchange, highest_exchange

def calculate_arbitrage_profit(prices, lowest_exchange, highest_exchange):
    buy_price = prices[lowest_exchange]['price']
    sell_price = prices[highest_exchange]['price']

    # Calculate potential profit
    potential_profit = sell_price - buy_price
    return potential_profit

def print_prices(prices):
    for exchange, data in prices.items():
        print(f"{exchange}:")
        print(f"  Price: {data['price']} USDT")
        print()


if __name__ == "__main__":
    # Updated list of 10 popular exchanges
    popular_exchanges = [
        'binance', 'coinbasepro', 'kraken', 'bitstamp', 'bitforex', 'okx', 'kucoin', 'gemini', 'bitfinex'
    ]

    symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'ADA/USDT', 'DOT/USDT', 'UNI/USDT', 'LINK/USDT', 'XLM/USDT']



    for symbol in symbols:

        exchange_data = get_exchange_prices(popular_exchanges,symbol)
        print_prices(exchange_data)

        # Find arbitrage opportunity
        lowest_exchange, highest_exchange = find_arbitrage_opportunity(exchange_data)
        potential_profit = calculate_arbitrage_profit(exchange_data, lowest_exchange, highest_exchange)
        print("\nArbitrage Opportunity:")
        print(f"Buy from {lowest_exchange} at {exchange_data[lowest_exchange]['price']} USDT")
        print(f"Sell on {highest_exchange} at {exchange_data[highest_exchange]['price']} USDT")
        print(f"Potential Profit: {potential_profit} %")
