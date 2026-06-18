---
page_id: "6022"
page_title: "生成小程序 URL Scheme"
item_id: "6"
cat_id: "785"
catalog_path:
  - "公众号/小程序"
author_username: "jianyuwang@reabam.com"
addtime: "2023-05-04 16:43:22"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6022"
---
# 生成小程序 URL Scheme

**请求URL：** 
- `/wx/generateScheme`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|groupId|否|String||
|type|否|Integer| 类型 0是微信 1是支付宝|
|wxSn|否|String||
|path|否|String||
|id|否|String||

### 请求参数Json格式
 
```
{
 "groupId" : "String",
 "type" : 0,
 "wxSn" : "String",
 "path" : "String",
 "id" : "String"
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|String| 主数据|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|traceId|否|String| 链路跟踪id|


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
