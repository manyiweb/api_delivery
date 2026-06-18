---
page_id: "8588"
page_title: "/config/b2b/refundWay/getV2"
item_id: "6"
cat_id: "87"
catalog_path:
  - "系统设置"
author_username: "admin"
addtime: "2024-07-24 13:52:39"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=8588"
---
# 获取订货设置退款方式

**请求URL：** 
- `/config/b2b/refundWay/getV2`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|refundTypeId|否|Long| 退款类型id|
|companyId|否|String| 门店id|

### 请求参数Json格式
 
```
{
 "refundTypeId" : 0,
 "companyId" : "String"
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List||
|--customPay|否|Boolean| 是否自定义账户支付|
|--refundWayName|否|String| 退款方式名称|
|--refundWayCode|否|String| 退款方式编码|
|--rebateAccountRecordId|否|Long| 自定义账户id|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : [{
 "customPay" : true,
 "refundWayName" : "String",
 "refundWayCode" : "String",
 "rebateAccountRecordId" : 0
 }],
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
