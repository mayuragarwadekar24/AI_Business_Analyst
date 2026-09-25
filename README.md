\# AI Business Analyst



An end-to-end retail analytics project that combines data analysis, SQL, machine learning, Power BI, and a local AI assistant to turn e-commerce data into business insights.



\## Project Overview



This project analyzes a synthetic e-commerce dataset containing customers, products, and orders.



The project covers the complete analytics workflow:



\*\*Python → PostgreSQL → SQL Analysis → Machine Learning → Power BI → Local AI Assistant\*\*



\## Technologies Used



\- Python

\- Pandas

\- NumPy

\- PostgreSQL

\- SQL

\- Scikit-learn

\- Power BI

\- Streamlit

\- Ollama

\- DeepSeek



\## Dataset



The project uses synthetic e-commerce data consisting of:



\- 500 customers

\- 30 products

\- 1,000 orders



The data includes customer information, product details, order quantities, order status, dates, prices, and sales values.



\## Data Analysis



Python and SQL were used to explore the data and identify business patterns such as:



\- Sales by category

\- Sales by brand

\- Sales by city

\- Monthly sales trends

\- Order status distribution

\- Top-selling products

\- Top customers



\## Power BI Dashboard



The Power BI dashboard provides an interactive view of retail sales and customer performance.



Key KPIs include:



\- Total Sales

\- Total Orders

\- Average Order Value

\- Total Customers



The dashboard also includes visualizations for:



\- Monthly Sales Trend

\- Sales by Category

\- Sales by Brand

\- Sales by City

\- Order Status

\- Top 5 Products

\- Top 5 Customers



\## Machine Learning



The project includes an experiment to predict a customer's next-order sales value.



Three regression models were compared:



\- Linear Regression

\- Ridge Regression

\- Random Forest



Ridge Regression produced the best result among the tested models, although the negative R² indicates that the available synthetic features had limited predictive power.



\## AI Business Analyst



A local AI assistant was developed using DeepSeek through Ollama.



The assistant connects to the PostgreSQL database, analyzes business metrics, and generates natural-language findings and suggested areas for further investigation.



Example insights include identifying:



\- Highest-sales categories

\- Top-selling products

\- Highest-sales brands

\- Highest-sales cities

\- Highest and lowest sales months

\- Order-status patterns

\- Machine-learning performance



\## Streamlit Application



A Streamlit interface was created to provide access to the AI-generated business findings through a simple web application.



\## Project Structure



```text

AI\_Business\_Analyst/

│

├── app.py

├── data/

│   ├── customers.csv

│   ├── products.csv

│   └── orders.csv

│

├── src/

│   ├── ai.py

│   ├── generate\_data.py

│   └── ml\_model.py

│

├── .gitignore

└── README.md

