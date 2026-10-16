@echo off
chcp 65001 >nul
echo ========================================
echo   Pixelle-Video 多用户版 - 启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 启动后端 API...
start "Pixelle-Video API" cmd /k "python api/app.py"
timeout /t 3 >nul

echo [2/2] 启动 Web 界面...
start "Pixelle-Video Web" cmd /k "streamlit run web/Login.py"

echo.
echo ✅ 服务启动中...
echo.
echo 后端 API: http://localhost:8000
echo Web 界面: http://localhost:8501
echo.
echo 默认管理员账号：
echo   用户名: admin
echo   密码: admin123
echo.
echo 按任意键关闭此窗口...
pause >nul
