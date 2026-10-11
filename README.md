Wealth Growth Simulator 

A compound interest calculator that grew into a full finance too, build with python 

Features: 
- Compound intereest with fees, tax (or ISA) and inflation 
- compare two interest rates side by side
- Goal Mode: how long until you reach a target amount
- Monte Carlo simulation of best, median and worst outcomes 
- Index fund growth ying real S&P 500 and NASDAQ 100 history (via yfinance) 
- Year-by-year table with CSV download

Ruit in locally 
```bash 
pip install -r requirements.txt
python3 -m streamlit run app.pu
``` 

Run the tests
```bash 
pytest
``` 

Notes: 
- Index data uses price indexes only, so dividents aren't included
- Index Values are in USD, and the rest of the app uses £ 
- This is a learning project, not financial advice 

Built with: 
Python, Streamlit, Pandas, Plotly, yfinance 
