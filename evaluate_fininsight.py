import json
import re

import ollama
from opik import track

from ai_router import answer_question


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

        return {
            "error": (
                "Evaluator did not return valid JSON."
            )
        }

    try:

        return json.loads(
            text[start:end + 1]
        )

    except json.JSONDecodeError:

        return {
            "error": (
                "Could not parse evaluator response."
            )
        }


@track
def evaluate_answer(question, answer):

    prompt = f"""
You are an evaluator for a financial AI application.

Evaluate the AI answer below.

USER QUESTION:
{question}

AI ANSWER:
{answer}

Return ONLY JSON.

Use exactly this format:

{{
    "correctness": 0.0,
    "relevance": 0.0,
    "faithfulness": 0.0,
    "reason": "short explanation"
}}

Scoring:

correctness:
0 = incorrect
0.5 = partially correct
1 = correct

relevance:
0 = irrelevant
0.5 = partially relevant
1 = directly answers the question

faithfulness:
0 = contains unsupported/invented information
0.5 = partially grounded
1 = stays grounded in the provided financial result

Do not invent information.
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


def run_evaluation():

    questions = [

        "What was Apple's revenue growth from 2021 to 2022?",

        "What was Apple's net income in 2022?",

        "What was Apple's profit margin in 2022?",

        "Give me Apple's financial summary for 2022."
    ]

    results = []

    for question in questions:

        print("\n" + "=" * 70)

        print(
            f"\nQuestion:\n{question}"
        )

        answer = answer_question(
            question
        )

        print(
            f"\nFinInsight Answer:\n{answer}"
        )

        evaluation = evaluate_answer(
            question,
            answer
        )

        print(
            "\nEvaluation:"
        )

        print(
            json.dumps(
                evaluation,
                indent=4
            )
        )

        results.append(
            {
                "question": question,
                "answer": answer,
                "evaluation": evaluation
            }
        )

    with open(
        "evaluation_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "\nEvaluation completed."
    )

    print(
        "Results saved to "
        "evaluation_results.json"
    )


if __name__ == "__main__":

    run_evaluation()