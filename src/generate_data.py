import pandas as pd
print(pd.__version__)
import random
from datetime import datetime, timedelta

names = [
    "Rahul Sharma",
    "Priya Patel",
    "Amit Singh",
    "Sneha Nair",
    "Rohan Desai"
]

city_state = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Panaji": "Goa",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Delhi": "Delhi"
}

product_details = {
    "MacBook Pro": {
        "Category": "Laptop",
        "Brand": "Apple",
        "Price": 199999
    },
    "Dell XPS": {
        "Category": "Laptop",
        "Brand": "Dell",
        "Price": 149999
    },
    "HP Spectre": {
        "Category": "Laptop",
        "Brand": "HP",
        "Price": 139999
    },
    "Lenovo ThinkPad": {
        "Category": "Laptop",
        "Brand": "Lenovo",
        "Price": 129999
    },
    "ASUS Zenbook": {
        "Category": "Laptop",
        "Brand": "ASUS",
        "Price": 119999
    },
    "Acer Swift": {
        "Category": "Laptop",
        "Brand": "Acer",
        "Price": 89999
    },
    "Microsoft Surface Laptop": {
        "Category": "Laptop",
        "Brand": "Microsoft",
        "Price": 159999
    },
    "Razer Blade": {
        "Category": "Laptop",
        "Brand": "Razer",
        "Price": 189999
    },
    "LG Gram": {
        "Category": "Laptop",
        "Brand": "LG",
        "Price": 149999
    },
    "MSI Stealth": {
        "Category": "Laptop",
        "Brand": "MSI",
        "Price": 179999
    },

    "iPhone": {
        "Category": "Smartphone",
        "Brand": "Apple",
        "Price": 89999
    },
    "Samsung Galaxy": {
        "Category": "Smartphone",
        "Brand": "Samsung",
        "Price": 79999
    },
    "Google Pixel": {
        "Category": "Smartphone",
        "Brand": "Google",
        "Price": 74999
    },
    "OnePlus": {
        "Category": "Smartphone",
        "Brand": "OnePlus",
        "Price": 54999
    },
    "Xiaomi": {
        "Category": "Smartphone",
        "Brand": "Xiaomi",
        "Price": 34999
    },
    "Nothing Phone": {
        "Category": "Smartphone",
        "Brand": "Nothing",
        "Price": 42999
    },
    "Motorola Edge": {
        "Category": "Smartphone",
        "Brand": "Motorola",
        "Price": 49999
    },
    "Vivo X": {
        "Category": "Smartphone",
        "Brand": "Vivo",
        "Price": 39999
    },
    "OPPO Find": {
        "Category": "Smartphone",
        "Brand": "OPPO",
        "Price": 45999
    },
    "Realme": {
        "Category": "Smartphone",
        "Brand": "Realme",
        "Price": 29999
    },

    "JBL Flip": {
        "Category": "Speaker",
        "Brand": "JBL",
        "Price": 9999
    },
    "Bose SoundLink": {
        "Category": "Speaker",
        "Brand": "Bose",
        "Price": 19999
    },
    "Sonos Move": {
        "Category": "Speaker",
        "Brand": "Sonos",
        "Price": 39999
    },
    "Marshall Emberton": {
        "Category": "Speaker",
        "Brand": "Marshall",
        "Price": 17999
    },
    "Ultimate Ears BOOM": {
        "Category": "Speaker",
        "Brand": "Ultimate Ears",
        "Price": 14999
    },
    "Sony SRS": {
        "Category": "Speaker",
        "Brand": "Sony",
        "Price": 12999
    },
    "Anker Soundcore": {
        "Category": "Speaker",
        "Brand": "Anker",
        "Price": 7999
    },
    "Bang & Olufsen Beosound": {
        "Category": "Speaker",
        "Brand": "Bang & Olufsen",
        "Price": 59999
    },
    "Harman Kardon Onyx": {
        "Category": "Speaker",
        "Brand": "Harman Kardon",
        "Price": 24999
    },
    "Apple HomePod": {
        "Category": "Speaker",
        "Brand": "Apple",
        "Price": 32999
    }
}



def generate_customers():
    customer_list = []
    for i in range(500):
        city = random.choice(list(city_state.keys()))
        customer = {
            "customer_id":"c{:04d}".format(i + 1), # this will generate customer_id like c0001, c0002, ..., c0500. and c{:04d} means 4 digit number with leading zeros . and d means decimal number. and i + 1 means starting from 1 to 500. and format() is used to format the string.
            "name":random.choice(names),
            "age":random.randint(18,60),
            "city": city,
            "state":city_state[city]
        }
        customer_list.append(customer)
       
    return pd.DataFrame(customer_list)

customer_df = generate_customers()

customer_df.to_csv("data/customers.csv",index = False)
print("customers.csv created successfully!!")



def generate_products():
    product_list = []
    for i, product_name in enumerate(product_details.keys(), start=1):
        product = {
        "product_id" :"p{:04d}".format(i),# this will generate product_id like p0001, p0002, ..., p0500. and p{:04d} means 4 digit number with leading zeros . and d means decimal number. and i + 1 means starting from 1 to 500. and format() is used to format the string.
        "product_name" :product_name,
        "category":product_details[product_name]["Category"],
        "brand" :product_details[product_name]["Brand"],
        "Price":product_details[product_name]["Price"],
        "stock":random.randint(0,100)
        }
        product_list.append(product)

    return pd.DataFrame(product_list)

product_df = generate_products()
product_df.to_csv("data/products.csv",index=False)
print("products.csv created successfully!!")



start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 12, 31)

def generate_orders():
 order_list = []
 
 for i in range(1000):
    customer_id = random.choice(customer_df["customer_id"])
    product_id = random.choice(product_df["product_id"])
    
    # Find the selected product
    selected_product = product_df[product_df["product_id"] == product_id].iloc[0]

    price = selected_product["Price"]
    quantity = random.randint(1,5)

    sales = price * quantity

    # Random order date
    random_days = random.randint(0,(end_date -start_date).days)
    order_date = start_date+timedelta(days = random_days)
    
    orders = {
    "order_id":"o{:04d}".format(i+1),   
    "customer_id" :customer_id,
    "product_id" :product_id,
    "quantity":random.randint(1,5),
    "status":random.choice(["pending","shipped","delivered","cancelled"]),
    "order_date":order_date.strftime("%y-%m-%d"),
    "price":selected_product["Price"],
    "quantity":quantity,
    "sales":sales
    }
    order_list.append(orders)

 return pd.DataFrame(order_list)

order_df = generate_orders()
order_df.to_csv("data/orders.csv",index=False)
print("orders.csv created successfully!!")