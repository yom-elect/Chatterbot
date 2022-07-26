import streamlit as st
from PIL import Image
import pandas as pd
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns

from utils.index import crypto_symbols, load_coin_prediction, coins_relationship

st.set_page_config(layout="wide")

image = Image.open('logo.png')

st.image(image, width = 700)

st.title('SOLiGence App')
st.markdown("""
This is a leading financial multinational organisation that deals with 
stock and shares, saving and  **investments**!

""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, requests, json, time
* **Data source:** [YahooFinance](https://finance.yahoo.com/cryptocurrencies/).
""")

col1 = st.sidebar
col2, col3 = st.columns((2,1))

col1.header('Users Input Options')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

selected_coin = col1.selectbox('Select Coin to Predict', tuple(crypto_symbols))

prediction_range = st.sidebar.slider('Number of Days', 1, 7)

col2.subheader(f'Price Prediction for {selected_coin}')
df, model_accuracy, pred_val, test_val = load_coin_prediction(selected_coin, currency_price_unit, prediction_range)
col2.dataframe(pd.DataFrame(df))

col3.subheader(f'Model Accuracy')
col3.write(model_accuracy)

plt.plot(figsize = (15,8) , fontsize = 13)
plt.plot(test_val, label='Original')
plt.plot(pred_val, label='Predicted')
plt.legend()
col3.pyplot(plt)

col3.subheader(f'R Squared Value')
R_squared = r2_score(test_val, pred_val)
col3.write(R_squared)


selected_coin = col1.multiselect('Coin Performance Relationship', crypto_symbols, crypto_symbols[:3])
CryptoClose, ret, norm = coins_relationship(selected_coin)

if st.button('Intercorrelation Close Prices'):
    CryptoClose.plot(figsize = (15,8) , fontsize = 13)
    plt.legend(fontsize = 15)
    col2.pyplot(plt)

if st.button('Coins Performamce'):
    norm.plot(figsize=(15,8), fontsize=13)
    plt.legend(fontsize=13)
    col2.pyplot(plt)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.5)
    sns.heatmap(ret.corr(), cmap = "Reds", annot = True, annot_kws={"size":15}, vmax=1)
    col2.pyplot(plt)

if st.button('Return Visualization'):
    ret.plot(kind="hist", f
    igsize = (12,8), bins=100)
    plt.legend(fontsize=13)
    col2.pyplot(plt)