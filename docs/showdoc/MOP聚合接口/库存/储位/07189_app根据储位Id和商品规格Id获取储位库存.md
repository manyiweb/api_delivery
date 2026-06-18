---
page_id: "7189"
page_title: "app根据储位Id和商品规格Id获取储位库存"
item_id: "6"
cat_id: "409"
catalog_path:
  - "库存"
  - "储位"
author_username: "weiqisu@reabam.com"
addtime: "2023-10-24 16:27:36"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=7189"
---
# app根据储位Id和商品规格Id获取储位库存

**请求URL：** 
- `/warehouse/location/app/location/item/stockQty`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|storeLocationId|是|Long| 储位Id|
|specIds|是|List| 规格Id|

### 请求参数Json格式
 
```
{
 "storeLocationId" : 0,
 "specIds" : null
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List||
|--storeLocationId|否|Long| 储位Id|
|--specId|否|String| 规格Id|
|--quantity|否|Double| 数量|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : [{
 "storeLocationId" : 0,
 "specId" : "String",
 "quantity" : 0
 }],
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
