---
page_id: "7352"
page_title: "三方平台webhookt通知设置-保存"
item_id: "6"
cat_id: "1021"
catalog_path:
  - "零售"
  - "三方对接"
author_username: "chenjiaxing@reabam.com"
addtime: "2023-12-25 17:18:35"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=7352"
---
# 三方平台webhookt通知设置-保存
 服务：reabam-extension-front
 

**请求URL：** 
- `/extension/platform/webhook/save`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|webhookIds|是|List||

### 请求参数Json格式
 
```
{
 "webhookIds" : null
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : null,
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
