# olist-ecommerce-analytics
# 🛒 Decoding Brazilian E-Commerce
## A Strategic Analytics Case Study on Olist's Marketplace (2016–2018)

> *An end-to-end data analytics project structured as a consulting-style deliverable — combining Python analysis, business insights, and strategic recommendations.*

---

## 📌 Project Overview

This project analyses **100,000+ real e-commerce transactions** from Olist, Brazil's largest marketplace aggregator, to answer a core business question:

> **Which customer segments, product categories, and cities are driving growth — and where are the operational risks that need fixing?**

The output is not just code — it is a full **analyst case study** with KPIs, trend narratives, and board-level recommendations, structured the way a strategy consulting firm would present findings.

---

## 🎯 Business Problem Statement

Olist connects thousands of small retailers to major e-commerce platforms across Brazil. With rapid market expansion between 2016–2018, the business needs clarity on:

- Where is revenue growth coming from, and is it sustainable?
- Which product categories and cities are over/underperforming?
- Are logistics operations meeting customer expectations?
- What strategic actions will drive the next phase of growth?

---

## 📊 Key Findings at a Glance

| Metric | Value |
|--------|-------|
| 💰 Total Revenue | R$ 13.6M+ |
| 📦 Total Orders | 96,478 |
| 👤 Unique Customers | 96,000+ |
| 🏪 Active Sellers | 3,095 |
| ⭐ Avg Review Score | 4.09 / 5.0 |
| 🚚 On-Time Delivery Rate | ~93% |
| 📈 AOV Growth (18 months) | +25% |

---

## 💡 Top Insights

- 📈 **Revenue grew 140%** from Jan to Nov 2017, peaking during Brazil's Black Friday — a classic emerging-market S-curve adoption pattern
- 🏙️ **São Paulo alone** accounts for more customers than the next 4 cities combined — a geographic concentration risk
- ⭐ **Bimodal review pattern** — 57% give 5 stars, 11% give 1 star — almost no average ratings, pointing to a **seller quality consistency problem**, not a platform issue
- 💰 **Average Order Value rose 25%** over 18 months — customers are spending more per visit, a strong monetisation signal
- 🚚 **7% of orders arrive late** — this small percentage is responsible for a disproportionate share of negative reviews

---

## 📉 Charts Generated

| # | Chart | Business Purpose |
|---|-------|-----------------|
| 1 | Monthly Revenue Trend | Identifies growth trajectory and seasonal spikes |
| 2 | Monthly Order Volume | Tracks demand momentum over time |
| 3 | Top 15 Cities by Customers | Reveals geographic concentration risk |
| 4 | Top 15 Product Categories | Highlights category mix and revenue drivers |
| 5 | Top 10 Customers by Revenue | Identifies high-value segment for retention |
| 6 | Payment Value Distribution | Defines the true transaction sweet spot |
| 7 | Delivery Delay Analysis | Quantifies logistics performance vs promise |
| 8 | Order Status Distribution | Measures fulfillment health across platform |
| 9 | Average Order Value Trend | Tracks monetisation efficiency over time |
| 10 | Review Score Distribution | Surfaces customer satisfaction polarisation |

---

## 🗂️ Project Structure

```
olist-ecommerce-analytics/
│
├── olist_vscode_notebook.py   ← Full analysis script (VS Code / Jupyter)
├── olist_case_study.html      ← Consulting-style case study document
├── README.md                  ← You are here
│
└── outputs/                   ← All generated charts (PNG)
    ├── 01_monthly_revenue.png
    ├── 02_monthly_orders.png
    ├── 03_top_cities.png
    ├── 04_top_categories.png
    ├── 05_top_customers.png
    ├── 06_payment_distribution.png
    ├── 07_delivery_delay.png
    ├── 08_order_status.png
    ├── 09_aov_trend.png
    └── 10_review_scores.png
```

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python** (pandas, matplotlib, seaborn) | Data cleaning, merging, analysis, visualisation |
| **SQL** | Relational data querying and joining logic |
| **Power BI** | Interactive dashboard design |
| **Excel** | Exploratory data checks and validation |

---

## ▶️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOURUSERNAME/olist-ecommerce-analytics.git
```

**2. Install dependencies**
```bash
pip install pandas matplotlib seaborn
```

**3. Download the dataset**

Get the CSV files from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and update the `DATA` path in the script:
```python
DATA = r"C:\your\path\to\csv\files\\"
```

**4. Run the notebook**

Open `olist_vscode_notebook.py` in VS Code. Each `# %%` block is a separate cell. Run cell by cell with `Shift + Enter`.

---

## 🧠 Strategic Recommendations

**1. 🎯 Launch a Customer Retention Engine**
Near-zero repeat purchase rates represent a massive LTV opportunity. A post-purchase CRM programme with loyalty incentives could increase revenue per customer by 40–60%.

**2. 🗺️ Geographic Expansion to Tier-2 Cities**
Fortaleza, Manaus, and Recife are large cities with low marketplace penetration. Targeted seller acquisition there would reduce freight times and unlock ~25M new potential customers.

**3. 📦 Seller Quality Tiering System**
Introduce a transparent seller scorecard (delivery SLA + review score + cancellation rate) with search ranking rewards for top performers — directly addressing the bimodal review problem.

**4. 💳 AOV Growth via Bundling & Instalments**
Brazil's strong instalment ("parcelamento") culture means promoting 0% instalment options on R$200+ baskets could push AOV from R$175 toward R$220 without acquiring new users.

---

## 📂 Dataset

**Olist Brazilian E-Commerce Public Dataset**
- Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 9 relational tables | ~100K orders | Sep 2016 – Oct 2018
- Note: Raw CSV files are not included in this repo (Kaggle license). Download directly from the link above.

---

## 👤 Author

Dhriti Garg
Aspiring Business / Data Analyst | Python · SQL · Power BI · Excel


---

*This project was built as a portfolio case study for business analyst internship applications, demonstrating end-to-end analytical thinking from raw data to strategic recommendations.*
