import streamlit as st
import pandas as pd
import plotly.express as px
import io
from pandas import ExcelWriter

# 🚨 Set page config early
st.set_page_config(page_title="🍕 Pizza Forecast Dashboard", layout="wide")

# ----------------------
# 📦 Load and Clean Data
# ----------------------
@st.cache_data
def load_data():
    forecast_df = pd.read_csv(r"C:\Users\NAGARAJAN K\Desktop\pizza projetc\7_day_pizza_forecast.csv")
    weekly_forecast = pd.read_csv(r"C:\Users\NAGARAJAN K\Desktop\pizza projetc\7week_day_pizza_forecast.csv")
    purchase_order = pd.read_csv(r"C:\Users\NAGARAJAN K\Desktop\pizza projetc\purchase_order_next_7_days.csv")

    # Clean and format
    forecast_df['date'] = pd.to_datetime(forecast_df['date'], errors='coerce').dt.strftime('%d-%m-%Y')
    forecast_df['pizza_name_id'] = forecast_df['pizza_name_id'].astype(str).str.strip()
    forecast_df['pizza_name'] = forecast_df['pizza_name'].astype(str).str.strip()
    forecast_df['estimated_pizzas'] = pd.to_numeric(forecast_df['estimated_pizzas'], errors='coerce').fillna(0)

    weekly_forecast = weekly_forecast.dropna(how='any')
    weekly_forecast['pizza_name_id'] = weekly_forecast['pizza_name_id'].astype(str).str.strip()
    weekly_forecast['weekly_estimated_pizzas'] = pd.to_numeric(weekly_forecast['weekly_estimated_pizzas'], errors='coerce').astype(float)

    purchase_order.columns = purchase_order.columns.astype(str)
    purchase_order['ingredient'] = purchase_order['ingredient'].astype(str)
    purchase_order['total_required_kg'] = pd.to_numeric(purchase_order['total_required_kg'], errors='coerce').fillna(0)

    return forecast_df, weekly_forecast, purchase_order

forecast_df, weekly_forecast, purchase_order = load_data()

# ----------------------
# 🎯 KPI Metrics
# ----------------------
st.title("🍕 Pizza Sales Forecast & Ingredient Purchase Order")
col1, col2 = st.columns(2)
col1.metric("📦 Total Pizzas (7 Days)", int(forecast_df['estimated_pizzas'].sum()))
col2.metric("🧂 Total Ingredients (KG)", round(purchase_order['total_required_kg'].sum(), 2))

# ----------------------
# 🔝 Top N Pizza Filter (by pizza_name_id)
# ----------------------
top_n = st.slider("🔝 Show Top N Pizzas (by pizza_name_id)", min_value=5, max_value=50, value=10)

# Group by pizza_name_id
grouped_df = (
    forecast_df
    .groupby('pizza_name_id')['estimated_pizzas']
    .sum()
    .reset_index()
    .sort_values(by='estimated_pizzas', ascending=False)
)

# Top N pizza_name_ids
top_pizza_ids = grouped_df.head(top_n)['pizza_name_id'].tolist()

# Filter forecast and weekly by pizza_name_id
filtered_forecast = forecast_df[forecast_df['pizza_name_id'].isin(top_pizza_ids)]
filtered_weekly = weekly_forecast[weekly_forecast['pizza_name_id'].isin(top_pizza_ids)]

# ----------------------
# 📈 7-Day Forecast Chart (pizza_name_id based)
# ----------------------
st.subheader("📈 7-Day Forecast (by Pizza ID)")
fig = px.line(
    filtered_forecast,
    x='date',
    y='estimated_pizzas',
    color='pizza_name_id',
    title="Estimated Daily Pizza Demand by Pizza ID"
)
st.plotly_chart(fig, use_container_width=True)

# ----------------------
# 📊 Total Pizza by ID
# ----------------------
st.subheader("📊 Total Estimated Pizzas by Pizza ID (7-Day Total)")
fig_bar = px.bar(
    grouped_df.head(top_n),
    x='pizza_name_id',
    y='estimated_pizzas',
    color='pizza_name_id',
    title="Total Estimated Pizzas per Pizza ID",
    labels={'pizza_name_id': 'Pizza ID', 'estimated_pizzas': 'Total Pizzas'}
)
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------
# 📊 Weekly Pizza Demand (by ID)
# ----------------------
st.subheader("📊 Weekly Pizza Demand (Bar Chart)")
fig_weekly = px.bar(
    filtered_weekly,
    x='pizza_name_id',
    y='weekly_estimated_pizzas',
    color='pizza_name_id',
    labels={'weekly_estimated_pizzas': 'Weekly Pizzas'},
    title="Weekly Estimated Pizza Demand"
)
st.plotly_chart(fig_weekly, use_container_width=True)

st.subheader("📊 Total Estimated Pizzas by Pizza Name (7-Day Total)")
pizza_name_group = (
    forecast_df
    .groupby('pizza_name')['estimated_pizzas']
    .sum()
    .reset_index()
    .sort_values(by='estimated_pizzas', ascending=False)
    .head(top_n)
)
pizza_name_group1 = (
    forecast_df
    .groupby('pizza_name')['estimated_pizzas']
    .sum()
    .reset_index()
    .sort_values(by='estimated_pizzas', ascending=False)
    
)


fig_name_bar = px.bar(
    pizza_name_group,
    x='pizza_name',
    y='estimated_pizzas',
    color='pizza_name',
    title="Total Estimated Pizzas per Pizza Name",
    labels={'pizza_name': 'Pizza Name', 'estimated_pizzas': 'Total Pizzas'}
)
st.plotly_chart(fig_name_bar, use_container_width=True)

# ----------------------
# 🧂 Ingredient Usage Pie Chart
# ----------------------
st.subheader("🥧 Ingredient Usage Breakdown")
fig_pie = px.pie(
    purchase_order,
    names='ingredient',
    values='total_required_kg',
    title="Ingredient Share for Next 7 Days"
)
st.plotly_chart(fig_pie, use_container_width=True)

# ----------------------
# 📦 Ingredient Requirement Chart
# ----------------------
st.subheader("📦 Ingredient Requirement (Bar Chart)")
fig_po = px.bar(
    purchase_order.sort_values("total_required_kg", ascending=False),
    x='ingredient',
    y='total_required_kg',
    labels={'total_required_kg': 'Total Required (KG)', 'ingredient': 'Ingredient'},
    title="Ingredients Needed for Next 7 Days",
    color='ingredient'
)
st.plotly_chart(fig_po, use_container_width=True)

# ----------------------
# 📥 Download as Excel
# ----------------------
output = io.BytesIO()
with ExcelWriter(output, engine='xlsxwriter') as writer:
    forecast_df.to_excel(writer, sheet_name='7-Day Forecast', index=False)
    grouped_df.to_excel(writer, sheet_name='Grouped Summary', index=False)
    pizza_name_group1.to_excel(writer,sheet_name='Grouped by pizza name',index=False)
    purchase_order.to_excel(writer, sheet_name='Purchase Order', index=False)

st.download_button("📤 Download Full Report (Excel)", data=output.getvalue(), file_name="pizza_forecast_report.xlsx")

# ----------------------
# 📥 CSV Downloads
# ----------------------
st.download_button("⬇️ Download 7-Day Forecast", forecast_df.to_csv(index=False), "7_day_forecast.csv", "text/csv")
st.download_button("⬇️ Download Weekly Forecast", weekly_forecast.to_csv(index=False), "weekly_forecast.csv", "text/csv")
st.download_button("⬇️ Download Purchase Order", purchase_order.to_csv(index=False), "purchase_order.csv", "text/csv")
