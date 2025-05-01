from pydantic import BaseModel, Field

class UseCase(BaseModel):
    title: str = Field(description="Title of the use case")
    description: str = Field(description="Description of the use case")

class RiskModel(BaseModel):
    description: str = Field(description="Description of the risk")

class MitigationModel(BaseModel):
    description: str = Field(description="Description of the mitigation strategy")

class BenefitModel(BaseModel):
    description: str = Field(description="Description of the benefit")

class RiskBenefitsMitigation(BaseModel):
    usecase_title: str = Field(description="Title of the use case")
    risks: List[RiskModel] = Field(description="Risk and mitigation associated with the use case")
    mitigation: List[MitigationModel] = Field(description="Mitigation strategy associated with the use case")
    benefits: List[BenefitModel] = Field(description="Benefit associated with the use case")
