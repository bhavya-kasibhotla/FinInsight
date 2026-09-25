# FinInsight

## AI-Powered Financial Document Analysis & Risk Intelligence Platform

FinInsight is an AI-powered financial analysis platform that combines **structured financial data analysis, Retrieval-Augmented Generation (RAG), local Large Language Models (LLMs), and AI observability** to help users analyze financial statements and obtain grounded insights from financial documents.

The platform can perform financial calculations directly from structured data while using RAG to retrieve relevant information from financial documents before generating explanations.

---

## 🚀 Key Features

### 📊 Financial Data Analysis
- Analyze structured financial statement data using Pandas.
- Calculate important financial metrics.
- Perform revenue and profitability analysis.
- Analyze net income and profit margins.
- Generate financial summaries from company data.

### 🤖 AI-Powered Financial Analysis
- Uses a local LLM through Ollama.
- AI router determines the appropriate analysis workflow.
- Combines deterministic Python calculations with AI-generated explanations.
- Reduces hallucination by providing calculated results to the LLM.

### 📚 RAG-Based Document Analysis
- Upload and process financial documents.
- Extract text from PDF documents.
- Split documents into searchable chunks.
- Generate semantic embeddings using Sentence Transformers.
- Store embeddings in ChromaDB.
- Retrieve relevant document sections based on user queries.
- Generate answers grounded in retrieved evidence.

### 🔎 Evidence & Source Context
- Displays retrieved document context.
- Provides relevant page information where available.
- Helps users understand which document content supports an AI response.

### 📈 AI Observability & Evaluation
- Integrated with Opik for monitoring and evaluating AI workflows.
- Enables analysis of AI interactions and application performance.
- Supports evaluation of the FinInsight AI pipeline.

### 🖥️ Interactive Web Application
- Built using Streamlit.
- Simple interface for financial analysis and document-based questions.
- Supports both structured financial analysis and RAG-based queries.

---

# 🏗️ System Architecture

```text
                         ┌───────────────────┐
                         │       User        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    Streamlit UI   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     AI Router     │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌───────────────────┐         ┌───────────────────┐
          │ Financial Analysis│         │    RAG Engine     │
          │      (Pandas)     │         │                   │
          └─────────┬─────────┘         └─────────┬─────────┘
                    │                             │
                    │                             ▼
                    │                   ┌───────────────────┐
                    │                   │    ChromaDB       │
                    │                   └─────────┬─────────┘
                    │                             │
                    │                             ▼
                    │                   ┌───────────────────┐
                    │                   │ Semantic Retrieval│
                    │                   └─────────┬─────────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   ▼
                         ┌───────────────────┐
                         │   Local LLM       │
                         │ Ollama / Llama    │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Grounded Response │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Opik Observability│
                         └───────────────────┘
