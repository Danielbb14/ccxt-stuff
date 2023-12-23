import csv

def find_highest_profit(csv_file):
    highest_profit = 0
    highest_profit_line = ""
    counter = 0

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            counter += 1
            potential_profit_str = row.get('Potential Profit (%)')
            
            # Check if the value is not None and is a valid float
            if potential_profit_str is not None and potential_profit_str.replace('.', '', 1).isdigit():
                potential_profit = float(potential_profit_str)
                
                if potential_profit > highest_profit:
                    highest_profit = potential_profit
                    highest_profit_line = row

    return highest_profit_line,counter

# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = 'arbitrage_opportunities.csv'

result,counter = find_highest_profit(csv_file_path)

if result:
    print("Line with the highest potential profit:")
    print(result)
    print(counter)
else:
    print("No data found.")
