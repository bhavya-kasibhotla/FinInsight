import json
import re

import ollama
from opik import track

from financial_analysis import (
    calculate_revenue_growth,
    get_net_income,
    get_profit_margin,
    get_financial_summary
)

from rag_engine import search_documents


def extract_json(text):
    text = text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Llama did not return valid JSON."
        )

    return json.loads(
        text[start:end + 1]
    )


@track
def understand_question(question):

    prompt = f"""
You are the intent detection system for FinInsight.

Analyze the user's financial question.

Return ONLY valid JSON.

Supported operations:

1. revenue_growth
2. net_income
3. profit_margin
4. financial_summary
5. document_question

Rules:

- Apple or AAPL means AAPL.
- Extract the year or years.
- For revenue_growth, identify previous_year and current_year.
- For other operations, identify year if required.
- If the user is asking about information that would normally
  come from an annual report or financial document,
  use document_question.
- Do NOT calculate anything.
- Do NOT explain anything.
- Return JSON only.

Example:

Question:
What was Apple's revenue growth from 2021 to 2022?

Return:
{{
    "operation": "revenue_growth",
    "company": "AAPL",
    "previous_year": 2021,
    "current_year": 2022
}}

Example:

Question:
What was Apple's net income in 2022?

Return:
{{
    "operation": "net_income",
    "company": "AAPL",
    "year": 2022
}}

Example:

Question:
What was Apple's profit margin in 2022?

Return:
{{
    "operation": "profit_margin",
    "company": "AAPL",
    "year": 2022
}}

Example:

Question:
Give me Apple's financial summary for 2022.

Return:
{{
    "operation": "financial_summary",
    "company": "AAPL",
    "year": 2022
}}

Example:

Question:
What risks did Apple mention in its annual report?

Return:
{{
    "operation": "document_question",
    "company": "AAPL"
}}

User question:
{question}
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return extract_json(
        response["message"]["content"]
    )


@track
def answer_document_question(question):

    results = search_documents(
        question,
        top_k=4
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    if not documents:
        return (
            "I could not find relevant information "
            "in the financial document."
        )

    context_parts = []

    for document, metadata in zip(
        documents,
        metadatas
    ):
        context_parts.append(
            f"Page {metadata.get('page')}:\n"
            f"{document}"
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are FinInsight, a financial document analysis assistant.

Answer the user's question using ONLY the provided
annual-report context.

USER QUESTION:
{question}

ANNUAL REPORT CONTEXT:
{context}

Rules:

- Do not invent information.
- Do not use outside knowledge.
- If the answer is not present in the context,
  say that the information was not found.
- Keep the answer clear and concise.
- Mention the relevant page number when possible.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


@track
def process_question(question):

    intent = understand_question(
        question
    )

    operation = intent.get(
        "operation"
    )

    company = intent.get(
        "company",
        "AAPL"
    )

    if operation == "revenue_growth":

        return calculate_revenue_growth(
            company,
            int(intent["previous_year"]),
            int(intent["current_year"])
        )

    if operation == "net_income":

        return get_net_income(
            company,
            int(intent["year"])
        )

    if operation == "profit_margin":

        return get_profit_margin(
            company,
            int(intent["year"])
        )

    if operation == "financial_summary":

        return get_financial_summary(
            company,
            int(intent["year"])
        )

    if operation == "document_question":

        return answer_document_question(
            question
        )

    return {
        "error":
        "I don't know how to answer that question yet."
    }


@track
def explain_result(question, result):

    prompt = f"""
You are FinInsight, a financial analysis assistant.

User question:
{question}

Exact result calculated by Python:
{result}

Explain the result clearly in simple financial language.

Rules:

- Do not change any numbers.
- Do not invent financial information.
- Do not perform a different calculation.
- Explain what the result means.
- Keep the answer concise.
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


@track
def answer_question(question):

    try:

        result = process_question(
            question
        )

        if (
            isinstance(result, dict)
            and "error" in result
        ):
            return result["error"]

        # Document questions already have
        # their final LLM-generated answer.
        if isinstance(result, str):
            return result

        return explain_result(
            question,
            result
        )

    except Exception as e:

        return (
            f"Error processing question: {str(e)}"
        )


if __name__ == "__main__":

    question = input(
        "\nAsk FinInsight: "
    )

    answer = answer_question(
        question
    )

    print("\nFinInsight:")
    print(answer)