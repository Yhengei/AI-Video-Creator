# AI-Video-Creator

一个面向短视频创作的 AI 工作流项目，包含 AI 文案、图像与视频生成、语音合成、视频合成和数字人口播等能力。这个仓库是在开源项目基础上的个人二次开发与学习实践，不是从零实现的基础模型或完整视频引擎。

## 项目简介

项目尝试把内容创作中的多个步骤连接成可配置的流水线：用户输入主题或上传素材，系统按所选模式调用语言模型、图像/视频服务、语音服务或 ComfyUI 工作流，最后合成并展示视频结果。

除原有的视频创作能力外，这个分支还加入了用户登录、角色和用户配置等多用户应用基础模块。当前重点是探索 AI 创作能力与 Web/API 应用的集成；认证和数据隔离仍有待完善，因此它是作品集原型，不适合直接部署到公网供真实用户使用。

## 主要功能

- **主题创作**：根据主题生成文案，并串接图像、视频、配音、背景音乐和视频合成步骤。
- **素材驱动创作**：上传图片或视频素材，分析素材并生成对应的视频脚本。
- **多种视频流程**：包含标准生成、素材生成、图生视频、数字人口播和动作迁移等流程。
- **模型与工作流接入**：通过配置选择兼容 API、DashScope、RunningHub 或本地 ComfyUI 工作流；实际可用能力取决于模型供应商、密钥和工作流配置。
- **Web 与 API**：使用 Streamlit 提供交互页面，FastAPI 提供后端接口。
- **账户原型**：包含登录认证、管理员/普通用户角色及用户配置、视频记录的数据模型和接口。多用户隔离及安全机制尚未达到生产要求。

## 技术栈

| 部分 | 技术 |
| --- | --- |
| Web 界面 | Python、Streamlit |
| 后端 API | FastAPI、Pydantic |
| 数据持久化 | SQLAlchemy、SQLite |
| 认证 | JWT |
| 视频与媒体处理 | FFmpeg、MoviePy、Pillow、NumPy |
| AI 能力接入 | OpenAI 兼容接口、DashScope、ComfyUI / RunningHub 工作流 |
| 运行方式 | Docker Compose 或本地 Python 环境 |

## 项目结构

```text
api/                FastAPI 接口、认证、数据库模型与任务管理
web/                Streamlit 页面、设置与生成流程
pixelle_video/      内容生成、媒体处理、模型适配与流水线
workflows/          本地 ComfyUI 和云端工作流示例
templates/          视频与图片模板
config.example.yaml 配置示例，不含个人 API Key
```

## 本地启动

需要 Docker Desktop 和 Docker Compose。首次启动会从配置示例创建本地 `config.yaml`：

```bash
docker compose up --build
```

- Web 页面：<http://localhost:8501>
- API 文档：<http://localhost:8000/docs>

启动后在应用设置中配置所需的模型服务、API Key 和工作流。API Key 只填写在本地配置或应用设置中，不要提交到 GitHub。`config.yaml`、本地数据库、临时素材和生成结果均已加入 Git 忽略规则。

## 项目来源与范围

本项目基于 [AIDC-AI/Pixelle-Video](https://github.com/AIDC-AI/Pixelle-Video) 进行二次开发。上游项目的版权声明、Apache-2.0 许可证和第三方依赖声明保留在 [LICENSE](LICENSE) 与 [NOTICE](NOTICE) 中。

仓库中的多用户部分仍是原型：部分业务接口尚未统一接入用户权限，任务管理使用进程内状态；认证实现也仍需安全加固。请勿把它视为已完成的生产级多租户平台，也不要在公网环境使用默认配置。

## 许可证

遵循仓库中的 [Apache-2.0 许可证](LICENSE)。
