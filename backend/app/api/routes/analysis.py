
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.repository import Repository
from app.models.analysis import Analysis

router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


@router.post("/{repository_id}/start")
def start_analysis(
    repository_id: int,
    db: Session = Depends(get_db)
):
    # Check whether repository exists
    repository = db.query(Repository).filter(
        Repository.id == repository_id
    ).first()

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    # Create a new analysis record
    analysis = Analysis(
        repository_id=repository_id,
        status="pending",
        analysis_type="full"
    )

    try:
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "message": "Analysis job created successfully",
            "analysis_id": analysis.id,
            "repository_id": analysis.repository_id,
            "status": analysis.status,
            "analysis_type": analysis.analysis_type
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not create analysis job"
        )


@router.get("/{analysis_id}/status")
def get_analysis_status(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return {
        "analysis_id": analysis.id,
        "repository_id": analysis.repository_id,
        "status": analysis.status,
        "analysis_type": analysis.analysis_type,
        "summary": analysis.summary,
        "created_at": analysis.created_at,
        "started_at": analysis.started_at,
        "completed_at": analysis.completed_at
    }


@router.get("/{analysis_id}/report")
def get_analysis_report(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id
    ).first()

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    repository = db.query(Repository).filter(
        Repository.id == analysis.repository_id
    ).first()

    return {
        "analysis_id": analysis.id,
        "repository": {
            "id": repository.id,
            "name": repository.name,
            "source_type": repository.source_type
        },
        "analysis": {
            "status": analysis.status,
            "analysis_type": analysis.analysis_type,
            "summary": analysis.summary,
            "created_at": analysis.created_at,
            "started_at": analysis.started_at,
            "completed_at": analysis.completed_at
        },
        "findings": {
            "code_quality": [],
            "security": [],
            "technical_debt": []
        },
        "message": "Detailed findings will be available after analysis processing is integrated."
    }
