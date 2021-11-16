from typing import Text, List
import pydantic

class CandidateData(pydantic.BaseModel):
    skills: float
    tools: List[Text]
