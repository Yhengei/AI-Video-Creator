# 配置页面

import sys
from pathlib import Path

# Add project root to sys.path
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st
from web.state.session import init_session_state
from web.components.settings import render_advanced_settings
from pixelle_video.config import config_manager

# Page config
st.set_page_config(
    page_title="配置 - 获嘉商户AI视频",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
    /* 科技风背景 */
    .stApp {
        background: #0a0e27;
    }

    /* 动态网格背景 */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            linear-gradient(rgba(14, 165, 233, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(14, 165, 233, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
        pointer-events: none;
    }

    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }

    .config-header {
        text-align: center;
        padding: 40px 20px 20px;
    }

    .config-title {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, #0ea5e9, #14b8a6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }

    .config-subtitle {
        font-size: 16px;
        color: rgba(148, 163, 184, 0.9);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #14b8a6 100%);
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
        padding: 16px 48px;
        border: none;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(14, 165, 233, 0.5);
    }

    /* 容器样式 */
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(14, 165, 233, 0.3);
        border-radius: 12px;
    }

    /* 文字颜色优化 */
    label, .stMarkdown, .stCaption, p {
        color: rgba(226, 232, 240, 0.95) !important;
    }

    /* 输入框样式 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(14, 165, 233, 0.3) !important;
        color: rgba(226, 232, 240, 0.95) !important;
        border-radius: 8px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3) !important;
    }

    /* 标签和帮助文本 */
    .stTextInput > label, .stSelectbox > label {
        color: rgba(226, 232, 240, 0.95) !important;
        font-weight: 500 !important;
    }

    /* help文本 */
    .stTextInput small, .stSelectbox small {
        color: rgba(148, 163, 184, 0.9) !important;
    }

    /* 成功/警告/错误提示 */
    .stSuccess, .stWarning, .stError {
        background: rgba(15, 23, 42, 0.9) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session
init_session_state()

# Header
st.markdown("""
<div class="config-header">
    <div class="config-title">⚙️ 系统配置</div>
    <div class="config-subtitle">配置AI服务，开启智能视频生成之旅</div>
</div>
""", unsafe_allow_html=True)

# Render settings
render_advanced_settings()

# Bottom buttons
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Check if configured
    is_configured = config_manager.validate()

    if is_configured:
        if st.button("✅ 保存并继续", use_container_width=True):
            st.success("✅ 配置已保存！")
            st.session_state.page = "generate"
            st.switch_page("pages/2_🎬_Generate.py")
    else:
        st.warning("⚠️ 请完成必要的配置项后继续")
        st.button("保存并继续", use_container_width=True, disabled=True)
