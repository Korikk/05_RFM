import pandas as pd
import datetime as dt

pd.set_option("display.max_columns", None)

df_ = pd.read_excel("datafiles\online_retail.xlsx")
df = df_.copy()
df.head()

df.info()
df.isnull().sum()

df["Description"].nunique()

df["Description"].value_counts()

df.groupby("Description").agg({"Quantity": "sum"}).head()

df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity", ascending=False).head()

df["InvoiceNo"].nunique()

df.dropna(inplace=True)

df = df[~df["InvoiceNo"].str.contains("C", na=False)]

df["TotalPrice"] = df["UnitPrice"] * df["Quantity"]

df.sort_values("UnitPrice", ascending=False).head()

df.groupby("Country").agg({"TotalPrice": "sum"}).sort_values("TotalPrice", ascending=False).head()

df.describe([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]).T

df["InvoiceDate"].max()
today_date = dt.datetime(2011, 12, 11)
rfm = df.groupby("CustomerID").agg({"InvoiceDate": lambda date: (today_date - date.max()).days,
                                    "InvoiceNo": lambda num: len(num),
                                    "TotalPrice": lambda TotalPrice: TotalPrice.sum()})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

rfm = rfm[(rfm["Monetary"]) > 0 & (rfm["Frequency"] > 0)]

rfm["RecencyScore"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])

rfm["FrequencyScore"] = pd.qcut(rfm['Frequency'], 5, labels=[1, 2, 3, 4, 5])

rfm["MonetaryScore"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm["RecencyScore"].astype(str) +
                    rfm["FrequencyScore"].astype(str) +
                    rfm["MonetaryScore"].astype(str))

rfm[rfm["RFM_SCORE"] == "555"].head()

seg_map = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At_Risk',
    r'[1-2]5': 'Cant_Loose',
    r'3[1-2]': 'About_to_Sleep',
    r'33': 'Need_Attention',
    r'[3-4][4-5]': 'Loyal_Customers',
    r'41': 'Promising',
    r'51': 'New_Customers',
    r'[4-5][2-3]': 'Potential_Loyalists',
    r'5[4-5]': 'Champions'
}

rfm['Segment'] = rfm['RecencyScore'].astype(str) + rfm['FrequencyScore'].astype(str)
rfm['Segment'] = rfm['Segment'].replace(seg_map, regex=True)
rfm[rfm["Segment"] == "Loyal_Customers"].head()
new_df = pd.DataFrame()
new_df["Loyal_Customers"] = rfm[rfm["Segment"] == "Loyal_Customers"].index
new_df.to_csv("Loyal_customer.csv")
