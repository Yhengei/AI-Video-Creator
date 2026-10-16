# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Home Page - Main video generation interface
"""

import sys
from pathlib import Path

# Add project root to sys.path
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st

# Import state management
from web.state.session import init_session_state, init_i18n, get_pixelle_video

# Import components
from web.components.header import render_header

# Page config
st.set_page_config(
    page_title="生成视频 - 获嘉商户AI视频",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main():
    """Main UI entry point"""
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

        .generate-header {
            text-align: center;
            padding: 20px;
        }

        .generate-title {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, #0ea5e9, #14b8a6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* 按钮样式 */
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9 0%, #14b8a6 100%);
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(14, 165, 233, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(14, 165, 233, 0.5);
        }

        /* 侧边栏样式 */
        section[data-testid="stSidebar"] {
            background: rgba(10, 14, 39, 0.95);
            border-right: 1px solid rgba(14, 165, 233, 0.3);
        }

        /* 文字颜色优化 */
        label, .stMarkdown, .stCaption, p, span {
            color: rgba(226, 232, 240, 0.95) !important;
        }

        /* 输入框样式 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input {
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(14, 165, 233, 0.3) !important;
            color: rgba(226, 232, 240, 0.95) !important;
            border-radius: 8px;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #0ea5e9 !important;
            box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3) !important;
        }

        /* help文本 */
        .stTextInput small, .stSelectbox small, .stTextArea small {
            color: rgba(148, 163, 184, 0.9) !important;
        }

        /* Tabs样式 */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(15, 23, 42, 0.8);
            border-radius: 12px;
            padding: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            color: rgba(148, 163, 184, 0.9) !important;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0ea5e9, #14b8a6) !important;
            color: #ffffff !important;
            border-radius: 8px;
        }

        /* 容器样式 */
        div[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 12px;
        }

        /* 上传组件 */
        .stFileUploader {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 2px dashed rgba(14, 165, 233, 0.4) !important;
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state and i18n
    init_session_state()
    init_i18n()

    # Header with config button
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("⚙️ 配置"):
            st.switch_page("pages/1_⚙️_Config.py")

    with col2:
        st.markdown("""
        <div class="generate-header">
            <div class="generate-title">🎬 视频生成</div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar contact info
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px;">
            <div style="background: linear-gradient(135deg, rgba(14, 165, 233, 0.15), rgba(20, 184, 166, 0.15)); border: 2px solid rgba(14, 165, 233, 0.4); border-radius: 12px; padding: 16px; text-align: center;">
                <div style="color: rgba(226, 232, 240, 0.95); font-size: 14px; margin-bottom: 8px;">需要帮助？添加微信</div>
                <div style="color: #0ea5e9; font-size: 20px; font-weight: 700;">19149253810</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Initialize Pixelle-Video
    pixelle_video = get_pixelle_video()
    
    # ========================================================================
    # Pipeline Selection & Delegation
    # ========================================================================
    from web.pipelines import get_all_pipeline_uis
    
    # Get all registered pipelines
    pipelines = get_all_pipeline_uis()
    
    # Use Tabs for pipeline selection
    # Note: st.tabs returns a list of containers, one for each tab
    tab_labels = [f"{p.icon} {p.display_name}" for p in pipelines]
    tabs = st.tabs(tab_labels)
    
    # Render each pipeline in its corresponding tab
    for i, pipeline in enumerate(pipelines):
        with tabs[i]:
            # Show description if available
            if pipeline.description:
                st.caption(pipeline.description)
            
            # Delegate rendering
            pipeline.render(pixelle_video)


if __name__ == "__main__":
    main()

