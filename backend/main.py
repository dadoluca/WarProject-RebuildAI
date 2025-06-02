import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from db.VectorDBManager import VectorDBManager
import json
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from writingrules import style_guide
from WarUseCaseAnalyzer import WarUseCaseAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__)

#cors management allowing all origins
CORS(app, resources={r"/*": {"origins": "*"}})

analyzer = WarUseCaseAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    try:
        data = request.json
        
        query = data.get('query', '')
        limit_use_cases = 3
        limit_risks = 5
        limit_benefits = 5
        limit_mitigations = 1
        top_k_retrieve = 10
        
        result = analyzer.analyze(
            query=query,
            limit_use_cases=limit_use_cases,
            limit_risks=limit_risks,
            limit_benefits=limit_benefits,
            limit_mitigations=limit_mitigations,
            top_k_retrieve=top_k_retrieve
        )
        
        return jsonify(result)
    
    except Exception as e:
        error = {"error": str(e)}
        return jsonify(error)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    