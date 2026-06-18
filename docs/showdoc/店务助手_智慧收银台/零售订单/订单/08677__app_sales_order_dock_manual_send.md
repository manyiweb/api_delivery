---
page_id: "8677"
page_title: "/app/sales/order/dock/manual/send"
item_id: "8"
cat_id: "361"
catalog_path:
  - "零售订单"
  - "订单"
author_username: "admin"
addtime: "2024-08-26 14:47:27"
source_url: "https://showdoc.reabam.com/web/#/8?page_id=8677"
---
# 外卖商家自送出
 

**请求URL：** 
- `/app/sales/order/dock/manual/send`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|orderId|否|String||

### 请求参数Json格式
 
```
{
 "orderId" : "String"
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
