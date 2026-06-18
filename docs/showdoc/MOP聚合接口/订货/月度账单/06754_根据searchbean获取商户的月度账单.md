---
page_id: "6754"
page_title: "根据searchbean获取商户的月度账单"
item_id: "6"
cat_id: "943"
catalog_path:
  - "订货"
  - "月度账单"
author_username: "admin"
addtime: "2024-09-26 10:26:08"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6754"
---
# 根据searchbean获取商户的月度账单
 

**请求URL：** 
- `/b2b/monthAccount/order/list/searchbean`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|orderId|否|Long| 主键|
|companyId|是|String| 商户id|
|monthAccountOrderId|否|String| 账单单号|
|monthAccountDate|否|DateTime| 账期|
|beginMonthAccountDate|否|DateTime| 范围查询 起始账期|
|endMonthAccountDate|否|DateTime| 范围查询 截至账期|
|monthAccountState|否|Integer| 分类查询 账单状态 0待确认 1已确认|
|billType|否|Integer| 格式类型|
|sword|否|String||
|tokenId|否|String||
|id|否|String||
|orderField|否|String||
|orderSort|否|String||
|searchBeans|否|List||
|--typeCode|否|String||
|--typeName|否|String||
|--dataType|否|String||
|--isSingle|否|String||
|--isLikeSearch|否|String||
|--items|否|List||
|----itemName|否|String||
|----itemValue|否|String||
|----minValue|否|String||
|----maxValue|否|String||
|----isCustom|否|String||
|----isRange|否|String||
|----isSelect|否|String||
|--current|否|Object||
|----itemName|否|String||
|----itemValue|否|String||
|----minValue|否|String||
|----maxValue|否|String||
|----isCustom|否|String||
|----isRange|否|String||
|----isSelect|否|String||
|--sword|否|String||
|--pageIndex|否|Integer||
|--pageSize|否|Integer||
|--curPageNum|否|Integer||
|--totalPage|否|Integer||
|--totalCount|否|Integer||
|status|否|Integer||
|pageIndex|否|Integer||
|pageSize|否|Integer||
|orderField|否|String||
|orderSort|否|String||

### 请求参数Json格式
 
```
{
 "orderId" : 0,
 "companyId" : "String",
 "monthAccountOrderId" : "String",
 "monthAccountDate" : "DateTime",
 "beginMonthAccountDate" : "DateTime",
 "endMonthAccountDate" : "DateTime",
 "monthAccountState" : 0,
 "billType" : 0,
 "sword" : "String",
 "tokenId" : "String",
 "id" : "String",
 "orderField" : "String",
 "orderSort" : "String",
 "searchBeans" : [{
 "typeCode" : "String",
 "typeName" : "String",
 "dataType" : "String",
 "isSingle" : "String",
 "isLikeSearch" : "String",
 "items" : [{
 "itemName" : "String",
 "itemValue" : "String",
 "minValue" : "String",
 "maxValue" : "String",
 "isCustom" : "String",
 "isRange" : "String",
 "isSelect" : "String"
 }],
 "current" : {
 "itemName" : "String",
 "itemValue" : "String",
 "minValue" : "String",
 "maxValue" : "String",
 "isCustom" : "String",
 "isRange" : "String",
 "isSelect" : "String"
 },
 "sword" : "String",
 "pageIndex" : 0,
 "pageSize" : 0,
 "curPageNum" : 0,
 "totalPage" : 0,
 "totalCount" : 0
 }],
 "status" : 0,
 "pageIndex" : 0,
 "pageSize" : 0,
 "orderField" : "String",
 "orderSort" : "String"
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|--pageIndex|否|Integer||
|--pageSize|否|Integer||
|--pageCount|否|Integer||
|--totalCount|否|Long||
|--first|否|Boolean||
|--last|否|Boolean||
|--content|否|List||
|----id|否|Long| 主键|
|----createDate|否|DateTime| 创建时间|
|----companyId|否|String| 商户id|
|----monthAccountOrderId|否|String| 账单单号|
|----monthAccountDate|否|DateTime| 账期|
|----monthAccountState|否|Integer| 账单状态 0为待确认 1为已确认|
|----monthAccountStateStr|否|String||
|----lastMonthSum|否|Double| 该账单时间的上个月账单金额|
|----afterMonthSum|否|Double| 累计金额这个月的金额|
|----confirmDate|否|DateTime| 确认时间|
|----confirmUserId|否|String| 确认人|
|----confirmUserName|否|String| 确认人|
|----billType|否|Integer| 账单类型1 格式1 2 格式2|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : {
 "pageIndex" : 0,
 "pageSize" : 0,
 "pageCount" : 0,
 "totalCount" : 0,
 "first" : true,
 "last" : true,
 "content" : [{
 "id" : 0,
 "createDate" : "DateTime",
 "companyId" : "String",
 "monthAccountOrderId" : "String",
 "monthAccountDate" : "DateTime",
 "monthAccountState" : 0,
 "monthAccountStateStr" : "String",
 "lastMonthSum" : 0,
 "afterMonthSum" : 0,
 "confirmDate" : "DateTime",
 "confirmUserId" : "String",
 "confirmUserName" : "String",
 "billType" : 0
 }]
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
