# Pixelle-Video 多用户版

基于 Pixelle-Video-simple 改造的多用户版本，保留所有原有功能，添加用户认证和数据隔离。

## 🎯 新增功能

### 多用户支持
- ✅ 用户登录/认证系统
- ✅ 用户角色管理（管理员/普通用户）
- ✅ 用户数据隔离
- ✅ 独立的用户配置

### 管理功能
- ✅ 管理员可创建/删除用户
- ✅ 用户统计和管理
- ✅ 系统监控

### 保留的所有功能
- ✅ 标准视频生成
- ✅ 资产导入生成
- ✅ 图生视频（I2V）
- ✅ 数字人视频
- ✅ 动作迁移
- ✅ API 工作流
- ✅ 历史记录管理
- ✅ 高级配置

## 🚀 快速开始

### 1. 启动后端 API
```bash
cd "D:\ai ZHINENGTI\Pixelle-Video-Multi"
python api/app.py
```

或者使用 uv：
```bash
uv run python api/app.py
```

后端将在 http://localhost:8000 启动

### 2. 启动 Web 界面
```bash
streamlit run web/Login.py
```

或者使用批处理文件：
```bash
start_web.bat
```

Web 界面将在 http://localhost:8501 启动

## 📝 使用说明

### 首次登录
1. 打开 http://localhost:8501
2. 使用默认管理员账号登录：
   - 用户名：`admin`
   - 密码：`admin123`

### 创建用户（管理员）
1. 登录后，点击"用户管理"（仅管理员可见）
2. 点击"创建用户"按钮
3. 填写用户信息并选择角色
4. 提交创建

### 配置 API Keys
1. 点击"⚙️ 配置"页面
2. 配置你的 API Keys：
   - OpenAI API Key
   - ComfyUI URL
   - RunningHub API Key
3. 保存配置

### 生成视频
1. 点击"🎬 生成视频"
2. 选择生成模式：
   - **标准生成**：输入主题自动生成
   - **资产导入**：上传素材生成
   - **图生视频**：图片转视频
   - **数字人**：生成数字人视频
   - **动作迁移**：动作转换
3. 填写参数并开始生成

### 查看历史
1. 点击"📚 历史记录"
2. 查看所有视频记录
3. 下载、删除或重新生成

## 🔧 技术架构

### 后端（FastAPI）
```
api/
├── app.py              # 主应用
├── database.py         # 数据库模型
├── auth.py            # 认证系统
├── routers/
│   ├── auth_router.py    # 用户认证路由
│   ├── config_router.py  # 配置管理路由
│   ├── video_router.py   # 视频生成路由
│   └── ...              # 其他路由
└── ...
```

### 前端（Streamlit）
```
web/
├── Login.py           # 登录页面（入口）
├── pages/
│   ├── 0_🏠_Welcome.py    # 欢迎页
│   ├── 1_⚙️_Config.py     # 配置页
│   ├── 2_🎬_Generate.py   # 生成页
│   └── 3_📚_History.py    # 历史页
├── pipelines/         # 所有生成管道
│   ├── standard.py
│   ├── asset_based.py
│   ├── i2v.py
│   ├── digital_human.py
│   └── ...
└── ...
```

### 数据库
- SQLite 数据库：`pixelle_video.db`
- 表结构：
  - `users` - 用户表
  - `user_configs` - 用户配置表
  - `videos` - 视频记录表

## 🔐 安全说明

### 生产环境部署建议
1. **修改密钥**：更改 `api/auth.py` 中的 `SECRET_KEY`
2. **强密码策略**：修改默认管理员密码
3. **HTTPS**：使用 SSL 证书
4. **防火墙**：限制 API 访问

### 数据隔离
- 每个用户独立的配置
- 视频记录按用户隔离
- 输出文件按用户目录分离

## 📊 数据库结构

### 用户表（users）
- id: 用户ID
- username: 用户名
- hashed_password: 密码哈希
- role: 角色（admin/user）
- created_at: 创建时间

### 用户配置表（user_configs）
- id: 配置ID
- user_id: 所属用户
- llm_api_key: LLM API密钥
- comfyui_url: ComfyUI地址
- 等等...

### 视频记录表（videos）
- id: 视频ID
- user_id: 所属用户
- title: 标题
- pipeline: 使用的管道
- status: 状态（pending/processing/completed/failed）
- output_path: 输出路径
- created_at: 创建时间

## 🎨 自定义

### 添加新的生成管道
1. 在 `web/pipelines/` 下创建新文件
2. 继承 `BasePipelineUI` 类
3. 实现 `render()` 方法
4. 在 `__init__.py` 中注册

### 修改界面样式
- 编辑各页面的 CSS 样式
- 修改配色方案

### 添加新功能
- 后端：在 `api/routers/` 添加新路由
- 前端：在 `web/pages/` 添加新页面

## 🐛 故障排查

### 无法连接到 API
- 检查后端是否启动：访问 http://localhost:8000/health
- 检查防火墙设置
- 查看后端日志

### 登录失败
- 确认用户名和密码正确
- 检查数据库是否已初始化
- 查看 API 日志

### 视频生成失败
- 检查 API Keys 配置
- 确认 ComfyUI 已启动
- 查看视频详情中的错误信息

## 📞 技术支持

- 微信：19149253810
- 项目地址：D:\ai ZHINENGTI\Pixelle-Video-Multi

## 📄 许可证

Apache License 2.0

---

**版本**：v2.0.0 (多用户版)  
**更新日期**：2026-09-15
