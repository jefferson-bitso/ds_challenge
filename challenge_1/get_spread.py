import requests
import time
import hashlib
import hmac
import csv
import os


# Provide Bitso API credentials (On Production environments, these
# credentials must be gathered from an AWS/K8s secret)
API_KEY = "API_KEY"
API_SECRET = "API_SECRET"


def export_to_file(data):
    year = time.strftime("%Y")
    month = time.strftime("%m")
    day = time.strftime("%d")
    hour = time.strftime("%H")
    min = time.strftime("%M")

    # Construct the folder path
    target_folder = f'./{year}/{month}/{day}'

    # Check if the folder structure exists, if not, create it
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Specify the CSV file name
    csv_file_name = f"{target_folder}/spread_{hour}{min}.csv"

    # Open the CSV file in write mode
    with open(csv_file_name, mode='a', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file, lineterminator='\n')

        # Write each row to the CSV file
        for row in data:
            csv_writer.writerow(row)

    print(f"Data has been written to {csv_file_name}")


def get_spread(books):

    # Initialize nonce as a Unix timestamp
    nonce = int(time.time()) * 1000

    # Set an empty string list variable
    output = []

    # Set the start time to be used by the timer
    start_time = time.time()

    continue_exec = True

    # Start the API until the threshold is completed
    while True:
        for book in books:
            # Define the HTTP method and request path
            method = "GET"

            # Define the Bitso API endpoint and path  for order book data
            url = f"https://stage.bitso.com/api/v3/order_book?book={book}"
            path = f"/api/v3/order_book?book={book}"

            # Construct the JSON payload (empty in this case)
            payload = ""

            # Create the concatenated string for signature
            signature_string = f"{nonce}{method}{path}{payload}"

            # Create the HMAC-SHA256 signature using API_SECRET as the key
            signature = hmac.new(
                API_SECRET.encode(),
                signature_string.encode(),
                hashlib.sha256).hexdigest()

            # Construct the Authorization header
            auth_header = f"Bitso {API_KEY}:{nonce}:{signature}"

            # Make the authenticated API request
            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            data = response.json()

            # Extract bid and ask values
            bids = data["payload"]["bids"]
            asks = data["payload"]["asks"]

            # Set an empty string list variable
            out_bids = []
            out_asks = []

            # Iterate through each row of the JSON response for bids and asks
            for row in range(len(bids)):
                bid_price = float(bids[row]["price"])
                out_bids.append(bid_price)

            for row in range(len(asks)):
                asks_price = float(asks[row]["price"])
                out_asks.append(asks_price)

            # Get the max bid and min ask
            max_bid = max(out_bids)
            min_ask = min(out_asks)

            # Calculate the spread
            spread = ((min_ask - max_bid) * 100 / min_ask)

            # Get the timestamp of API call
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")

            # Construct the output array
            output_loop = [
                f'{timestamp},{book},{max_bid},{min_ask},{round(spread,2)}']
            output.append(output_loop)

            # Get the current loop time
            loop_time = time.time()

        # Stop the script if the execution time was reached
        if loop_time - start_time >= 600:
            # continue_exec = False
            start_time = time.time()
            export_to_file(output)
            output = []

        # Wait 200ms until the next iteration
        time.sleep(0.200)

get_spread(["btc_mxn", "usd_mxn"])