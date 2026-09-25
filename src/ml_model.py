import mysql.connector
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AI_Business_Analyst"
)

print("Connection established successfully!!")



customers = pd.read_sql("select * from customers",conn)
orders = pd.read_sql("select * from orders",conn)
print(customers.head())
print(orders.head())


# to get the order date in datetime format and sort the orders by customer_id and order_date
orders['order_date'] = pd.to_datetime(orders['order_date'])
orders = orders.sort_values(['customer_id', 'order_date'])
print(orders.head())

def create_features(orders):
    # How many orders did this customer have BEFORE this order?
    # to get the previous orders, we can use the cumcount() function to get the cumulative count of orders for each customer.
    orders["previous_orders"] = orders.groupby("customer_id").cumcount()
    print(orders[["customer_id", "order_id", "order_date", "previous_orders"]].head(10))

    # Before this order, how many total items had this customer purchased?
    # to get the previous quantity, we can use the cumsum() function to get the cumulative sum of quantity 
    # for each customer and then subtract the current order's quantity from it.
    orders["previous_quantity"] = (
        orders.groupby("customer_id")["quantity"].cumsum() - orders["quantity"])
    print(orders[["customer_id", "order_id", "order_date", "quantity", "previous_quantity"]].head(10))


    # How much money had this customer generated from previous orders before the current order?
    # to get the previous sales, we can use the cumsum() function to get the cumulative sum of 
    # sales for each customer and then subtract the current order's sales from it.
    orders["previous_sales"] = (orders.groupby("customer_id")["sales"].cumsum() - orders["sales"])
    print(orders[["customer_id", "order_id", "order_date", "sales", "previous_sales"]].head(10))

    # On average, how much did this customer spend per previous order?
    # to get the previous average order value, we can divide the previous sales by the previous orders.
    orders["prev_avg_order_value"] = (orders["previous_sales"] / orders["previous_orders"].replace(0, np.nan))
    print(orders[["customer_id", "previous_sales", "previous_orders", "prev_avg_order_value"]].head(10))

   
    return orders

    
orders = create_features(orders)

orders = orders.merge(customers, on="customer_id", how="left")
print(orders.columns)

orders = orders[
    (orders["age"] > 0) &
    (orders["city"] != "city") &
    (orders["state"] != "state")
]

orders = orders[orders["previous_orders"] > 0]

X = orders[["previous_orders", "previous_quantity", "previous_sales", 
            "prev_avg_order_value",
              'age', 'city','state']]

y = orders["sales"]

X = pd.get_dummies(X,columns=["city","state"])
print(X.head())


def split_data(X,y):
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    return X_train,X_test,y_train,y_test


X_train,X_test,y_train,y_test = split_data(X,y)

print(X.shape)
print(X_test.shape)
print(X_train.shape) 


# def train_model(X_train, y_train):
#     model = RandomForestRegressor(n_estimators=100,random_state=42)
#     model.fit(X_train, y_train)
#     return model Mean Squared Error: 50267341045.0692  r_squared:-0.3221803164311088


# def train_model(X_train, y_train):
#     model = Ridge(alpha=1.0)
#     model.fit(X_train, y_train)
#     return model


def train_model(X_train,y_train):
    model = LinearRegression()
    model.fit(X_train,y_train)
    return model

model = train_model(X_train,y_train)
 
def make_predictions(model,X_test):
    y_predict = model.predict(X_test)
    return y_predict

predictions = make_predictions(model,X_test)

print(X_test.shape)
print(X_train.shape)

def evaluate_model(y_test,predictions):
    mse = mean_squared_error(y_test,predictions)
    r2 = r2_score(y_test,predictions)

    return mse,r2

mse,r2 = evaluate_model(y_test,predictions)
print(f"Mean Squared Error: {mse}")
print(f"r_squared:{r2}")




