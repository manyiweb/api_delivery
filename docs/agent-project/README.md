# agent 项目 GitLab CI/CD 配置说明（无单元测试版本）

本文档逐段解释 `docs/agent-project/.gitlab-ci.yml` 为什么这么写，适合没有做过 CI/CD 的同学阅读。

---

## 一、这份配置解决了什么问题？

假设场景：

> **你修改了 agent 项目代码，push 到 develop 分支后，希望自动完成：**
> 1. **编译构建**
> 2. **部署到 FAT 测试环境**
> 3. **确认服务真的可用了**
> 4. **触发 `api-auto-test` 项目跑接口自动化冒烟测试**

很多老项目或业务驱动项目**没有单元测试**（或覆盖率极低），所以这份配置**去掉了 test 阶段**，重点展示：

```
build → deploy → health-check → trigger-api-tests
```

这样的流水线在面试时反而更真实——国内企业里大量后端项目就是这样的现状。

---

## 二、什么是 `.gitlab-ci.yml`？

`.gitlab-ci.yml` 是 GitLab CI/CD 的配置文件，放在项目根目录。

GitLab 每次检测到代码提交（push / MR）时，会读取这个文件，按照里面的定义自动执行一系列任务（job）。

一个 `.gitlab-ci.yml` 里通常包含：

| 概念 | 作用 | 类比 |
|---|---|---|
| `workflow` | 决定整条流水线什么时候执行 | 总开关 |
| `variables` | 定义全局变量 | 全局常量 |
| `stages` | 定义流水线的阶段顺序 | 工序流程 |
| `job` | 每个具体执行的任务 | 一道工序 |
| `image` | 这个 job 用什么 Docker 镜像运行 | 工具箱 |
| `script` | 具体执行的命令 | 操作步骤 |
| `needs` | 定义 job 之间的依赖关系 | 前置条件 |
| `rules` | 决定这个 job 在什么条件下执行 | 分支判断 |
| `artifacts` | 把产物传给后面的 job | 传送带 |

---

## 三、逐段解释

### 1. `workflow` —— 流水线的总开关

```yaml
workflow:
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH =~ /^release\//'
```

**作用**：只有 `main`、`develop`、`release/*` 分支的提交才会触发流水线。

**为什么这样写**：
- 开发者每天在 `feature/xxx` 分支上会有很多次 push，如果每次都跑部署和接口测试，非常浪费资源。
- 只有合并到主干分支（develop/main/release）时，才需要完整验证。

> `$CI_COMMIT_BRANCH` 是 GitLab 自动提供的预置变量，表示当前提交所在的分支。

---

### 2. `variables` —— 全局变量

```yaml
variables:
  FAT_HEALTH_URL: "http://fat-pos.example.com:60030/api/health"
  UAT_HEALTH_URL: "https://pos.example.com/api/health"
  IMAGE_TAG: "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
```

**作用**：定义一些全局可用的值，方便下面各个 job 引用。

**为什么这样写**：
- `FAT_HEALTH_URL` / `UAT_HEALTH_URL`：健康检查地址，后面 health_check job 会用到。
- `IMAGE_TAG`：镜像标签，用 GitLab 容器仓库地址 + 短 commit ID，保证每次部署的镜像唯一且可追溯。

> `$CI_REGISTRY_IMAGE` 和 `$CI_COMMIT_SHORT_SHA` 也是 GitLab 预置变量。

---

### 3. `stages` —— 阶段顺序

```yaml
stages:
  - build
  - deploy
  - health-check
  - trigger-api-tests
```

**作用**：定义流水线有几个阶段，以及执行顺序。

**为什么这样设计**：

| 阶段 | 目的 |
|---|---|
| build | 先编译打包 |
| deploy | 构建通过后再部署 |
| health-check | 部署完确认服务可用 |
| trigger-api-tests | 最后才触发接口自动化 |

这个顺序体现了 CI/CD 的**快速失败**原则：
- 如果 build 失败，后面都不跑
- 如果服务没起来，不触发接口测试

---

### 4. `build` job —— 编译

```yaml
build:
  stage: build
  image: node:20-alpine
  script:
    - echo "开始构建 agent 项目..."
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
      - node_modules/
    expire_in: 1 hour
```

**作用**：编译 agent 项目。

**关键点**：
- `image: node:20-alpine`：用 Node.js 20 镜像运行。如果你的后端是 Java/Go/Python，换成对应镜像。
- `npm ci`：比 `npm install` 更适合 CI，会严格按 `package-lock.json` 安装。
- `artifacts`：把 `dist/` 和 `node_modules/` 传给后面的 job，避免重复安装和构建。

---

### 5. `deploy` job —— 部署

```yaml
deploy:
  stage: deploy
  image: alpine/k8s:latest
  needs:
    - job: build
  variables:
    DEPLOY_ENV: "fat"
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
      variables:
        DEPLOY_ENV: "fat"
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH =~ /^release\//'
      variables:
        DEPLOY_ENV: "uat"
  script:
    - echo "部署到 $DEPLOY_ENV 环境..."
```

**作用**：把服务部署到测试环境。

**关键点**：
- `image: alpine/k8s:latest`：包含 kubectl/helm，适合 K8s 部署。如果你用 Docker Compose 或脚本部署，换对应镜像。
- `needs: [build]`：必须等 build 成功才部署。
- `rules` 里的 `variables`：根据分支动态设置 `DEPLOY_ENV`。
  - `develop` → `fat`
  - `main` / `release/*` → `uat`
- `script` 里的 `echo` 是占位符，你需要换成真实部署命令，比如：
  ```bash
  docker build -t $IMAGE_TAG .
  docker push $IMAGE_TAG
  kubectl set image deployment/agent agent=$IMAGE_TAG -n $DEPLOY_ENV
  ```

---

### 6. `health_check` job —— 健康检查（最重要）

```yaml
health_check:
  stage: health-check
  image: curlimages/curl:latest
  needs:
    - job: deploy
  variables:
    HEALTH_URL: "$FAT_HEALTH_URL"
    TEST_ENV: "fat"
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
      variables:
        HEALTH_URL: "$FAT_HEALTH_URL"
        TEST_ENV: "fat"
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH =~ /^release\//'
      variables:
        HEALTH_URL: "$UAT_HEALTH_URL"
        TEST_ENV: "uat"
  script:
    - |
      for i in $(seq 1 30); do
        if curl -sf "$HEALTH_URL" > /dev/null; then
          echo "✅ 服务已就绪"
          exit 0
        fi
        echo "⏳ 第 $i 次检查未通过，10秒后重试..."
        sleep 10
      done
      exit 1
```

**作用**：等待服务真正可用。

**为什么必须有这一步**：
- `deploy` job 执行完，只代表“部署命令发过去了”。
- 容器启动、数据库连接、缓存预热、注册中心上报都需要时间。
- 如果这时立刻跑接口自动化，会有一堆 500/502/连接超时。

**实现原理**：
- 用 curl 轮询健康检查接口，最多尝试 30 次，每次间隔 10 秒。
- 如果服务返回 200，立刻退出并标记成功。
- 如果 5 分钟内都没成功，标记失败，流水线停止，不会触发接口测试。

**健康接口建议**：
- 优先用真实的 `/health` 接口。
- 如果没有，可以用一个稳定的只读接口代替，比如 `GET /api/xxx` 只要返回非 5xx 就说明服务活了。

---

### 7. `trigger_api_auto_tests` job —— 跨项目触发

```yaml
trigger_api_auto_tests:
  stage: trigger-api-tests
  image: curlimages/curl:latest
  needs:
    - job: health_check
  variables:
    TEST_ENV: "fat"
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
      variables:
        TEST_ENV: "fat"
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_COMMIT_BRANCH =~ /^release\//'
      variables:
        TEST_ENV: "uat"
  script:
    - |
      curl -X POST \
        -F token="$API_AUTO_TEST_TRIGGER_TOKEN" \
        -F ref=master \
        -F "variables[ENV]=$TEST_ENV" \
        -F "variables[TRIGGER_SOURCE_PROJECT]=$CI_PROJECT_PATH" \
        -F "variables[TRIGGER_SOURCE_COMMIT]=$CI_COMMIT_SHORT_SHA" \
        -F "variables[TRIGGER_SOURCE_BRANCH]=$CI_COMMIT_REF_NAME" \
        "https://gitlab.com/api/v4/projects/$API_AUTO_TEST_PROJECT_ID/trigger/pipeline"
```

**作用**：调用 `api-auto-test` 项目的 GitLab Trigger API，让它开始跑接口测试。

**关键点**：
- `needs: [health_check]`：必须等健康检查通过才执行。
- `-F token=...`：Trigger Token，需要在 agent 项目的 CI/CD Variables 里配置。
- `-F ref=master`：触发 api-auto-test 的 master 分支。
- `-F "variables[ENV]=..."`：把环境变量传给 api-auto-test，这样它就知道跑 FAT 还是 UAT。
- `TRIGGER_SOURCE_*`：把触发来源信息传过去，方便在 Allure 报告里展示。

---

## 四、你需要配置哪些变量？

在 agent 项目 **Settings → CI/CD → Variables** 中添加：

| 变量名 | 是否 Mask | 说明 |
|---|---|---|
| `API_AUTO_TEST_TRIGGER_TOKEN` | ✅ 是 | 从 api-auto-test 项目复制的 trigger token |
| `API_AUTO_TEST_PROJECT_ID` | 否 | api-auto-test 项目的数字 ID |
| `FAT_HEALTH_URL` | 否 | FAT 环境健康检查地址 |
| `UAT_HEALTH_URL` | 否 | UAT 环境健康检查地址 |

---

## 五、如何拿到 api-auto-test 的 trigger token 和项目 ID？

1. 打开 `https://gitlab.com/my-ci-lab1/api-auto-test`
2. 项目首页右侧找到 **Project ID**，复制数字
3. 进入 **Settings → CI/CD → Pipeline triggers**
4. 点击 **Add trigger**，输入描述如 `agent-project-trigger`
5. 复制生成的 token

---

## 六、完整执行流程

以 `develop` 分支提交为例：

```
push 代码到 develop
        ↓
    GitLab 读取 .gitlab-ci.yml
        ↓
    build 阶段：编译 agent 项目
        ↓
    deploy 阶段：部署到 FAT 环境
        ↓
    health-check 阶段：轮询 FAT_HEALTH_URL，最多等 5 分钟
        ↓
    trigger-api-tests 阶段：调用 api-auto-test trigger API，传入 ENV=fat
        ↓
    api-auto-test 项目开始跑 unit → smoke/critical → Allure 报告 → 企业微信通知
```

---

## 七、常见问题

### Q1：没有单元测试会不会被面试官质疑？

不会。你可以这样解释：

> “这个 agent 项目是我用来演示跨项目 CI/CD 触发流程的 demo。真实企业里很多老项目确实单元测试覆盖率低，我这边先保证构建、部署、健康检查、接口自动化这套链路跑通。后续如果要真正落地，会在 build 和 deploy 之间补单元测试门禁。”

### Q2：健康检查接口应该返回什么？

最简单的是返回 HTTP 200：

```json
{"status": "ok"}
```

如果没有 `/health`，可以用任何稳定的只读接口，只要返回非 5xx 就行。

### Q3：如果 agent 项目只是 demo，不真部署怎么办？

把 `deploy` 和 `health_check` 阶段简化：

```yaml
deploy:
  stage: deploy
  image: alpine:latest
  script:
    - echo "模拟部署到 $DEPLOY_ENV"

health_check:
  stage: health-check
  image: curlimages/curl:latest
  needs: [deploy]
  script:
    - echo "模拟健康检查通过"
```

这样也能完整演示 CI/CD 流程。

---

## 八、面试时可以这样说

> "agent 项目提交后，CI 会按 build → deploy → health-check → trigger-api-tests 的顺序执行。
>
> 这里最关键的是 health-check 阶段。因为部署命令执行完不代表服务真的可用了，容器启动、数据库连接、缓存预热都需要时间。我会轮询健康检查接口，最多等 5 分钟，服务返回 200 之后才触发下游的接口自动化测试，避免服务没起来就跑测试导致大量 500。
>
> 环境选择通过分支规则实现：develop 对应 FAT，main/release 对应 UAT。触发 api-auto-test 时通过 variables[ENV] 把环境参数传过去。"
