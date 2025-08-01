# app/schemas.py
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, Dict, Any
from datetime import date
import json

# Custom JSON serializer for date objects
def json_date_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# --- WheelSpecification Schemas ---
class WheelSpecificationFields(BaseModel):
    treadDiameterNew: str
    lastShopIssueSize: str
    condemningDia: str
    wheelGauge: str
    variationSameAxle: str
    variationSameBogie: str
    variationSameCoach: str
    wheelProfile: str
    intermediateWWP: str
    bearingSeatDiameter: str
    rollerBearingOuterDia: str
    rollerBearingBoreDia: str
    rollerBearingWidth: str
    axleBoxHousingBoreDia: str
    wheelDiscWidth: str
    additionalProp1: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"
        json_encoders = {
            date: json_date_serializer
        }

class WheelSpecificationCreate(BaseModel):
    formNumber: str = Field(..., example="WS-001")
    submittedBy: str = Field(..., example="Ajeet Kumar")
    submittedDate: date = Field(..., example="2025-07-25")
    fields: WheelSpecificationFields

class WheelSpecificationResponse(WheelSpecificationCreate):
    id: int = Field(..., example=1)
    status: str = Field(..., example="Saved")

    class Config:
        from_attributes = True
        json_encoders = {
            date: json_date_serializer
        }


# --- BogieChecksheet Schemas ---
class BogieChecksheetFields(BaseModel):
    bogieType: str = Field(..., example="EMU-TypeA")
    lastCheckDate: date = Field(..., example="2025-01-15")
    defectFound: str = Field(..., example="Minor crack on frame")
    repairedBy: str = Field(..., example="Team B")
    nextCheckDueDate: date = Field(..., example="2026-01-15")
    brakeSystemStatus: str = Field(..., example="OK")
    suspensionCondition: str = Field(..., example="Good")
    additionalNotes: Optional[str] = Field(None, example="No major issues noted.")
    additionalProp1: Optional[Dict[str, Any]] = None

    class Config:
        extra = "allow"
        json_encoders = {
            date: json_date_serializer
        }

class BogieChecksheetCreate(BaseModel):
    formNumber: str = Field(..., example="BCS-001")
    submittedBy: str = Field(..., example="Supervisor C")
    submittedDate: date = Field(..., example="2025-07-25")
    fields: BogieChecksheetFields

# New Schema for updating BogieChecksheet
# All fields are Optional, meaning they don't have to be provided for an update
class BogieChecksheetUpdate(BaseModel):
    submittedBy: Optional[str] = Field(None, example="Updated Supervisor C")
    submittedDate: Optional[date] = Field(None, example="2025-08-01")
    fields: Optional[BogieChecksheetFields] = None # Fields can also be updated
    status: Optional[str] = Field(None, example="Approved")

    class Config:
        extra = "allow" # Allow additional properties that are not explicitly defined
        json_encoders = {
            date: json_date_serializer
        }
        # Pydantic v2 needs this to allow dict for Optional[BaseModel]
        # This is important for 'fields: Optional[BogieChecksheetFields] = None'
        # to correctly parse a dictionary into the BogieChecksheetFields model
        # if a 'fields' dictionary is provided in the update payload.
        # However, for `Optional[BaseModel]`, Pydantic v2 often handles this automatically.
        # If you encounter issues, consider adding a custom validator for 'fields'.

class BogieChecksheetResponse(BogieChecksheetCreate):
    id: int = Field(..., example=1)
    status: str = Field(..., example="Saved")

    class Config:
        from_attributes = True
        json_encoders = {
            date: json_date_serializer
        }