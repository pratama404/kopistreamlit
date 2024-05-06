import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Kedai tera", page_icon="☕", layout="wide")
st.title("Dashboard penjualan kopi tera 🦖")
st.markdown(
    "<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True
)

# Load the data
df = pd.read_excel('saleskopi.xlsx')



# Buat sorting tanggal
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Buat tanggal awal dan akhir
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()


st.sidebar.title("About")
st.sidebar.markdown(
    "**[Ageng Putra Pratama](https://lynk.id/agengputrapratama)**")
st.sidebar.info("Dashboard ini menampilkan visualisasi untuk sekumpulan data Penjualan Kopi ☕. "
                "Dataset ini berisi infomasi hasil penjualan kopi dari tahun 2019- 2022 di beberapa kota di tiap negara dengan tipe dan jenis kopi masing masing.")
st.sidebar.markdown("[Download Dataset](https://github.com/pratama404/kopistreamlit/raw/main/saleskopi.xlsx)")

if st.sidebar.checkbox("Lihat EDA dulu !"):
    st.subheader("Exploratory data analysis")
    st.write(df.describe())


# Sidebar untuk filter tanggal
st.sidebar.header("Filter")
startDate = df['Order Date'].min().date()
endDate = df['Order Date'].max().date()
date1 = st.sidebar.date_input(":date: Tanggal awal", startDate)
date2 = st.sidebar.date_input(":date: Tanggal Akhir", endDate)

# Filter data berdasarkan rentang tanggal yang dipilih
df_filtered = df[(df["Order Date"].dt.date >= date1) & (df["Order Date"].dt.date <= date2)].copy()

# Hitung jumlah hari antara dua tanggal yang dipilih
days_diff = (date2 - date1).days

# Tampilkan output setiap kali rentang tanggal berubah
st.write(f"Rentang waktu yang dipilih: {date1} sampai {date2}")
st.write(f"Jumlah hari antara dua tanggal yang dipilih: {days_diff} hari")


# Filter negara
country = st.sidebar.multiselect(":world_map: Negara", df["Customer Country"].unique())
if not country:
    df_filtered = df.copy()
else:
    df_filtered = df[df["Customer Country"].isin(country)]

# Filter kota
city = st.sidebar.multiselect(":cityscape: Kota", df_filtered["Customer City"].unique())
if not city:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Customer City"].isin(city)]

# Filter Loyalty Card
card = st.sidebar.multiselect(
    ":credit_card: Loyalti Card",
    df_filtered["Customer Loyalty Card"].unique(),
)
if not card:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Customer Loyalty Card"].isin(card)]

# Filter jenis kopi
coffee_type = st.sidebar.multiselect(
    ":coffee: Tipe Kopi", df_filtered["Product Coffee Type"].unique()
)
if not coffee_type:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Product Coffee Type"].isin(coffee_type)]

# Filter jenis sangrai
roast_type = st.sidebar.multiselect(
    ":fire: Tipe Sangrai", df_filtered["Product Roast Type"].unique()
)
if not roast_type:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Product Roast Type"].isin(roast_type)]

# Filter ukuran
size = st.sidebar.multiselect(
    ":cup_with_straw: Tipe Ukuran", df_filtered["Product Size (kg)"].unique()
)
if not size:
    df_filtered = df_filtered.copy()
else:
    df_filtered = df_filtered[df_filtered["Product Size (kg)"].isin(size)]


# Method dan perulangan untuk filter dengan semua kondisi dari 0-6
def filter_dataframe(df, **filter):
    filtered_df = df.copy()
    for key1, value1 in filter.items():
        if value1:
            for key2, value2 in filter.items():
                if value2 and key1 != key2:
                    for key3, value3 in filter.items():
                        if value3 and key2 != key3 and key1 != key3:
                            for key4, value4 in filter.items():
                                if (
                                    value4
                                    and key3 != key4
                                    and key2 != key4
                                    and key1 != key4
                                ):
                                    for key5, value5 in filter.items():
                                        if (
                                            value5
                                            and key4 != key5
                                            and key3 != key5
                                            and key2 != key5
                                            and key1 != key5
                                        ):
                                            for key6, value6 in filter.items():
                                                if (
                                                    value6
                                                    and key5 != key6
                                                    and key4 != key6
                                                    and key3 != key6
                                                    and key2 != key6
                                                    and key1 != key6
                                                ):
                                                    filtered_df = filtered_df[
                                                        filtered_df[key1].isin(value1)
                                                        & filtered_df[key2].isin(value2)
                                                        & filtered_df[key3].isin(value3)
                                                        & filtered_df[key4].isin(value4)
                                                        & filtered_df[key5].isin(value5)
                                                        & filtered_df[key6].isin(value6)
                                                    ]
    return filtered_df


filtered_df = filter_dataframe(
    df_filtered,
    country=country,
    city=city,
    card=card,
    coffee_type=coffee_type,
    roast_type=roast_type,
    size=size,
)


def Home(filtered_df):
    sum_order_quantity = filtered_df["Order Quantity"].sum()
    count_order = filtered_df["Order ID"].count()
    sum_total_profit = filtered_df["Product Profit"].sum()
    avg_total_profit = filtered_df["Product Profit"].mean()

    # Menampilkan summary
    total1, total2, total3 = st.columns((3))
    with total1:
        st.info(":pencil: Jumlah Kopi Terjual")
        st.metric(label="Total Penjualan", value=f"${sum_order_quantity:.2f}")
    with total2:
        st.info(":pencil: Rata-Rata Keuntungan")
        st.metric(label="Keuntungan", value=f"${avg_total_profit:.2f}")
    with total3:
        st.info(":pencil: Total Pendapatan")
        st.metric(label="Pendapatan Bersih", value=f"${sum_total_profit:.2f}")



# Panggil method yang sudah dibuat dengan DataFrame yang sudah difilter
Home(filtered_df)


# Menentukan besar kolom kontainer
col1, col2 = st.columns((2))
# bar chart jenis sangrai
penjualanJenisSangrai_df = filtered_df.groupby(
    by=["Order Date", "Product Roast Type"], as_index=False
)["Order Quantity"].sum()

# ambil tahun dari order data
penjualanJenisSangrai_df["Year"] = pd.to_datetime(
    penjualanJenisSangrai_df["Order Date"]
).dt.year


# konversi agar sumbu x bisa dipakai menggunakan tahun saja
penjualanJenisSangrai_df["Tahun"] = penjualanJenisSangrai_df["Year"].astype(str)

# dikelompokkan dari tahun dan tipe roasting
penjualanJenisSangrai_df = penjualanJenisSangrai_df.groupby(
    by=["Tahun", "Product Roast Type"], as_index=False
)["Order Quantity"].sum()

# Sorting by tahun saja
penjualanJenisSangrai_df["Tahun"] = pd.to_datetime(penjualanJenisSangrai_df["Tahun"])
penjualanJenisSangrai_df = penjualanJenisSangrai_df.sort_values(by="Tahun")

with col1:
    # Kelompokkan data berdasarkan jenis kopi dan tahun, kemudian jumlahkan keuntungan
    product_profit_year = (
        filtered_df.groupby(["Product Coffee Type", filtered_df["Order Date"].dt.year])["Product Profit"]
        .sum()
        .reset_index()
    )

    # Buat area chart untuk tren keuntungan tiap jenis kopi
    fig = px.area(
        product_profit_year,
        x="Order Date",
        y="Product Profit",
        title="Tren Keuntungan Tiap Jenis Kopi",
        template="seaborn",
        color="Product Coffee Type",
        labels={"Product Profit": "Keuntungan", "Order Date": "Tahun"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
# Chart top 5
# Kelompokkan data berdasarkan nama pelanggan dan jumlahkan jumlah pesanan
    with col2:
        customer_orders = (
        filtered_df.groupby("Customer Name")["Order Quantity"].sum().reset_index()
    )

    # Urutkan pelanggan berdasarkan jumlah pesanan secara menurun
    customer_orders = customer_orders.sort_values(by="Order Quantity", ascending=False)

    # Pilih top 5 pelanggan dengan jumlah pesanan tertinggi
    top_5_customers = customer_orders.head(5)

    # Buat grouped bar chart untuk top 5 pelanggan
    fig = px.bar(
        top_5_customers,
        y="Order Quantity",
        x="Customer Name",
        title="Top 5 Pelanggan dengan Jumlah Pesanan Tertinggi",
        template="seaborn",
        barmode="group",
        text="Order Quantity",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    

with col1:
    # Kelompokkan data berdasarkan jenis kopi dan jumlahkan jumlah pesanan serta total keuntungan
    product_sales_profit = (
        filtered_df.groupby("Product Coffee Type")
        .agg({"Order Quantity": "sum", "Product Profit": "sum"})
        .reset_index()
    )

    # Urutkan berdasarkan total penjualan
    product_sales_profit = product_sales_profit.sort_values(by="Product Profit", ascending=False)

    # Buat bar chart horizontal untuk total penjualan tiap jenis kopi
    fig = px.bar(
        product_sales_profit,
        x="Product Profit",
        y="Product Coffee Type",
        title="Total Penjualan Tiap Jenis Kopi",
        template="seaborn",
        orientation="h",
        labels={"Product Profit": "Total Penjualan", "Product Coffee Type": "Jenis Kopi"},
        category_orders={"Product Coffee Type": product_sales_profit["Product Coffee Type"].tolist()}
    )
    st.plotly_chart(fig, use_container_width=True)

# Bar Chart
# Kelompokkan data berdasarkan "Product Size (kg)" dan "Product Coffee Type"
productSize_df = filtered_df.groupby(
    by=["Product Size (kg)", "Product Coffee Type"], as_index=False
)["Order Quantity"].sum()

# Jumlah Pesanan Berdasarkan Ukuran Produk (Kg) dan jenis kopi
with col2:
    # Kelompokkan data berdasarkan jenis kopi dan tahun, kemudian jumlahkan jumlah pesanan
    product_sales_year = (
        filtered_df.groupby(["Product Coffee Type", filtered_df["Order Date"].dt.year])["Order Quantity"]
        .sum()
        .reset_index()
    )

    # Buat area chart untuk tren penjualan semua jenis kopi
    fig = px.line(
        product_sales_year,
        x="Order Date",
        y="Order Quantity",
        title="Tren Penjualan Semua Jenis Kopi",
        template="seaborn",
        color="Product Coffee Type",
        labels={"Order Quantity": "Jumlah Penjualan", "Order Date": "Tahun"},
    )
    st.plotly_chart(fig, use_container_width=True)

# Map
# Scatter plot geografis
with col1:
    # Membuat scatter plot geografis
    fig = px.scatter_geo(
        filtered_df,
        title="Distribusi Penjualan Kopi di Kota-kota Negara Tertentu",
        locations="Customer Country",  # Ubah lokasi ke negara
        locationmode="country names",
        color="Customer Country",  # Berikan warna berdasarkan negara
        size="Order Quantity",
        hover_name="Customer City",
        projection="natural earth",
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig.update_geos(
        showcountries=True, countrycolor="Black"
    )
    st.plotly_chart(fig, use_container_width=True, width=1000, height=800)


    
# Top 5 kota dengan total penjualan tertinggi
top_5_cities = (
    filtered_df.groupby("Customer City")["Order Quantity"]
    .sum()
    .reset_index()
    .sort_values(by="Order Quantity", ascending=False)
    .head(5)
)

# Bar chart untuk top 5 kota dengan total penjualan tertinggi
with col2:
    fig = px.bar(
        top_5_cities,
        y="Order Quantity",
        x="Customer City",
        title="Top 5 Kota dengan Total Penjualan Tertinggi",
        template="seaborn",
        text="Order Quantity",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(xaxis_title="Kota", yaxis_title="Total Penjualan")
    st.plotly_chart(fig, use_container_width=True)

    

# bar chart Tren Total Pendapatan di Setiap Negara
pendapatanTotal_df = filtered_df.groupby(
    by=["Order Date", "Customer Country"], as_index=False
)["Product Profit"].sum()

# ambil tahun dan bulan dari order data
pendapatanTotal_df["Year"] = pd.to_datetime(pendapatanTotal_df["Order Date"]).dt.year
pendapatanTotal_df["Month"] = pd.to_datetime(pendapatanTotal_df["Order Date"]).dt.month

# gabung tahun dan bulan jadi 1
pendapatanTotal_df["Year_Month"] = (
    pendapatanTotal_df["Year"].astype(str)
    + "-"
    + pendapatanTotal_df["Month"].astype(str)
)

# dikelompokkan dari Year_Month dan Customer Country
pendapatanTotal_df = pendapatanTotal_df.groupby(
    by=["Year_Month", "Customer Country"], as_index=False
)["Product Profit"].sum()

# Sorting by Year dan Month
pendapatanTotal_df["Year_Month"] = pd.to_datetime(pendapatanTotal_df["Year_Month"])
pendapatanTotal_df = pendapatanTotal_df.sort_values(by="Year_Month")

# setting line chart
st.subheader("Tren Pendapatan Setiap Negara")
fig = px.line(
    pendapatanTotal_df,
    x="Year_Month",
    y="Product Profit",
    color="Customer Country",
    template="seaborn",
)
fig.update_traces(mode="lines")
st.plotly_chart(fig, use_container_width=True, height=400)

if st.button("Caritau hasilnya!"):
    # Display results
    col1, = st.columns(1)
    with col1:
        st.subheader("Insigt Yang didapatkan")
        st.warning("Dari visualisasi data yang ditampilkan 📊, terlihat bahwa total keuntungan dari penjualan kopi sangat fluktuatif. Namun, ada beberapa kondisi unik dimana terdapat jenis kopi dengan tingkat penjualan tinggi namun dengan harga yang terjangkau, sehingga keuntungan yang dihasilkan masih belum seimbang ⚖️.Tahun 2021 menunjukkan bahwa kopi jenis Robusta sangat menguntungkan 💵, namun Arabika tetap diminati oleh banyak orang karena kualitasnya yang tinggi ☕️. Meskipun begitu, total pendapatan dari semua jenis kopi sangat menguntungkan 💰. Distribusi penjualan yang bervariasi di tiap negara juga mempengaruhi daya konsumsi masyarakat 🌍. Berdasarkan analisis data, rata-rata pembeli dengan daya konsumsi tinggi banyak ditemui di negara Amerika Serikat 🇺🇸. Banyak dari kota dengan penjualan tertinggi juga terdapat di wilayah Amerika Serikat. Oleh karena itu, tren total pendapatan dari tiap negara sangat didominasi oleh Amerika Serikat.")

        st.markdown("[🌏Bantu Untuk Keberlanjutan bumi yang lebih baik ](https://forms.gle/kgEKZiqXYUNyx8Wx8)")



