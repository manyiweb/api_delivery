---
page_id: "8647"
page_title: "消费预警通知webhook-保存"
item_id: "6"
cat_id: "1152"
catalog_path:
  - "零售"
  - "监控预警"
author_username: "675355567@qq.com"
addtime: "2024-08-12 10:31:18"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=8647"
---
# 消费预警通知webhook-保存

**请求URL：** 
- `/config/retail/monitor/webhook/save`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|webhookIds|否|List| webhookId集合|

### 请求参数Json格式
 
```
{
 "webhookIds" : null
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|String||
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : "String",
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
