# 欢迎页面

import streamlit as st
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="欢迎 - Pixelle Video 多用户版",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ========== 登录检查 ==========
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("请先登录")
    st.switch_page("web/Login.py")
    st.stop()

# ========== 用户信息显示 ==========
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    st.write(f"👤 {st.session_state.username}")
    if st.button("退出登录", key="logout_btn"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("web/Login.py")

# 获取背景图片的 base64
bg_image_path = Path(__file__).parent.parent / "assets" / "main_bg.jpg"

def get_base64_image(image_path):
    """读取图片并转换为 base64"""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_base64 = get_base64_image(bg_image_path)

# Custom CSS - 获嘉背景
st.markdown(f"""
<style>
    /* 全屏背景图片 */
    .stApp {{
        background: linear-gradient(rgba(10, 14, 39, 0.75), rgba(10, 14, 39, 0.85)),
                    url('data:image/jpeg;base64,{bg_base64}');
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}

    /* 确保背景图片铺满 */
    [data-testid="stAppViewContainer"] {{
        background: transparent !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* 动态网格叠加 */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            linear-gradient(rgba(14, 165, 233, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(14, 165, 233, 0.02) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }}

    @keyframes gridMove {{
        0% {{ transform: translate(0, 0); }}
        100% {{ transform: translate(50px, 50px); }}
    }}

    /* 标题动画 */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes glow {{
        0%, 100% {{ filter: drop-shadow(0 0 20px rgba(14, 165, 233, 0.5)); }}
        50% {{ filter: drop-shadow(0 0 40px rgba(14, 165, 233, 0.8)); }}
    }}

    /* 标题样式 */
    h1 {{
        font-size: 52px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-align: center !important;
        margin-bottom: 24px !important;
        animation: fadeInUp 0.8s ease !important;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
        letter-spacing: 2px;
    }}

    /* 副标题样式 */
    h2 {{
        font-size: 32px !important;
        font-weight: 700 !important;
        color: rgba(255, 255, 255, 0.95) !important;
        text-align: center !important;
        margin-bottom: 16px !important;
        animation: fadeInUp 1s ease !important;
        text-shadow: 0 2px 15px rgba(0, 0, 0, 0.5);
    }}

    /* 描述文字 */
    h3 {{
        font-size: 18px !important;
        color: rgba(255, 255, 255, 0.85) !important;
        text-align: center !important;
        margin-bottom: 48px !important;
        animation: fadeInUp 1.2s ease !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }}

    /* 特性卡片 - 毛玻璃效果 */
    .feature-card {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px) saturate(180%);
        -webkit-backdrop-filter: blur(15px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        padding: 32px;
        margin: 24px 0;
        text-align: center;
        transition: all 0.4s ease;
        cursor: pointer;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }}

    .feature-card:hover {{
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 255, 255, 0.4);
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.4);
    }}

    .feature-icon {{
        font-size: 48px;
        margin-bottom: 16px;
        transition: all 0.3s ease;
        filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.3));
    }}

    .feature-card:hover .feature-icon {{
        transform: scale(1.2);
    }}

    .feature-title {{
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }}

    .feature-desc {{
        font-size: 16px;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.6;
        text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
    }}

    /* 按钮样式 */
    .stButton > button {{
        background: rgba(14, 165, 233, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(14, 165, 233, 0.5) !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 32px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
    }}

    .stButton > button:hover {{
        background: rgba(14, 165, 233, 0.35) !important;
        border-color: rgba(14, 165, 233, 0.8) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(14, 165, 233, 0.5) !important;
    }}

    /* 分隔线 */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 48px 0;
    }}
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown("# 🎬 Pixelle Video 多用户版")
st.markdown("### AI 驱动的智能视频生成平台")
st.markdown("---")

# 特性展示
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">智能生成</div>
        <div class="feature-desc">
            基于 AI 的视频内容生成<br>
            支持多种生成模式<br>
            一键创作精彩视频
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👥</div>
        <div class="feature-title">多用户管理</div>
        <div class="feature-desc">
            独立的用户账号系统<br>
            数据完全隔离<br>
            权限精细控制
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">高效工作流</div>
        <div class="feature-desc">
            快速配置和部署<br>
            自动化处理流程<br>
            提升创作效率
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 快速开始
st.markdown("## 🚀 快速开始")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📝 配置 API
    前往 **⚙️ 配置** 页面设置：
    - OpenAI API Key
    - ComfyUI 服务地址
    - 其他服务配置
    """)
    if st.button("前往配置 →", key="goto_config"):
        st.switch_page("pages/1_⚙️_Config.py")

with col2:
    st.markdown("""
    ### 🎬 生成视频
    前往 **🎬 Generate** 页面：
    - 标准生成模式
    - 资产导入模式
    - 图生视频模式
    - 数字人模式
    """)
    if st.button("开始生成 →", key="goto_generate"):
        st.switch_page("pages/2_🎬_Generate.py")

st.markdown("---")

# 页脚
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.6); padding: 20px;">
    <p>Pixelle Video Multi-User v2.0.0</p>
    <p>技术支持：微信 19149253810</p>
</div>
""", unsafe_allow_html=True)
