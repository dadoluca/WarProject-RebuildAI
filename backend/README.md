# War Use Case Analyzer

A Flask-based API service that analyzes war-related and post-conflict technology solution using Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs). From a query of a problem, the system generates structured JSON Decision Support Cards containing solution with associated risks, mitigations, steps and benefits for humanitarian and post-conflict scenarios.

## Overview

The folder contains two main component:

1. **WarUseCaseAnalyzer Class**: Core analysis engine that processes queries through a RAG pipeline. The input of the system is a query with a problem and the output is a list of Support Decision Cards.
2. **Flask API**: REST API endpoint that exposes the analyzer functionality. It is the backend part of the application

## Features

- **RAG-based Analysis**: Retrieves relevant information from vector databases containing use cases, risks, benefits, and mitigations
- **LLM-powered Generation**: Uses OpenAI's GPT models to generate tailored content based on retrieved information
- **Structured Output**: Returns JSON cards with standardized format for easy integration
- **Multi-dimensional Analysis**: Covers use cases, risks, benefits, and mitigation strategies
- **Configurable Parameters**: Adjustable limits for generated content and retrieval depth

## Architecture

The system uses:
- **Vector Databases** (Pinecone): Store and retrieve relevant use cases, risks, benefits, and mitigations
- **OpenAI API**: Generate contextually relevant content using GPT models
- **Pydantic Models**: Ensure structured and validated output
- **Flask**: Provide REST API interface

## Prerequisites

- Python 3.8+
- OpenAI API key
- Pinecone API key and index
- Required Python packages (see installation)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dadoluca/WarProject-RebuildAI.git
   cd war-use-case-analyzer
   ```

2. **Install required packages**:
   ```bash
   pip install flask flask-cors openai pinecone-client pydantic python-dotenv
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


## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_INDEX_NAME`: Name of your Pinecone index (default: "war-use-cases")
- `LLM_MODEL`: OpenAI model to use (default: "gpt-4o-mini")

## Usage

### Starting the Application

1. **Start the Flask server**:
   ```bash
   python main.py
   ```
   
   The server will start on `http://0.0.0.0:5000` by default.

2. **Verify the server is running**:
   Check the console output for:
   ```
   * Running on all addresses.
   * Running on http://127.0.0.1:5000/
   * Running on http://[your-ip]:5000/
   ```

### API Endpoint

**POST** `/analyze`

**Request Body**:
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
