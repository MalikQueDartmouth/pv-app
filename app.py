import requests
import streamlit as st
import streamlit.components.v1 as components

sec_headers = {'User-Agent': 'malik@verdantcapitaladvisors.com'}


@st.cache_data
def get_cik_ticker_lists():
    companyTickers = requests.get(
        "https://www.sec.gov/files/company_tickers.json", headers=sec_headers
        )
    return companyTickers.json()

def get_trader_view_string(ticker, name, exch):
    return_str3 = f"""
    <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-overview.js" async>
      {{
      "symbols": [
        [
          "{name}",
          "{ticker}|1D"
        ]
      ],
      "chartOnly": false,
      "width": "100%",
      "height": 500,
      "locale": "en",
      "colorTheme": "light",
      "autosize": false,
      "showVolume": false,
      "showMA": false,
      "hideDateRanges": false,
      "hideMarketStatus": false,
      "hideSymbolLogo": false,
      "scalePosition": "right",
      "scaleMode": "Normal",
      "fontFamily": "-apple-system, BlinkMacSystemFont, Trebuchet MS, Roboto, Ubuntu, sans-serif",
      "fontSize": "10",
      "noTimeScale": false,
      "valuesTracking": "1",
      "changeMode": "price-and-percent",
      "chartType": "area",
      "maLineColor": "#2962FF",
      "maLineWidth": 1,
      "maLength": 9,
      "lineWidth": 2,
      "lineType": 0,
      "dateRanges": [
        "1d|1",
        "1m|30",
        "3m|60",
        "12m|1D",
        "60m|1W",
        "all|1M"
      ],
      "timeHoursFormat": "12-hours"
    }}
      </script>
    </div>
    <!-- TradingView Widget END -->
    """
    return return_str3 

def main():
    
    st.set_page_config(layout="wide")

    tickers_list = []
    cik_list = []
    tickers_list = []
    name_list = []
    cik_ticker_data = get_cik_ticker_lists()

    cik_ticker_pairs = {}
    name_ticker_pairs = {}
    for i in range(len(cik_ticker_data)):
        cik_list.append(cik_ticker_data[str(i)]['cik_str']) 
        tickers_list.append(cik_ticker_data[str(i)]['ticker']) 
        name_list.append(cik_ticker_data[str(i)]['title']) 
        cik_ticker_pairs[cik_ticker_data[str(i)]['ticker']] = str(cik_ticker_data[str(i)]['cik_str']).zfill(10)
        name_ticker_pairs[cik_ticker_data[str(i)]['ticker']] = str(cik_ticker_data[str(i)]['title']).upper()

    selected_ticker = st.sidebar.selectbox(label="Select Ticker", options=tickers_list)

    # get latest stock quote
    url = f"{API_BASE_URL}markets/quotes"
    headers = {'Authorization': f"Bearer {TRADIER_ACCESS_TOKEN}",
               'Accept': 'application/json'
               }
    response = requests.post(url,
                              data={'symbols': selected_ticker},
                              headers=headers
                              )

    json_response = response.json()
    data = json_response["quotes"]["quote"]
    
    if data["exch"]=="Q":
        exchange="NASDAQ"
    elif data["exch"]=="N":
        exchange="NYSE"

    chart_str = get_trader_view_string(selected_ticker, name_ticker_pairs[selected_ticker], exchange)

    components.html(chart_str, height=500)

if __name__ == "__main__":
    main()
