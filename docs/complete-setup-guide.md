# 完整 CI 配置流程：agent 项目 → api-auto-test 项目

本文档从零开始，手把手带你完成：

1. 把 `api-auto-test` 项目上传到个人 GitLab
2. 配置 `api-auto-test` 的 CI/CD 变量、trigger token、本地 runner
3. 在 `agent` 项目添加 CI 配置并配置变量
4. 实现：agent 提交 → 部署 → 健康检查 → 触发 api-auto-test 跑接口测试

---

## 一、前置条件

| 项目 | 要求 |
|---|---|
| GitLab 账号 | 已有 `gitlab.com` 账号，能创建 private project |
| 本地环境 | macOS / Linux，能跑 GitLab Runner，能访问公司内网 FAT/UAT |
| 代码状态 | `api-auto-test` 本地项目已完成敏感信息清理（`.env` 和 `Jenkinsfile` 已移除） |

---

## 二、把 api-auto-test 上传到 GitLab

### 2.1 在 gitlab.com 创建仓库

1. 打开 `https://gitlab.com/projects/new`
2. 选择 **Create blank project**
3. 填写：
   - **Project name**：`api-auto-test`
   - **Project slug**：`api-auto-test`
   - **Visibility Level**：**Private**
   - **Initialize repository with a README**：**不要勾选**
4. 点击 **Create project**

创建后，页面会显示仓库地址：

```text
https://gitlab.com/my-ci-lab1/api-auto-test.git
```

> 注意：`my-ci-lab1` 换成你的 GitLab 用户名或 group 名。

### 2.2 推送本地代码

```bash
cd /Users/reabam/Projects/api_auto_test

# 添加远程仓库，名字叫 gitlab
git remote add gitlab https://gitlab.com/my-ci-lab1/api-auto-test.git

# 推送 master 分支
git push -u gitlab master
```

### 2.3 确认敏感文件没上传

```bash
git ls-files | grep -E '^\.env$|^Jenkinsfile$'
```

如果没有任何输出，说明 `.env` 和 `Jenkinsfile` 不在版本控制中，是安全的。

> 如果 `Jenkinsfile` 之前提交过 git history，里面的 `SIGN`、`DEVELOPER_ID`、`E_POI_ID` 已经泄露，建议尽快轮换。

---

## 三、配置 api-auto-test 项目

打开 `https://gitlab.com/my-ci-lab1/api-auto-test`

### 3.1 配置 CI/CD Variables

路径：**Settings → CI/CD → Variables → Expand → Add variable**

按下面表格添加变量：

| Key | Value | Mask | Protected | 说明 |
|---|---|---|---|---|
| `ENV` | `fat` | 否 | 否 | 默认环境 |
| `BASE_URL` | `http://fat-pos.xxx.com:60030/api` | 否 | 否 | FAT 基础地址 |
| `UAT_URL` | `https://pos.xxx.com/api` | 否 | 否 | UAT 基础地址 |
| `DB_HOST` | 数据库地址 | 否 | 否 | |
| `DB_PORT` | `3306` | 否 | 否 | |
| `DB_USER` | `root` | 否 | 否 | |
| `DB_PASSWORD` | 数据库密码 | **是** | 否 | |
| `DB_NAME` | 数据库名 | 否 | 否 | |
| `DEVELOPER_ID` | FAT developer id | 否 | 否 | |
| `DEVELOPER_ID_UAT` | UAT developer id | 否 | 否 | |
| `E_POI_ID` | FAT e_poi_id | 否 | 否 | |
| `E_POI_ID_UAT` | UAT e_poi_id | 否 | 否 | |
| `SIGN` | FAT sign | **是** | 否 | |
| `SIGN_UAT` | UAT sign | **是** | 否 | |
| `WECHAT_WEBHOOK` | 企业微信机器人地址 | **是** | 否 | 失败通知用 |
| `LOGIN_MOBILE` | 登录手机号 | 否 | 否 | |
| `LOGIN_WORD` | 登录密码 MD5 | **是** | 否 | |

> 如果 Mask 选项提示不满足正则表达式，改用 **隐藏** 级别。

### 3.2 创建 Pipeline Trigger Token

路径：**Settings → CI/CD → Pipeline triggers → Expand → Add trigger token**

1. 描述填：`agent-project-trigger`
2. 点击 **Add trigger token**
3. 复制生成的 **Token**（一串字符）
4. 记下 **Trigger URL** 或项目首页的 **Project ID**

例如：

```text
Token: glpat-xxxxxxxxxxxxxxxxxxxx
Project ID: 12345678
```

这个 token 后面要填到 agent 项目的变量里。

### 3.3 注册本地 GitLab Runner

因为公司 FAT/UAT 在内网，必须用本地 runner。

#### 安装 gitlab-runner

```bash
brew install gitlab-runner
```

#### 注册 runner

```bash
sudo gitlab-runner register \
  --non-interactive \
  --url https://gitlab.com \
  --token <PROJECT_REGISTRATION_TOKEN> \
  --executor docker \
  --docker-image python:3.12-slim \
  --name "api-auto-test-local-runner" \
  --tag-list "api-test" \
  --docker-privileged
```

**`<PROJECT_REGISTRATION_TOKEN>` 获取方式**：

`api-auto-test` 项目 → **Settings → CI/CD → Runners → Expand → New project runner**

点击后复制 **registration token**。

#### 启动 runner

```bash
sudo gitlab-runner start
```

#### 验证 runner 在线

回到 GitLab 页面：**Settings → CI/CD → Runners**，应该能看到 `api-auto-test-local-runner` 状态是绿色的。

> 如果 Docker 容器无法访问公司 VPN，改用 shell executor：
> ```bash
> sudo gitlab-runner register \
>   --url https://gitlab.com \
>   --token <TOKEN> \
>   --executor shell \
>   --name "api-auto-test-shell-runner" \
>   --tag-list "api-test"
> sudo gitlab-runner start
> ```

---

## 四、配置 agent 项目

### 4.1 确认 agent 项目已在 GitLab

假设地址是：

```text
https://gitlab.com/my-ci-lab1/agent
```

### 4.2 添加 .gitlab-ci.yml

把 `docs/agent-project/.gitlab-ci.yml` 复制到 agent 项目根目录：

```bash
cp /Users/reabam/Projects/api_auto_test/docs/agent-project/.gitlab-ci.yml /path/to/agent/.gitlab-ci.yml
```

然后修改里面的占位符：

1. `FAT_HEALTH_URL` 和 `UAT_HEALTH_URL` 改成真实的健康检查地址
2. `deploy` 阶段的 `echo` 替换成真实部署命令

> 这份配置去掉了 `test` 阶段，因为很多老项目没有单元测试。如果你后续要补单元测试，可以在 `build` 和 `deploy` 之间加一个 `test` stage。

### 4.3 配置 CI/CD Variables

路径：**Settings → CI/CD → Variables → Expand → Add variable**

| Key | Value | Mask | 说明 |
|---|---|---|---|
| `API_AUTO_TEST_TRIGGER_TOKEN` | 3.2 步复制的 token | **是** | api-auto-test 的 trigger token |
| `API_AUTO_TEST_PROJECT_ID` | api-auto-test 的项目 ID | 否 | 比如 `12345678` |
| `FAT_HEALTH_URL` | FAT 健康检查地址 | 否 | 如果已在 .gitlab-ci.yml 写死可不加 |
| `UAT_HEALTH_URL` | UAT 健康检查地址 | 否 | 如果已在 .gitlab-ci.yml 写死可不加 |

### 4.4 提交并推送

```bash
cd /path/to/agent
git add .gitlab-ci.yml
git commit -m "ci: add pipeline with health check and trigger api-auto-test"
git push origin develop
```

---

## 五、验证完整流程

### 5.1 在 agent 项目触发 pipeline

push 后，打开：

```text
https://gitlab.com/my-ci-lab1/agent/-/pipelines
```

应该看到一条 pipeline 正在跑，包含这些 job：

```text
build → deploy → health_check → trigger_api_auto_tests
```

### 5.2 检查 api-auto-test 是否被触发

打开：

```text
https://gitlab.com/my-ci-lab1/api-auto-test/-/pipelines
```

应该出现一条新的 pipeline，来源显示为 `trigger`。

### 5.3 期望结果

agent 项目：
- `build` ✅
- `deploy` ✅
- `health_check` ✅
- `trigger_api_auto_tests` ✅（curl 返回 200）

api-auto-test 项目：
- `setup` ✅
- `unit` ✅
- `smoke` ✅
- `critical` ✅
- `allure_report` ✅
- `pages` ✅
- `notify` 只在失败时执行

### 5.4 查看 Allure 报告

成功后，报告地址：

```text
https://my-ci-lab1.gitlab.io/api-auto-test
```

---

## 六、分支环境映射

| 提交分支 | 部署环境 | 触发 api-auto-test 环境 |
|---|---|---|
| `develop` | FAT | `ENV=fat` |
| `main` | UAT | `ENV=uat` |
| `release/*` | UAT | `ENV=uat` |

---

## 七、常见问题排查

### 7.1 agent 项目的 trigger job 报 401

原因：`API_AUTO_TEST_TRIGGER_TOKEN` 错了，或者 token 被撤销。

解决：到 api-auto-test 项目重新生成 token，更新 agent 项目变量。

### 7.2 agent 项目报 404

原因：`API_AUTO_TEST_PROJECT_ID` 错了。

解决：确认项目 ID 是数字，不是路径。

### 7.3 api-auto-test pipeline 一直 pending

原因：没有可用的 runner。

解决：检查本地 runner 是否启动，tag 是否匹配 `api-test`。

### 7.4 health_check 一直失败

原因：健康检查地址不对，或服务真的没起来。

解决：
- 手动 curl 一下 `FAT_HEALTH_URL` 看能否通
- 检查 deploy 阶段是否真的部署成功
- 如果没有 `/health` 接口，换成一个稳定的只读接口

### 7.5 api-auto-test 的 integration test 报 500

原因：服务没起来，或环境变量不对。

解决：
- 检查 api-auto-test 的 CI/CD Variables 是否配置正确
- 检查 runner 是否能访问公司内网
- 检查 `ENV` 变量是否生效

---

## 八、文件清单

| 文件 | 位置 | 用途 |
|---|---|---|
| `.gitlab-ci.yml` | `api-auto-test` 项目根目录 | api-auto-test 自己的测试流水线 |
| `.gitlab-ci.yml` | `agent` 项目根目录 | agent 项目的构建/部署/触发流水线 |
| `docs/agent-project/README.md` | `api-auto-test` 项目 | agent 项目 CI 配置解释文档 |
| `docs/interview-script.md` | `api-auto-test` 项目 | 面试话术 |
| `docs/cross-project-trigger.md` | `api-auto-test` 项目 | 跨项目触发原理说明 |

---

## 九、下一步建议

1. 先手动在 api-auto-test 项目跑一条 pipeline，确认 runner 和变量没问题
2. 再测试 agent 项目的跨项目触发
3. 最后加一个定时 schedule，每晚跑全量回归

如果在某一步卡住了，把页面截图或错误日志发给我，我帮你定位。
