---
page_id: "3980"
page_title: "根据specId查询商品清单价"
item_id: "6"
cat_id: "513"
catalog_path:
  - "系统设置"
  - "商品"
  - "商品价签"
author_username: "huayongjin@reabam.com"
addtime: "2021-05-26 13:55:53"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=3980"
---
# 根据specId查询商品清单价等
 

**请求URL：** 
- `/config/mitemPriceTag/searchSpecItemPrice `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|companyId|否|String| 门店商户ID|
|priceListId|否|String| 价格清单id|
|specIdList|否|List| 商品规格id集合|

###请求参数Json格式
 
```
{
 "companyId" : "String",
 "priceListId" : "String",
 "specIdList" : null
}
```

###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List| 主数据|
|--itemId|否|String| 商品ID|
|--itemCode|否|String| 商品编码|
|--itemName|否|String| 商品名称|
|--skuBarcode|否|String| 条码|
|--specId|否|String| 规格ID|
|--specName|否|String| 规格名称|
|--unit|否|String| 单位|
|--specPrice|否|Double| 建议零售价|
|--listPrice|否|Double| 清单价|
|--specifyListPrice|否|Double| 指定清单价|
|--customizePrice1|否|Double| 自定义价格1|
|--customizePrice2|否|Double| 自定义价格2|
|--customizePrice3|否|Double| 自定义价格3|
|--printNumber|否|Double| 打印份数|
|--unitList|否|List| 单位列表|
|----itemId|否|String||
|----specId|否|String||
|----unitId|否|String||
|----unitName|否|String||
|----unitRate|否|Double||
|----costExpressFee|否|Double||
|----expressFee|否|Double||
|----isOrder|否|Object||
|------lowestSetBit|否|Integer||
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|monitorRequestId|否|String| 请求监控ID|


###返回参数Json格式
 
```
{
 "data" : [{
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "skuBarcode" : "String",
 "specId" : "String",
 "specName" : "String",
 "unit" : "String",
 "specPrice" : 0,
 "listPrice" : 0,
 "specifyListPrice" : 0,
 "customizePrice1" : 0,
 "customizePrice2" : 0,
 "customizePrice3" : 0,
 "printNumber" : 0,
 "unitList" : [{
 "itemId" : "String",
 "specId" : "String",
 "unitId" : "String",
 "unitName" : "String",
 "unitRate" : 0,
 "costExpressFee" : 0,
 "expressFee" : 0,
 "isOrder" : {
 "lowestSetBit" : 0
 }
 }]
 }],
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "monitorRequestId" : "String"
}
```
