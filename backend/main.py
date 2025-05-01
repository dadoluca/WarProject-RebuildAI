import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from db.VectorDBManager import VectorDBManager

# Load environment variables
load_dotenv()

# Define Pydantic models for structured data
class UseCase(BaseModel):
    title: str = Field(description="Title of the use case")
    description: str = Field(description="Detailed description of the use case")
    context: str = Field(description="Context where the use case applies")
    relevance_score: float = Field(description="Relevance score to the query (0-1)")
    source: Optional[str] = Field(description="Source of the use case information")

class RiskModel(BaseModel):
    title: str = Field(description="Title of the risk")
    description: str = Field(description="Detailed description of the risk")
    context: Optional[str] = Field(description="Context where this risk applies")
    source: Optional[str] = Field(description="Source of the risk information")

class BenefitModel(BaseModel):
    title: str = Field(description="Title of the benefit")
    description: str = Field(description="Detailed description of the benefit")
    context: Optional[str] = Field(description="Context where this benefit applies")
    source: Optional[str] = Field(description="Source of the benefit information")

class MitigationModel(BaseModel):
    title: str = Field(description="Title of the mitigation strategy")
    description: str = Field(description="Detailed description of the mitigation strategy")
    effectiveness: str = Field(description="Effectiveness of the mitigation: Low, Medium, or High")
    context: Optional[str] = Field(description="Context where this mitigation applies")
    source: Optional[str] = Field(description="Source of the mitigation information")

class AnalysisReport(BaseModel):
    query: str = Field(description="Original query that initiated the analysis")
    summary: str = Field(description="Executive summary of the analysis")
    use_cases: List[UseCase] = Field(description="List of relevant use cases")
    analysis_by_use_case: str = Field(description="Detailed analysis for each use case including risks, benefits, and mitigations")
    #recommendations: str = Field(description="Overall recommendations based on the analysis")
    considerations: Optional[str] = Field(None, description="Additional considerations or limitations")


class WarUseCaseAnalyzer:
    """
    A class for analyzing war-related use cases using RAG and LLMs.
    Implements a pipeline that retrieves relevant use cases, associated risks, benefits, 
    and mitigation strategies to generate a comprehensive analysis report.
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

    def analyze_use_cases(self, query: str, search_results):
        """
        Analyzes retrieved use cases to determine relevance and generate structured data.
        
        Args:
            query: The original user query.
            search_results: Results from vector DB search.
            
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
             "You are an expert in analyzing technology use cases for post-conflict and humanitarian contexts. "
             "Based on the retrieved use cases and the user's query, analyze each use case for relevance, appropriateness, "
             "and potential application. Format the information into structured use case entries."},
            {"role": "user", "content": 
             f"Query: {query}\n\nRetrieved use cases:\n\n{context_text}\n\n"
             f"Analyze these use cases in relation to the query. For each use case, assess its relevance to the query "
             f"on a scale of 0-1, where 1 is highly relevant. Structure the information according to the provided model."}
        ]
        
        # Define the structure for multiple use cases
        class UseCaseList(BaseModel):
            use_cases: List[UseCase] = Field(description="List of analyzed use cases")
        
        # Query LLM for structured analysis
        result = self._query_llm(messages, response_model=UseCaseList)
        return result.use_cases

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

    def analyze_risks_and_benefits(self, use_case: UseCase, risks_results, benefits_results):
        """
        Analyzes retrieved risks and benefits to generate structured assessments.
        
        Args:
            use_case: The use case being analyzed.
            risks_results: Results from risks vector DB search.
            benefits_results: Results from benefits vector DB search.
            
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
        
        # Prepare prompt for risks analysis
        risk_messages = [
            {"role": "system", "content": 
             "You are an expert in risk assessment for technologies used in post-conflict and humanitarian contexts. "
             "Analyze the risks associated with the given use case based on the retrieved information."},
            {"role": "user", "content": 
             f"Use Case: {use_case.title}\n\nDescription: {use_case.description}\n\n"
             f"Retrieved risks:\n\n{risk_context}\n\n"
             f"Analyze these risks in relation to the use case. Assess severity and likelihood for each risk. "
             f"Structure your analysis according to the provided model."}
        ]
        
        # Prepare prompt for benefits analysis
        benefit_messages = [
            {"role": "system", "content": 
             "You are an expert in benefit assessment for technologies used in post-conflict and humanitarian contexts. "
             "Analyze the benefits associated with the given use case based on the retrieved information."},
            {"role": "user", "content": 
             f"Use Case: {use_case.title}\n\nDescription: {use_case.description}\n\n"
             f"Retrieved benefits:\n\n{benefit_context}\n\n"
             f"Analyze these benefits in relation to the use case. Assess impact for each benefit. "
             f"Structure your analysis according to the provided model."}
        ]
        
        # Define the structure for multiple risks and benefits
        class RiskList(BaseModel):
            risks: List[RiskModel] = Field(description="List of analyzed risks")
            
        class BenefitList(BaseModel):
            benefits: List[BenefitModel] = Field(description="List of analyzed benefits")
        
        # Query LLM for structured analysis
        risks = self._query_llm(risk_messages, response_model=RiskList).risks
        benefits = self._query_llm(benefit_messages, response_model=BenefitList).benefits
        
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

    def analyze_mitigations(self, risk: RiskModel, mitigations_results):
        """
        Analyzes retrieved mitigations to generate structured strategies.
        
        Args:
            risk: The risk being mitigated.
            mitigations_results: Results from mitigations vector DB search.
            
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
        
        # Prepare prompt for mitigation analysis
        messages = [
            {"role": "system", "content": 
             "You are an expert in developing mitigation strategies for risks in post-conflict and humanitarian technology use. "
             "Analyze the mitigations for the given risk based on the retrieved information."},
            {"role": "user", "content": 
             f"Risk: {risk.title}\n\nDescription: {risk.description}\n\n"
             f"Retrieved mitigations:\n\n{mitigation_context}\n\n"
             f"Analyze these mitigations in relation to the risk. Assess effectiveness and implementation difficulty for each. "
             f"Structure your analysis according to the provided model."}
        ]
        
        # Define the structure for multiple mitigations
        class MitigationList(BaseModel):
            mitigations: List[MitigationModel] = Field(description="List of analyzed mitigations")
        
        # Query LLM for structured analysis
        result = self._query_llm(messages, response_model=MitigationList)
        return result.mitigations

    def generate_report(self, query: str, use_cases: List[UseCase], use_case_analyses: List[Dict]):
        """
        Generates a final comprehensive report based on all analyses.
        
        Args:
            query: The original user query.
            use_cases: List of analyzed use cases.
            use_case_analyses: List of dictionaries containing risks, benefits, and mitigations for each use case.
            
        Returns:
            AnalysisReport object.
        """
        # Prepare context with all analyses
        context_items = []
        
        # Add use cases overview
        context_items.append("## Use Cases Overview")
        for uc in use_cases:
            context_items.append(f"- {uc.title} (Relevance: {uc.relevance_score})")
        
        # Add detailed analysis for each use case
        for i, uc in enumerate(use_cases):
            analysis = use_case_analyses[i]
            
            context_items.append(f"\n## Use Case: {uc.title}")
            context_items.append(f"Description: {uc.description}")
            context_items.append(f"Context: {uc.context}")
            
            # Risks
            context_items.append("\n### Risks")
            for risk in analysis["risks"]:
                context_items.append(f"- {risk.title} (Severity: {risk.severity}, Likelihood: {risk.likelihood})")
            
            # Benefits
            context_items.append("\n### Benefits")
            for benefit in analysis["benefits"]:
                context_items.append(f"- {benefit.title} (Impact: {benefit.impact})")
            
            # Mitigations (grouped by risk)
            context_items.append("\n### Mitigation Strategies")
            for risk_idx, risk in enumerate(analysis["risks"]):
                context_items.append(f"\nFor risk '{risk.title}':")
                if "mitigations" in analysis and risk_idx < len(analysis["mitigations"]):
                    for mitigation in analysis["mitigations"][risk_idx]:
                        context_items.append(f"- {mitigation.title} (Effectiveness: {mitigation.effectiveness}, "
                                           f"Implementation Difficulty: {mitigation.implementation_difficulty})")
                else:
                    context_items.append("- No specific mitigations found")
        
        context_text = "\n".join(context_items)
        
        # Prepare prompt for report generation
        messages = [
            {"role": "system", "content": 
            "You are an expert analyst specializing in humanitarian technology applications for post-conflict zones. "
            "Generate a comprehensive analysis report based on the provided information about use cases, risks, benefits, "
            "and mitigation strategies. The report should include an executive summary, analysis of each use case, "
            "and overall recommendations."},
            {"role": "user", "content": 
            f"Original Query: {query}\n\n"
            f"Analysis Information:\n\n{context_text}\n\n"
            f"Generate a comprehensive analysis report structured according to the provided model. "
            f"Include a concise executive summary, analysis of the use cases with their associated risks, benefits, "
            f"and mitigations in the 'analysis_by_use_case' field, overall recommendations, and any additional considerations or limitations."}
        ]
        
        # Query LLM for structured report
        report = self._query_llm(messages, response_model=AnalysisReport)
        return report

    def analyze(self, query: str, top_k_use_cases: int = 3, top_k_risks_benefits: int = 3, top_k_mitigations: int = 3):
        """
        Main pipeline function that executes the entire analysis process.
        
        Args:
            query: The user's query about a post-conflict challenge.
            top_k_use_cases: Number of use cases to retrieve.
            top_k_risks_benefits: Number of risks and benefits to retrieve for each use case.
            top_k_mitigations: Number of mitigations to retrieve for each risk.
            
        Returns:
            AnalysisReport object with the complete analysis.
        """
        print(f"Starting analysis for query: '{query}'")
        
        # Step 1: Retrieve relevant use cases
        print("Step 1: Retrieving relevant use cases...")
        use_case_results = self.retrieve_use_cases(query, top_k=top_k_use_cases)
        
        # Step 2: Analyze use cases with LLM
        print("Step 2: Analyzing use cases...")
        use_cases = self.analyze_use_cases(query, use_case_results)
        
        # Steps 3-7: For each use case, retrieve and analyze risks, benefits, and mitigations
        use_case_analyses = []
        for use_case in use_cases:
            print(f"Processing use case: {use_case.title}")
            
            # Step 3-4: Retrieve and analyze risks and benefits
            print("Retrieving risks and benefits...")
            risks_results, benefits_results = self.retrieve_risks_and_benefits(use_case, top_k=top_k_risks_benefits)
            
            print("Analyzing risks and benefits...")
            risks, benefits = self.analyze_risks_and_benefits(use_case, risks_results, benefits_results)
            
            # Steps 5-6: For each risk, retrieve and analyze mitigations
            all_mitigations = []
            for risk in risks:
                print(f"Processing risk: {risk.title}")
                
                print("Retrieving mitigations...")
                mitigations_results = self.retrieve_mitigations(risk, top_k=top_k_mitigations)
                
                print("Analyzing mitigations...")
                mitigations = self.analyze_mitigations(risk, mitigations_results)
                all_mitigations.append(mitigations)
            
            # Store analysis for this use case
            use_case_analyses.append({
                "risks": risks,
                "benefits": benefits,
                "mitigations": all_mitigations
            })
        
        # Step 8: Generate final report
        print("Step 8: Generating final analysis report...")
        report = self.generate_report(query, use_cases, use_case_analyses)

        return report


# Example usage
if __name__ == "__main__":
    analyzer = WarUseCaseAnalyzer()
    
    # Example query
    query = "lack of clean water in Sudan after conflict"
    
    # Run analysis
    report = analyzer.analyze(query)
    
    # Print report
    print("\n=== ANALYSIS REPORT ===\n")
    print(f"QUERY: {report.query}\n")
    print(f"SUMMARY: {report.summary}\n")
    print("USE CASES:")
    for uc in report.use_cases:
        print(f"- {uc.title} (Relevance: {uc.relevance_score})")

    print("\nANALYSIS BY USE CASE:")
    print(report.analysis_by_use_case)

    print("\nRECOMMENDATIONS:")
    print(report.recommendations)

    if report.considerations:
        print("\nADDITIONAL CONSIDERATIONS:")
        print(report.considerations)

    print("Analysis complete.")