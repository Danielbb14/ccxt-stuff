import ccxt
import threading
import time
import csv
from datetime import datetime

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def get_exchange_prices(exchanges, symbol='BTC/USDT'):
    prices = {}
    threads = []

    def fetch_price(exchange_id):
        try:
            exchange = getattr(ccxt, exchange_id)()
            ticker = exchange.fetch_ticker(symbol)
            prices[exchange_id] = {
                'price': ticker['last']
            }
        except ccxt.NetworkError as e:
            print(f"Network error for {exchange_id}: {str(e)}")
        except ccxt.ExchangeError as e:
            print(f"Exchange error for {exchange_id}: {str(e)}")

    start_time = time.time()

    for exchange_id in exchanges:
        thread = threading.Thread(target=fetch_price, args=(exchange_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

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
    potential_profit = (sell_price / buy_price - 1) * 100
    return potential_profit

def write_to_csv(file_path, symbol, lowest_exchange, highest_exchange,prices, potential_profit):
    buy_price = prices[lowest_exchange]['price']
    sell_price = prices[highest_exchange]['price']
    with open(file_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header if the file is empty
        if csvfile.tell() == 0:
            csv_writer.writerow(['Symbol', f'Best Buy Exchange', f'Best Sell Exchange', 'Potential Profit (%)', 'Current Time'])

        # Write data
        csv_writer.writerow([symbol, f'{lowest_exchange}: {buy_price}', f'{highest_exchange}: {sell_price}', f'{potential_profit:.2f}', f'{get_current_time()}'])
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



    while True:
        for symbol in symbols:
            exchange_data = get_exchange_prices(popular_exchanges, symbol)
            print_prices(exchange_data)

            # Find arbitrage opportunity
            lowest_exchange, highest_exchange = find_arbitrage_opportunity(exchange_data)
            potential_profit = calculate_arbitrage_profit(exchange_data, lowest_exchange, highest_exchange)

            # Log information to CSV file
            write_to_csv('arbitrage_opportunities.csv', symbol, lowest_exchange, highest_exchange,exchange_data, potential_profit)

            print("\nArbitrage Opportunity:")
            print(f"Buy from {lowest_exchange} at {exchange_data[lowest_exchange]['price']} USDT")
            print(f"Sell on {highest_exchange} at {exchange_data[highest_exchange]['price']} USDT")
            print(f"Potential Profit: {potential_profit:.2f} %")
            print(f'Current Time: {get_current_time()}')

        with open('arbitrage_opportunities.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['-' * 100])