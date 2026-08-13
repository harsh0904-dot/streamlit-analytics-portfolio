# Streamlit Analytics Portfolio

A professional multi-page analytics portfolio built with **Streamlit**, **Pandas**, **NumPy**, and **Plotly** by **Harsh Vardhan Singh**.

This project showcases three end-to-end dashboard applications across different business domains:

- 🛒 **E-commerce Performance Dashboard**
- ✈️ **Travel Price Intelligence Dashboard**
- 🍽️ **Zomato Intelligence Dashboard**

Each dashboard is built as a production-style Streamlit experience with interactive filters, KPI cards, upload workflows, data quality checks, 2D/3D visualizations, and business storytelling.

---

## Live Demo

Live app URL: https://github.com/harsh0904-dot/streamlit-analytics-portfolio

After deployment on Streamlit Cloud, add the public app link here.

---

## Screenshots

Add screenshots or GIFs after final capture:

```text
screenshots/
├── portfolio-home.png
├── ecommerce-dashboard.png
├── travel-dashboard.png
└── zomato-dashboard.png
```

---

## Features

- Multi-page Streamlit portfolio app
- Premium portfolio homepage with dark/light mode
- Three domain-specific dashboard suites
- Upload → column mapping → quality check → dashboard workflow
- Bundled datasets for reproducible demo usage
- Interactive Plotly visualizations
- 3D visual exploration in each dashboard domain
- KPI cards and business metrics
- Sidebar filters and dynamic dashboard updates
- Clean folder structure for future dashboard expansion

---

## Dashboard Overview

### 🛒 E-commerce Performance Dashboard

A premium marketplace analytics dashboard focused on revenue, product performance, returns, fulfillment, and operations.

Highlights:

- Category tile filters
- Revenue, order, profit proxy, discount, and return KPIs
- Monthly revenue trends
- Product/category performance
- Payment and sales channel analysis
- Return rate analysis
- Shipment provider and warehouse breakdown
- 3D commerce universe visualization

Dataset:

```text
data/E-Commerce/online_sales_dataset.csv
```

---

### ✈️ Travel Price Intelligence Dashboard

A flight pricing analytics dashboard built around airline fares, route behavior, booking lead time, and travel-class insights.

Highlights:

- Airline and class filters
- Upload/mapping/quality flow
- Route heatmaps
- Fare trend by days-left
- Source/destination analysis
- Economy vs Business comparison
- Duration and stop analysis
- 3D fare space visualization

Dataset:

```text
data/Travel/Clean_Dataset.csv
```

---

### 🍽️ Zomato Intelligence Dashboard

A restaurant market intelligence dashboard for ratings, cuisines, city-level patterns, cost, votes, and geospatial insights.

Highlights:

- Upload/mapping/quality flow
- Demo dataset option
- City and cost filters
- Cuisine analysis
- Geo map
- Restaurant KPIs
- Weighted rating
- 3D restaurant space visualization
- Dark/light theme support

Dataset:

```text
data/zomato/zomato_data.xlsx
```

---

## Project Structure

```text
streamlit_portfolio/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   ├── E-Commerce/
│   │   └── online_sales_dataset.csv
│   ├── Travel/
│   │   └── Clean_Dataset.csv
│   └── zomato/
│       └── zomato_data.xlsx
└── pages/
    ├── 1_🛒_Ecommerce_Dashboard.py
    ├── 2_✈️_Travel_Dashboard.py
    └── 3_🍽️_Zomato_Dashboard.py
```

---

## Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Plotly**
- **OpenPyXL**
- **PyArrow**
- **xlrd**

---

## Local Setup

### 1. Open the project folder

```powershell
cd D:\StreamLit\streamlit_portfolio
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

```powershell
.venv\Scripts\activate
```

### 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 5. Install dependencies

```powershell
pip install -r requirements.txt
```

### 6. Run the app

```powershell
streamlit run app.py
```

Local URL:

```text
http://localhost:8501
```

---

## Deployment on Streamlit Cloud

1. Push this project to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click **New app**.
4. Select the GitHub repository.
5. Set the main file path as:

```text
app.py
```

6. Deploy the app.
7. Copy the public URL and add it to the **Live Demo** section.

Required files for deployment:

```text
app.py
pages/
data/
requirements.txt
.streamlit/config.toml
README.md
```

---

## Dataset Notes

The datasets are included locally inside the `data/` folder so the project works immediately after cloning.

For future dashboards, follow the same convention:

```text
data/<project-name>/<dataset-file>
```

Examples:

```text
data/marketing/campaign_data.csv
data/finance/transactions.csv
```

---

## Future Enhancements

Planned improvements:

- Add screenshots and demo GIFs
- Add deployed Streamlit Cloud link
- Add downloadable reports
- Add more dashboards such as marketing, finance, HR, or supply chain
- Add SQL-backed dashboards
- Add automated data validation scripts
- Add Docker support
- Add tests for data loading and transformations

---

## Author

**Harsh Vardhan Singh**

Analytics portfolio built to demonstrate practical dashboarding, data storytelling, and Python-based business intelligence using Streamlit.
