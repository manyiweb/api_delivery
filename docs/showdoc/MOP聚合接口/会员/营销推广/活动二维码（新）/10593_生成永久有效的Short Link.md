---
page_id: "10593"
page_title: "生成永久有效的Short Link"
item_id: "6"
cat_id: "1339"
catalog_path:
  - "会员"
  - "营销推广"
  - "活动二维码（新）"
author_username: "admin"
addtime: "2025-10-27 16:49:26"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=10593"
---
# 生成永久有效的Short Link

**请求URL：** 
- `/config/activities/share/v2/createPermanentShortLink`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|id|是|Long||
|sword|否|String||

### 请求参数Json格式
 
```
{
 "id" : 0,
 "sword" : "String"
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
