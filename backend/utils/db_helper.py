import mysql.connector

global cnx
# Database config information
# Change according to your values
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="food_delivery"
)

# Function to insert a record into the order_tracking table
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    cursor.close()

# Get total order price using function from database
def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    return result

# Inserting item in database using stored procedure
def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()
        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        cnx.commit()

        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")

        cnx.rollback()

        return -1


# Get the next available ID from database
def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1

def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None