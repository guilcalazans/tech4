import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title = 'TC 4',
    layout = 'wide'
)

st.header("**Painel de Preço de Fechamento de ações do Brent**")

ticker = yf.Ticker('BZ=F')

tickerDF = ticker.history(period = "1d",
                           start = "2019-01-01",
                           end ="2025-01-20")
col1, col2 = st.columns([1,1])

with col1:
    st.write(f"**Empresa:** {ticker.info['shortName']}")

with col2:
    st.write(f"**Preço Atual: $** {ticker.info['previousClose']}")

st.line_chart(tickerDF.Close)
