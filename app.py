import streamlit as st

from ai_router import (
    answer_question,
    process_question,
    understand_question
)

from rag_engine import search_documents


st.set_page_config(
    page_title="FinInsight",
    page_icon="📊",
    layout="centered"
)


st.title("📊 FinInsight")

st.subheader(
    "AI-Powered Financial Analysis & Document Intelligence"
)

st.write(
    "Ask questions about financial data and "
    "financial documents using a local AI model."
)


st.info(
    "Powered by Ollama + Llama 3.2 + Pandas + "
    "ChromaDB + RAG + Opik"
)


question = st.text_input(
    "Ask a financial question",
    placeholder=(
        "What was Apple's revenue growth "
        "from 2021 to 2022?"
    )
)


if st.button("Analyze"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "Analyzing your financial question..."
        ):

            try:

                # Determine what type of question
                # the user asked.
                intent = understand_question(
                    question
                )

                operation = intent.get(
                    "operation"
                )

                # --------------------------------
                # DOCUMENT / RAG QUESTION
                # --------------------------------

                if operation == "document_question":

                    answer = answer_question(
                        question
                    )

                    st.subheader(
                        "📄 Document Analysis"
                    )

                    st.write(answer)

                    st.divider()

                    st.subheader(
                        "🔎 Retrieved Evidence"
                    )

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

                    if documents:

                        for i, (
                            document,
                            metadata
                        ) in enumerate(
                            zip(
                                documents,
                                metadatas
                            ),
                            start=1
                        ):

                            page = metadata.get(
                                "page",
                                "Unknown"
                            )

                            with st.expander(
                                f"Source {i} — Page {page}"
                            ):

                                st.write(
                                    document
                                )

                    else:

                        st.warning(
                            "No relevant document "
                            "evidence was found."
                        )

                # --------------------------------
                # STRUCTURED DATA QUESTION
                # --------------------------------

                else:

                    answer = answer_question(
                        question
                    )

                    st.subheader(
                        "📊 Financial Analysis"
                    )

                    st.write(answer)

                    st.divider()

                    st.subheader(
                        "⚙️ Analysis Type"
                    )

                    st.write(
                        f"Operation: `{operation}`"
                    )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )


st.divider()

st.subheader(
    "💡 Example Questions"
)

st.markdown(
    """
### 📊 Structured Financial Data

**Revenue growth**

> What was Apple's revenue growth from 2021 to 2022?

**Net income**

> What was Apple's net income in 2022?

**Profit margin**

> What was Apple's profit margin in 2022?

**Financial summary**

> Give me Apple's financial summary for 2022.

### 📄 Financial Document / RAG

**Risk analysis**

> What risks did Apple mention in its annual report?

**Business information**

> What products and services does Apple describe in its annual report?

**Financial discussion**

> What factors affected Apple's business according to the annual report?
"""
)