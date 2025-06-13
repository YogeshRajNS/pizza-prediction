# 🍕 Pizza Sales Forecasting & Ingredient Planning

An end-to-end data science project that forecasts weekly pizza sales and generates ingredient-level purchase orders to optimize inventory management. The project includes data cleaning, EDA, feature engineering, model training, forecasting, and a visual dashboard built with Streamlit.

---

## 📌 Project Objective

- Forecast weekly pizza sales using historical data.
- Generate ingredient-level purchase orders for efficient inventory planning.

---

## 🧰 Libraries & Tools Used

- **Pandas, NumPy** – Data manipulation
- **Matplotlib, Seaborn** – Visualizations
- **Prophet, SARIMA, LSTM** – Time series modeling
- **scikit-learn** – Feature engineering & evaluation
- **Joblib** – Save encoders
- **Streamlit** – Dashboard development

---

## 🔧 Workflow Breakdown

### 1. **Data Cleaning**
- Handled missing/inconsistent entries.
- Outliers managed using IQR.
- Standardized datetime and input formats.

### 2. **Exploratory Data Analysis (EDA)**
- Trends analyzed: monthly, weekly, hourly.
- Classic and Supreme pizzas identified as top sellers.
- Large size pizzas had the highest sales.
- Correlation heatmap created for feature insights.

### 3. **Feature Engineering**
- Created: `day_of_week`, `is_weekend`, `is_veg`, `order_hour`, `month`, `number_of_ingredients`.
- Categorical encoding via `LabelEncoder`.
- Lag features and holiday flags added.
- Feature set saved as Pickle and Excel.

### 4. **Model Evaluation**
- MAPE used to assess models.
- Prophet achieved the best score: **MAPE = 2.94**.
- Actual vs Predicted visualized.

### 5. **Model Selection**
- Evaluated SARIMA, Prophet, LSTM, Linear Regression.
- **Prophet** chosen for performance & interpretability.

### 6. **Model Training**
- Trained on historical data.
- Rolling forecast validation used.
- Preprocessed features improved accuracy.

### 7. **Sales Forecasting**
- Generated 7-day forecast with Prophet.
- Columns standardized, negatives clipped, rounded results.
- Saved forecast as `7_day_pizza_forecast.csv`.
- Aggregated and saved weekly forecast as `7week_day_pizza_forecast.csv`.

### 8. **Ingredient Planning**
- Merged ingredient dataset with forecasts.
- Calculated required quantity in kilograms.
- Created purchase order: `purchase_order_next_7_days.csv`.

### 9. **📊 Streamlit Dashboard**
- KPIs: total pizzas, ingredient weight.
- Interactive filters for pizza IDs.
- Line & bar charts for sales and demand.
- Ingredient usage visualized in pie/bar charts.
- Excel & CSV downloads enabled for all reports.

---

## ✅ Results

- 🔍 **Accurate forecasting with Prophet**
- 📦 **Ingredient demand calculated**
- 🛒 **Purchase orders generated**
- 📈 **Interactive Streamlit dashboard built**
- 💡 **Actionable business insights delivered**

---

## 📂 File Structure

```plaintext
📁 pizza-forecasting
├── feature_engineered.pkl
├── feature_engineered.xlsx
├── 7_day_pizza_forecast.csv
├── 7week_day_pizza_forecast.csv
├── purchase_order_next_7_days.csv
├── streamlit_app.py
├── notebooks/
├── data/
└── README.md
