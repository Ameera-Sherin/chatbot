from pydantic import BaseModel
from typing import List

class BasicDetails(BaseModel):
    name: str
    age: float
    
class EducationDetail(BaseModel):
    grade: float
    institution: str
    start_date: str
    end_date: str
    duration: float

class EductionDetails(BaseModel):
    educationDetails: List[EducationDetail]
    
class WorkDetail(BaseModel):
    post: str
    company: str
    start_date: str
    end_sate: str
    duration: float

class WorkDetails(BaseModel):
    workDetails: List[WorkDetail]
    
class FamilyDetails(BaseModel):
    fathers_name: str
    mothers_namee: str
    spouse_name: str
    
class ProfileDetails(BaseModel):
    basicDetails: BasicDetails
    educationDetails: EductionDetails
    workDetails: WorkDetails
    familyDetails: FamilyDetails