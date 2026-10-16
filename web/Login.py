"""
登录页面
多用户系统入口
"""
import streamlit as st
import requests
import base64
from pathlib import Path

# API 配置
API_BASE = "http://localhost:8001/api"


def get_base64_image(image_path):
    """读取图片并转换为 base64"""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def login_page():
    """登录页面"""
    st.set_page_config(
        page_title="登录 - Pixelle Video 多用户版",
        page_icon="🎬",
        layout="centered",
    )

    # 获取背景图片的 base64
    bg_image_path = Path(__file__).parent / "assets" / "login_bg.jpg"
    bg_base64 = get_base64_image(bg_image_path)

    # 自定义样式 - 武王雕像背景
    st.markdown(f"""
    <style>
        /* 全屏背景图片 */
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.5)),
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

        /* 毛玻璃效果登录框 */
        .login-container {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 60px 50px;
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.6),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            max-width: 450px;
            margin: 100px auto;
            animation: fadeInUp 0.8s ease-out;
        }}

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

        .login-title {{
            text-align: center;
            font-size: 36px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            text-shadow: 0 2px 20px rgba(0, 0, 0, 0.5);
            letter-spacing: 2px;
        }}

        .login-subtitle {{
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            font-size: 15px;
            margin-bottom: 40px;
            text-shadow: 0 1px 10px rgba(0, 0, 0, 0.4);
            letter-spacing: 1px;
        }}

        .login-icon {{
            text-align: center;
            font-size: 70px;
            margin-bottom: 25px;
            filter: drop-shadow(0 4px 15px rgba(0, 0, 0, 0.5));
        }}

        /* 输入框样式优化 */
        .stTextInput > div > div > input {{
            background: rgba(255, 255, 255, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            font-size: 15px !important;
            color: #333 !important;
            transition: all 0.3s ease !important;
        }}

        .stTextInput > div > div > input:focus {{
            background: rgba(255, 255, 255, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 4px 20px rgba(255, 255, 255, 0.2) !important;
        }}

        .stTextInput > label {{
            color: rgba(255, 255, 255, 0.95) !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            text-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
        }}

        /* 按钮样式 */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            width: 100% !important;
            margin-top: 15px !important;
            box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4) !important;
            transition: all 0.3s ease !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 35px rgba(102, 126, 234, 0.6) !important;
        }}

        /* 提示文字样式 */
        .caption {{
            color: rgba(255, 255, 255, 0.8) !important;
            text-align: center !important;
            font-size: 13px !important;
            text-shadow: 0 1px 5px rgba(0, 0, 0, 0.4);
        }}

        /* 错误/成功消息 */
        .stAlert {{
            background: rgba(255, 255, 255, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: white !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    # 登录表单
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="login-icon">🎬</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Pixelle Video</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">多用户视频生成平台</div>', unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            submit = st.form_submit_button("🔐 登录", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("请输入用户名和密码")
                else:
                    # 调用登录 API
                    try:
                        response = requests.post(
                            f"{API_BASE}/auth/login",
                            json={"username": username, "password": password}
                        )

                        if response.status_code == 200:
                            data = response.json()
                            # 保存登录信息到 session_state
                            st.session_state.logged_in = True
                            st.session_state.token = data["access_token"]
                            st.session_state.user_id = data["user_id"]
                            st.session_state.username = data["username"]
                            st.session_state.role = data["role"]

                            st.success(f"欢迎回来，{username}！")
                            st.rerun()
                        else:
                            error_data = response.json()
                            st.error(error_data.get("detail", "登录失败"))
                    except Exception as e:
                        st.error(f"连接服务器失败：{str(e)}")

        st.markdown("---")
        st.caption("默认管理员账号：admin / admin123")
        st.caption("需要帮助？联系微信：19149253810")


def main():
    """主入口"""
    # 检查是否已登录
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        # 已登录，跳转到主页
        st.switch_page("pages/0_🏠_Welcome.py")
    else:
        # 未登录，显示登录页
        login_page()


if __name__ == "__main__":
    main()
