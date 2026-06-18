---
page_id: "10294"
page_title: "/b2b/wmc/order/importData"
item_id: "6"
cat_id: "1196"
catalog_path:
  - "订货"
  - "订货设置"
author_username: "admin"
addtime: "2025-08-07 17:51:57"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=10294"
---
# 导入数据

**请求URL：** 
- `/b2b/wmc/order/importData`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|fileUrl|否|String| 导入路径|
|companyList|否|List| 商户列表|
|--companyId|否|String| 商户ID|
|--companyCode|否|String| 商户code|
|--companyName|否|String| 商户名称|
|--merchantsTypeName|否|String| 商户名称|
|--orderTypeCode|否|String| 订单类型code|
|--orderTypeName|否|String| 订单类型名称|
|--orderTypeCodeId|否|String| 订单类型id|
|--orderTypeId|否|Long| 订单类型id|
|--isDef|否|Boolean| 是否默认|
|--deliveryDate|否|DateTime| 配送日期|
|--deliveryDays|否|Integer| 配送日期天数|
|--deliveryType|否|String| 配送方式|
|--deliveryTypeName|否|String| 配送方式名称|
|--itemsMap|否|Map| 商品map|
|itemList|否|List| 商品列表|
|--itemUnit|否|String| 单位|
|--unitRate|否|Double| 单位|
|--quantity|否|Double| 基本数量|
|--itemQuantity|否|Double| 单位数量|
|--itemId|否|String| 商品ID|
|--itemCode|否|String| 商品编码|
|--itemName|否|String| 商品名称|
|--skuBarcode|否|String| 条码|
|--specId|否|String| 规格ID|
|--specName|否|String| 规格名称|
|--validDays|否|Integer| 保质期(天)|
|--itemTypeId|否|String| 商品分类|
|--unit|否|String| 单位(最小单位)|
|--brandName|否|String| 商品品牌名称|
|--isStartBatch|否|Integer| 是否开启批次管理 1是0否|
|--referenceCostPrice|否|Double| 参考成本价|
|--costPrice|否|Double| 成本价|
|--specPrice|否|Double| 规格价|
|--colourName|否|String| 规格一名称|
|--sizeName|否|String| 规格二名称|
|--description|否|String| 规格说明|
|--unitGroupId|否|Long| 单位组id|
|--unitGroupStart|否|Integer| 是否启用单位组 1-启用 0-不启用|

### 请求参数Json格式
 
```
{
 "fileUrl" : "String",
 "companyList" : [{
 "companyId" : "String",
 "companyCode" : "String",
 "companyName" : "String",
 "merchantsTypeName" : "String",
 "orderTypeCode" : "String",
 "orderTypeName" : "String",
 "orderTypeCodeId" : "String",
 "orderTypeId" : 0,
 "isDef" : true,
 "deliveryDate" : "DateTime",
 "deliveryDays" : 0,
 "deliveryType" : "String",
 "deliveryTypeName" : "String",
 "itemsMap" : null
 }],
 "itemList" : [{
 "itemUnit" : "String",
 "unitRate" : 0,
 "quantity" : 0,
 "itemQuantity" : 0,
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "skuBarcode" : "String",
 "specId" : "String",
 "specName" : "String",
 "validDays" : 0,
 "itemTypeId" : "String",
 "unit" : "String",
 "brandName" : "String",
 "isStartBatch" : 0,
 "referenceCostPrice" : 0,
 "costPrice" : 0,
 "specPrice" : 0,
 "colourName" : "String",
 "sizeName" : "String",
 "description" : "String",
 "unitGroupId" : 0,
 "unitGroupStart" : 0
 }]
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|--companyList|否|List| 商户列表|
|----companyId|否|String| 商户ID|
|----companyCode|否|String| 商户code|
|----companyName|否|String| 商户名称|
|----merchantsTypeName|否|String| 商户名称|
|----orderTypeCode|否|String| 订单类型code|
|----orderTypeName|否|String| 订单类型名称|
|----orderTypeCodeId|否|String| 订单类型id|
|----orderTypeId|否|Long| 订单类型id|
|----isDef|否|Boolean| 是否默认|
|----deliveryDate|否|DateTime| 配送日期|
|----deliveryDays|否|Integer| 配送日期天数|
|----deliveryType|否|String| 配送方式|
|----deliveryTypeName|否|String| 配送方式名称|
|----itemsMap|否|Map| 商品map|
|--itemList|否|List| 商品列表|
|----itemUnit|否|String| 单位|
|----unitRate|否|Double| 单位|
|----quantity|否|Double| 基本数量|
|----itemQuantity|否|Double| 单位数量|
|----itemId|否|String| 商品ID|
|----itemCode|否|String| 商品编码|
|----itemName|否|String| 商品名称|
|----skuBarcode|否|String| 条码|
|----specId|否|String| 规格ID|
|----specName|否|String| 规格名称|
|----validDays|否|Integer| 保质期(天)|
|----itemTypeId|否|String| 商品分类|
|----unit|否|String| 单位(最小单位)|
|----brandName|否|String| 商品品牌名称|
|----isStartBatch|否|Integer| 是否开启批次管理 1是0否|
|----referenceCostPrice|否|Double| 参考成本价|
|----costPrice|否|Double| 成本价|
|----specPrice|否|Double| 规格价|
|----colourName|否|String| 规格一名称|
|----sizeName|否|String| 规格二名称|
|----description|否|String| 规格说明|
|----unitGroupId|否|Long| 单位组id|
|----unitGroupStart|否|Integer| 是否启用单位组 1-启用 0-不启用|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : {
 "companyList" : [{
 "companyId" : "String",
 "companyCode" : "String",
 "companyName" : "String",
 "merchantsTypeName" : "String",
 "orderTypeCode" : "String",
 "orderTypeName" : "String",
 "orderTypeCodeId" : "String",
 "orderTypeId" : 0,
 "isDef" : true,
 "deliveryDate" : "DateTime",
 "deliveryDays" : 0,
 "deliveryType" : "String",
 "deliveryTypeName" : "String",
 "itemsMap" : null
 }],
 "itemList" : [{
 "itemUnit" : "String",
 "unitRate" : 0,
 "quantity" : 0,
 "itemQuantity" : 0,
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "skuBarcode" : "String",
 "specId" : "String",
 "specName" : "String",
 "validDays" : 0,
 "itemTypeId" : "String",
 "unit" : "String",
 "brandName" : "String",
 "isStartBatch" : 0,
 "referenceCostPrice" : 0,
 "costPrice" : 0,
 "specPrice" : 0,
 "colourName" : "String",
 "sizeName" : "String",
 "description" : "String",
 "unitGroupId" : 0,
 "unitGroupStart" : 0
 }]
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
