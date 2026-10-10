from finance import compound_interest  

def test_compound_interest(): 
    final, history = compound_interest(1000, 0, 0, 1) 
    assert final == 1000 

def test_contributions_only(): 
    final, history = compound_interest(0, 100, 0, 1)  
    assert final == 1200 

def test_history_length(): 
    final, history = compound_interest(1000, 100, 5, 10) 
    assert len(history) == 10 * 12 + 1 

def test_one_year_growth(): 
    final, history = compound_interest(1000, 0, 12, 1) 
    assert round(final, 2) == 1126.83
