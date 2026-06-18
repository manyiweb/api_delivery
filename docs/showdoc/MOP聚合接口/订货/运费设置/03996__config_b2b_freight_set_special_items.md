---
page_id: "3996"
page_title: "/config/b2b/freight/set/special/items"
item_id: "6"
cat_id: "517"
catalog_path:
  - "订货"
  - "运费设置"
author_username: "alexli@reabam.com"
addtime: "2021-05-26 16:54:39"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=3996"
---
# 分页查询指定线路 订单运费-特殊运费列表
 

**请求URL：** 
- `/config/b2b/freight/set/special/items `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|id|否|String| 业务ID|
|tokenId|否|String| 用户标识|
|pageIndex|否|Integer| 分页页码|
|pageSize|否|Integer| 分页大小|
|sword|否|String| 搜索关键字|

###请求参数Json格式
 
```
{
 "id" : "String",
 "tokenId" : "String",
 "pageIndex" : 0,
 "pageSize" : 0,
 "sword" : "String"
}
```

###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object| 主数据|
|--pageIndex|否|Integer| 页码|
|--pageSize|否|Integer| 显示记录数|
|--pageCount|否|Integer| 总页数|
|--totalCount|否|Long| 总记录数|
|--first|否|Boolean| 首页|
|--last|否|Boolean| 尾页|
|--content|否|List| 分页数据|
|----id|否|Long| ID|
|----lineId|否|String| 线路ID|
|----itemId|否|String| 商品id|
|----itemCode|否|String| 商品编码|
|----itemName|否|String| 商品名称|
|----specId|否|String| 规格id|
|----specName|否|String| 规格名称|
|----skuBarcode|否|String| sku码|
|----costFreight|否|Double| 成本运费|
|----freight|否|Double| 运费|
|----itemNameFull|否|String| 商品名称|
|----createId|否|String| 创建人id|
|----createName|否|String| 创建人|
|----createDate|否|DateTime| 创建时间|
|----modifyId|否|String| 修改人id|
|----modifyName|否|String| 修改人|
|----modifyDate|否|DateTime| 修改时间|
|----dbKey|否|Integer| 分库标识|
|----groupId|否|String| 品牌商id|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|monitorRequestId|否|String| 请求监控ID|


###返回参数Json格式
 
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
 "lineId" : "String",
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "specId" : "String",
 "specName" : "String",
 "skuBarcode" : "String",
 "costFreight" : 0,
 "freight" : 0,
 "itemNameFull" : "String",
 "createId" : "String",
 "createName" : "String",
 "createDate" : "DateTime",
 "modifyId" : "String",
 "modifyName" : "String",
 "modifyDate" : "DateTime",
 "dbKey" : 0,
 "groupId" : "String"
 }]
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "monitorRequestId" : "String"
}
```
