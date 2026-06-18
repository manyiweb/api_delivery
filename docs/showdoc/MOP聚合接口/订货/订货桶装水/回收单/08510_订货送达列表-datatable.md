---
page_id: "8510"
page_title: "订货送达列表-datatable"
item_id: "6"
cat_id: "1112"
catalog_path:
  - "订货"
  - "订货桶装水"
  - "回收单"
author_username: "admin"
addtime: "2024-07-09 16:36:11"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=8510"
---
# 订货送达列表

**请求URL：** 
- `/b2b/delivery/list/{source}`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|ordStatus|否|List| 单据状态 S0已送达 S1部分送达 S2未送达|
|companyId|否|String| 门店id|
|deliveryDate|否|Object| 到货日期|
|--start|否|DateTime||
|--end|否|DateTime||
|createDate|否|Object| 创建日期|
|--start|否|DateTime||
|--end|否|DateTime||
|id|否|String||
|pageSize|否|Integer||
|pageNo|否|Integer||
|sortField|否|String||
|sortDirection|否|String||
|viewId|否|String||

### 请求参数Json格式
 
```
{
 "ordStatus" : null,
 "companyId" : "String",
 "deliveryDate" : {
 "start" : "DateTime",
 "end" : "DateTime"
 },
 "createDate" : {
 "start" : "DateTime",
 "end" : "DateTime"
 },
 "id" : "String",
 "pageSize" : 0,
 "pageNo" : 0,
 "sortField" : "String",
 "sortDirection" : "String",
 "viewId" : "String"
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|--content|否|List||
|----orderId|否|String| 主键id|
|----ordCode|否|String| 单据号|
|----orderStatusCode|否|String| 单据状态|
|----orderStatusName|否|String| 单据状态名称|
|----orderTypeName|否|String| 单据类型|
|----companyId|否|String| 订货商户id|
|----cardName|否|String| 订货商户名称|
|----cardCode|否|String| 订货商户编码|
|----realTotal|否|Double| 单据实付金额|
|----needsCount|否|Double| 订单数量|
|----receiveQuantity|否|Double| 送达总数|
|----readyToDeliverQuantity|否|Double| 待送数量|
|----deliveryDate|否|DateTime| 到货日期|
|----conAddress|否|String| 收货地址|
|----remark|否|String| 备注|
|----deliveryPersonnelId|否|String| 配送员id|
|----deliveryPersonnelName|否|String| 配送员名称|
|----createDate|否|DateTime| 创建时间|
|----createName|否|String| 创建人|
|--pageSize|否|Integer||
|--pageNo|否|Integer||
|--total|否|Long||
|--totalPage|否|Integer||
|--hasNextPage|否|Boolean||
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : {
 "content" : [{
 "orderId" : "String",
 "ordCode" : "String",
 "orderStatusCode" : "String",
 "orderStatusName" : "String",
 "orderTypeName" : "String",
 "companyId" : "String",
 "cardName" : "String",
 "cardCode" : "String",
 "realTotal" : 0,
 "needsCount" : 0,
 "receiveQuantity" : 0,
 "readyToDeliverQuantity" : 0,
 "deliveryDate" : "DateTime",
		 "conAddress" : "String",
 "remark" : "String",
 "deliveryPersonnelId" : "String",
 "deliveryPersonnelName" : "String",
 "createDate" : "DateTime",
 "createName" : "String"
 }],
 "pageSize" : 0,
 "pageNo" : 0,
 "total" : 0,
 "totalPage" : 0,
 "hasNextPage" : true
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
