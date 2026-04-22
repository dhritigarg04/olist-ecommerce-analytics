"""
=============================================================================
PROJECT: Decoding Brazilian E-Commerce — A Strategic Analytics Deep Dive
         into Olist's Marketplace Performance (2016–2018)
=============================================================================
Author  : [Your Name]
Dataset : Olist Brazilian E-Commerce Public Dataset (Kaggle)
Tools   : Python | pandas | matplotlib | seaborn
Purpose : Portfolio project for business analyst / strategy internship
=============================================================================

HOW TO USE THIS SCRIPT
-----------------------
1. Download the dataset from:
   https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. Extract all CSV files into a folder called  'data/'  in the same directory
   as this script.
3. Run:  python olist_analysis.py
4. All charts are saved as high-resolution PNGs inside  'outputs/'

=============================================================================
"""

# ── 0. IMPORTS ───────────────────────────────────────────────────────────────
import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

warnings.filterwarnings("ignore")

# Create output directory for saving charts
os.makedirs("outputs", exist_ok=True)

# ── GLOBAL STYLE ─────────────────────────────────────────────────────────────
# A clean, corporate colour palette suited for strategy/consulting presentations
BRAND_BLUE   = "#1B3A6B"   # deep navy  – primary
ACCENT_TEAL  = "#00A896"   # teal       – highlight / positive
ACCENT_AMBER = "#F4A261"   # amber      – secondary highlight
ACCENT_RED   = "#E63946"   # red        – negative / alert
LIGHT_GREY   = "#F0F4F8"   # background panels
MID_GREY     = "#8D99AE"   # gridlines / annotations

plt.rcParams.update({
    "figure.facecolor"  : "white",
    "axes.facecolor"    : LIGHT_GREY,
    "axes.edgecolor"    : "white",
    "axes.grid"         : True,
    "grid.color"        : "white",
    "grid.linewidth"    : 1.2,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.spines.left"  : False,
    "axes.spines.bottom": False,
    "axes.titlesize"    : 14,
    "axes.titleweight"  : "bold",
    "axes.titlepad"     : 14,
    "axes.labelsize"    : 11,
    "axes.labelcolor"   : BRAND_BLUE,
    "xtick.labelsize"   : 9,
    "ytick.labelsize"   : 9,
    "xtick.color"       : MID_GREY,
    "ytick.color"       : MID_GREY,
    "font.family"       : "DejaVu Sans",
    "legend.frameon"    : False,
    "legend.fontsize"   : 9,
})

def save(fig, name):
    """Save a figure to the outputs/ folder at presentation quality."""
    path = f"outputs/{name}.png"
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✔  Saved → {path}")

def section(title):
    print(f"\n{'='*70}\n  {title}\n{'='*70}")


# ═══════════════════════════════════════════════════════════════════════════
# 1. DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════
section("1 · LOADING DATA")

DATA = "data/"   # ← change this path if your CSVs live elsewhere

# Load every relevant table from the Olist dataset
orders      = pd.read_csv(f"{DATA}olist_orders_dataset.csv")
order_items = pd.read_csv(f"{DATA}olist_order_items_dataset.csv")
customers   = pd.read_csv(f"{DATA}olist_customers_dataset.csv")
payments    = pd.read_csv(f"{DATA}olist_order_payments_dataset.csv")
products    = pd.read_csv(f"{DATA}olist_products_dataset.csv")
sellers     = pd.read_csv(f"{DATA}olist_sellers_dataset.csv")
reviews     = pd.read_csv(f"{DATA}olist_order_reviews_dataset.csv")
geo         = pd.read_csv(f"{DATA}olist_geolocation_dataset.csv")
category    = pd.read_csv(f"{DATA}product_category_name_translation.csv")

print("  All 9 tables loaded successfully.")


# ═══════════════════════════════════════════════════════════════════════════
# 2. DATA CLEANING & PREPARATION
# ═══════════════════════════════════════════════════════════════════════════
section("2 · CLEANING & PREPARATION")

# ── 2a. Parse all date columns ───────────────────────────────────────────────
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# ── 2b. Keep only delivered orders for revenue/time analysis ────────────────
delivered = orders[orders["order_status"] == "delivered"].copy()

# ── 2c. Derive time features ────────────────────────────────────────────────
delivered["year_month"] = delivered["order_purchase_timestamp"].dt.to_period("M")
delivered["year"]       = delivered["order_purchase_timestamp"].dt.year

# ── 2d. Delivery delay in days (negative = delivered EARLY) ─────────────────
delivered["delivery_delay_days"] = (
    delivered["order_delivered_customer_date"]
    - delivered["order_estimated_delivery_date"]
).dt.days

# ── 2e. Translate product category names to English ─────────────────────────
products = products.merge(category, on="product_category_name", how="left")

# ── 2f. Build the MASTER analytical table ───────────────────────────────────
# orders + customers + items + payments + products + sellers
master = (
    delivered
    .merge(customers,   on="customer_id",   how="left")
    .merge(order_items, on="order_id",       how="left")
    .merge(products,    on="product_id",     how="left")
    .merge(payments,    on="order_id",       how="left")
    .merge(sellers,     on="seller_id",      how="left")
)

# ── 2g. Handle missing values ───────────────────────────────────────────────
master["product_category_name_english"].fillna("Unknown", inplace=True)
master["delivery_delay_days"].fillna(
    master["delivery_delay_days"].median(), inplace=True
)

print(f"  Master table shape: {master.shape[0]:,} rows × {master.shape[1]} cols")
print(f"  Date range: {delivered['order_purchase_timestamp'].min().date()} "
      f"→ {delivered['order_purchase_timestamp'].max().date()}")


# ═══════════════════════════════════════════════════════════════════════════
# 3. KEY PERFORMANCE INDICATORS
# ═══════════════════════════════════════════════════════════════════════════
section("3 · KEY PERFORMANCE INDICATORS")

total_revenue   = master["payment_value"].sum()
total_orders    = master["order_id"].nunique()
total_customers = master["customer_id"].nunique()
total_sellers   = master["seller_id"].nunique()
avg_order_value = total_revenue / total_orders
avg_review      = reviews["review_score"].mean()
on_time_rate    = (master["delivery_delay_days"] <= 0).mean() * 100

print(f"""
  ┌─────────────────────────────────────────────┐
  │  OLIST  |  HEADLINE KPIs (Delivered Orders) │
  ├─────────────────────────────────────────────┤
  │  Total Revenue        : R$ {total_revenue:>12,.0f}     │
  │  Total Orders         : {total_orders:>12,}           │
  │  Unique Customers     : {total_customers:>12,}           │
  │  Active Sellers       : {total_sellers:>12,}           │
  │  Avg Order Value      : R$ {avg_order_value:>12,.2f}     │
  │  Avg Review Score     : {avg_review:>12.2f} / 5.0      │
  │  On-Time Delivery Rate: {on_time_rate:>12.1f}%          │
  └─────────────────────────────────────────────┘
""")


# ═══════════════════════════════════════════════════════════════════════════
# 4. CHARTS
# ═══════════════════════════════════════════════════════════════════════════
section("4 · GENERATING CHARTS")

# ── CHART 1 : Monthly Revenue Trend ─────────────────────────────────────────
print("\n  Chart 1 · Monthly Revenue Trend")

monthly_rev = (
    master.groupby("year_month")["payment_value"]
    .sum()
    .reset_index()
    .sort_values("year_month")
)
monthly_rev["year_month_str"] = monthly_rev["year_month"].astype(str)
# Remove sparse early months (< 2017) for a clean story
monthly_rev = monthly_rev[monthly_rev["year_month"] >= pd.Period("2017-01")]

fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(
    monthly_rev["year_month_str"],
    monthly_rev["payment_value"],
    alpha=0.18, color=BRAND_BLUE
)
ax.plot(
    monthly_rev["year_month_str"],
    monthly_rev["payment_value"],
    color=BRAND_BLUE, linewidth=2.5, marker="o", markersize=5
)
# Annotate peak month
peak_idx = monthly_rev["payment_value"].idxmax()
ax.annotate(
    f"Peak\nR$ {monthly_rev.loc[peak_idx,'payment_value']/1e6:.1f}M",
    xy=(monthly_rev.loc[peak_idx,"year_month_str"],
        monthly_rev.loc[peak_idx,"payment_value"]),
    xytext=(0, 18), textcoords="offset points",
    ha="center", fontsize=8.5, color=BRAND_BLUE, fontweight="bold",
    arrowprops=dict(arrowstyle="-", color=BRAND_BLUE, lw=1)
)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"R$ {x/1e6:.1f}M"))
ax.set_xticks(range(len(monthly_rev)))
ax.set_xticklabels(monthly_rev["year_month_str"], rotation=45, ha="right")
ax.set_title("Monthly Revenue Trend  |  Jan 2017 – Aug 2018", color=BRAND_BLUE)
ax.set_xlabel("")
ax.set_ylabel("Gross Revenue (R$)")
fig.tight_layout()
save(fig, "01_monthly_revenue_trend")

# ── CHART 2 : Monthly Order Volume ──────────────────────────────────────────
print("  Chart 2 · Monthly Order Volume")

monthly_orders = (
    master.groupby("year_month")["order_id"]
    .nunique().reset_index()
    .sort_values("year_month")
    .rename(columns={"order_id": "num_orders"})
)
monthly_orders = monthly_orders[monthly_orders["year_month"] >= pd.Period("2017-01")]
monthly_orders["ym_str"] = monthly_orders["year_month"].astype(str)

fig, ax = plt.subplots(figsize=(13, 5))
bars = ax.bar(
    monthly_orders["ym_str"],
    monthly_orders["num_orders"],
    color=ACCENT_TEAL, edgecolor="white", linewidth=0.6, zorder=3
)
# Colour the max bar differently
max_i = monthly_orders["num_orders"].idxmax()
bars[monthly_orders.index.get_loc(max_i)].set_color(BRAND_BLUE)

ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_xticklabels(monthly_orders["ym_str"], rotation=45, ha="right")
ax.set_title("Monthly Order Volume  |  Jan 2017 – Aug 2018", color=BRAND_BLUE)
ax.set_ylabel("Number of Orders")
fig.tight_layout()
save(fig, "02_monthly_order_volume")

# ── CHART 3 : Top 15 Cities by Customer Count ───────────────────────────────
print("  Chart 3 · Top 15 Cities by Customers")

top_cities = (
    master.groupby("customer_city")["customer_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
    .rename(columns={"customer_id": "customers"})
)
top_cities["customer_city"] = top_cities["customer_city"].str.title()

fig, ax = plt.subplots(figsize=(11, 6))
colors = [BRAND_BLUE if i < 3 else ACCENT_TEAL for i in range(len(top_cities))]
bars = ax.barh(
    top_cities["customer_city"][::-1],
    top_cities["customers"][::-1],
    color=colors[::-1], edgecolor="white", linewidth=0.5
)
for bar, val in zip(bars, top_cities["customers"][::-1]):
    ax.text(bar.get_width() + 30, bar.get_y() + bar.get_height()/2,
            f"{val:,}", va="center", fontsize=8.5, color=BRAND_BLUE)
ax.set_title("Top 15 Cities by Customer Base", color=BRAND_BLUE)
ax.set_xlabel("Unique Customers")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
fig.tight_layout()
save(fig, "03_top_cities_customers")

# ── CHART 4 : Top 15 Product Categories by Sales Volume ─────────────────────
print("  Chart 4 · Top 15 Product Categories")

top_cats = (
    master.groupby("product_category_name_english")["order_id"]
    .count()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
    .rename(columns={"order_id": "items_sold"})
)

fig, ax = plt.subplots(figsize=(11, 6))
palette = [BRAND_BLUE] + [ACCENT_TEAL] * 4 + [MID_GREY] * 10
ax.barh(
    top_cats["product_category_name_english"][::-1],
    top_cats["items_sold"][::-1],
    color=palette[::-1], edgecolor="white"
)
for i, (_, row) in enumerate(top_cats[::-1].iterrows()):
    ax.text(row["items_sold"] + 80,
            i, f"{row['items_sold']:,}",
            va="center", fontsize=8, color=BRAND_BLUE)
ax.set_title("Top 15 Product Categories by Items Sold", color=BRAND_BLUE)
ax.set_xlabel("Items Sold")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
fig.tight_layout()
save(fig, "04_top_product_categories")

# ── CHART 5 : Top 10 Customers by Lifetime Revenue ──────────────────────────
print("  Chart 5 · Top 10 Customers by Revenue")

top_cust = (
    master.groupby("customer_unique_id")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
top_cust["label"] = [f"Customer {i+1:02d}" for i in range(len(top_cust))]

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(top_cust["label"], top_cust["payment_value"],
       color=[BRAND_BLUE if i == 0 else ACCENT_TEAL for i in range(10)],
       edgecolor="white", zorder=3)
for i, val in enumerate(top_cust["payment_value"]):
    ax.text(i, val + 50, f"R$ {val:,.0f}", ha="center", fontsize=8,
            color=BRAND_BLUE, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.set_title("Top 10 Customers by Lifetime Revenue (Anonymised)", color=BRAND_BLUE)
ax.set_ylabel("Total Revenue (R$)")
fig.tight_layout()
save(fig, "05_top_customers_revenue")

# ── CHART 6 : Payment Value Distribution ────────────────────────────────────
print("  Chart 6 · Payment Value Distribution")

pay_data = master.drop_duplicates("order_id")["payment_value"].dropna()
pay_data = pay_data[pay_data < pay_data.quantile(0.99)]  # trim extreme outliers

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(pay_data, bins=60, color=BRAND_BLUE, edgecolor="white",
        alpha=0.85, zorder=3)
ax.axvline(pay_data.median(), color=ACCENT_AMBER, linewidth=2,
           label=f"Median  R$ {pay_data.median():.0f}")
ax.axvline(pay_data.mean(),   color=ACCENT_RED,   linewidth=2, linestyle="--",
           label=f"Mean    R$ {pay_data.mean():.0f}")
ax.legend()
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_title("Distribution of Order Payment Values", color=BRAND_BLUE)
ax.set_xlabel("Payment Value (R$)")
ax.set_ylabel("Number of Orders")
fig.tight_layout()
save(fig, "06_payment_value_distribution")

# ── CHART 7 : Delivery Delay Analysis ───────────────────────────────────────
print("  Chart 7 · Delivery Delay Analysis")

delay_data = master.drop_duplicates("order_id")["delivery_delay_days"].dropna()
delay_data = delay_data[
    (delay_data > delay_data.quantile(0.01)) &
    (delay_data < delay_data.quantile(0.99))
]

on_time_pct  = (delay_data <= 0).mean() * 100
late_pct     = (delay_data  > 0).mean() * 100

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Left: histogram
axes[0].hist(delay_data[delay_data <= 0], bins=40,
             color=ACCENT_TEAL, edgecolor="white", alpha=0.9,
             label=f"On-time / Early ({on_time_pct:.1f}%)", zorder=3)
axes[0].hist(delay_data[delay_data > 0],  bins=40,
             color=ACCENT_RED,  edgecolor="white", alpha=0.9,
             label=f"Late ({late_pct:.1f}%)", zorder=3)
axes[0].axvline(0, color=BRAND_BLUE, linewidth=1.5, linestyle="--")
axes[0].legend()
axes[0].set_title("Delivery Delay Distribution", color=BRAND_BLUE)
axes[0].set_xlabel("Days vs. Promised Date (negative = early)")
axes[0].set_ylabel("Orders")

# Right: donut
sizes  = [on_time_pct, late_pct]
labels = [f"On-Time\n{on_time_pct:.1f}%", f"Late\n{late_pct:.1f}%"]
wedge_props = {"width": 0.45, "edgecolor": "white", "linewidth": 2}
axes[1].pie(sizes, labels=labels, colors=[ACCENT_TEAL, ACCENT_RED],
            wedgeprops=wedge_props, startangle=90,
            textprops={"fontsize": 10, "color": BRAND_BLUE, "fontweight": "bold"})
axes[1].set_title("On-Time vs. Late Delivery Split", color=BRAND_BLUE)

fig.tight_layout()
save(fig, "07_delivery_delay_analysis")

# ── CHART 8 : Order Status Distribution ─────────────────────────────────────
print("  Chart 8 · Order Status Distribution")

status_counts = orders["order_status"].value_counts().reset_index()
status_counts.columns = ["status", "count"]
status_counts["pct"] = status_counts["count"] / status_counts["count"].sum() * 100
# Colour mapping by status type
color_map = {
    "delivered"  : ACCENT_TEAL,
    "shipped"    : BRAND_BLUE,
    "canceled"   : ACCENT_RED,
    "unavailable": ACCENT_AMBER,
    "processing" : MID_GREY,
    "invoiced"   : "#2D6A4F",
    "approved"   : "#457B9D",
    "created"    : "#A8DADC",
}
bar_colors = [color_map.get(s, MID_GREY) for s in status_counts["status"]]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(status_counts["status"], status_counts["count"],
              color=bar_colors, edgecolor="white", zorder=3)
for bar, row in zip(bars, status_counts.itertuples()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
            f"{row.pct:.1f}%", ha="center", fontsize=8.5,
            color=BRAND_BLUE, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_title("Order Status Distribution  |  All Orders", color=BRAND_BLUE)
ax.set_ylabel("Number of Orders")
fig.tight_layout()
save(fig, "08_order_status_distribution")

# ── CHART 9 : Average Order Value Trend ─────────────────────────────────────
print("  Chart 9 · Average Order Value Trend")

aov_trend = (
    master.drop_duplicates("order_id")
    .groupby("year_month")["payment_value"]
    .mean()
    .reset_index()
    .sort_values("year_month")
)
aov_trend = aov_trend[aov_trend["year_month"] >= pd.Period("2017-01")]
aov_trend["ym_str"] = aov_trend["year_month"].astype(str)

fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(aov_trend["ym_str"], aov_trend["payment_value"],
                alpha=0.15, color=ACCENT_AMBER)
ax.plot(aov_trend["ym_str"], aov_trend["payment_value"],
        color=ACCENT_AMBER, linewidth=2.5, marker="s", markersize=5)
# Rolling 3-month average
rolling = aov_trend["payment_value"].rolling(3, min_periods=1).mean()
ax.plot(aov_trend["ym_str"], rolling,
        color=BRAND_BLUE, linewidth=1.5, linestyle="--",
        label="3-Month Rolling Avg")
ax.legend()
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R$ {x:.0f}"))
ax.set_xticklabels(aov_trend["ym_str"], rotation=45, ha="right")
ax.set_title("Average Order Value (AOV) Trend  |  Jan 2017 – Aug 2018",
             color=BRAND_BLUE)
ax.set_ylabel("Avg Order Value (R$)")
fig.tight_layout()
save(fig, "09_average_order_value_trend")

# ── CHART 10 : Review Score Distribution (Bonus) ────────────────────────────
print("  Chart 10 · Review Score Distribution (bonus)")

score_counts = reviews["review_score"].value_counts().sort_index()
score_pcts   = (score_counts / score_counts.sum() * 100).round(1)
score_colors = [ACCENT_RED, ACCENT_RED, ACCENT_AMBER,
                ACCENT_TEAL, ACCENT_TEAL]   # 1-2 red, 3 amber, 4-5 green

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(score_counts.index, score_counts.values,
              color=score_colors, edgecolor="white", width=0.6, zorder=3)
for bar, pct in zip(bars, score_pcts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f"{pct}%", ha="center", fontsize=9,
            color=BRAND_BLUE, fontweight="bold")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_title("Customer Review Score Distribution  (1 = Poor → 5 = Excellent)",
             color=BRAND_BLUE)
ax.set_xlabel("Review Score")
ax.set_ylabel("Number of Reviews")
fig.tight_layout()
save(fig, "10_review_score_distribution")


# ═══════════════════════════════════════════════════════════════════════════
# 5. SUMMARY EXPORT  (optional — useful for Power BI import)
# ═══════════════════════════════════════════════════════════════════════════
section("5 · EXPORTING SUMMARY TABLES")

monthly_rev.to_csv("outputs/summary_monthly_revenue.csv", index=False)
top_cats.to_csv("outputs/summary_top_categories.csv", index=False)
top_cities.to_csv("outputs/summary_top_cities.csv", index=False)
status_counts.to_csv("outputs/summary_order_status.csv", index=False)

print("  Summary CSVs saved → outputs/")
print("\n  ✅  All done! Open the 'outputs/' folder to find your charts.\n")
