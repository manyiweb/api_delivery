---
page_id: "9255"
page_title: "抖音来客绑定accountId"
item_id: "6"
cat_id: "697"
catalog_path:
  - "系统设置"
  - "零售"
  - "外卖管理"
  - "抖音相关"
author_username: "675355567@qq.com"
addtime: "2024-12-25 18:13:12"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=9255"
---
# 抖音来客绑定accountId
 

**请求URL：** 
- `/dock/douyin/shop/bind/account`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|accountId|是|String| 商户id|

### 请求参数Json格式
 
```
{
 "accountId" : "String"
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
