
import os
import uuid
import zipfile

from pathlib import Path, PurePosixPath

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.models.repository import Repository


router = APIRouter(prefix="/api/repositories", tags=["Repositories"])

UPLOAD_DIR = Path("uploads")
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_EXTRACTED_SIZE = 200 * 1024 * 1024  # 200 MB
MAX_ZIP_FILES = 5000


@router.post("/upload")
async def upload_repository(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are allowed"
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    saved_path = UPLOAD_DIR / f"{uuid.uuid4().hex}.zip"

    total_size = 0

    try:
        with saved_path.open("wb") as destination:
            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_UPLOAD_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="ZIP file exceeds the 50 MB upload limit"
                    )

                destination.write(chunk)

        if not zipfile.is_zipfile(saved_path):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid ZIP archive"
            )

        with zipfile.ZipFile(saved_path) as archive:
            members = archive.infolist()

            if len(members) > MAX_ZIP_FILES:
                raise HTTPException(
                    status_code=400,
                    detail="ZIP archive contains too many files"
                )

            extracted_size = 0

            for member in members:
                member_path = PurePosixPath(member.filename)

                if (
                    member_path.is_absolute()
                    or ".." in member_path.parts
                    or "\\" in member.filename
                    or ":" in member.filename
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="ZIP archive contains an unsafe file path"
                    )

                extracted_size += member.file_size

                if extracted_size > MAX_EXTRACTED_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail="ZIP archive expands beyond the allowed size"
                    )

        original_name = Path(file.filename).stem[:255] or "repository"

        repository = Repository(
            name=original_name,
            source_type="upload",
            local_path=str(saved_path),
            status="uploaded"
        )

        db.add(repository)
        db.commit()
        db.refresh(repository)

        return {
            "message": "Repository uploaded successfully",
            "repository_id": repository.id,
            "name": repository.name,
            "status": repository.status
        }

    except HTTPException:
        if saved_path.exists():
            saved_path.unlink()
        raise

    except Exception:
        db.rollback()

        if saved_path.exists():
            saved_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Repository upload failed"
        )

    finally:
        await file.close()

@router.get("/")
def get_repositories(db: Session = Depends(get_db)):
    repositories = db.query(Repository).order_by(
        Repository.created_at.desc()
    ).all()

    return [
        {
            "id": repo.id,
            "name": repo.name,
            "source_type": repo.source_type,
            "source_url": repo.source_url,
            "status": repo.status,
            "created_at": repo.created_at
        }
        for repo in repositories
    ]


@router.get("/{repository_id}")
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db)
):
    repository = db.query(Repository).filter(
        Repository.id == repository_id
    ).first()

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    return {
        "id": repository.id,
        "name": repository.name,
        "source_type": repository.source_type,
        "source_url": repository.source_url,
        "status": repository.status,
        "created_at": repository.created_at
    }
