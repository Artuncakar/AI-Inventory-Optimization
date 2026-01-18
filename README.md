# 📦 AI-Powered Inventory Optimization Dashboard

An interactive decision-support system designed for Industrial Engineers to optimize inventory levels using Machine Learning and classical Inventory Management models.

🚀 **[Live Demo: Click Here to Explore the Dashboard](https://artun-cakar-stok-yonetimi.streamlit.app/)**

## ✨ Core Engineering Features
- **Demand Forecasting:** Utilizes a **Linear Regression** model to predict future sales based on historical data.
- **Economic Order Quantity (EOQ):** Minimizes total holding and ordering costs to find the optimal order size.
- **Dynamic Safety Stock:** Calculates statistical safety levels based on the **Z-score** of a target Service Level.
- **Reorder Point (ROP):** Determines exactly when to re-order by considering lead time demand and safety buffers.

## 🛠️ Tech Stack
- **Language:** Python
- **Framework:** Streamlit (Web UI)
- **Data Science:** Pandas, NumPy, Scikit-learn, SciPy
- **Visualization:** Matplotlib

## 📊 Business Logic
This tool solves the "Overstock vs. Out-of-Stock" dilemma. By adjusting the **Service Level (%)** slider in the app, you can see how the **Safety Buffer (Orange Zone)** expands to protect the supply chain against uncertainty.

---
*Developed as part of an Industrial Engineering portfolio to showcase the integration of Data Science with Supply Chain management.*
