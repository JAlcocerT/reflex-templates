import pandas as pd
from cagr import calculate_cagr

def test_cagr_basic():
    # 2 years, price from 100 to 121, CAGR should be 10%
    df = pd.DataFrame({
        "Stock": ["A", "A"],
        "Date": ["2020-01-01", "2022-01-01"],
        "Close": [100, 121],
    })
    result = calculate_cagr(df)
    print("\n[test_cagr_basic] Result:")
    print(result)
    cagr = result.loc[result["Stock"] == "A", "CAGR"].iloc[0]
    assert abs(cagr - 0.10) < 1e-4, f"Expected ~0.10, got {cagr}"

def test_cagr_one_value():
    # Only one value, CAGR should be None
    df = pd.DataFrame({
        "Stock": ["B"],
        "Date": ["2020-01-01"],
        "Close": [100],
    })
    result = calculate_cagr(df)
    print("\n[test_cagr_one_value] Result:")
    print(result)
    cagr = result.loc[result["Stock"] == "B", "CAGR"].iloc[0]
    assert cagr is None

def test_cagr_zero_or_negative():
    # Zero or negative values, CAGR should be None
    df = pd.DataFrame({
        "Stock": ["C", "C"],
        "Date": ["2020-01-01", "2022-01-01"],
        "Close": [0, 100],
    })
    result = calculate_cagr(df)
    print("\n[test_cagr_zero_or_negative] Result (C):")
    print(result)
    cagr = result.loc[result["Stock"] == "C", "CAGR"].iloc[0]
    assert cagr is None

    df = pd.DataFrame({
        "Stock": ["D", "D"],
        "Date": ["2020-01-01", "2022-01-01"],
        "Close": [-100, 100],
    })
    result = calculate_cagr(df)
    print("\n[test_cagr_zero_or_negative] Result (D):")
    print(result)
    cagr = result.loc[result["Stock"] == "D", "CAGR"].iloc[0]
    assert cagr is None

def test_cagr_multiple_stocks():
    # Multiple stocks
    df = pd.DataFrame({
        "Stock": ["A", "A", "B", "B"],
        "Date": ["2020-01-01", "2022-01-01", "2020-01-01", "2022-01-01"],
        "Close": [100, 121, 200, 242],
    })
    result = calculate_cagr(df)
    print("\n[test_cagr_multiple_stocks] Result:")
    print(result)
    cagr_a = result.loc[result["Stock"] == "A", "CAGR"].iloc[0]
    cagr_b = result.loc[result["Stock"] == "B", "CAGR"].iloc[0]
    assert abs(cagr_a - 0.10) < 1e-4
    assert abs(cagr_b - 0.10) < 1e-4

if __name__ == "__main__":
    test_cagr_basic()
    test_cagr_one_value()
    test_cagr_zero_or_negative()
    test_cagr_multiple_stocks()
    print("All CAGR tests passed!")
