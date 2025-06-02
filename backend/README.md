# Rebuild AI - Pipeline and Backend

A **Flask-based API service** that analyzes war-related and post-conflict technology solutions using **Retrieval-Augmented Generation (RAG)** and **Large Language Models (LLMs)**. From a problem query, the system generates structured **JSON Decision Support Cards** with solutions, risks, mitigation strategies, steps, and benefits.

## 🌍 Overview

This folder contains two main components:

1. **`WarUseCaseAnalyzer` Class**
   Core analysis engine that processes queries through a RAG pipeline. Input: a problem query. Output: structured decision support cards.
2. **Flask API**
   REST API exposing the analyzer functionality, forming the backend of the application.

## ✨ Features

* 📚 **RAG-based Analysis**: Retrieves relevant information from vector databases
* 🤖 **LLM-powered Generation**: Uses OpenAI’s GPT models to generate tailored insights
* 📦 **Structured Output**: Returns JSON cards in a standardized format
* 🛡️ **Multi-dimensional Analysis**: Solutions, risks, mitigations, and benefits
* ⚙️ **Configurable Parameters**: Adjustable limits for generated content and retrieval

## 🏗️ Architecture

The system uses:

* **Vector Databases** (Pinecone) for use case and risk/benefit retrieval
* **OpenAI API** for contextual generation
* **Pydantic Models** for validated, structured output
* **Flask** for the REST API interface

## 🛠️ Prerequisites

* **Python 3.8+**
* **OpenAI API Key**
* **Pinecone API Key and Index**
* Required Python packages (see below)

## 🚀 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/dadoluca/WarProject-RebuildAI.git
   cd war-use-case-analyzer
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   PINECONE_INDEX_NAME=war-use-cases
   LLM_MODEL=gpt-4o-mini
   EMBEDDING_MODEL=text-embedding-ada-002
   ```

## 🔧 Configuration

### Environment Variables

* `OPENAI_API_KEY`: Your OpenAI API key
* `PINECONE_API_KEY`: Your Pinecone API key
* `PINECONE_INDEX_NAME`: Pinecone index name (default: `war-use-cases`)
* `LLM_MODEL`: OpenAI model to use (default: `gpt-4o-mini`)

## ⚡ Usage

### Starting the Application

1. **Run the Flask server**:

   ```bash
   python main.py
   ```

   By default, it will run at `http://0.0.0.0:5000`.

2. **Check the server status**:

   ```
   * Running on all addresses.
   * Running on http://127.0.0.1:5000/
   * Running on http://[your-ip]:5000/
   ```

### API Endpoint

**POST** `/analyze`

**Request Example**:

```json
{
  "query": "How can AI be used to help refugees in post-conflict zones?"
}
```

**Response Format**:

```json
{
  "query": "How can AI be used to help refugees in post-conflict zones?",
  "cards": [
    {
      "title": "AI-Powered Refugee Registration System",
      "description": "Digital system for efficient refugee registration and documentation",
      "context": "Post-conflict humanitarian response",
      "relevance_score": 0.95,
      "source": "Generated based on humanitarian technology research",
      "steps_to_implementation": ["Step 1", "Step 2", "Step 3"],
      "risks_mitigations": [
        {
          "risk_title": "Data Privacy Concerns",
          "risk_description": "Risk of personal data exposure",
          "risk_source": "Privacy assessment studies",
          "risk_context": "Refugee data protection",
          "mitigation_title": "Encrypted Database Storage",
          "mitigation_description": "Implement end-to-end encryption",
          "mitigation_source": "Security best practices",
          "mitigation_context": "Data protection measures"
        }
      ],
      "benefits": [
        {
          "title": "Improved Registration Efficiency",
          "description": "Faster processing of refugee applications",
          "context": "Operational improvement",
          "source": "Field implementation studies"
        }
      ]
    }
  ]
}
```

### ⚙️ Modifying Output Parameters

You can tweak the output by adjusting these variables in the Python code:

```python
top_k_retrieve = 10  # Number of rows retrieved per query
limit_use_cases = 3  # Number of solutions returned
limit_risks = 5      # Number of risks per solution
limit_benefits = 5   # Number of benefits per solution
```
