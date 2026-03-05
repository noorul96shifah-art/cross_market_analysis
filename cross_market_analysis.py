import streamlit as st

st.title(" 📊 Cross-Market Analysis: Crypto, Oil & Stocks with SQL")

import pandas as pd
from sqlalchemy import create_engine

st.subheader("Cross-Market Analysis Dashboard")

st.write("Data Preview")

# Database connection
engine = create_engine(
    "mysql+pymysql://3jcisCTAgR1WuCJ.root:I9bxsJvxbNG9ln6d@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/coin_db",
    connect_args={"ssl": {"ssl": True}}
)

st.set_page_config(page_title="Market Analysis", layout="wide")

page = st.sidebar.radio(
    "Navigation",
    [
        "Data Exploration",
        "Query Analysis",
        "Insights"
    ]
)   

if page == " 🔎 Data Exploration":

    st.title("Data Exploration")

    st.write("Select Date Range")

    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")

    if st.button("Bitcoin Average Price Analysis"):
        btc_avg = pd.read_sql(
         """   
            SELECT AVG(current_price) AS bitcoin_avg_price
            FROM Cryptocurrency 
            WHERE id= %s
            AND DATE(last_updated) BETWEEN %s AND %s
         """,
         engine, 
         params=('bitcoin',start_date,end_date)
        )
        st.write(btc_avg)
    if st.button("Oil Average Price Analysis"):
        oil_avg = pd.read_sql(
           """
             SELECT AVG(price) AS avg_oil_price
             FROM Oil_price
             WHERE DATE(date) BETWEEN %s AND %s
           """,
           engine,
           params=(start_date, end_date)
        )
        st.write(oil_avg)    
  
    if st.button("^GSPC Average Price Analysis"):
        sp500_avg = pd.read_sql(
          """
            SELECT AVG(close) AS avg_sp500_price
            FROM Stocks
            WHERE ticker = '^GSPC'
            AND DATE(date) BETWEEN %s AND %s
          """,  
          engine,
          params=(start_date,end_date) 
          
         )   
        s.write(sp500_avg)

    if st.button("^NSEI Average Price Analysis"):
        nifty_avg=pd.read_sql(
          """
            SELECT AVG(close) AS avg_nifty_price
            FROM StocKs
            WHERE ticker = '^NSEI'
            AND DATE(date) BETWEEN %s AND %s
          """,
          engine,
          params=(start_date,end_date) 
         ) 
        st.write(nifty_avg)  
    snapshot_df = pd.read_sql(   
        """
            SELECT
            DATE (c.date) AS date,
            c.price AS bitcoin_price,
            o.price AS oil_price,
            sp.close AS sp500_close,
            ni.close AS nifty_close
            FROM  Crypto_prices c
            LEFT JOIN Oil_price o
            ON c.date = o.date
            LEFT JOIN Stocks sp
            ON c.date = sp.date
            AND sp.ticker = '^GSPC'
            LEFT JOIN Stocks ni
            ON c.date = ni.date
            AND ni.ticker = '^NSEI'
            WHERE c.coin_id = 'bitcoin'
            ORDER BY c.date
         """,
         engine
        )    
    st.subheader("Daily market snapshot table")
    st.dataframe(snapshot_df)  


elif page == "Query Analysis":
    st.title(" 💻 Query Analysis")
    st.write("Select a predefined SQL query and click **Run Query**")
    query_option = st.selectbox(
        "Choose a query",
         (
            "Find the top 3 cryptocurrencies by market cap",
            "Get coins that are within 10 percent of their all-time-high (ATH).",
            "Find the highest daily price of Bitcoin in the last 365 days.",
            "Show oil prices during COVID crash (March-April 2020).",
            "List all coins where circulating supply exceeds 90 percent of total supply.",
            "Find the average market cap rank of coins with volume above $1B.",
            "Get the most recently updated coin.",
            "Calculate the average daily price of Ethereum in the past 1 year.",
            "Show the daily price trend of Bitcoin in Feb 2026.",
            "Find the coin with the highest average price over 1 year.",
            "Get the percentage change in Bitcoin price during Feb 2026",
            "Find the highest oil price in the last 5 years.",
            "Get the average oil price per year.",
            "Find the lowest price of oil in the last 10 years.",
            "Calculate the volatility of oil prices (max-min difference per year).",
            "Get all stock prices for ^IXIC ticker",
            "Find the highest closing price for NASDAQ (^IXIC)",
            "List top 5 days with highest price difference for S&P 500 (^GSPC)",
            "Get monthly average closing price for each ticker",
            "Get average trading volume of NSEI in 2024",
            "Check if Bitcoin moves with ^GSPC.",
            "Find days when oil price spiked and compare with Bitcoin price change during Feb 2026",
            "Compare stock prices (^GSPC) with crude oil prices on the same dates",
            "Correlate Bitcoin closing price with crude oil closing price (same date)",
            "Compare NASDAQ (^IXIC) with Ethereum price trends",
            "Join top 3 crypto coins with stock indices for 2025",
            "Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison",
            "Compare top 3 coins daily price trend vs Nifty (^NSEI)."
        )
    )         
    if st.button("Run Query"):

        if query_option == "Find the top 3 cryptocurrencies by market cap": 
             sql="SELECT * FROM Cryptocurrency ORDER BY market_cap DESC LIMIT 3"

        elif query_option== "Get coins that are within 10 percent of their all-time-high (ATH)":    
             sql=""" 
             SELECT id,symbol,name,circulating_supply,total_supply 
             FROM Cryptocurrency 
             WHERE circulating_supply>0.9 * total_supply
             """
     
        elif query_option=="Find the highest daily price of Bitcoin in the last 365 days":
             sql="""
               SELECT MAX(price) AS highest_price 
               FROM Crypto_prices 
               WHERE coin_id='bitcoin'
               AND date >= CURDATE()-INTERVAL 365 DAY
             """ 

        elif query_option== " List all coins where circulating supply exceeds 90% of total supply":
             sql="""
              SELECT AVG(market_cap_rank) AS avg_market_cap_rank
              FROM Cryptocurrency 
              WHERE total_volume > 1000000000
             """


        elif query_option== " Get the most recently updated coin":
             sql="""
              SELECT id,name,last_updated
              FROM Cryptocurrency
              ORDER BY last_updated DESC LIMIT 1
             """ 

        elif query_option== "Find the average market cap rank of coins with volume above $1B":
             sql="""
              SELECT AVG(market_cap_rank) AS avg_market_cap_rank
              FROM Cryptocurrency 
              WHERE total_volume > 1000000000
             """


        elif query_option== "Calculate the average daily price of Ethereum in the past 1 year":
             sql="""
              SELECT AVG(price) AS avg_eth_price
              FROM Crypto_prices 
              WHERE coin_id='ethereum'
              AND date>=CURDATE()-INTERVAL 1 YEAR   
             """

        elif query_option== "Show the daily price trend of Bitcoin in January 2025":
             sql="""
              SELECT date, price 
              FROM Crypto_prices
              WHERE coin_id='bitcoin'
              AND date BETWEEN '2025-01-01' AND '2025=01=31' 
              ORDER BY date
            """

        elif query_option== " Find the coin with the highest average price over 1 year":
             sql="""
               SELECT coin_id , MAX (price) AS  highest_price
               FROM Crypto_prices
               GROUP BY coin_id
             """

        elif query_option== "Get the % change in Bitcoin price between Sep 2024 and Sep 2025":
             sql="""
               SELECT cp.coin_id,cp.date,cp.price
               FROM Crypto_prices AS cp
               WHERE cp.date=(
               SELECT MAX(date)
               FROM Crypto_prices
               WHERE coin_id=cp.coin_id)
             """

        elif query_option==  "Find the highest oil price in the last 5 years":
             sql="SELECT MAX(price)AS highest_oil_price FROM Oil_price"

        elif query_option== "Get the average oil price per year":
             sql="SELECT AVG(price) AS avg_oil_price FROM Oil_price"

        elif query_option== "Show oil prices during COVID crash (March–April 2020)":
             sql="""
              SELECT * FROM Oil_price
              WHERE date BETWEEN '2020-03-01' AND '2020-04-30'
              ORDER BY date
             """

        elif query_option==  " Find the lowest price of oil in the last 10 years":
             sql="""
               SELECT MIN(price) AS lowest_oil_price_last_10_years
               FROM Oil_price 
               WHERE date >=DATE_SUB(CURDATE(),INTERVAL 10 YEAR)
             """

        elif query_option== "Calculate the volatility of oil prices (max-min difference per year)":
             sql="""
               SELECT YEAR(date) AS year,
               MAX(price)-MIN(price) AS yearly_voltility
               FROM Oil_price
               GROUP BY YEAR(date)
               ORDER BY year
             """

        elif query_option== " Get all stock prices for a given ticker":
             sql="SELECT * FROM Stocks WHERE ticker='^IXIC'"

        elif query_option== " Find the highest closing price for NASDAQ (^IXIC)":
             sql="SELECT MAX(close) AS highest_close FROM Stocks WHERE ticker='^IXIC'"

        elif query_option== " List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)":
             sql="""
              SELECT date, (high-low) AS price_difference
              FROM Stocks WHERE ticker='^GSPC'
              ORDER BY price_difference DESC LIMIT 5 
             """

        elif query_option== "Get monthly average closing price for each ticker":
             sql="""
              SELECT ticker, YEAR(date) AS year,
              MONTH(date) AS month,
              AVG(close) AS avg_close
              FROM Stocks
              GROUP BY ticker,YEAR(date),MONTH(date)
              ORDER BY year,month
             """

        elif query_option== "Get average trading volume of NSEI in 2024":
             sql="""
              SELECT AVG(volume) AS avg_volume_2024 
              FROM Stocks WHERE ticker='^NSEI'
              AND YEAR(date)=2024
             """

        elif query_option== "Compare Bitcoin vs Oil average price in 2025":
             sql="""
              SELECT  AVG(c.price) AS bitcoin_avg_price, AVG(o.price) AS oil_avg_price,c.date
              FROM Crypto_prices c
              JOIN Oil_price o
              ON o.date=c.date
              WHERE YEAR(c.date)=2025
              AND c.coin_id='bitcoin'
              GROUP BY c.date 
              ORDER BY c.date
             """

        elif query_option== "Check if Bitcoin moves with S&P 500 (correlation idea)":
             sql="""
               SELECT s.date,s.close AS SP500_close_price, c.price AS bitcoin_price
               FROM Stocks s JOIN Crypto_prices c 
               ON s.date=c.date
               WHERE s.ticker='^GSPC'
               AND c.coin_id='bitcoin'
             """

        elif query_option== " Compare Ethereum and NASDAQ daily prices for 2025":
             sql="""
                SELECT c.date,c.Price AS ethereum_price,
                s.close AS nasdaq_price
                FROM Crypto_prices c 
                JOIN Stocks s 
                ON c.date=s.date
                WHERE c.coin_id='ethereum'
                AND s.ticker='^IXIC'
                AND YEAR(c.date)=2025
             """

        elif query_option== "Find days when oil price spiked and compare with Bitcoin price change":
             sql="""
                SELECT o1.date, o1.price AS oil_price,(o1.price-o2.price) AS oil_change, c.price AS bitcoin_price
                FROM Oil_price o1
                JOIN Oil_price o2
                ON o1.date=DATE_ADD(o2.date, INTERVAL 1 DAY)
                JOIN Crypto_prices c 
                ON c.date=o1.date
                WHERE YEAR(o1.date)=2025
                AND c.coin_id='bitcoin'
                AND (o1.date-o2.date)>0
                ORDER BY o1.date
             """

        elif query_option== "Compare top 3 coins daily price trend vs Nifty (^NSEI)":
             sql="""
               SELECT c.date,c.coin_id ,c.price,s.close AS nifty_price
               FROM Crypto_prices c
               JOIN Stocks s
               ON s.date=c .date
               WHERE c.coin_id IN(SELECT id
               FROM Cryptocurrency ORDER BY market_cap DESC LIMIT 3)
               AND s.ticker='^NSEI'
               ORDER BY  c.date,c.coin_id;
             """


        elif query_option== "Compare stock prices (^GSPC) with crude oil prices on the same dates" :
             sql="""
               SELECT s.date,s.close AS sp500_price,o.price AS oil_price,o.date
               FROM Stocks s 
               JOIN Oil_price o
               ON o.date=s.date
               WHERE s.ticker='"^GSPC'
               ORDER BY s.date
             """
     
        elif query_option== " Correlate Bitcoin closing price with crude oil closing price (same date)":
             sql="""
               SELECT  AVG(c.price) AS bitcoin_avg_price, AVG(o.price) AS oil_avg_price,c.date
               FROM Crypto_prices c
               JOIN Oil_price o
               ON o.date=c.date
               WHERE YEAR(c.date)=2025
               AND c.coin_id='bitcoin'
               GROUP BY c.date 
               ORDER BY c.date
             """                             
                         
        elif query_option== "Compare NASDAQ (^IXIC) with Ethereum price trends":
             sql="""
             SELECT c.date,c.Price AS ethereum_price,
             s.close AS nasdaq_price
             FROM Crypto_prices c 
             JOIN Stocks s 
             ON c.date=s.date
             WHERE c.coin_id='ethereum'
             AND s.ticker='^IXIC'
             AND YEAR(c.date)=2025
            """ 


        elif query_option== "Join top 3 crypto coins with stock indices for 2025":
             sql="""
              SELECT c.date,c.coin_id,c.price AS crypto_price,s.ticker,s.close AS stock_close
              FROM Crypto_prices c
              JOIN Stocks s 
              ON c.date=s.date
              WHERE coin_id IN ('bitcoin','ethereum','tether')
              AND s.ticker IN ('^GSPC','^IXIC','^NSEI')
              ORDER BY c.date
             """
        elif query_option== "Multi-join: stock prices, oil prices, and Bitcoin prices for daily comparison":
             sql="""
               SELECT
               DATE (c.date) AS date,
               c.price AS bitcoin_price,
               o.price AS oil_price,
               sp.close AS sp500_close,
               ni.close AS nifty_close
               FROM  Crypto_prices c
               LEFT JOIN Oil_price o
               ON c.date = o.date
               LEFT JOIN Stocks sp
               ON c.date = sp.date
               AND sp.ticker = '^GSPC'
               LEFT JOIN Stocks ni
               ON c.date = ni.date
               AND ni.ticker = '^NSEI'
               WHERE c.coin_id = 'bitcoin'
               ORDER BY c.date
             """

        df = pd.read_sql(sql, engine)

        st.subheader("Query Result")
        st.dataframe(df)

elif page == "Insights":
    st.title(" 🚀 Insights on Top 3 Cryptocurrencies")
    st.write("Select a coin and date range to view price trends")

    coin = st.selectbox(
        "Select Coin",
        ("bitcoin", "ethereum", "tether")
    )

    start_date = st.date_input("Start date", key="p3_start")
    end_date = st.date_input("End date", key="p3_end")

    if st.button("View Price Trend"):
        df = pd.read_sql(
            """
              SELECT
              date, price
              FROM Crypto_prices
              WHERE coin_id = %s
              AND DATE(date) BETWEEN %s AND %s
              ORDER BY date
             """,
             engine,
             params=(coin, start_date, end_date)
        )

        if df.empty:
            st.warning("No data available for the selected coin and date range.")

        else:

            # --- Table ---
            st.subheader("Daily Price Table")
            st.dataframe(df)    


 
     