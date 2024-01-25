from flask import Flask, request, jsonify
from datetime import datetime
import pytz

app = Flask(__name__) #Create Flask application

def calculate_delivery_fee(cart_value, delivery_distance, number_of_items, time):
    """
    Calculate the delivery fee based on cart value, delivery distance, number of items, and time.

    The delivery fee is determined by several factors:
    - If the cart value is less than 10 EUR, a surcharge is added to make up the difference.
    - A base delivery fee is charged for the first 1000 meters. Beyond that, an additional fee is 
      charged for every 500 meters or part thereof.
    - If the number of items is 5 or more, a surcharge is added for each item above 4. An 
      additional fee applies for more than 12 items.
    - On Fridays, during rush hours (3-7 PM UTC), the delivery fee is increased by a multiplier.
    - The delivery fee is capped at 15 EUR.
    - Orders of 200 EUR or more are eligible for free delivery.

    Parameters:
    - cart_value (int): The total value of the cart in cents.
    - delivery_distance (int): The delivery distance in meters.
    - number_of_items (int): The number of items in the cart.
    - time (str): The time of the order in ISO 8601 format.

    Returns:
    - int: The total delivery fee in cents.
    """
    
    # Convert cart value from cents to EUR
    cart_value_eur = cart_value / 100
    if cart_value_eur >= 200: #Free shipping for orders at least 200 EUR
        return 0

    delivery_fee = 0 

    #Check for small order 
    if cart_value_eur < 10:
        delivery_fee += (10 - cart_value_eur) * 100 # Add surcharge in cents

    #Calculate the distance fee based on delivery_distance
    distance_fee = 200
    if delivery_distance > 1000:
        extra_dist = delivery_distance - 1000
        distance_fee += (extra_dist // 500) * 100 #Add 1 EUR for 500m
        if extra_dist % 500 > 0: 
            distance_fee += 100 #If any remaining meters exist
    delivery_fee += distance_fee
        
    #Number of items surcharge calculation
    if number_of_items >= 5: 
        items_fee = (number_of_items - 4) * 50 #50 cent surchage for 5+ items
        if number_of_items > 12:
            items_fee += 120
        delivery_fee += items_fee 

    #Friday rush hour multiplier/fee check in b/w Friday 3-7PM UTC
    curr_time = datetime.fromisoformat(time)
    if curr_time.weekday() == 4 and 15 <= curr_time.hour < 19:
        delivery_fee = int(delivery_fee * 1.2)
    
    #Delivery fee cannot exceed 15 EUR
    delivery_fee = min(delivery_fee, 1500)

    return int(delivery_fee)

#Define route for Flask application /calculate_delivery_fee to accept POST requests
@app.route('/calculate_delivery_fee', methods=['POST'])

def api_calculate_delivery_fee():
    data = request.json
    delivery_fee = calculate_delivery_fee(
        data['cart_value'],
        data['delivery_distance'],
        data['number_of_items'],
        data['time']
    )
    return jsonify({"delivery_fee": delivery_fee})

if __name__ == '__main__':
    app.run(debug=True)