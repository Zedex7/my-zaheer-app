
import requests
import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse

st.title("🎈 My new app")

resultSize = st.number_input(label="Set Results per Search", value=10, min_value=10, max_value=50)

uploaded_file = st.file_uploader("Choose a file", type='csv')

if uploaded_file is not None:
    
    dataframe = pd.read_csv(uploaded_file)
    table = []

    for input in dataframe.index:
        search_word = dataframe.iat[input,0]
        brand_word = dataframe.iat[input,1]
        is_brand_name_empty = type(brand_word) is not str or brand_word.strip() == ""

        data = requests.get("https://digital.dmart.in/api/v2/search/" + urllib.parse.quote_plus(search_word) + "?page=1&size=" + str(resultSize) + "&channel=web&storeId=10689").json()

        for item in data["products"]:
            for variant in item["sKUs"]:
                if (is_brand_name_empty or brand_word in variant["name"]):
                    direct_url = "https://www.dmart.in/product/" + item["seo_token_ntk"] + "?selectedProd=" + variant["skuUniqueID"]
                    table.append({
                        "Search": search_word,
                        "By Brand": not is_brand_name_empty,
                        'Name': variant["name"],
                        'MRP': variant["priceMRP"],
                        'Selling': variant["priceSALE"],
                        "Discount %": variant["savingPercentage"],
                        'Variant': variant["variantText"],
                        'Variant Value': variant["variantTextValue"],
                        "Link": direct_url
                    })

    df = pd.DataFrame(table)
    st.dataframe(df)
