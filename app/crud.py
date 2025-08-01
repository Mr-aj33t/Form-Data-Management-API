# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from datetime import date
from fastapi import HTTPException, status

from . import models, schemas

# --- Existing WheelSpecification CRUD ---
def create_wheel_specification(db: Session, spec: schemas.WheelSpecificationCreate):
    db_spec = models.WheelSpecification(
        formNumber=spec.formNumber,
        submittedBy=spec.submittedBy,
        submittedDate=spec.submittedDate,
        fields=spec.fields.model_dump(mode='json'),
        status="Saved"
    )
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

def get_wheel_specifications(
    db: Session,
    form_number: Optional[str] = None,
    submitted_by: Optional[str] = None,
    submitted_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.WheelSpecification]:
    query = select(models.WheelSpecification)

    if form_number:
        query = query.where(models.WheelSpecification.formNumber == form_number)
    if submitted_by:
        query = query.where(models.WheelSpecification.submittedBy == submitted_by)
    if submitted_date:
        query = query.where(models.WheelSpecification.submittedDate == submitted_date)

    query = query.offset(skip).limit(limit)
    return db.execute(query).scalars().all()


# --- BogieChecksheet CRUD Operations ---

def create_bogie_checksheet(db: Session, checksheet: schemas.BogieChecksheetCreate):
    # Check if a BogieChecksheet with the same formNumber already exists
    existing_checksheet = db.query(models.BogieChecksheet).filter(
        models.BogieChecksheet.formNumber == checksheet.formNumber
    ).first()

    if existing_checksheet:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bogie Checksheet with this form number already exists"
        )

    fields_to_save = checksheet.fields.model_dump(mode='json')

    db_checksheet = models.BogieChecksheet(
        formNumber=checksheet.formNumber,
        submittedBy=checksheet.submittedBy,
        submittedDate=checksheet.submittedDate,
        fields=fields_to_save,
        status="Saved"
    )
    db.add(db_checksheet)
    db.commit()
    db.refresh(db_checksheet)
    return db_checksheet

# NEW: Get BogieChecksheet by ID
def get_bogie_checksheet_by_id(db: Session, checksheet_id: int):
    return db.query(models.BogieChecksheet).filter(models.BogieChecksheet.id == checksheet_id).first()

# UPDATED: Update BogieChecksheet
def update_bogie_checksheet(db: Session, checksheet_id: int, checksheet_update: schemas.BogieChecksheetUpdate):
    db_checksheet = db.query(models.BogieChecksheet).filter(models.BogieChecksheet.id == checksheet_id).first()
    if db_checksheet is None:
        return None # Indicate not found

    # Pydantic model_dump(exclude_unset=True) will give a dictionary with only provided fields
    update_data = checksheet_update.model_dump(exclude_unset=True)
    
    # Handle 'fields' separately because it's a JSONB column and needs special serialization if updated
    if "fields" in update_data and update_data["fields"] is not None:
        # Get the fields from the update request, ensuring dates are serialized
        # Use a new Pydantic model instance for the incoming fields to leverage json_encoders
        # This re-validates and serializes the incoming 'fields' data
        incoming_fields_model = schemas.BogieChecksheetFields(**update_data["fields"])
        incoming_fields_serialized = incoming_fields_model.model_dump(mode='json') # THIS IS THE KEY FIX

        # Merge with existing fields.
        # Note: This performs a shallow merge. If you need deep merging of nested dicts within 'fields',
        # you'd need a more complex recursive merge function.
        existing_fields = db_checksheet.fields.copy() if db_checksheet.fields else {}
        existing_fields.update(incoming_fields_serialized)
        db_checksheet.fields = existing_fields # Assign the merged, serialized fields

        update_data.pop("fields") # Remove 'fields' from update_data as it's handled manually

    # Apply other top-level updates (submittedBy, submittedDate, status)
    for key, value in update_data.items():
        # Handle submittedDate if it's being updated, ensure it's a date object
        # (model_dump(mode='json') handles serializing date to str on output,
        # but here we're setting an attribute which expects a date object)
        if key == "submittedDate" and isinstance(value, str):
            setattr(db_checksheet, key, date.fromisoformat(value))
        else:
            setattr(db_checksheet, key, value)

    db.add(db_checksheet)
    db.commit()
    db.refresh(db_checksheet)
    return db_checksheet

# NEW: Delete BogieChecksheet
def delete_bogie_checksheet(db: Session, checksheet_id: int):
    db_checksheet = db.query(models.BogieChecksheet).filter(models.BogieChecksheet.id == checksheet_id).first()
    if db_checksheet:
        db.delete(db_checksheet)
        db.commit()
        return True # Indicate successful deletion
    return False # Indicate not found


def get_bogie_checksheets(
    db: Session,
    form_number: Optional[str] = None,
    submitted_by: Optional[str] = None,
    submitted_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.BogieChecksheet]:
    query = select(models.BogieChecksheet)

    if form_number:
        query = query.where(models.BogieChecksheet.formNumber == form_number)
    if submitted_by:
        query = query.where(models.BogieChecksheet.submittedBy == submitted_by)
    if submitted_date:
        query = query.where(models.BogieChecksheet.submittedDate == submitted_date)

    query = query.offset(skip).limit(limit)
    return db.execute(query).scalars().all()