# 跨项目触发 CI 配置

本文档说明如何让**后端/API 项目**在提交或部署后，自动触发本测试框架的 GitLab CI pipeline，并根据后端分支选择运行环境（FAT / UAT）。

---

## 1. 本项目（api-auto-test）需要做什么

### 1.1 确认 workflow 支持 trigger 来源

`.gitlab-ci.yml` 已经配置好：

```yaml
workflow:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == "$CI_DEFAULT_BRANCH"'
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
    - if: '$CI_PIPELINE_SOURCE == "trigger"'   # 支持跨项目触发
```

所有 job 的 `rules` 也已加入 `trigger` 来源。

### 1.2 生成 Pipeline Trigger Token

1. 打开 GitLab 项目：`https://gitlab.com/<用户名>/api-auto-test`
2. 进入 **Settings → CI/CD → Pipeline triggers**
3. 点击 **Add trigger**，输入描述如 `backend-api-trigger`
4. 复制生成的 **token** 和 **trigger URL**

你会得到类似这样的信息：

```text
Token: 1234567890abcdef
Trigger URL: https://gitlab.com/api/v4/projects/12345678/trigger/pipeline
```

---

## 2. 后端项目需要做什么

在后端项目的 `.gitlab-ci.yml` 里，添加一个 trigger job：

```yaml
stages:
  - build
  - deploy
  - trigger-tests

trigger_api_auto_tests:
  stage: trigger-tests
  image: curlimages/curl:latest
  variables:
    # 根据后端分支决定测试环境
    TEST_ENV: "fat"
  rules:
    # feature 分支合并后触发 FAT 冒烟
    - if: '$CI_COMMIT_BRANCH == "develop"'
      variables:
        TEST_ENV: "fat"
    # release/master 分支合并后触发 UAT 回归
    - if: '$CI_COMMIT_BRANCH == "master" || $CI_COMMIT_BRANCH == "release"'
      variables:
        TEST_ENV: "uat"
  script:
    - |
      curl -X POST \
        -F token=$API_AUTO_TEST_TRIGGER_TOKEN \
        -F ref=master \
        -F "variables[ENV]=$TEST_ENV" \
        -F "variables[TRIGGER_SOURCE_PROJECT]=$CI_PROJECT_NAME" \
        -F "variables[TRIGGER_SOURCE_COMMIT]=$CI_COMMIT_SHORT_SHA" \
        https://gitlab.com/api/v4/projects/<你的项目数字ID>/trigger/pipeline
```

### 2.1 在后端项目配置 CI/CD Variable

进入后端项目 **Settings → CI/CD → Variables**，添加：

| 变量名 | Mask | 值 |
|---|---|---|
| `API_AUTO_TEST_TRIGGER_TOKEN` | **是** | 从 api-auto-test 项目复制的 trigger token |

---

## 3. 环境选择映射建议

| 后端分支 | 建议测试环境 | 触发用例 |
|---|---|---|
| `feature/*` | 不触发 | 开发者本地验证 |
| `develop` | `fat` | smoke + unit |
| `release/*` | `uat` | smoke + critical |
| `master` | `uat` | smoke + critical |

如果你希望更灵活，也可以在后端项目根据 MR 标签或 commit message 决定：

```yaml
  rules:
    - if: '$CI_COMMIT_BRANCH == "master"'
      variables:
        TEST_ENV: "uat"
    - if: '$CI_COMMIT_BRANCH == "develop"'
      variables:
        TEST_ENV: "fat"
```

---

## 4. 手动测试触发

不用等后端提交，先在本地用 curl 测试：

```bash
# 触发 FAT 环境测试
curl -X POST \
  -F token=<TRIGGER_TOKEN> \
  -F ref=master \
  -F "variables[ENV]=fat" \
  https://gitlab.com/api/v4/projects/<PROJECT_ID>/trigger/pipeline

# 触发 UAT 环境测试
curl -X POST \
  -F token=<TRIGGER_TOKEN> \
  -F ref=master \
  -F "variables[ENV]=uat" \
  https://gitlab.com/api/v4/projects/<PROJECT_ID>/trigger/pipeline
```

---

## 5. 在测试报告里区分触发来源

触发时传入的 `TRIGGER_SOURCE_PROJECT` 和 `TRIGGER_SOURCE_COMMIT` 可以在 Allure 报告里展示。

在 `conftest.py` 的 `pytest_configure` 中，把这些变量也写入 `environment.properties`：

```python
f.write(f"TRIGGER_SOURCE_PROJECT={os.getenv('TRIGGER_SOURCE_PROJECT', 'manual')}\n")
f.write(f"TRIGGER_SOURCE_COMMIT={os.getenv('TRIGGER_SOURCE_COMMIT', 'n/a')}\n")
```

这样 Allure 报告里就能看到是哪个后端项目、哪次提交触发的测试。

---

## 6. 安全注意事项

1. **Trigger Token 要 Mask**，不要打印在日志里。
2. **不要在前端/公开仓库暴露 token**。
3. 如果后端项目也是公司项目，建议让后端项目也用个人 GitLab 账号或独立仓库做演示。
4. 跨项目触发会消耗本项目的 runner 资源，注意定时清理过期 pipeline。

---

## 7. 面试时可以补充的话术

> “这套测试框架不仅支持手动触发和定时触发，还接入了后端项目的 CI/CD。后端项目 develop 分支合并后自动触发 FAT 环境冒烟，master/release 分支合并后触发 UAT 环境关键业务回归。
>
> 实现上我在后端项目的 `.gitlab-ci.yml` 里加了一个 `trigger` job，通过 GitLab Pipeline Trigger API 调用测试框架项目，并通过 `variables[ENV]` 动态传入环境参数。测试报告里也会展示触发来源的项目和 commit。”
