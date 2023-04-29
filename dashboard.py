### MENYIAPKAN DATAFRAME

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

### CREATE HELPER FUNCTION
### CREATE SHIPPING LIMIT DATE
def create_shipping_limit_date_df(df):
    shipping_limit_date_df = df.resample(rule='D', on='shipping_limit_date').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    shipping_limit_date_df = shipping_limit_date_df.reset_index()
    shipping_limit_date_df.rename(columns={
        "order_id": "shipping_count",
        "price": "revenue"
    }, inplace=True)

    return shipping_limit_date_df

### Create_sum_order_highprice_items_df() yang bertanggung jawab untuk menyiapkan sum_order_highprice_items_df
def create_sum_order_highprice_items_df(df):
    sum_order_highprice_items_df = all_df.groupby("product_category_name").price.sum().sort_values(ascending=False).reset_index()
    return sum_order_highprice_items_df

### Create_sum_order_highptice_items_df() yang bertanggung jawab untuk menyiapkan sum_order_lowprice_items_df
def create_sum_order_lowprice_items_df(df):
    sum_order_lowprice_items_df = all_df.groupby("product_category_name").price.sum().sort_values(ascending=False).reset_index()
    return sum_order_lowprice_items_df

### create_bystate_df() digunakan untuk menyiapkan bystate_df
def create_bystate_df(df):
    bystate_df = all_df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bystate_df

### create_bytopcity_df() digunakan untuk menyiapkan bytopcity_df
def create_bytopcity_df(df):
    bycity_df = all_df.groupby("customer_city").agg(
        {"customer_id": pd.Series.nunique}
    ).reset_index().rename(columns={"customer_id": "customer_count"})

    top_cities = bycity_df.sort_values(
        "customer_count", ascending=False
    ).reset_index(drop=True)[:10]

    top_customers = all_df[all_df["customer_city"].isin(top_cities["customer_city"])]

    bytopcity_df = top_customers.groupby("customer_city").agg(
        {"customer_id": pd.Series.nunique}
    ).reset_index().rename(columns={"customer_id": "customer_count"})

    bytopcity_df = bytopcity_df.sort_values(
        "customer_count", ascending=False
    ).reset_index(drop=True)

    return bytopcity_df

### create_bybottomcity_df() digunakan untuk menyiapkan bybottomcity_df
def create_bybottomcity_df(df):
    bycity_df = all_df.groupby("customer_city").agg(
        {"customer_id": pd.Series.nunique}
    ).reset_index().rename(columns={"customer_id": "customer_count"})

    bottom_cities = bycity_df.sort_values(
        "customer_count", ascending=True
    ).reset_index(drop=True)[:10]

    bottom_customers = all_df[all_df["customer_city"].isin(bottom_cities["customer_city"])]

    bybottomcity_df = bottom_customers.groupby("customer_city").agg(
        {"customer_id": pd.Series.nunique}
    ).reset_index().rename(columns={"customer_id": "customer_count"})

    bybottomcity_df = bybottomcity_df.sort_values(
        "customer_count", ascending=True
    ).reset_index(drop=True)

    return bybottomcity_df

### create_bybottomcity_df() digunakan untuk menyiapkan bybottomcity_df
def create_order_payment_df(df):
    order_payment_df = all_df.groupby('payment_type')['payment_value'].count().reset_index(name='count')

    return order_payment_df

### Load Berkas all_data.csv
all_df = pd.read_csv("all_data.csv")

### Urutkan DataFrame berdasarkan shipping_limit_date dan pastikan kolomnya bertipe datetime
datetime_columns = ["shipping_limit_date"]
all_df.sort_values(by="shipping_limit_date", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


## MEMBUAT KOMPONEN FILTER
min_date = all_df["shipping_limit_date"].min()
max_date = all_df["shipping_limit_date"].max()

st.markdown(
    """
    # Welcome to Kumaku E-Commerce
    Hello, customers!
    """
)

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Information of Shipping Limit Date', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    # Mennyertakan slider
    with st.sidebar:

        values = st.slider(
            label='How much fun to shopping in Kumaku E-Commerce?',
            min_value=0, max_value=100, value=(0, 100)
        )
        st.write('Values:', values)
### start_date dan end_date untuk memfilter all_df. Data yang telah difilter disimpan dalam main_df.
main_df = all_df[(all_df["shipping_limit_date"] >= str(start_date)) &
                (all_df["shipping_limit_date"] <= str(end_date))]

## HELPER FUNCTION
shipping_limit_date_df = create_shipping_limit_date_df(main_df)
sum_order_highprice_items_df = create_sum_order_highprice_items_df(main_df)
sum_order_lowprice_items_df = create_sum_order_lowprice_items_df(main_df)
bystate_df = create_bystate_df(main_df)
bytopcity_df = create_bytopcity_df(main_df)
bybottomcity_df = create_bybottomcity_df(main_df)
order_payment_df = create_order_payment_df(main_df)

## MELENGKAPI DASHBOARD DENGAN BERBAGAI VISUALISASI DATA

### Menambahkan Header
st.header('Kumaku E-Commerce Dashboard :sparkles:')

## Tampilkan informasi shipping date order dan total order dan revenue dalam range waktu tertentu.

## Tampilkan 15 produk termahal dan termurah di Kumaku E-Commerce
st.subheader("High & Low Price Products")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#2ca25f"]

sns.barplot(x="price", y="product_category_name", data=sum_order_highprice_items_df.head(15), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Orders", fontsize=30)
ax[0].set_title("High Price Products", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="price", y="product_category_name",
            data=sum_order_lowprice_items_df.sort_values(by="price", ascending=True).head(15), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Orders", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Low Price Products", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

## Tampilkan Demografi Pelanggan
## Demografi Pelanggan berdasarkan Negara, 10 Kota Penyumbang Pelanggan Terbanyak &
# 10 Kota Penyumbang Pelanggan Terendah
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#2ca25f"]

    sns.barplot(
        y="customer_count",
        x="customer_city",
        data=bytopcity_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Top 10 Cities by Number of Customers", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#2ca25f"]

    sns.barplot(
        y="customer_count",
        x="customer_city",
        data=bybottomcity_df.sort_values(by="customer_city", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Bottom 10 Cities by Number of Customers", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#2ca25f"]
sns.barplot(
    x="customer_count",
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

## Tampilkan Order Payment
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#99d8c9", "#2ca25f"]
sns.barplot(
    x='payment_type',
    y='count',
    data=order_payment_df,
    palette=colors,
    ax=ax)
ax.set_title('Number of Transactions by Payment Type')
ax.set_xlabel('Payment Type')
ax.set_ylabel('Number of Transactions')
st.pyplot(fig)




