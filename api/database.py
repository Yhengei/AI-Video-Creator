"""
数据库模型和连接
支持多用户系统
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

# 数据库配置
DATABASE_URL = "sqlite:///./pixelle_video.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UserRole(str, enum.Enum):
    """用户角色"""
    ADMIN = "admin"
    USER = "user"


class VideoStatus(str, enum.Enum):
    """视频状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    config = relationship("UserConfig", back_populates="user", uselist=False, cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="user", cascade="all, delete-orphan")


class UserConfig(Base):
    """用户配置表"""
    __tablename__ = "user_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # LLM 配置
    llm_api_key = Column(String(200))
    llm_base_url = Column(String(200))
    llm_model = Column(String(100))

    # ComfyUI 配置
    comfyui_url = Column(String(200))
    comfyui_api_key = Column(String(200))
    runninghub_api_key = Column(String(200))
    runninghub_instance_type = Column(String(100))

    # 默认工作流
    default_image_workflow = Column(String(200))
    default_video_workflow = Column(String(200))

    # 模板
    default_template = Column(String(200))

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="config")


class Video(Base):
    """视频记录表"""
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 视频信息
    title = Column(String(200), nullable=False)
    pipeline = Column(String(50), nullable=False)  # standard, asset_based, i2v, digital_human 等
    input_data = Column(Text)  # JSON 格式存储输入参数

    # 状态
    status = Column(SQLEnum(VideoStatus), default=VideoStatus.PENDING)
    output_path = Column(String(500))
    error_message = Column(Text)

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 关系
    user = relationship("User", back_populates="videos")


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)

    # 创建默认管理员账号
    from api.auth import get_password_hash

    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN
            )
            db.add(admin)
            db.commit()
            print("Default admin account created: admin / admin123")
    finally:
        db.close()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
