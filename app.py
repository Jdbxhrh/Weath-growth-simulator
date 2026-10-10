import streamlit as st
import pandas as pd 
import random  
import plotly.graph_objects as go 
from finance import compound_interest 
st.set_page_config(page_title="Wealth Growth Simulator", layout="wide") 
st.title("Wealth Growth Simulator") 
st.caption("See how your money could grow with compound interest, fees, tax and inflation")

def monte_carlo(start, monthly, rate, years, volatility, runs):
    results = []
    for i in range(runs):
        balance = start
        yearly = []
        for year in range(years):
            r = random.gauss(rate, volatility) / 100
            for month in range(12):
                balance = balance * (1 + r / 12) + monthly
            yearly.append(balance)
        results.append(yearly)
    return results 

def money_chart(df, x_title="Month", stacked=false)" 
    fig = go.Figure() 
    for col in df.columns: 
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col, stackgroup="one" if stacked else None, hovertemplate="%{fullData.name}: £%{y:,.0f}<extra></extra?")) 
    ymax = df.sum(axis=1).max() if stacked else df.max().max() 
    fig.update_layout(hovermode="x unified", xaxis_title=x_title, yaxis_tickprefix="£") 
    fig.update_xaxes(minallowed=df.index.min(), maxallowed=df.index.max()) 
    fig.update_yaxes(minallowed=0, maxallowed=ymax * 1.05) 
    return fig 

st.title("Wealth Growth Simulator")

start = st.sidebar.number_input("Starting Amount (£):", value=1000) 
monthly = st.sidebar.number_input("Monthly Contribution (£):", value=100) 
rate = st.sidebar.slider("Annual Interest Rate (%)", 0.0, 15.0, 5.0) 
years = st.sidebar.slider("Years", 1, 40, 10) 
inflation = st.sidebar.slider("Inflation (%)", 0.0, 10.0, 2.5) 
fee = st.sidebar.slider("Annual fee (%)", 0.0, 3.0, 0.5) 
rate2 = st.sidebar.slider("Compare with rate (%)", 0.0, 15.0, 7.0) 
isa = st.sidebar.checkbox("Stocks & Shares ISA (tax-free)", value=True) 
tax_rate = st.sidebar.slider("Tax on growth (%)", 0, 45, 20) 
volatility = st.sidebar.slider("Yearly return swing (%)", 0, 30, 15)

tax = 0 if isa else tax_rate 
net_rate = (rate - fee) * (1 - tax / 100) 
net_rate2 = (rate2 - fee) * (1 - tax / 100) 
final, history = compound_interest(start, monthly, net_rate, years) 
final2, history2 = compound_interest(start, monthly, net_rate2, years)  
real_balance = final / (1 + inflation / 100) ** years 
col1, col2 = st.columns(2) 
col1.metric("Final Balance", f"£{final:,.2f}") 
col2.metric("Real Balance (today's money)", f"£{real_balance:,.2f}") 
total_contributed = start + monthly * years * 12 
col3, col4 = st.columns(2) 
col3.metric("Total Contributed", f"£{total_contributed:,.2f}") 
col4.metric("Total Growth", f"£{final - total_contributed:,.2f}") 
st.metric("Final Balance at comparison rate", f"£{final2:,.2f}", f"£{final2 - final:,.2f} vs your rate") 
contributed = [start + monthly * m for m in range(len(history))]
real_history = [b / (1 + inflation / 100) ** (m / 12) for m, b in enumerate(history)] 
st.plotly_chart(money_chart(pd.DataFrame({"Balance": history, "Contributions": contributed, "Real Balance": real_history, "Alternative Rate": history2})), use_container_width=True)
growth = [b - c for b, c in zip(history, contributed)] 
st.plotly_chart(money_chart(pd.DataFrame({"Contributions": contributed, "Growth": growth}), stacked=True), use_container_width=True) 

yearly = pd.DataFrame({"Year": range(years + 1), "Balance": history[::12], "Contributed": contributed[::12], "Real Balance": real_history[::12]}) 
with st.expander("Year-by-year table"): 
    st.dataframe(yearly) 
    st.download_button("Download CSV", yearly.to_csv(index=False), "Wealth_growth.csv", "text/csv") 
goal = st.sidebar.number_input("Goal Amount(£):", value=50000) 
months_needed = next((m for m, b in enumerate(history) if b >= goal), None) 
if months_needed is None: 
    st.warning("You won't reach this goal within the chosen year.") 
else:
     st.success(f"You reach £{goal:,.0f} in {months_needed // 12} years and {months_needed % 12} months.")  

st.subheader("Monte Carlo Simulation") 
sims = monte_carlo(start, monthly, net_rate, years, volatility, 200) 
mc = pd.DataFrame(sims) 
chart_data = pd.DataFrame({"Best": mc.max(), "Median": mc.median(), "Worst": mc.min()}) 
st.plotly_chart(money_chart(chart_data, x_title="Year"), use_container_width=True) 
