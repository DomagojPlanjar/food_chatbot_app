import logging
import re
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from utils import db_helper
from utils import generic_helper
app = FastAPI()
in_progress_orders = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('uvicorn')

@app.post("/")
async def handle_request(request: Request):
    # Retrieve JSON data from the request
    payload = await request.json()
    logger.info("Received POST request")

    # Extract information from the payload based on the structure of
    # WebhookRequest from Dialogflow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler_dict = {
        'new.order': new_order,
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)

# Delete incomplete orders, making sure that new order is empty
def new_order(parameters, session_id):
    fulfillment_text = "Ok, starting a new order. You can say things like " \
                       "I want two pizzas and one cheeseburger. Make sure to specify a quantity " \
                       "for every food item! You can also remove items before completing your order."

    if session_id in in_progress_orders:
        del in_progress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def remove_from_order(parameters: dict, session_id: str):
    if session_id not in in_progress_orders:
        return JSONResponse(content={
            "fulfillmentText": "Unfortunately, we're having trouble finding your order. Please place a new one."
        })

    current_order = in_progress_orders[session_id]
    food_items = parameters['food-item']

    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f"Removed {",".join(removed_items)} from your order."

    if len(no_such_items) > 0:
        fulfillment_text = f"Your current order does not have {','.join(no_such_items)}."

    if len(current_order.keys()) == 0:
        fulfillment_text += " Your current order does not have any items."
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"\nHere is your updated order: {order_str}."

    print(fulfillment_text)
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def complete_order(parameters:dict, session_id):
    if session_id not in in_progress_orders:
        fulfillment_text = "I'm having trouble finding your order, sorry! Please place a new one."
    else:
        order = in_progress_orders[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to an error, " \
                                "please place a new order again."
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Excellent. We have placed your order. " \
                               f"Here is your order id #{order_id}. " \
                               f"Your total is {order_total}$. Please prepare the amount at the delivery time. " \
                               f"You can type track order to get order status."

        del in_progress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        print(food_item)
        r_code = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )
        # If database error
        if r_code == -1:
            return -1

    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

def add_to_order(parameters: dict, session_id: str):
    try:
        food_items = parameters['food-item']
        quantities = parameters['number']
        #print(food_items, quantities)
        if len(food_items) != len(quantities):
            fulfillment_text = "Sorry I did not understand, please specify food items and quantities"
        else:
            new_food_dict = dict(zip(food_items, quantities))

            if session_id in in_progress_orders:
                current_food_dict = in_progress_orders[session_id]
                current_food_dict.update(new_food_dict)
                in_progress_orders[session_id] = current_food_dict
            else:
                in_progress_orders[session_id] = new_food_dict

            order_string = generic_helper.get_str_from_food_dict(in_progress_orders[session_id])
            fulfillment_text = f"This is your order so far: {order_string}. Do you need anything else?"

        return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })
    except Exception as e:
        logger.error(f"Error: {e}")
        return JSONResponse(content={
            "fulfillmentText": "null returned"
        })


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"Status for order id {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"


    return JSONResponse(content={
        'fulfillmentText': fulfillment_text
    })

@app.get("/")
async def root():
    return {"Hello": "World"}

