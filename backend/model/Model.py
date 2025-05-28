from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

# Define Pydantic models for structured data
class UseCase(BaseModel):
    title: str = Field(description="Title of the use case")
    description: str = Field(description="Detailed description of the use case")
    context: str = Field(description="Context where the use case applies")
    relevance_score: float = Field(description="Relevance score to the query (0-1)")
    source: str = Field(description="Source of the use case information")
    steps_to_implementation: Optional[List[str]] = Field(description="List of steps to implement the use case. Be realistic and practical. ")

class RiskModel(BaseModel):
    title: str = Field(description="Title of the risk")
    description: str = Field(description="Detailed description of the risk")
    context: Optional[str] = Field(description="Context where this risk applies")
    source: str = Field(description="Source of the risk information, from the retrived file. Write th name of paper if possible")

class MitigationModel(BaseModel):
    title: str = Field(description="Title of the mitigation strategy")
    description: str = Field(description="Detailed description of the mitigation strategy")
    context: Optional[str] = Field(description="Context where this mitigation applies")
    source: str = Field(description="Source of the mitigation information, from the retrived file. Write th name of paper if possible")

class BenefitModel(BaseModel):
    title: str = Field(description="Title of the benefit")
    description: str = Field(description="Detailed description of the benefit")
    context: Optional[str] = Field(description="Context where this benefit applies")
    source: str = Field(description="Source of the benefit information, from the retrived file. Write the name of paper if possible")

class RiskMitigationCard(BaseModel):
    risk_title: str = Field(description="Title of the risk")
    risk_description: str = Field(description="Description of the risk")
    risk_source: Optional[str] = Field(description="Source of the risk information, from the retrived file. Write the name of paper if possible")
    risk_context: Optional[str] = Field(description="Context where this risk applies")
    mitigation_title: str = Field(description="Title of the mitigation")
    mitigation_source: Optional[str] = Field(description="Source of the mitigation information, from the retrived file. Write the name of paper if possible")
    mitigation_context: Optional[str] = Field(description="Context where this mitigation applies")
    mitigation_description: str = Field(description="Description of the mitigation")

class UseCaseCard(BaseModel):
    title: str = Field(description="Title of the use case")
    description: str = Field(description="Description of the use case")
    context: str = Field(description="Context where the use case applies")
    source: Optional[str] = Field(description="Source of the use case information")
    risks_mitigations: List[RiskMitigationCard] = Field(description="List of risks and their mitigations")
    benefits: List[Dict[str, str]] = Field(
        description="List of benefits with title, description, context, and source"
    )
    relevance_score: float = Field(description="Relevance score to the query (0-1)")
    steps_to_implementation: Optional[List[str]] = Field(description="List of steps to implement the use case. Be realistic and practical. ")
    
class CardResponse(BaseModel):
    query: str = Field(description="Original query that initiated the analysis")
    cards: List[UseCaseCard] = Field(description="List of use case cards with risks, mitigations, and benefits")


class UseCaseList(BaseModel):
    use_cases: List[UseCase] = Field(description="List of generated use cases")
    
class MitigationList(BaseModel):
    mitigations: List[MitigationModel] = Field(description="List of generated mitigations")
