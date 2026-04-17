pip install streamlit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
st.set_page_config(page_title = "Stock Data Extraction", layout="wide")

st.title ("Stock Indicator app")

st.write("Extract stock market prices from yahoo finance using ticker")

st.sidebar.header("User input")

ticker = st.sidebar.text_input("Enter Ticker", "AAPL")

start_date = st.sidebar.date_input("start date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if st.sidebar.button("Get Data"):

  # create ticker object
  stock = yf.Ticker(ticker)

  #  download historical prices
  df = stock.history(start = start_date, end = end_date)

  # check the data
  if df.empty:
    st.error("No Data Found. Please check the ticker symbol or date range")
  else:
    st.success(f"Data Successfully extracted for {ticker}")

    # display company info
    st.subheader("Company Information")
    info = stock.info


    company_name = info.get("longName", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    market_cap = info.get("marketCap", "N/A")
    website = info.get("website", "N/A")


    st.write(f"**Company Name:** {company_name}")
    st.write(f"**Sector:** {sector}")
    st.write(f"**Industry:** {industry}")
    st.write(f"**Market Cap:** {market_cap:,}")
    st.write(f"**Website:** {website}")


    st.subheader("Historical data")
    st.dataframe(df)

    st.subheader("Closing price chart")
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Close'])
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    st.pyplot(fig)

    st.subheader("Moving Averages and Trend Analysis")

    # Calculate moving averages
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    # Plot moving averages
    fig_ma, ax_ma = plt.subplots(figsize=(12, 6))
    ax_ma.plot(df["Close"], label="Price")
    ax_ma.plot(df["MA20"], label="MA20")
    ax_ma.plot(df["MA50"], label="MA50")
    ax_ma.plot(df["MA200"], label="MA200")
    ax_ma.set_title("Moving Averages Vs Price")
    ax_ma.set_xlabel("Date")
    ax_ma.set_ylabel("Price")
    ax_ma.legend()
    st.pyplot(fig_ma)

    # Trend analysis
    close_prices = df["Close"]
    if len(close_prices) >= 200: # Ensure enough data for all MAs
        current_price = close_prices.iloc[-1]
        ma_20 = df["MA20"].iloc[-1]
        ma_50 = df["MA50"].iloc[-1]
        ma_200 = df["MA200"].iloc[-1]

        st.write(f"**Current Price:** {current_price:.2f}")
        st.write(f"**20-Day Moving Average (MA20):** {ma_20:.2f}")
        st.write(f"**50-Day Moving Average (MA50):** {ma_50:.2f}")
        st.write(f"**200-Day Moving Average (MA200):** {ma_200:.2f}")

        if current_price > ma_20 and current_price > ma_50 and current_price > ma_200:
            st.success("**Trend:** Upward trend")
        elif current_price < ma_20 and current_price < ma_50 and current_price < ma_200:
            st.error("**Trend:** Downward trend")
        else:
            st.info("**Trend:** Mixed trend")
    else:
        st.warning("Not enough data to calculate 200-day moving average and determine a clear trend. Need at least 200 data points.")

    csv = df.to_csv().encode("utf-8")


    st.download_button(
      label = "Download Data as CSV",
      data = csv,
      file_name = f"{ticker}_stock_data.csv",
      mime = "text/csv"
    )

ticker = "XOM"
data = yf.download(ticker, period="5y", auto_adjust= False)

data["MA20"] = data["Close"].rolling(20).mean()
data["MA50"] = data["Close"].rolling(50).mean()
data["MA200"] = data["Close"].rolling(200).mean()

plt.figure(figsize=(12,6))
plt.plot(data["Close"], label = "price")
plt.plot(data["MA20"], label = "MA20")
plt.plot(data["MA50"], label = "MA50")
plt.plot(data["MA200"], label = "MA200")

plt.legend
plt.show
plt.title("Moving averages Vs Price")

close = data["Close"].squeeze()

current_price = close.iloc[-1]
print(f"Current price : {current_price:.2f}")

ma_20 = close.iloc[-20:].mean()
ma_50 = close.iloc[-50:].mean()
ma_200 = close.iloc[-200:].mean()

if current_price > ma_20 and current_price > ma_50 and current_price > ma_200:
  print("Upward trend ")
elif current_price < ma_20 and current_price < ma_50 and current_price < ma_200:
    print("down trend")
else:
  print("mixed trend")
