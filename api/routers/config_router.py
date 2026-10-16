"""
用户配置管理路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from api.database import get_db, User, UserConfig
from api.auth import get_current_user

router = APIRouter(prefix="/config", tags=["配置"])


# ========== Schemas ==========
class UserConfigResponse(BaseModel):
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_model: Optional[str] = None
    comfyui_url: Optional[str] = None
    comfyui_api_key: Optional[str] = None
    runninghub_api_key: Optional[str] = None
    runninghub_instance_type: Optional[str] = None
    default_image_workflow: Optional[str] = None
    default_video_workflow: Optional[str] = None
    default_template: Optional[str] = None

    class Config:
        from_attributes = True


class UserConfigUpdate(BaseModel):
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_model: Optional[str] = None
    comfyui_url: Optional[str] = None
    comfyui_api_key: Optional[str] = None
    runninghub_api_key: Optional[str] = None
    runninghub_instance_type: Optional[str] = None
    default_image_workflow: Optional[str] = None
    default_video_workflow: Optional[str] = None
    default_template: Optional[str] = None


# ========== Routes ==========
@router.get("/", response_model=UserConfigResponse)
async def get_user_config(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户配置"""
    config = db.query(UserConfig).filter(UserConfig.user_id == current_user.id).first()

    if not config:
        # 如果配置不存在，创建默认配置
        config = UserConfig(user_id=current_user.id)
        db.add(config)
        db.commit()
        db.refresh(config)

    return config


@router.put("/", response_model=UserConfigResponse)
async def update_user_config(
    update: UserConfigUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户配置"""
    config = db.query(UserConfig).filter(UserConfig.user_id == current_user.id).first()

    if not config:
        config = UserConfig(user_id=current_user.id)
        db.add(config)

    # 更新字段
    for field, value in update.dict(exclude_unset=True).items():
        setattr(config, field, value)

    db.commit()
    db.refresh(config)

    return config
