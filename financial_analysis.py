from data_loader import load_financial_data
from opik import track


@track
def calculate_revenue_growth(company, previous_year, current_year):

    df = load_financial_data()

    previous = df[
        (df["Company"] == company) &
        (df["Year"] == previous_year)
    ]

    current = df[
        (df["Company"] == company) &
        (df["Year"] == current_year)
    ]

    if previous.empty or current.empty:
        return {
            "error": f"Data not available for {company} "
                     f"for {previous_year} and {current_year}."
        }

    previous_revenue = float(previous.iloc[0]["Revenue"])
    current_revenue = float(current.iloc[0]["Revenue"])

    growth = (
        (current_revenue - previous_revenue)
        / previous_revenue
    ) * 100

    return {
        "company": company,
        "previous_year": previous_year,
        "previous_revenue": previous_revenue,
        "current_year": current_year,
        "current_revenue": current_revenue,
        "revenue_growth_percent": round(growth, 2)
    }


@track
def get_net_income(company, year):

    df = load_financial_data()

    data = df[
        (df["Company"] == company) &
        (df["Year"] == year)
    ]

    if data.empty:
        return {
            "error": f"Data not available for {company} in {year}."
        }

    return {
        "company": company,
        "year": year,
        "net_income": float(data.iloc[0]["Net Income"])
    }


@track
def get_profit_margin(company, year):

    df = load_financial_data()

    data = df[
        (df["Company"] == company) &
        (df["Year"] == year)
    ]

    if data.empty:
        return {
            "error": f"Data not available for {company} in {year}."
        }

    return {
        "company": company,
        "year": year,
        "net_profit_margin": float(
            data.iloc[0]["Net Profit Margin"]
        )
    }


@track
def get_financial_summary(company, year):

    df = load_financial_data()

    data = df[
        (df["Company"] == company) &
        (df["Year"] == year)
    ]

    if data.empty:
        return {
            "error": f"Data not available for {company} in {year}."
        }

    row = data.iloc[0]

    return {
        "company": company,
        "year": year,
        "revenue": float(row["Revenue"]),
        "gross_profit": float(row["Gross Profit"]),
        "net_income": float(row["Net Income"]),
        "ebitda": float(row["EBITDA"]),
        "eps": float(row["EPS"]),
        "current_ratio": float(row["Current Ratio"]),
        "debt_equity_ratio": float(row["Debt/Equity Ratio"]),
        "roe": float(row["ROE"]),
        "roa": float(row["ROA"]),
        "roi": float(row["ROI"]),
        "net_profit_margin": float(row["Net Profit Margin"])
    }