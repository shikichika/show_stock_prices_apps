import pandas as pd
import altair as alt
import yfinance as yf
import streamlit as st

st.title('Stock prices Apps')



st.sidebar.write(
"""
# Stock prices of Gafa + MN
This apps show stock prices of GAFA + MN
Please select days from below options  

"""
)

st.sidebar.write("""
## Select Days
""")

days = st.sidebar.slider('days', 1, 50, 20)

st.write(f"""
### Stock prices of GAFA + MN in past **{days}days**
""")

@st.cache
def get_data(days, tickers):

    df = pd.DataFrame()

    for company in tickers.keys():

        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


try:
    st.sidebar.write("""
    ## Range of stock pricess
    """)
    ymin, ymax = st.sidebar.slider(
        'Select range',
        0.0, 3500.00, (0.0, 3500.00)
        
    )

    tickers = {
        'apple' : 'AAPL',
        'facebook' : 'FB',
        'google' : 'GOOGL',
        'microsoft' : 'MSFT',
        'netflix' : 'NFLX',
        'amazon' : 'AMZN'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        'Select companies name',
        list(df.index),
        list(df.index)
    )

    if not companies:
        st.error('Please select at least one company')
    else:
        data = df.loc[companies]
        st.write('### Stock Price (USD)', data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars = ['Date']).rename(

            columns = {'value' : 'Stock prices (USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x = "Date:T",
                y = alt.Y('Stock prices (USD):Q', stack = None, scale = alt.Scale(domain = [ymin, ymax])),
                color = 'Name:N'
            )
        )

        st.altair_chart(chart, use_container_width=True)
except:
    st.error("Opps, somethings went wrong!")