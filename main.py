import sqlite3
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# 1. Fetch data
conn = sqlite3.connect("BubbleTeaDB_2026.db")
query = """
SELECT 
    strftime('%H:00', order_time) AS hour_of_day,
    channel,
    COUNT(order_id) AS total_orders
FROM Orders
GROUP BY hour_of_day, channel
ORDER BY hour_of_day ASC;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 2. Build the Peak Hours Chart
fig = px.bar(
    df,
    x="hour_of_day",
    y="total_orders",
    color="channel",
    barmode="group",
    title="Daily Peak Hours: Walk-in vs. Foodpanda Orders",
    labels={"hour_of_day": "Hour of Day", "total_orders": "Number of Orders", "channel": "Order Channel"},
    color_discrete_map={"Walk-in": "#4CAF50", "Foodpanda": "#D81B60"}
)

# 3. Simple Dash App
app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("Bubble Tea Store - Rush Hour Analysis", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)