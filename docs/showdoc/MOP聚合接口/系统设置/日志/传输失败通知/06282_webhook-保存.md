---
page_id: "6282"
page_title: "webhook-保存"
item_id: "6"
cat_id: "900"
catalog_path:
  - "系统设置"
  - "日志"
  - "传输失败通知"
author_username: "luobin"
addtime: "2023-01-09 17:15:15"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6282"
---
# webhook-保存

**请求URL：** 
- `/config/webhook/save `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|id|否|Long| 主键|
|webhookCode|否|String| webhook编号|
|webhookName|否|String| webhook名称|
|platformType|否|String| 平台类型 DD-钉钉，FS-飞书，QW-企业微信|
|webhookUrl|否|String| webhook地址|
|webhookSecret|否|String| 密钥|
|signStatus|否|Boolean| 签名状态 true启用 false停用|
|status|否|Boolean| 活跃状态 true启用 false停用|

###请求参数Json格式
 
```
{
 "id" : 0,
 "webhookCode" : "String",
 "webhookName" : "String",
 "platformType" : "String",
 "webhookUrl" : "String",
 "webhookSecret" : "String",
 "signStatus" : true,
 "status" : true
}
```

###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|String| 主数据|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|traceId|否|String| 链路跟踪id|


###返回参数Json格式
 
```
{
 "data" : "String",
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
