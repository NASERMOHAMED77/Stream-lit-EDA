import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui

st.title("Mahlii Data Visualization")
st.subheader("Take a look on data sample")
data=pd.read_csv("sales.csv")  
data["OrderDate"]=pd.to_datetime(data["OrderDate"])

quarters=data["OrderDate"].dt.quarter
years=data["OrderDate"].dt.year
data["month"]=data["OrderDate"].dt.month
selected_Status=st.sidebar.multiselect("Status",data.Status.unique())
selected_Year=st.sidebar.multiselect("Year",years.unique())
selected_querter=st.sidebar.multiselect("quarter",list(quarters.unique()))
selected_territory=st.sidebar.multiselect("TerritoryGroup",data["TerritoryGroup"].unique())
selected_category=st.sidebar.multiselect("Category",data.ProductCategory.unique())

filterd_data_status=data[data.Status.isin(selected_Status)]
filterd_data=filterd_data_status[filterd_data_status.TerritoryGroup.isin(selected_territory)]
filterd_data=filterd_data[(filterd_data.OrderDate.dt.year.isin(selected_Year))&(filterd_data.OrderDate.dt.quarter.isin(selected_querter))]
st.dataframe(filterd_data)

sales_category=filterd_data.groupby("ProductCategory",)["TotalDue"].sum().reset_index()
# sales_pay_methods=filterd_data.groupby("Payment_Method",)["Price (Rs.)"].sum().reset_index()
total_items=filterd_data["OrderDetailID"].nunique()
total_orders=len(filterd_data["OrderID"].drop_duplicates())
total_costumers=len(filterd_data["CustomerID"].drop_duplicates())
total_sales=filterd_data["TotalDue"].sum()
total_Tax=filterd_data["TaxAmt"].sum()
total_shipping=filterd_data["Freight"].sum()

cols=st.columns(3)


with cols[0]:

   ui.metric_card( title="Total User"
   , content=str(total_costumers),
   description="Users ordered in this Quarter "
   )
with cols[1]:

   ui.metric_card( title="Total orders"
   , content=str(total_orders),
      description="Orders in this Quarter "

   )
with cols[2]:

   ui.metric_card( title="Total Sales"
   , content=str(round((int(total_sales)/1000000),3))+"M  EG",
   description="Total Sales in this Quarter"

   )

cols=st.columns(3)


with cols[0]:

   ui.metric_card( title="Total otems"
   , content=str(total_items),
   description=" items ordered in this Quarter "
   )
with cols[1]:

   ui.metric_card( title="Total Taxs"
   , content=str(round((int(total_Tax)/1000),3))+"k  EG",
      description="Taxs in this Quarter "

   )
with cols[2]:

   ui.metric_card( title="Total Shipping"
   , content=str(round((int(total_shipping)/1000),3))+"k  EG",
   description="Total Shipping in this Quarter"

   )


st.subheader("Total Revenue Amount of Each Product Sub Category ")
st.bar_chart(filterd_data.set_index('ProductSubCategory')[["TotalDue","UnitPrice"]],stack=False)

st.subheader("Total Revenue Amount For Each Territory ")
st.scatter_chart(filterd_data.set_index('TotalDue')[["Territory"]],)
st.subheader("Total Revenue Amount For Each Territory ")
st.scatter_chart(filterd_data.set_index('TotalDue')[["TerritoryGroup"]],use_container_width=True)

df=filterd_data.groupby(["month"])[["TotalDue","LineTotal","UnitPrice"]].sum().reset_index()

df
st.subheader("Unit price / Total Price / Price after Taxs")

st.line_chart(df)
df2=filterd_data.groupby(["Territory"])[["CustomerID","OrderID"]].nunique().reset_index()
df2
st.subheader("Customers And Orders For Each Territory")
st.line_chart(df2.set_index('Territory'))
