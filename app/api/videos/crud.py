import datetime
import uuid
from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.api.models import Video
from app.api.schemas import VideoSchema


def get_video(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    order_by: Optional[str] = None,
    search: Optional[str] = None,
):
    if skip < 0:
        skip = 0

    query = db.query(Video)
    if search:
        search = f"%{search}%"
        query = query.filter(or_(Video.name.ilike(search)))

    if order_by == "descend":
        query = query.order_by(Video.name.desc())
    elif order_by == "ascend":
        query = query.order_by(Video.name.asc())
    else:
        query = query.order_by(Video.created_at.desc())

    return query.offset(skip * limit).limit(limit).all()


def count_videos(db: Session):
    return db.query(func.count(Video.id)).scalar()


def get_video_by_id(db: Session, video_id: uuid.UUID):
    return db.query(Video).filter(Video.id == video_id).first()


def create_video(db: Session, video: VideoSchema):
    _video = Video(
        name=video.name,
        video_url=video.video_url,
        created_at=datetime.datetime.now(),
    )
    db.add(_video)
    db.commit()
    db.refresh(_video)
    return _video


def delete_video(db: Session, video_id: uuid.UUID):
    db.query(Video).filter(Video.id == video_id).delete()
    db.commit()


def update_video(db: Session, video: VideoSchema, video_id: uuid.UUID):
    _video = get_video_by_id(db=db, video_id=video_id)
    _video.name = video.name
    _video.video_url = video.video_url
    _video.updated_at = datetime.datetime.now()
    db.commit()
    db.refresh(_video)
    return _video
