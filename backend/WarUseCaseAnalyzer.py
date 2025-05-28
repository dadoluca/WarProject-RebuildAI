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
from model.Model import (MitigationList, UseCaseList, CardResponse, UseCaseCard, RiskMitigationCard, BenefitModel, MitigationModel, RiskModel, UseCase)

class WarUseCaseAnalyzer:
    """
    A class for analyzing war-related use cases using RAG and LLMs.
    Creates JSON cards for use cases with associated risks, mitigations, and benefits.
    """
    
    def __init__(self):
        """
        Initialize the WarUseCaseAnalyzer with necessary connections to Vector DBs and LLM.
        """
        # Load API keys from environment variables
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        if not self.openai_api_key or not self.pinecone_api_key:
            raise ValueError("Missing required API keys in environment variables")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # Initialize VectorDBManager instances for different data types
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "war-use-cases")
        
        self.use_cases_db = VectorDBManager(
            pinecone_api=self.pinecone_api_key,
            openai_api=self.openai_api_key,
            index_name=self.index_name,
            namespace="use_cases"
        )
        
        self.risks_db = VectorDBManager(
            pinecone_api=self.pinecone_api_key,
            openai_api=self.openai_api_key,
            index_name=self.index_name,
            namespace="risks"
        )
        
        self.benefits_db = VectorDBManager(
            pinecone_api=self.pinecone_api_key,
            openai_api=self.openai_api_key,
            index_name=self.index_name,
            namespace="benefits"
        )
        
        self.mitigations_db = VectorDBManager(
            pinecone_api=self.pinecone_api_key,
            openai_api=self.openai_api_key,
            index_name=self.index_name,
            namespace="mitigations"
        )
        
        # Default LLM model
        self.default_model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def _query_llm(self, messages: List[Dict[str, str]], response_model=None, temperature: float = 0.3):
        """
        Helper function to query an OpenAI-compatible chat model.
        
        Args:
            messages: List of message dictionaries with role and content.
            response_model: Optional Pydantic model for structured output.
            temperature: Controls randomness in generation (0.0-1.0).
            
        Returns:
            Either parsed structured data or raw completion text.
        """
        try:
            if response_model:
                completion = self.openai_client.beta.chat.completions.parse(
                    model=self.default_model,
                    messages=messages,
                    response_format=response_model,
                    temperature=temperature
                )
                return completion.choices[0].message.parsed
            else:
                completion = self.openai_client.chat.completions.create(
                    model=self.default_model,
                    messages=messages,
                    temperature=temperature
                )
                return completion.choices[0].message.content
        except Exception as e:
            print(f"Error querying LLM: {e}")
            raise

    def retrieve_use_cases(self, query: str, top_k: int = 3):
        """
        Retrieves relevant use cases from the vector database based on the query.
        
        Args:
            query: The user's input query.
            top_k: Number of use cases to retrieve.
            
        Returns:
            List of retrieved use cases with metadata.
        """
        results = self.use_cases_db.search_kb(query, top_k=top_k)
        return results

    def generate_use_cases(self, query: str, search_results, limit_use_cases: int = 3):
        """
        Generates use cases based on retrieved information, but synthesizes 
        and adapts them to be more relevant to the specific query.
        
        Args:
            query: The original user query.
            search_results: Results from vector DB search.
            limit_use_cases: Number of use cases to generate.
            
        Returns:
            List of UseCase objects.
        """
        # Prepare context from search results
        context_items = []
        for match in search_results.matches:
            metadata = match.metadata
            context_items.append(f"Title: {metadata.get('title', 'N/A')}\n"
                                f"Description: {metadata.get('description', 'N/A')}\n"
                                f"Context: {metadata.get('context', 'N/A')}\n"
                                f"Source: {metadata.get('source', 'N/A')}\n"
                                f"Score: {match.score}")
        
        context_text = "\n\n".join(context_items)
        
        # Prepare prompt for LLM
        messages = [
            {"role": "system", "content": 
             "You are an expert in analyzing technology/AI use cases for post-conflict and humanitarian contexts. "
             "Based on the retrieved use cases and the user's query, generate tailored use cases that are specifically relevant "
             "to the query context. Don't just analyze the retrieved use cases - use them as inspiration to generate."
             "highly relevant use cases that would be most applicable to the specific query. Be creative but practical."},
            {"role": "user", "content": 
             f"Query: {query}\n\nRetrieved use cases:\n\n{context_text}\n\n"
             f"Generate tailored use cases that are highly relevant to this specific query. Use the retrieved information "
             f"as inspiration but create use cases that directly address the query. For each use case, assign a relevance score "
             f"to the query on a scale of 0-1, where 1 is highly relevant. Structure the information according to the provided model."
             f" Generate exactly {limit_use_cases} use cases."
             f" Follow the rues of the style guide: {style_guide}"}
        ]
        
        # Query LLM for structured analysis
        result = self._query_llm(messages, response_model=UseCaseList)
        use_cases = result.use_cases
        
        # Apply limit if necessary
        if len(use_cases) > limit_use_cases:
            use_cases = use_cases[:limit_use_cases]
            
        return use_cases

    def retrieve_risks_and_benefits(self, use_case: UseCase, top_k: int = 3):
        """
        Retrieves risks and benefits associated with a use case.
        
        Args:
            use_case: The UseCase object to find risks and benefits for.
            top_k: Number of items to retrieve for each category.
            
        Returns:
            Tuple of (risks_results, benefits_results).
        """
        # Create a search query based on the use case title and description
        search_query = f"{use_case.title} {use_case.description}"
        
        # Retrieve risks and benefits
        risks_results = self.risks_db.search_kb(search_query, top_k=top_k)
        benefits_results = self.benefits_db.search_kb(search_query, top_k=top_k)
        
        return risks_results, benefits_results

    def generate_risks_and_benefits(self, query: str, use_case: UseCase, risks_results, benefits_results, 
                                   limit_risks: int = 3, limit_benefits: int = 3):
        """
        Generates risks and benefits that are specifically tailored to the use case and query,
        using the retrieved information as inspiration.
        
        Args:
            query: The original user query.
            use_case: The use case being analyzed.
            risks_results: Results from risks vector DB search.
            benefits_results: Results from benefits vector DB search.
            limit_risks: Number of risks to generate.
            limit_benefits: Number of benefits to generate.
            
        Returns:
            Tuple of (List[RiskModel], List[BenefitModel]).
        """
        # Prepare context from risk results
        risk_items = []
        for match in risks_results.matches:
            metadata = match.metadata
            risk_items.append(f"Title: {metadata.get('title', 'N/A')}\n"
                            f"Description: {metadata.get('description', 'N/A')}\n"
                            f"Context: {metadata.get('context', 'N/A')}\n"
                            f"Source: {metadata.get('source', 'N/A')}\n"
                            f"Score: {match.score}")
        
        risk_context = "\n\n".join(risk_items)
        
        # Prepare context from benefit results
        benefit_items = []
        for match in benefits_results.matches:
            metadata = match.metadata
            benefit_items.append(f"Title: {metadata.get('title', 'N/A')}\n"
                               f"Description: {metadata.get('description', 'N/A')}\n"
                               f"Context: {metadata.get('context', 'N/A')}\n"
                               f"Source: {metadata.get('source', 'N/A')}\n"
                               f"Score: {match.score}")
        
        benefit_context = "\n\n".join(benefit_items)
        
        # Prepare prompt for risks generation
        risk_messages = [
            {
                "role": "system",
                "content": (
                    "You are a risk analyst focused on technologies used in humanitarian and post-conflict settings. "
                    "Your task is to generate **realistic, specific, and concrete risks** relevant to the provided use case. "
                    "Start by **reusing or adapting risks retrieved from the knowledge base**. Only invent new risks if the retrieved ones are insufficient "
                    "to fully cover the scenario. Your analysis must include both **strategic/systemic risks** (e.g., cultural misalignment, supply chain issues) "
                    "and **basic, physical risks** (e.g., fire hazards, sanitation, structural failure, overcrowding, weather exposure). "
                    "All risks must be practical and grounded in common sense and field experience. Avoid generic or overly abstract risks."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Query: {query}\n\n"
                    f"Use Case Title: {use_case.title}\n\n"
                    f"Use Case Description: {use_case.description}\n\n"
                    f"Retrieved Risks from the knowledge base:\n{risk_context}\n\n"
                    f"Using the retrieved risks as your primary source, generate exactly {limit_risks} risks that are clearly tied to this use case. "
                    f"Adapt or reuse existing risks where possible. Create new risks **only if necessary** to ensure coverage, especially for common operational concerns. "
                    f"Make sure to include at least some **basic day-to-day risks** (e.g., hygiene, safety, fire, overcrowding, poor ventilation, etc.). "
                    f"Use clear and accessible language. Format the risks according to the provided structure and follow the style guide: {style_guide}"
                )
            }
        ]


        # Prepare prompt for benefits generation
        benefit_messages = [
            {"role": "system", "content": 
             "You are an expert in benefit assessment for technologies used in post-conflict and humanitarian contexts. "
             "Using the retrieved information as inspiration, generate tailored benefits that are specifically relevant "
             "to the given use case and query context. Be creative but realistic in identifying potential benefits."},
            {"role": "user", "content": 
             f"Original Query: {query}\n\n"
             f"Use Case: {use_case.title}\n\nDescription: {use_case.description}\n\n"
             f"Retrieved benefits:\n\n{benefit_context}\n\n"
             f"Generate tailored benefits that are specific to this use case in the context of the original query. "
             f"Use the retrieved information as inspiration, but create benefits that directly address the specific use case "
             f"and query context. Structure according to the provided model. Generate exactly {limit_benefits} benefits."
             f" Follow the rues of the style guide: {style_guide}"}
        ]
        
        # Define the structure for multiple risks and benefits
        class RiskList(BaseModel):
            risks: List[RiskModel] = Field(description="List of generated risks")
            
        class BenefitList(BaseModel):
            benefits: List[BenefitModel] = Field(description="List of generated benefits")
        
        # Query LLM for structured generation
        risks = self._query_llm(risk_messages, response_model=RiskList).risks
        benefits = self._query_llm(benefit_messages, response_model=BenefitList).benefits
        
        # Apply limits if necessary
        if len(risks) > limit_risks:
            risks = risks[:limit_risks]
        
        if len(benefits) > limit_benefits:
            benefits = benefits[:limit_benefits]
        
        return risks, benefits

    def retrieve_mitigations(self, risk: RiskModel, top_k: int = 3):
        """
        Retrieves mitigations for a specific risk.
        
        Args:
            risk: The risk to find mitigations for.
            top_k: Number of mitigations to retrieve.
            
        Returns:
            Mitigation search results.
        """
        # Create a search query based on the risk title and description
        search_query = f"{risk.title} {risk.description}"
        
        # Retrieve mitigations
        mitigations_results = self.mitigations_db.search_kb(search_query, top_k=top_k)
        
        return mitigations_results

    def generate_mitigations(self, query: str, use_case: UseCase, risk: RiskModel, mitigations_results, 
                           limit_mitigations: int = 1):
        """
        Generates mitigations for a specific risk, tailored to the use case and query context,
        using the retrieved information as inspiration.
        
        Args:
            query: The original user query.
            use_case: The use case context.
            risk: The risk being mitigated.
            mitigations_results: Results from mitigations vector DB search.
            limit_mitigations: Number of mitigations to generate per risk.
            
        Returns:
            List of MitigationModel objects.
        """
        # Prepare context from mitigation results
        mitigation_items = []
        for match in mitigations_results.matches:
            metadata = match.metadata
            mitigation_items.append(f"Title: {metadata.get('title', 'N/A')}\n"
                                  f"Description: {metadata.get('description', 'N/A')}\n"
                                  f"Context: {metadata.get('context', 'N/A')}\n"
                                  f"Source: {metadata.get('source', 'N/A')}\n"
                                  f"Score: {match.score}")
        
        mitigation_context = "\n\n".join(mitigation_items)
        
        # Prepare prompt for mitigation generation
        messages = [
            {"role": "system", "content": 
             "You are an expert in developing mitigation strategies for risks in post-conflict and humanitarian technology use. "
             "Using the retrieved information as inspiration, generate tailored mitigation strategies that are specifically "
             "relevant to the given risk, use case, and query context. Be creative but practical."},
            {"role": "user", "content": 
             f"Original Query: {query}\n\n"
             f"Use Case: {use_case.title}\n\nDescription: {use_case.description}\n\n"
             f"Risk: {risk.title}\n\nDescription: {risk.description}\n\n"
             f"Retrieved mitigations:\n\n{mitigation_context}\n\n"
             f"Generate tailored mitigation strategies that are specific to this risk in the context of the use case and "
             f"original query. Use the retrieved information as inspiration, but create mitigations that directly address "
             f"the specific risk, use case, and query context. Structure according to the provided model. "
             f"Generate exactly {limit_mitigations} mitigations."
             f"Follow the rues of the style guide: {style_guide}"}
        ]
        
        # Query LLM for structured generation
        result = self._query_llm(messages, response_model=MitigationList)
        mitigations = result.mitigations
        
        # Apply limit if necessary
        if len(mitigations) > limit_mitigations:
            mitigations = mitigations[:limit_mitigations]
        
        return mitigations

    def create_cards(self, query: str, use_cases: List[UseCase], use_case_analyses: List[Dict]):
        """
        Creates JSON cards for each use case with risks, mitigations, and benefits.
        
        Args:
            query: The original user query.
            use_cases: List of analyzed use cases.
            use_case_analyses: List of dictionaries containing risks, benefits, and mitigations.
            
        Returns:
            CardResponse object containing the list of cards.
        """
        cards = []
        
        # Create a card for each use case
        for i, use_case in enumerate(use_cases):
            analysis = use_case_analyses[i]
            risks = analysis["risks"]
            benefits = analysis["benefits"]
            
            # Create a list of risk-mitigation pairs
            risks_mitigations = []
            for risk_idx, risk in enumerate(risks):
                if "mitigations" in analysis and risk_idx < len(analysis["mitigations"]) and analysis["mitigations"][risk_idx]:
                    # For each risk, use the first mitigation
                    mitigation = analysis["mitigations"][risk_idx][0]
                    
                    # Create risk-mitigation pair with complete context and source information
                    risk_mitigation = RiskMitigationCard(
                        # Risk information
                        risk_title=risk.title,
                        risk_description=risk.description,
                        risk_source=risk.source or "Not specified",
                        risk_context=risk.context or "General context",
                        # Mitigation information
                        mitigation_title=mitigation.title,
                        mitigation_description=mitigation.description,
                        mitigation_source=mitigation.source or "Not specified",
                        mitigation_context=mitigation.context or "General context"
                    )
                    risks_mitigations.append(risk_mitigation)
            
            # Create benefit objects with complete context and source information
            benefit_objects = [
                {
                    "title": benefit.title,
                    "description": benefit.description,
                    "context": benefit.context or "General context",
                    "source": benefit.source or "Not specified"
                }
                for benefit in benefits
            ]
            
            # Create the use case card
            card = UseCaseCard(
                title=use_case.title,
                description=use_case.description,
                context=use_case.context or "General context",
                risks_mitigations=risks_mitigations,
                benefits=benefit_objects,
                relevance_score=use_case.relevance_score,
                source=use_case.source,
                steps_to_implementation=use_case.steps_to_implementation
            )
            
            cards.append(card)
        
        # Create the final card response
        card_response = CardResponse(
            query=query,
            cards=cards
        )
        
        return card_response

    def analyze(self, query: str, 
                limit_use_cases: int = 3, 
                limit_risks: int = 3, 
                limit_benefits: int = 3, 
                limit_mitigations: int = 1, 
                top_k_retrieve: int = 5):
        """
        Main pipeline function that executes the entire analysis process and creates JSON cards.
        
        Args:
            query: The user's query about a post-conflict challenge.
            limit_use_cases: Number of use cases to generate.
            limit_risks: Number of risks to generate per use case.
            limit_benefits: Number of benefits to generate per use case.
            limit_mitigations: Number of mitigations to generate per risk.
            top_k_retrieve: Number of items to retrieve from the vector database (applies to all retrieval operations).
            
        Returns:
            JSON string containing the cards with use cases, risks, mitigations, and benefits.
        """
        print(f"Starting analysis for query: '{query}'")
        
        # Step 1: Retrieve relevant use cases
        print("Step 1: Retrieving relevant use cases...")
        use_case_results = self.retrieve_use_cases(query, top_k=top_k_retrieve)
        
        # Step 2: Generate tailored use cases
        print("Step 2: Generating tailored use cases...")
        use_cases = self.generate_use_cases(query, use_case_results, limit_use_cases=limit_use_cases)
        
        # Steps 3-7: For each use case, retrieve and generate risks, benefits, and mitigations
        use_case_analyses = []
        for use_case in use_cases:
            print(f"Processing use case: {use_case.title}")
            
            # Step 3-4: Retrieve and generate risks and benefits
            print("Retrieving risks and benefits...")
            risks_results, benefits_results = self.retrieve_risks_and_benefits(use_case, top_k=top_k_retrieve)
            
            print("Generating tailored risks and benefits...")
            risks, benefits = self.generate_risks_and_benefits(
                query, use_case, risks_results, benefits_results,
                limit_risks=limit_risks, limit_benefits=limit_benefits
            )
            
            # Steps 5-6: For each risk, retrieve and generate mitigations
            all_mitigations = []
            for risk in risks:
                print(f"Processing risk: {risk.title}")
                
                print("Retrieving mitigations...")
                mitigations_results = self.retrieve_mitigations(risk, top_k=top_k_retrieve)
                
                print("Generating tailored mitigations...")
                mitigations = self.generate_mitigations(
                    query, use_case, risk, mitigations_results,
                    limit_mitigations=limit_mitigations
                )
                all_mitigations.append(mitigations)
            
            # Store analysis for this use case
            use_case_analyses.append({
                "risks": risks,
                "benefits": benefits,
                "mitigations": all_mitigations
            })
        
        # Step 7: Create JSON cards
        print("Step 7: Creating JSON cards...")
        card_response = self.create_cards(
            query, 
            use_cases, 
            use_case_analyses
        )
        
        # Convert to JSON
        return card_response.model_dump()