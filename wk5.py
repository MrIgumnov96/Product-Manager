
import csv
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
host = os.environ.get("mysql_host")
user = os.environ.get("mysql_user")
password = os.environ.get("mysql_pass")
database = os.environ.get("mysql_db")

# Establish a database connection
connection = pymysql.connect(
    host,
    user,
    password,
    database
)

# A cursor is an object that represents a DB cursor, which is used to manage the context of a fetch operation.
cursor = connection.cursor()
cursor.execute("SELECT * FROM product")
cursor.execute("SELECT * FROM courier")
cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()
# for row in rows:
#     print(f'product_id: {str(row[0])}, Product: {row[1]}, Price: {row[2]}')

order_list = []
g_couriers = []
g_products = []
g_couriers_file_name = 'c:/Users/denis/Desktop/python/Data-engineering/fifth-week/courier-names.csv'
g_products_file_name = 'c:/Users/denis/Desktop/python/Data-engineering/fifth-week/product-names.csv'
order_file_name = 'c:/Users/denis/Desktop/python/Data-engineering/fifth-week/orders.csv'

# --------------------------------------------------------------------------------------------------------------------------
#                                             WRITING AND READING FILES
# --------------------------------------------------------------------------------------------------------------------------


def read_order_list():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM orders')
        rows = cursor.fetchall()
        order_list.append(rows)
        connection.commit()

def read_couriers_file():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM courier')
        rows = cursor.fetchall()
        g_couriers.append(rows)
        connection.commit()

def read_product_file():
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM product')
        rows = cursor.fetchall()
        g_products.append(rows)
        connection.commit()

# --------------------------------------------------------------------------------------------------------------------------
#                                                   PRINT STUFF ON SCREEN
# --------------------------------------------------------------------------------------------------------------------------

def print_order_list():
    print( "\n" )
    for orders in order_list:
        for order in orders:
            print(order)
    program__order_main_rutine()

def print_couriers_list():
    print( "\n" )
    for couriers in g_couriers:
        for courier in couriers:
            print(courier)
    program_courier_main_rutine()


def print_products_list():
    print("\n")
    for products in g_products:
        for product in products:
            print(product)
    program_product_main_rutine()


# --------------------------------------------------------------------------------------------------------------------------
#                                                          ADD NEW ORDER
# --------------------------------------------------------------------------------------------------------------------------


def add_new_order():
    print("\n"*2)
    order_dictionary = {'Customer Name': '', 'Address': '', 'Number': '', 'Courier': '', 'Status': 'Preparing', 'Items': []}
    add_name(order_dictionary)

def add_name(order_dictionary):
    print("Order list")
    print("Add Your Name")
    adding_order_name = input()
    order_dictionary["Customer Name"] = adding_order_name
    add_address(order_dictionary)

def add_address(order_dictionary):
    print("Add Address")
    adding_address = input()
    order_dictionary["Address"] = adding_address
    add_number(order_dictionary)

def add_number(order_dictionary):
    print("Add Phone Number")
    adding_number = input()
    order_dictionary["Number"] = adding_number
    add_status(order_dictionary)

def add_status(order_dictionary):
    status = "Preparing"
    order_dictionary["Status"] = status
    print("\n")
    for key, value in order_dictionary.items():
        print(f'{key}: {value}')
    print("\nThe new order has successfully been added to your Order List")
    add_courier_to_order(order_dictionary)
    # add_products_to_order(order_dictionary)
    add_another_products_to_order(order_dictionary)
    add_order_to_database(order_dictionary)


def add_courier_to_order(order_dictionary):
    
    for couriers in g_couriers:
        for courier in couriers:
            print(f'{courier}')
    user_input = int(input("Enter the number of the courier you wish to choose: "))
    for courier in couriers:
        if user_input == courier['courier_id']:
            courier
    order_dictionary['Courier'] = user_input


def add_another_products_to_order(order_dictionary):
    while True:
        for products in g_products:
            for product in products:
                print(f'{product}')
        try:
            chosen_product = int(input("Choose a Product or press 0 to skip: "))
        except:
            print('Incorrect Command')
            continue
        if product in products:
            if chosen_product == product['product_id']:
                product
        if chosen_product == 0:
            print('Items Selected')
            print('\n')
            break
        order_dictionary['Items'].append(chosen_product)
    order_list.append(order_dictionary)


def add_order_to_database(order_dictionary):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        print(order_dictionary)
        items_str =','.join(str(v) for v in order_dictionary["Items"])
        sql = ('INSERT INTO orders (order_name, order_address, order_number, order_courier, order_status, order_product) VALUES (%s, %s, %s, %s, %s, %s)')
        val = (order_dictionary["Customer Name"], order_dictionary["Address"], order_dictionary["Number"], order_dictionary["Courier"], order_dictionary["Status"], items_str)
        cursor.execute(sql, val)
        connection.commit()
        order_list.clear()
        read_order_list()
        program__order_main_rutine()

# --------------------------------------------------------------------------------------------------------------------------\
#                                                         UPDATE STATUS
# --------------------------------------------------------------------------------------------------------------------------/

def update_order_status(selected_order):
    user_input = input("[0] order cancelled\n[1] preparing order\n[2] delivering order\n[3] order finished""\nSelect a new status of the order:\n ")
    
    cancelled = user_input == '0'
    preparing = user_input == '1'
    delivering = user_input == '2'
    finished = user_input == '3'
    
    if cancelled:
        new_status = "cancelled"
        selected_order["order_status"] = new_status
    elif preparing:
        new_status = "preparing"
        selected_order["order_status"] = new_status
    elif delivering:
        new_status = "delivering"
        selected_order["order_status"] = new_status
    elif finished:
        new_status = "finished"
        selected_order["order_status"] = new_status


def change_order_status():
    print("Order List:\n")
    for orders in order_list:
            for order in orders:
                print(order)
    print('\n')
    try:
        user_input = int(input("Which order would you like to change the status of?\nPlease enter the number"))
        for orders in order_list:
            for order in orders:
                if user_input == order['order_id']:
                    selected_order = order
    except:
        print("Wrong command")
    if user_input == 0:
        program__order_main_rutine()
    print('Select order:\n')
    for orders in order_list:
        for order in orders:
            print(order)
    update_order_status(selected_order)
    update_order_to_database(selected_order)

def update_order_to_database(selected_order):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        val = (selected_order["order_status"], selected_order["order_id"])
        sql = ('UPDATE orders SET order_status = %s WHERE order_id = %s')
        cursor.execute(sql, val)
        connection.commit()
        program__order_main_rutine()

# --------------------------------------------------------------------------------------------------------------------------
#                                                        CHANGE ORDER DETAILS
# --------------------------------------------------------------------------------------------------------------------------

def change_order_details():
    for orders in order_list:
        for order in orders:
            print(order)
    print('\n')
    user_input = int(input( "Enter the number of the order you would you like to add changes too: "))
    for orders in order_list:
        for order in orders:
            if user_input == order['order_id']:
                selected_order = order
    change_order_name(selected_order) 

def change_order_name(selected_order):
    print(selected_order)
    user_input = int(input("If you wish to change the name press 1 \nOr press 0 to not change name: "))
    if user_input == (1):
        adding_order_name = input("Enter a new name: ")
        if adding_order_name == "":
            change_order_address(selected_order)
        else:
            selected_order["order_name"] = adding_order_name
            val = (selected_order["order_name"], selected_order["order_id"])
            sql = ('UPDATE orders SET order_name = %s WHERE order_id = %s')
            cursor.execute(sql, val)
            connection.commit()
            change_order_address(selected_order)
    else:
        change_order_address(selected_order)


def change_order_address(selected_order):
    print(selected_order)
    user_input = int(input("If you wish to change the address press 1 \nOr press 0 to not change address: "))
    if user_input == (1):
        adding_address = input("Enter a new address: ")
        if adding_address == "":
            change_order_number(selected_order)
        else:
            selected_order["order_address"] = adding_address
            val = (selected_order["order_address"], selected_order["order_id"])
            sql = ('UPDATE orders SET order_address = %s WHERE order_id = %s')
            cursor.execute(sql, val)
            connection.commit()
            change_order_number(selected_order)
    else:
        change_order_number(selected_order)

def change_order_number(selected_order):
    print(selected_order)
    user_input = int(input("If you wish to change the number press 1 \nOr press 0 to not change number: "))
    if user_input == (1):
        adding_number = input("Enter a new number: ")
        if adding_number == "":
            change_oder_courier(selected_order)
        else:
            selected_order["order_number"] = adding_number
            val = (selected_order["order_number"], selected_order["order_id"])
            sql = ('UPDATE orders SET order_number = %s WHERE order_id = %s')
            cursor.execute(sql, val)
            connection.commit()
            change_oder_courier(selected_order)
    else:
        change_oder_courier(selected_order)

def change_oder_courier(selected_order):
    print(selected_order)
    user_input = int(input("If you wish to change the courier press 1 \nOr press 0 to not change the courier: "))
    if user_input == (1):
        for couriers in g_couriers:
            for courier in couriers:
                print(courier)
        selected_courier = int(input("Enter the id of the courier: "))
        # adding_courier = g_couriers[selected_courier -1]
        for orders in order_list:
            for order in orders:
                if user_input == order["order_courier"]:
                    selected_courier = order
        if selected_courier == "":
            change_order_product(selected_order)
        else:
            selected_order['order_courier'] = selected_courier
            val = (selected_order["order_courier"], selected_order["order_id"])
            sql = ('UPDATE orders SET order_courier = %s WHERE order_id = %s')
            cursor.execute(sql, val)
            connection.commit()
            change_order_product(selected_order)
    else:
        change_order_product(selected_order)

        
def change_order_product(selected_order):
    print(selected_order)  
    order_id = selected_order['order_id']
    user_input = int(input("If you wish to update the product press 1 \nOr press 0 to not update the product: "))
    asses_user_input_op( user_input, order_id )
    
def asses_user_input_op( user_input, order_id ):
    if user_input == 1:
        oderids_str = ""
        print_product_list()

        while True:
            selected_product_id = int( input( "Enter the product id or enter 0 to exit: " ) )  

            if selected_product_id == 0:
                break

            if check_if_product_exists( selected_product_id ) == True:
                if oderids_str != "":
                    oderids_str += ", "
                oderids_str += str(selected_product_id)
                
        update_order( oderids_str, order_id )
    program__order_main_rutine()

def update_order( orders, order_id ):
    val = ( orders, order_id )
    sql = ('UPDATE orders SET order_product = %s WHERE order_id = %s')
    cursor.execute(sql, val)
    connection.commit()
    order_list.clear()
    read_order_list()
    
def check_if_product_exists( product_id ):
    for products in g_products:
        for product in products:
            if product_id == int(product['product_id']):
                return True
    return False
        
def print_product_list():
    for products in g_products:
            for product in products:
                print(product)


# --------------------------------------------------------------------------------------------------------------------------
#                                                        REMOVING ORDER
# --------------------------------------------------------------------------------------------------------------------------

def remove_order():
    for orders in order_list:
        for order in orders:
            print(order)
    sql = "DELETE FROM orders WHERE order_id = %s"
    val = input('Please enter the id of the order: ')
    cursor.execute(sql, val)
    connection.commit()
    order_list.clear()
    read_order_list()
    program__order_main_rutine()

# --------------------------------------------------------------------------------------------------------------------------
#                                                           ADDING 
# --------------------------------------------------------------------------------------------------------------------------

def add_new_courier():
    for couriers in g_couriers:
        for courier in couriers:
            print(courier)
    name_input = input("Please enter the name of the Courier: ")
    number_input = input("Please enter the Number: ")
    sql = "INSERT INTO courier (courier_name, courier_number) VALUES (%s, %s)"
    val = (name_input, number_input)
    cursor.execute(sql, val)
    connection.commit()
    g_couriers.clear()
    read_couriers_file()
    program_courier_main_rutine()

def add_new_product():
    for products in g_products:
        for product in products:
            print(product)
    product_input = input("Please enter the of product: ")
    price_input = input("Please enter the price: ")
    sql = "INSERT INTO product (product_name, product_price) VALUES (%s, %s)"
    val = (product_input, price_input)
    cursor.execute(sql, val)
    connection.commit()
    g_products.clear()
    read_product_file()
    program_product_main_rutine()

# --------------------------------------------------------------------------------------------------------------------------
#                                                  REMOVE COURIER / PRODUCT
# --------------------------------------------------------------------------------------------------------------------------

def remove_courier():
    for products in g_products:
        for product in products:
            print(product)
    sql = "DELETE FROM courier WHERE courier_id = %s"
    val = input('Please enter the id of the courier: ')
    cursor.execute(sql, val)
    connection.commit()
    g_couriers.clear()
    read_couriers_file()
    program_courier_main_rutine()

def remove_product():
    for products in g_products:
        for product in products:
            print(product)
    sql = "DELETE FROM product WHERE product_id = %s"
    val = input('Please enter the id of the product: ')
    cursor.execute(sql, val)
    connection.commit()
    g_products.clear()
    read_product_file()
    program_product_main_rutine()

# --------------------------------------------------------------------------------------------------------------------------
#                                               SUBSTITUDE COURIER / PRODUCT
# --------------------------------------------------------------------------------------------------------------------------

def sub_courier():
    for couriers in g_couriers:
        for courier in couriers:
            print(courier)
    name_input = input("Please enter the name of the courier: ")
    if name_input == "":
        print("Exiting to Courier's menu")
        program_courier_main_rutine()
    else:
        substitude_courier(name_input)
def substitude_courier(name_input):
    number_input = int(input("Please enter the phone number: "))
    id_input = int(input('Please enter the id of the courier you want to change: '))
    sql ="UPDATE courier SET courier_name = %s, courier_number = %s WHERE courier_id = %s"
    val = (name_input, number_input, id_input)
    cursor.execute(sql, val)
    connection.commit()
    g_couriers.clear()
    read_couriers_file()
    program_courier_main_rutine()

def sub_product():
    for products in g_products:
        for product in products:
            print(product)
    name_input = input('Please enter the new name of the product: ')
    if name_input == "":
        print("Exiting to Product's menu")
        program_product_main_rutine()
    else:
        substitude_product(name_input)
def substitude_product(name_input):
    price_input = float(input('Please enter the new price of the product: '))
    id_input = int(input('Please enter the id of the product you want to change: '))
    sql = "UPDATE product SET product_name = %s, product_price = %s WHERE product_id = %s"
    val = (name_input, price_input, id_input)
    cursor.execute(sql, val)
    connection.commit()
    g_products.clear()
    read_product_file()
    program_product_main_rutine()

# --------------------------------------------------------------------------------------------------------------------------
#                                                              MENUS
# --------------------------------------------------------------------------------------------------------------------------


def process_usr_input_multi(uinput, o, p, a, s, r):
    if uinput == 0:
        print("Exiting to main menu")
        o()
    elif uinput == 1:
        p()
    elif uinput == 2:
        a()
    elif uinput == 3:
        s()
    elif uinput == 4:
        r()

def process_user_input_courier( uinput ):
    process_usr_input_multi(uinput, opening, print_couriers_list, add_new_courier, sub_courier, remove_courier)
    # if uinput == 0:
    #     print("Exiting to main menu")
    #     opening()
    # elif uinput == 1:
    #     print_couriers_list()
    # elif uinput == 2:
    #     add_new_courier()
    # elif uinput == 3:
    #     sub_courier()
    # elif uinput == 4:
    #     remove_courier()
    # items_str = ''.join(str(v) for v in items)
        # items_str = tuple(items_str)


def process_user_input_product( uinput ):
    if uinput == 0:
        print( "Exiting to main menu" )
        opening()
    elif uinput == 1:
        print_products_list()
    elif uinput == 2:
        add_new_product()
    elif uinput == 3:
        sub_product()
    elif uinput == 4:
        remove_product()

def process_user_input_order( uinput ):
    if uinput == 0:
        print("Exiting to main menu")
        opening()
    elif uinput == 1:
        print_order_list()
    elif uinput == 2:
        add_new_order()
    elif uinput == 3:
        change_order_status()
    elif uinput == 4:
        change_order_details()
    elif uinput == 5:
        remove_order()



def program_product_main_rutine():
    print( "Choose one of the following options:\n 0 - to exit\n 1 - Print all products\n 2 - Create a new product\n 3 - Substitude product\n 4 - Remove product" ) 
    user_input = int( input() )
    if user_input in (0, 1, 2, 3, 4):
        process_user_input_product( user_input )
    else:
        print( "This choice {} doesn't exist, buy goggles and try once more!".format( user_input ) )
        program_product_main_rutine()

def program_courier_main_rutine():
    print("Choose one of the following options:\n 0 - to exit\n 1 - Print all couriers names\n 2 - Add a New Courier\n 3 - Substitude couriers' names\n 4 - Remove courier")
    user_input = int( input() )
    if user_input in (0, 1, 2, 3, 4):
        process_user_input_courier( user_input )
    else:
        print( "This choice {} doesn't exist, buy goggles and try once more!".format( user_input ) )
        program_product_main_rutine()

def program__order_main_rutine():
    print("Choose one of the following options:\n 0 - to exit\n 1 - Print all orders out on screen\n 2 - Create new order_list\n 3 - Update order status\n 4 - Update order's details\n 5 - Delete Order")
    user_input = int( input() )
    if user_input in (0, 1, 2, 3, 4, 5):
        process_user_input_order( user_input )
    else:
        print("This choice {} doesn't exist, buy goggle and try once more!".format( user_input ))

def opening():
    print("Choose one of the following options:\n 0 - To exit\n 1 - Open the Product Menu\n 2 - Open Courier menu\n 3 - Open Order Menu" )
    app_input = int( input() )
    if app_input == (3):
        program__order_main_rutine()
    elif app_input == (2):
        program_courier_main_rutine()
    elif app_input == (1):
        program_product_main_rutine()
    elif app_input == (0):
        print("App is Closed")
    else:
        print("Enter valid index, {} is not recognized".format( app_input ))
        opening()

# --------------------------------------------------------------------------------------------------------------------------
#                                                        Execution
# --------------------------------------------------------------------------------------------------------------------------

def main():
    read_couriers_file()
    read_product_file()
    read_order_list()
    opening()

print( "Welcome to your app !" )
main()

