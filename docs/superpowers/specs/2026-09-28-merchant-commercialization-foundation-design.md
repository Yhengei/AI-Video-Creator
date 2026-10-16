# Pixelle-Video 本地商家商业化基础改造设计

日期：2026-09-28  
阶段：设计确认版  
目标：在暂不重做 Streamlit 前端的前提下，把现有项目改造成可由单台无 GPU 服务器承载、多个本地商家安全共用、商家自带第三方 API Key（BYOK）的多租户视频生成平台。

## 1. 产品边界

### 1.1 第一阶段服务对象

- 平台由运营方统一部署和维护。
- 客户主要是本地商家，不面向匿名大众开放注册。
- 商家账号由管理员创建，或后续通过邀请码开通。
- 商家自行购买并配置模型供应商 API Key。
- 平台收取软件使用费、维护费或服务费，不代收第一阶段的模型调用费用。
- 服务器不运行本地图像或视频模型，主要负责业务 API、任务调度、轻量视频合成、文件管理和审计。

### 1.2 第一阶段不做

- 不重做完整前端，不追求复杂视觉设计。
- 不接微信支付、支付宝或自动订阅。
- 不做公众自助注册、开放市场或模板交易。
- 不同时接入大量新模型供应商；优先稳定现有适配器。
- 不建设复杂企业组织架构，只保留未来扩展空间。
- 不在第一阶段引入 Kubernetes 或微服务拆分。

## 2. 方案比较与选择

### 方案 A：只修登录和页面

保留全局配置、内存任务和公共文件目录，只在页面上限制访问。

优点是开发量最小；缺点是后端接口仍可绕过页面访问，任务、文件和 API Key 仍可能串租户，不满足收费运营的安全底线。因此不采用。

### 方案 B：单体应用内完成多租户基础改造（推荐）

保留 FastAPI、Streamlit 和现有核心生成模块，新增统一租户上下文、数据库任务、加密凭据、文件隔离、队列 Worker 和审计。前端只做必要对接。

优点是复用现有约 2.5 万行代码，风险和成本可控，适合首批本地商家；缺点是需要系统性修改生成入口，不能只做局部补丁。

### 方案 C：立即重写为完整 SaaS

采用独立前端、微服务、对象存储、计费中心和复杂组织权限。

长期扩展性最好，但开发周期、运维复杂度和初期成本过高，尚未经过真实商家需求验证。因此暂不采用。

**决定：采用方案 B。** 先完成安全、隔离、任务可靠性和可运维性，再根据实际商家使用情况决定是否重做前端或升级架构。

## 3. 总体架构

```text
商家浏览器
    │
    ▼
Streamlit Web（暂时保留）
    │  只通过受保护 API 操作业务数据
    ▼
FastAPI
    ├── 身份认证与租户上下文
    ├── 商家、成员、凭据、项目和任务 API
    ├── 配额、限流与审计
    └── 生成任务提交
             │
             ▼
        Redis 任务队列
             │
             ▼
        Worker 进程
    ├── 加载商家加密凭据
    ├── 调用 LLM / 图片 / 视频 / TTS API
    ├── 轮询、重试和超时处理
    ├── FFmpeg 轻量合成
    └── 保存结果并更新任务状态
             │
      ┌──────┴──────┐
      ▼             ▼
 PostgreSQL       文件存储
 业务元数据       本地隔离目录，后续可切 OSS/COS/S3
```

第一阶段仍然是一个代码仓库，但运行时至少分为 `web`、`api`、`worker`、`postgres`、`redis` 五类进程或容器。API 进程不得直接执行长时间视频任务。

## 4. 核心领域模型

所有商家业务数据必须带 `tenant_id`。仅带 `user_id` 不足以表达一个商家下未来可能存在多个员工。

### 4.1 tenants（商家）

| 字段 | 说明 |
|---|---|
| id | UUID 或不可预测主键 |
| name | 商家名称 |
| slug | 内部唯一标识 |
| status | active / suspended / closed |
| plan_code | 人工分配的套餐标识 |
| max_concurrent_jobs | 最大并发任务数 |
| daily_job_limit | 每日任务数限制 |
| storage_limit_bytes | 存储上限 |
| created_at / updated_at | 审计时间 |

### 4.2 users（用户）

| 字段 | 说明 |
|---|---|
| id | 用户主键 |
| username | 登录名，全局唯一或租户内唯一需选定一种；第一阶段采用全局唯一 |
| password_hash | Argon2id 或 bcrypt 哈希 |
| status | active / disabled |
| is_platform_admin | 是否为平台管理员 |
| last_login_at | 最近登录时间 |
| created_at / updated_at | 审计时间 |

### 4.3 tenant_memberships（商家成员关系）

| 字段 | 说明 |
|---|---|
| tenant_id | 商家 ID |
| user_id | 用户 ID |
| role | owner / manager / member |
| created_at | 创建时间 |

首版 UI 可以做到一个账号只属于一个商家，但后端数据结构不写死这一限制。

### 4.4 provider_credentials（供应商凭据）

| 字段 | 说明 |
|---|---|
| id | 凭据 ID |
| tenant_id | 所属商家 |
| provider | openai / dashscope / ark / kling / runninghub 等 |
| label | 商家可识别名称 |
| encrypted_payload | 加密后的 API Key、Secret 等 JSON |
| key_fingerprint | 不可逆指纹，用于识别重复密钥和审计 |
| masked_hint | 例如末四位，供页面显示 |
| status | active / invalid / disabled |
| last_tested_at | 最近连接测试时间 |
| last_test_result | success / failed |
| created_by | 创建人 |
| created_at / updated_at | 审计时间 |

凭据查询接口永远不返回完整密钥。更新时，空值表示保留原密钥，显式 `delete=true` 才删除。

### 4.5 projects（项目）

用于把同一商家的素材和生成任务按活动、商品或门店归组。

| 字段 | 说明 |
|---|---|
| id | 项目 ID |
| tenant_id | 所属商家 |
| name | 项目名称 |
| created_by | 创建人 |
| status | active / archived |
| created_at / updated_at | 审计时间 |

### 4.6 assets（素材）

| 字段 | 说明 |
|---|---|
| id | 素材 ID |
| tenant_id / project_id | 所属商家和项目 |
| object_key | 存储键，不保存任意绝对路径 |
| original_name | 原始文件名，仅用于展示 |
| media_type | image / video / audio / document |
| mime_type / size_bytes / sha256 | 文件校验信息 |
| status | uploading / ready / quarantined / deleted |
| created_by / created_at | 审计信息 |

### 4.7 generation_jobs（生成任务）

替代当前内存任务，并成为视频历史的唯一真实来源。

| 字段 | 说明 |
|---|---|
| id | 不可预测任务 ID |
| tenant_id / project_id / created_by | 所属范围 |
| job_type | standard / asset_based / i2v / digital_human / action_transfer |
| status | queued / running / waiting_provider / succeeded / failed / cancelled |
| progress_percent / progress_stage | 进度 |
| request_payload | 去除密钥后的规范化输入 JSON |
| result_payload | 输出素材 ID、时长、尺寸等，不保存公开 URL |
| provider_snapshot | 供应商和模型名称，不包含凭据 |
| attempt_count | 已尝试次数 |
| idempotency_key | 防止重复提交 |
| error_code / error_message | 对用户安全的错误信息 |
| queued_at / started_at / completed_at | 生命周期时间 |

### 4.8 job_events 与 audit_logs

`job_events` 记录任务进度和供应商调用阶段；`audit_logs` 记录登录、配置密钥、创建/取消任务、下载/删除文件和管理员操作。两者均不得记录完整 API Key、Authorization 头或敏感素材内容。

## 5. 身份认证与授权边界

### 5.1 登录安全

- JWT 签名密钥从环境变量或 secret 文件读取，启动时缺失则拒绝生产模式启动。
- 密码改为 Argon2id 或 bcrypt，不继续使用无盐 SHA-256。
- 默认 `admin/admin123` 只允许首次初始化使用，并强制首次登录改密；生产部署不得在页面展示默认密码。
- Access Token 缩短有效期，并提供可撤销的会话或 refresh token 机制。
- 登录增加速率限制和失败审计。

### 5.2 租户上下文

所有受保护请求统一得到：

```text
RequestContext {
  user_id,
  tenant_id,
  tenant_role,
  is_platform_admin,
  request_id
}
```

业务路由不得自行相信前端提交的 `tenant_id`。普通用户的租户必须由登录身份和成员关系推导；平台管理员跨租户操作必须使用独立管理接口并写审计日志。

### 5.3 路由策略

- `/health` 可匿名访问，但只返回存活状态，不暴露内部配置。
- `/auth/login` 可匿名访问并限流。
- 模板公共元数据可以按需匿名或登录可见；工作流内容、任务、模型调用、文件和配置必须登录。
- 所有 `llm`、`content`、`image`、`tts`、`video`、`frame`、`tasks` 和 `files` 业务接口必须注入租户上下文。
- 任务查看、取消、文件下载必须同时匹配 `tenant_id` 和资源 ID，不能只靠猜测 task ID 或文件路径。

## 6. BYOK 密钥管理

### 6.1 加密方案

- 使用服务器主密钥对供应商凭据做信封加密或至少使用成熟的对称认证加密算法。
- 主密钥不进入数据库、不写进代码仓库、不出现在日志中。
- 支持后续密钥轮换，密文带 `key_version`。
- 只有 Worker 在执行任务时短暂解密所需凭据。
- 解密后的密钥不进入任务 JSON、异常文本、缓存键或日志字段。

### 6.2 配置体验

前端暂时只需提供四个动作：选择供应商、填写密钥、测试连接、保存。模型名、Base URL 和常规参数尽量由服务器提供推荐默认值；高级字段折叠展示。

### 6.3 配置应用方式

现有全局 `config.yaml` 只保存平台级非敏感默认值。商家生成任务时：

1. 根据 `tenant_id` 读取商家选择的供应商和模型配置。
2. Worker 加载对应加密凭据。
3. 构造任务级 `GenerationContext`。
4. 将上下文显式传递给 LLM、图片、视频和 TTS 服务。

不得再通过全局可变 `config_manager` 切换不同商家的密钥，否则并发任务会互相污染。

## 7. 任务系统

### 7.1 状态流转

```text
queued → running → waiting_provider → running → succeeded
                   └───────────────→ failed
queued/running/waiting_provider ───→ cancelled
```

每次状态变化同时写数据库和 `job_events`。Redis 只承担投递、锁和短期进度，不作为任务事实来源。

### 7.2 执行原则

- API 创建数据库任务后再投递队列；投递失败则任务标记为失败或进入补偿扫描。
- Worker 使用数据库抢占或可靠队列机制，避免同一任务重复执行。
- 外部供应商调用设置连接超时、响应超时和总任务截止时间。
- 只对明确可重试的网络错误、限流和供应商 5xx 重试，参数错误和余额不足不自动重试。
- 使用指数退避并限制最大次数。
- 任务提交支持幂等键，浏览器重复点击不能重复扣占资源。
- 服务重启后，超时的 `running` 任务由恢复任务重新判断或标记失败。
- 取消任务需要同时更新状态，并在供应商支持时调用供应商取消接口。

### 7.3 供应商调用记录

每次外部调用记录供应商、模型、请求时间、响应时间、状态码、供应商任务 ID、重试次数和可获得的用量数据。不得记录密钥和完整敏感输入。

即使采用 BYOK，也需要这些记录来排查商家问题和识别平台资源消耗。

## 8. 文件与存储隔离

### 8.1 存储键

第一阶段可继续使用服务器磁盘，但目录必须按租户和任务隔离：

```text
data/tenants/{tenant_id}/assets/{asset_id}/source.ext
output/tenants/{tenant_id}/jobs/{job_id}/final.mp4
output/tenants/{tenant_id}/jobs/{job_id}/intermediate/...
```

业务接口只接受 `asset_id` 或 `file_id`，不接受客户端传入任意服务器路径。

### 8.2 下载接口

- 下载前查询数据库并验证资源所属租户。
- 使用规范化、解析后的受控路径，并确认最终路径位于该租户根目录之内。
- 不直接公开 `workflows/`、`templates/` 或服务器文件系统。
- 响应增加合适的 Content-Type、文件名和缓存策略。
- 后续迁移对象存储时，接口可改成短时签名 URL，数据库模型无需变化。

### 8.3 生命周期

- 删除素材或任务先做软删除，再由后台清理文件。
- 临时文件必须绑定任务并设置过期时间。
- 定期统计每个租户的存储用量。
- 上传限制扩展名、MIME、文件大小和媒体可解析性；高风险文件不直接执行或渲染。

## 9. 配额、限流和资源保护

即使商家自带 API Key，平台仍需限制自身资源：

- 每商家同时运行任务数。
- 每用户和每 IP 的登录及 API 请求频率。
- 每日提交任务数。
- 单任务场景数、素材数量、原始文件大小、输出时长和分辨率。
- 每商家存储空间。
- Worker 全局并发数和 FFmpeg 并发数。

配额检查发生在任务入队前；Worker 执行前再次校验关键限制，避免竞态。额度不足或并发已满应返回明确的业务错误，不返回服务器异常。

## 10. 供应商适配层

现有 API 服务代码继续复用，但统一为以下能力接口：

```text
LLMProvider.generate(...)
ImageProvider.submit(...) / poll(...) / cancel(...)
VideoProvider.submit(...) / poll(...) / cancel(...)
TTSProvider.synthesize(...)
```

统一输出标准错误类型：认证失败、余额不足、限流、参数错误、内容审核拒绝、供应商超时、供应商故障和未知错误。业务层不依赖供应商原始错误文案。

第一阶段不做复杂自动选路。每项能力由商家明确选择一个默认供应商；后续可以增加备用供应商和失败切换。

## 11. 前端最小调整

暂不改变整体页面和视觉风格，只做维持安全闭环所必需的修改：

- 所有业务操作通过 FastAPI，不再直接读写全局 `config.yaml` 或本地历史目录。
- 每个页面统一检查服务端会话，不能只相信 `st.session_state.logged_in`。
- 配置页面改为商家凭据列表、掩码显示和连接测试。
- 生成页面提交任务后轮询任务 API，不在 Streamlit 会话内执行完整生成。
- 历史页面从数据库任务 API 读取，只显示当前租户数据。
- 下载、删除和取消操作均调用受保护 API。

## 12. 部署与运维

### 12.1 推荐组件

- Nginx：HTTPS、请求大小限制和反向代理。
- FastAPI：无状态 API，可先运行 1～2 个进程。
- Streamlit：现阶段 Web UI。
- PostgreSQL：业务数据和任务事实来源。
- Redis：任务队列、分布式锁和限流。
- Worker：外部 API 调用、轮询和 FFmpeg 合成。
- 本地持久卷：第一阶段文件存储；定期备份，后续迁移对象存储。

### 12.2 可观测性

- 每个请求和任务生成 `request_id/job_id`，贯穿日志。
- 日志结构化输出，自动脱敏 Authorization、Cookie、API Key 和 Secret。
- 至少监控 API 存活、队列长度、运行任务数、任务成功率、平均耗时、磁盘空间和供应商错误率。
- 数据库和用户文件分别备份，并定期验证恢复流程。

## 13. 迁移策略

### 阶段 0：立即止血

- 轮换当前配置文件中出现过的真实外部服务密钥。
- 生产环境禁用默认管理员密码和硬编码 JWT 密钥。
- 补齐依赖声明并建立可重复安装流程。
- 临时限制 API 和文件服务只允许可信网络访问，直到鉴权改造完成。

### 阶段 1：建立租户与安全基座

- 引入 PostgreSQL 和数据库迁移工具。
- 建立 tenants、memberships、credentials、projects、assets、jobs、events、audit_logs 表。
- 改造登录、密码哈希、JWT 和统一租户上下文。
- 为所有业务路由补充鉴权和资源所有权检查。
- 实现凭据加密、掩码返回和连接测试。

### 阶段 2：任务与文件可靠性

- 用数据库任务 + Redis Worker 替代内存任务。
- 将现有生成管线改为接收任务级上下文。
- 建立租户文件目录、受保护下载和临时文件清理。
- 将历史记录统一迁移为 `generation_jobs`。

### 阶段 3：运营保护

- 增加并发、任务、时长和存储限制。
- 完善审计、脱敏日志、重试、恢复和监控。
- 做跨租户权限测试、供应商故障测试和备份恢复演练。

### 阶段 4：前端与业务增强

- 改善行业模板、品牌素材、批量生成和商家体验。
- 根据真实运营数据决定是否增加平台代付 API、支付套餐和独立前端。

## 14. 测试与验收标准

### 14.1 安全与隔离

- 商家 A 无法通过猜测 ID、修改 URL 或调用 API 查看、下载、取消或删除商家 B 的任务和文件。
- 任何 API 响应、日志、任务记录和错误信息中都不存在完整供应商密钥。
- `../`、绝对路径、编码路径穿越和符号链接逃逸测试均无法访问租户根目录之外的文件。
- 被禁用用户、被暂停商家和过期会话无法提交新任务。

### 14.2 任务可靠性

- API 或 Worker 重启后，已提交任务仍可查询。
- 浏览器重复提交相同幂等键只创建一个任务。
- 可重试错误按策略重试，不可重试错误立即给出明确状态。
- Worker 异常退出后，任务最终能恢复执行或进入可解释的失败状态，不长期卡在 running。
- 取消任务后不再产生可见结果，已产生的临时文件会被清理。

### 14.3 配置与 BYOK

- 每个商家可独立保存和测试自己的凭据。
- 商家更新一个供应商配置不会影响其他商家正在执行的任务。
- 删除凭据后，新任务无法再使用该凭据，历史任务只保留供应商名称和模型快照。

### 14.4 运维

- 新服务器可以从代码、环境配置和迁移脚本重复部署。
- 数据库和文件备份可以恢复到测试环境。
- 磁盘不足、Redis 不可用、数据库不可用和供应商超时都有明确告警或错误表现。

## 15. 现有代码的主要改造落点

| 当前位置 | 主要改造 |
|---|---|
| `api/auth.py` | 环境密钥、安全密码哈希、会话撤销、统一身份上下文 |
| `api/database.py` | 拆分为正式模型与数据库配置，迁移至 PostgreSQL |
| `api/routers/*.py` | 全面鉴权、租户过滤、资源所有权校验和安全错误响应 |
| `api/tasks/manager.py` | 由内存任务改为数据库任务和 Redis Worker |
| `api/routers/files.py` | 取消任意路径下载，改为基于 file/asset ID 的授权下载 |
| `api/dependencies.py` | 取消共享全局业务配置，注入任务级租户上下文 |
| `pixelle_video/service.py` | 接受明确的 GenerationContext，不依赖全局可变配置 |
| `pixelle_video/services/api_services/*` | 统一供应商接口、超时、重试和标准错误 |
| `pixelle_video/services/persistence.py` | 任务历史迁移到数据库，文件元数据进入 assets/jobs |
| `web/state/session.py` | 以服务端会话为准，不在会话内直接运行长任务 |
| `web/pages/1_⚙️_Config.py` | 对接加密凭据 API，掩码显示和连接测试 |
| `web/pages/2_🎬_Generate.py` | 只提交任务和显示进度 |
| `web/pages/3_📚_History.py` | 只读取当前租户任务 API |
| `docker-compose.yml` | 增加 PostgreSQL、Redis、Worker、健康检查和持久卷 |
| `pyproject.toml` | 补齐数据库、认证、队列、加密、迁移和测试依赖 |

## 16. 完成定义

商业化基础改造完成，不以“页面可以登录”为标准，而以以下结果为准：

1. 两个测试商家可以同时使用各自 API Key 生成视频，配置不会互相污染。
2. 两个商家的任务、素材、历史、输出文件和用量完全隔离。
3. 服务器或 Worker 重启不会丢失任务事实和历史记录。
4. 所有密钥均加密存储且不会通过接口或日志泄露。
5. 所有文件下载均经过身份和租户授权。
6. 平台能限制单商家并发、任务数量和存储使用。
7. 管理员能够查看任务运行情况和错误，但默认不能看到商家的完整 API Key。
8. 项目具备自动化测试、数据库迁移、备份恢复说明和可重复部署流程。

