---
page_id: "6279"
page_title: "传输失败通知webhook-列表"
item_id: "6"
cat_id: "900"
catalog_path:
  - "系统设置"
  - "日志"
  - "传输失败通知"
author_username: "luobin"
addtime: "2023-01-11 16:19:00"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6279"
---
# 传输失败通知webhook-列表

**请求URL：** 
- `/config/transfer/failed/notice/webhook/list `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|noticeId|否|Long| 传输失败通知主键|

###请求参数Json格式
 
```
{
 "noticeId" : 0
}
```

###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List| 主数据|
|--id|否|Long| 主键|
|--noticeId|否|Long| 传输失败通知id|
|--webhookId|否|Long| webhookId|
|--webhookCode|否|String| webhook编号|
|--webhookName|否|String| webhook名称|
|--status|否|Boolean| 活跃状态 true启用 false停用|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|traceId|否|String| 链路跟踪id|


###返回参数Json格式
 
```
{
 "data" : [{
 "id" : 0,
 "noticeId" : 0,
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
