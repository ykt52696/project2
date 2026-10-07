import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 讀取資料

df = pd.read_csv("project2_dataset.csv")

# 資料清理

 # 移除重複資料
df = df.drop_duplicates()

 # 日期格式轉換
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d/%m/%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d/%m/%Y"
)

 # 需要清理的文字欄位
text_cols = [
    "Ship Mode",
    "Customer ID",
    "Customer Name",
    "Segment",
    "Country",
    "City",
    "State",
    "Region",
    "Product ID",
    "Category",
    "Product Name"
]     # The "Sub-Category" column was unintentionally overlooked during the data analysis process and was not included in the current analysis.

 # 移除文字前後空白
df[text_cols] = df[text_cols].apply(
    lambda x: x.astype("string").str.strip()
)


 # 建立時間欄位

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month


# 基本分析

 # Category 銷售總額
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

 # Category 平均銷售額
category_avg_sales = (
    df.groupby("Category")["Sales"]
    .mean()
    .sort_values(ascending=False)
)

 # Region 銷售總額
region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

 # State 銷售總額 Top 10
state_sales = (
    df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

 # Product 銷售總額 Top 10
product_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

 # Customer 銷售總額 Top 10
customer_sales = (
    df.groupby(["Customer ID", "Customer Name"])["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)


# 月份銷售分析

 # 每月總銷售額
monthly_sales = (
    df.groupby(["Year", "Month"])["Sales"]
    .sum()
    .reset_index()
)

 # 建立 Year-Month 欄位
monthly_sales["Year_Month"] = (
    monthly_sales["Year"].astype(str)
    + "-"
    + monthly_sales["Month"].astype(str).str.zfill(2)
)

 # 按時間排序
monthly_sales = monthly_sales.sort_values(
    ["Year", "Month"]
)

 # Top 5 銷售月份
top5_month = (
    monthly_sales
    .sort_values("Sales", ascending=False)
    .head(5)
)


# Category × Month 分析

category_monthly = (
    df.groupby(
        ["Year", "Month", "Category"]
    )["Sales"]
    .sum()
    .reset_index()
)

category_monthly["Year_Month"] = (
    category_monthly["Year"].astype(str)
    + "-"
    + category_monthly["Month"].astype(str).str.zfill(2)
)



# Category × Region 分析


category_region = pd.pivot_table(
    df,
    values="Sales",
    index="Region",
    columns="Category",
    aggfunc="sum"
)

 # 每個 Region 銷售最高的 Category
top_category_by_region = category_region.idxmax(axis=1)

 # 每個 Region 最高 Category 的銷售額
top_sales_by_region = category_region.max(axis=1)

 # 建立摘要表
region_summary = pd.DataFrame({
    "Top Category": top_category_by_region,
    "Top Sales": top_sales_by_region
})

 # 每個 Region 第二高的 Category 銷售額
second_category_sales = category_region.apply(
    lambda row: row.drop(
        top_category_by_region[row.name]
    ).max(),
    axis=1
)

 # 第一名與第二名的銷售差距
gap = top_sales_by_region - second_category_sales

 # 差距百分比
gap_percent = (
    gap / second_category_sales * 100
)


# 找出最高 / 最低銷售月份

max_month_index = monthly_sales["Sales"].idxmax()

max_month = monthly_sales.loc[max_month_index]

min_month_index = monthly_sales["Sales"].idxmin()

min_month = monthly_sales.loc[min_month_index]


# 視覺化


 # Chart 1：Monthly Sales Trend


plt.figure(figsize=(12, 5))

plt.plot(
    monthly_sales["Year_Month"],
    monthly_sales["Sales"],
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.title("Monthly Sales Trend")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/monthly_sales_trend.png"
)

plt.show()


 # Chart 2：Total Sales by Category


plt.figure(figsize=(8, 5))

plt.bar(
    category_sales.index,
    category_sales.values
)

plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.title("Total Sales by Category")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/sales_by_category.png"
)

plt.show()


 # Chart 3：Sales by Region and Category


plt.figure(figsize=(10, 6))

category_region.plot(
    kind="bar"
)

plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.title("Sales by Region and Category")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "charts/sales_by_region_category.png"
)

plt.show()


 # Chart 4：Top 10 States by Sales


plt.figure(figsize=(10, 6))

plt.bar(
    state_sales.index,
    state_sales.values
)

plt.xlabel("State")
plt.ylabel("Total Sales")
plt.title("Top 10 States by Sales")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/top10_states_by_sales.png"
)

plt.show()



 # Chart 5：Top 10 Customers by Sales


plt.figure(figsize=(10, 6))

plt.barh(
    customer_sales["Customer Name"],
    customer_sales["Sales"]
)

plt.xlabel("Total Sales")
plt.ylabel("Customer")
plt.title("Top 10 Customers by Sales")

plt.tight_layout()

plt.savefig(
    "charts/top10_customers_by_sales.png"
)

plt.show()

