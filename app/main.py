# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from . import models, schemas, crud
from .database import engine, get_db

# Create database tables (This will create all tables defined in models.Base)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPA Form Data API",
    description="API for managing KPA form data, including wheel specifications and bogie checksheets.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the KPA Backend! Access docs at /docs"}

# --- Wheel Specification Endpoints ---
@app.post(
    "/api/forms/wheel-specifications/",
    response_model=schemas.WheelSpecificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Wheel Specification entry"
)
def create_wheel_specification(spec: schemas.WheelSpecificationCreate, db: Session = Depends(get_db)):
    db_spec = crud.create_wheel_specification(db=db, spec=spec)
    return db_spec

@app.get(
    "/api/forms/wheel-specifications/",
    response_model=List[schemas.WheelSpecificationResponse],
    summary="Read Wheel Specification entries with optional filters"
)
def read_wheel_specifications(
    formNumber: Optional[str] = Query(None, description="Filter by form number"),
    submittedBy: Optional[str] = Query(None, description="Filter by submitted by user"),
    submittedDate: Optional[date] = Query(None, description="Filter by submission date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Skip a number of items (for pagination)"),
    limit: int = Query(100, ge=1, le=100, description="Limit the number of items returned (for pagination)"),
    db: Session = Depends(get_db)
):
    specs = crud.get_wheel_specifications(
        db,
        form_number=formNumber,
        submitted_by=submittedBy,
        submitted_date=submittedDate,
        skip=skip,
        limit=limit
    )
    return specs


# --- Bogie Checksheet Endpoints ---
@app.post(
    "/api/forms/bogie-checksheet/",
    response_model=schemas.BogieChecksheetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Bogie Checksheet entry"
)
def create_bogie_checksheet(checksheet: schemas.BogieChecksheetCreate, db: Session = Depends(get_db)):
    db_checksheet = crud.create_bogie_checksheet(db=db, checksheet=checksheet)
    return db_checksheet

@app.get(
    "/api/forms/bogie-checksheet/",
    response_model=List[schemas.BogieChecksheetResponse],
    summary="Read Bogie Checksheet entries with optional filters"
)
def read_bogie_checksheets(
    formNumber: Optional[str] = Query(None, description="Filter by form number"),
    submittedBy: Optional[str] = Query(None, description="Filter by submitted by user"),
    submittedDate: Optional[date] = Query(None, description="Filter by submission date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Skip a number of items (for pagination)"),
    limit: int = Query(100, ge=1, le=100, description="Limit the number of items returned (for pagination)"),
    db: Session = Depends(get_db)
):
    checksheets = crud.get_bogie_checksheets(
        db,
        form_number=formNumber,
        submitted_by=submittedBy,
        submitted_date=submittedDate,
        skip=skip,
        limit=limit
    )
    return checksheets

# NEW: Get Bogie Checksheet by ID
@app.get(
    "/api/forms/bogie-checksheet/{checksheet_id}",
    response_model=schemas.BogieChecksheetResponse,
    summary="Read a single Bogie Checksheet entry by ID"
)
def read_bogie_checksheet_by_id(checksheet_id: int, db: Session = Depends(get_db)):
    db_checksheet = crud.get_bogie_checksheet_by_id(db, checksheet_id=checksheet_id)
    if db_checksheet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bogie Checksheet not found")
    return db_checksheet

# UPDATED: Update Bogie Checksheet by ID
@app.put(
    "/api/forms/bogie-checksheet/{checksheet_id}",
    response_model=schemas.BogieChecksheetResponse,
    summary="Update an existing Bogie Checksheet entry by ID"
)
def update_bogie_checksheet(
    checksheet_id: int,
    checksheet_update: schemas.BogieChecksheetUpdate,
    db: Session = Depends(get_db)
):
    updated_checksheet = crud.update_bogie_checksheet(db, checksheet_id, checksheet_update)
    if updated_checksheet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bogie Checksheet not found")
    return updated_checksheet

# NEW: Delete Bogie Checksheet by ID
@app.delete(
    "/api/forms/bogie-checksheet/{checksheet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Bogie Checksheet entry by ID"
)
def delete_bogie_checksheet(checksheet_id: int, db: Session = Depends(get_db)):
    success = crud.delete_bogie_checksheet(db, checksheet_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bogie Checksheet not found")
    # FastAPI automatically returns 204 No Content for empty returns from delete
    return