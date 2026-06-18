---
page_id: "8965"
page_title: "外卖订单传输日志失败通知webhook-保存"
item_id: "6"
cat_id: "900"
catalog_path:
  - "系统设置"
  - "日志"
  - "传输失败通知"
author_username: "admin"
addtime: "2024-10-28 18:12:53"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=8965"
---
# 外卖订单传输日志失败通知webhook-保存

**请求URL：** 
- `/config/dock/order/failed/notice/webhook/save`

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
