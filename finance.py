def compound_interest(start, monthly, rate, years): 
    balance = start 
    history = [balance] 
    for month in range(years * 12): 
        balance += monthly
        balance *= 1 + rate / 100 / 12 
        history.append(balance) 
    return balance, history  
