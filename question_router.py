import re
from financial_analysis import calculate_revenue_growth


def route_question(question):

    question_lower = question.lower()

    # Detect company
    if "apple" in question_lower or "aapl" in question_lower:
        company = "AAPL"
    else:
        return "Currently, I can analyze Apple (AAPL) only."

    # Detect years
    years = re.findall(r"\b(20\d{2})\b", question)

    if len(years) < 2:
        return "Please provide two years for revenue-growth analysis."

    previous_year = int(years[0])
    current_year = int(years[1])

    # Detect analysis type
    if "revenue growth" in question_lower or "revenue" in question_lower:

        return calculate_revenue_growth(
            company,
            previous_year,
            current_year
        )

    return "I don't know how to analyze that question yet."


if __name__ == "__main__":

    question = input("\nAsk FinInsight: ")

    result = route_question(question)

    print("\nFinInsight Result:")
    print(result)