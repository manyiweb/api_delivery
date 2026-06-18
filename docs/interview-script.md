# 面试话术：GitLab CI/CD 实践

> 核心原则：**不造假、不冒充公司项目**，但可以强调“按企业级标准在个人项目中落地”。

---

## 1. 开场介绍（30 秒版）

"我维护了一套 Python 接口自动化框架，早期用 Jenkins 跑，但它是 Windows bat 脚本、Hard code 路径和 Python 解释器，迁移性差。

后来我在个人 GitLab 上重新搭了一套 CI/CD 流水线，目标是对齐企业级做法：多阶段流水线、并发执行、Allure 报告、失败通知、Secrets 管理。因为测试环境在公司内网，我在本地注册了一个 GitLab Runner 来执行。”

---

## 2. 流水线结构（配合 .gitlab-ci.yml 讲）

"流水线分了 7 个 stage：

1. **setup**：安装依赖并做 pip cache
2. **unit**：单元测试，不访问外部接口，作为后续集成测试的门禁
3. **smoke**：冒烟测试，真实调用 FAT/UAT 接口
4. **critical**：关键业务测试
5. **report**：合并 Allure 结果生成 HTML 报告
6. **pages**：把报告发布到 GitLab Pages
7. **notify**：失败时推企业微信通知

其中 smoke 和 critical 通过 GitLab 的 `needs` 机制在 unit 通过后并发跑，缩短整体耗时。”

---

## 3. 为什么从 Jenkins 迁到 GitLab CI（常见问题）

"主要考虑三点：

- **平台通用性**：Jenkinsfile 里写死了 Windows 路径和 bat 命令，换到 Linux/Mac 跑不了；GitLab CI 基于 Docker，平台无关。
- **代码与流水线同仓库**：`.gitlab-ci.yml` 和代码一起版本管理，MR 时可以 review pipeline 变更。
- **原生支持 DAG 和 artifact**：并发 job、跨 job 传递 Allure 结果、GitLab Pages 发布报告，这些比 Jenkins 插件链更轻量。”

---

## 4. 安全与 Secrets 管理（加分点）

"我做了一个关键改造：把代码里所有敏感信息清掉了。

- 原 `.env` 文件里有真实数据库密码、企业微信 webhook、sign，我把它从 git 移除，并加到 `.gitignore`。
- Jenkinsfile 里也硬编码了 FAT/UAT 的 URL、DEVELOPER_ID、SIGN，我把 Jenkinsfile 也移出代码库。
- 所有真实凭证都通过 GitLab CI/CD Variables 注入，敏感字段开启 Mask，这样日志里不会泄露。
- 登录手机号和 MD5 密码也从 `conftest.py` 里抽到环境变量。

**提醒**：如果之前这些凭证已经提交过 git history，还需要轮换凭证，并用 `git filter-repo` 做历史清理。”

---

## 5. Runner 部署方式（关键细节）

"因为 FAT/UAT 环境在公司内网，云端 runner 访问不到，所以我在本地 MacBook 上注册了一个 GitLab Runner。

- 首选 **Docker executor**，跑在 `python:3.12-slim` 镜像里，环境干净、可复现。
- 如果 Docker 容器走不了公司 VPN，就改用 **shell executor**，直接用宿主机的网络和 VPN。

真实企业里，runner 会部署在公司内网服务器或 K8s 集群上；我本地 runner 只是为了个人演示和面试。”

---

## 6. 报告与通知

"测试报告用了 Allure：

- 每个测试 job 把自己的 Allure 结果作为 artifact 上传
- `allure_report` job 汇总后生成 HTML
- `pages` job 发布到 GitLab Pages，每次流水线都有固定链接

失败通知通过企业微信 webhook 发送，消息里包含分支、提交人、流水线链接和 Allure 报告链接，方便开发和测试第一时间定位。”

---

## 6.5 跨项目触发（重点加分项）

"这套测试框架还接入了后端项目的 CI/CD。

- 后端 `develop` 分支合并后，自动触发 FAT 环境冒烟测试
- 后端 `master` / `release` 分支合并后，自动触发 UAT 环境关键业务回归

实现方式是在后端项目的 `.gitlab-ci.yml` 里加一个 `trigger` job，通过 GitLab Pipeline Trigger API 调用本测试项目，同时通过 `variables[ENV]` 动态传入 `fat` 或 `uat`。Allure 报告里也会展示触发来源的项目和 commit，方便定位问题。”

---

## 7. 稳定性与效率优化

"为了降低 flaky test 影响：

- 集成测试加了 `--reruns 2 --reruns-delay 1`，失败自动重试
- 单元测试设置 `SKIP_HANDOVER=1`，避免不必要的开班检查，加快反馈
- pip 依赖按分支做了 cache，重复安装很快
- smoke 和 critical 并发执行，缩短总耗时”

---

## 8. 可能被追问的问题

### Q：如果测试环境不稳定，CI 一直失败怎么办？

"可以分几层处理：

1. 用 pytest-rerunfailures 做有限重试，区分 flaky 和真失败
2. 对核心接口加 mock 或 contract test，减少对外部环境依赖
3. 非阻塞场景下把部分 job 设为 `allow_failure: true`，先保证主流程不卡死
4. 定时任务（schedule）跑全量，MR 时只跑 smoke 门禁”

### Q：你怎么保证本地和 CI 跑的结果一致？

"三点：

1. 用同一个 `requirements.txt` 和 Docker 镜像锁定依赖版本
2. 用 Makefile 统一本地命令，`make unit` / `make smoke` 和 CI 里的 pytest 参数一致
3. 环境变量通过 `.env.example` 文档化，CI 用 Variables 注入相同变量名”

### Q：如果团队扩大，这套 CI 怎么扩展？

"横向扩展 runner：

1. 在公司内网部署多台 runner，打不同 tag，比如 `api-test`、 `heavy-test`
2. 大job 用 `parallel: matrix` 按模块或环境拆分到多个 runner
3. 全量回归走 nightly schedule，MR 只跑 unit + smoke
4. 把 Allure 报告存到对象存储或公司文档系统，替代 GitLab Pages”

---

## 9. 诚实边界（必看）

- **不要说是公司项目**：个人项目就是个人项目，面试官追问团队、业务线、部署规模会露馅。
- **强调“企业级标准”**：重点讲你学习了企业的 CI/CD 规范，并在个人项目中落地。
- **承认 runner 在本地**：正常说明因为测试环境在内网，本地 runner 是合理选择。

---

## 10. 一句话总结

> “我把一个原本只能 Windows 本地 Jenkins 跑的接口自动化框架，迁移到了跨平台、可复现、具备 Secrets 管理和 Allure 报告的 GitLab CI/CD 流水线上，并且能真实跑通公司内网测试环境，还能被后端项目按分支自动触发不同环境的回归测试。”
