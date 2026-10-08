from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Pergunta sobre os dados",
    )
