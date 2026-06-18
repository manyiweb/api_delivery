---
page_id: "3879"
page_title: "列表-appcode"
item_id: "6"
cat_id: "490"
catalog_path:
  - "会员"
  - "拉新渠道码"
author_username: "baichenlin@reabam.com"
addtime: "2021-04-27 14:50:55"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=3879"
---
# appcode列表
 

**请求URL：** 
- `/mem/pullnew/appcodes `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|cTypeCode|否|String| 类型编码|

###请求参数Json格式
 
```
{
 "cTypeCode" : "String"
}
```

###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List| 主数据|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|monitorRequestId|否|String| 请求监控ID|


###返回参数Json格式
 
```
{
 "data" : null,
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "monitorRequestId" : "String"
}
```
