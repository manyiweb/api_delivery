---
page_id: "7351"
page_title: "第三方平台webhookt通知设置-查询列表"
item_id: "6"
cat_id: "1021"
catalog_path:
  - "零售"
  - "三方对接"
author_username: "chenjiaxing@reabam.com"
addtime: "2023-12-20 15:47:23"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=7351"
---
# 第三方平台webhookt通知设置-查询列表
 服务：reabam-extension-front
 

**请求URL：** 
- `/extension/platform/webhook/getAll`

**请求方式：**
- POST
- FormData


### 请求参数<业务参数>
 
无参数


### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List||
|--id|否|Long||
|--createId|否|String||
|--createName|否|String||
|--createDate|否|DateTime||
|--groupId|否|String||
|--webhookId|否|Long| webhookId|
|--webhookCode|否|String| webhook编号|
|--webhookName|否|String| webhook名称|
|--status|否|Boolean| 活跃状态 true启用 false停用|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : [{
 "id" : 0,
 "createId" : "String",
 "createName" : "String",
 "createDate" : "DateTime",
 "groupId" : "String",
 "webhookId" : 0,
 "webhookCode" : "String",
 "webhookName" : "String",
 "status" : true
 }],
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
