import dash  # use Dash version 1.16.0 or higher for this app to work
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px
app = dash.Dash(__name__) 
githubpath = './data/'


df_customers = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="customers")
df_order = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="order")
df_employee = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="employee")
df_products = pd.read_excel(githubpath + "my_shop_data.xlsx", sheet_name="products")

def get_data():
    # Employee name
    df_employee['emp_name'] = df_employee['firstname'] + ' ' + df_employee['lastname']

    # Customers name
    df_customers['cust_name'] = df_customers['first_name'] + ' ' + df_customers['last_name']

    # Data - Add: total, order, year, month
    df_order['total'] = df_order['unitprice'] * df_order['quantity']
    df_order['deliverytime'] = df_order['deliverydate'] - df_order['orderdate']
    df_order['orderyear'] = df_order['orderdate'].dt.strftime("%Y")
    df_order['ordermonth'] = pd.to_datetime(df_order['orderdate'])
    df_order['ordermonth'] = df_order['ordermonth'].dt.month_name()

    # ***************************************
    # Data - Relationer
    # ***************************************
    order = pd.merge(df_order, df_products, on='product_id')
    order = pd.merge(order, df_employee, on='employee_id')
    order = pd.merge(order, df_customers, on='customer_id')

    # Order - Select colomns
    order = order[['order_id', 
                'product_id', 'productname', 'type',
                'customer_id', 'cust_name', 'city', 'country',
                'employee_id', 'emp_name', 
                'orderdate', 'deliverydate', 'deliverytime', 'orderyear', 'ordermonth',
                'total']]

    # Retuner til app.py
    return order


app.layout = html.Div([
    html.Div([
        html.Label(['Sales by Employee']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                     {'label': 'Sales by Employees', 'value': 'emp_name'},
                     {'label': 'Sales by Product', 'value':'productname'}

            ],
            value='emp_name',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def update_graph(my_dropdown):
    dff = get_data()
    piechart=px.pie(
            data_frame=dff,
            names=my_dropdown,
            hole=.3,
            )

    return (piechart)


if __name__ == '__main__':
    app.run_server(debug=True)