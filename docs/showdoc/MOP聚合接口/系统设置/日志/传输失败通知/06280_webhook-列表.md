---
page_id: "6280"
page_title: "webhook-列表"
item_id: "6"
cat_id: "900"
catalog_path:
  - "系统设置"
  - "日志"
  - "传输失败通知"
author_username: "luobin"
addtime: "2023-02-02 10:54:52"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6280"
---
# webhook-列表

**请求URL：** 
- `/config/webhook/list `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|id|否|Long| 主键|
|sword|否|String| 请求参数|
|status|否|Boolean| 启用状态，false停用 true启用|
|pageIndex|否|Integer| 页号|
|pageSize|否|Integer| 页大小|
|orderField|否|String| 商品排序字段|
|orderSort|否|String| 商品排序方式 desc 倒序 asc 正序|

###请求参数Json格式
 
```
{
 "id" : 0,
 "sword" : "String",
 "status" : true,
 "pageIndex" : 0,
 "pageSize" : 0,
 "orderField" : "String",
 "orderSort" : "String"
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
|----id|否|Long| 主键|
|----webhookCode|否|String| webhook编号|
|----webhookName|否|String| webhook名称|
|----platformType|否|String| 平台类型|
|----lastSendTime|否|DateTime| 最后发送时间|
|----webhookUrl|否|String| webhook地址|
|----webhookSecret|否|String| 密钥|
|----signStatus|否|Boolean| 签名状态 true启用 false停用|
|----status|否|Boolean| 活跃状态 true启用 false停用|
|----createName|否|String| 创建人|
|----createDate|否|DateTime| 创建时间|
|----modifyName|否|String| 修改人|
|----modifyDate|否|DateTime| 修改时间|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|traceId|否|String| 链路跟踪id|


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
 "webhookCode" : "String",
 "webhookName" : "String",
 "platformType" : "String",
 "lastSendTime" : "DateTime",
 "webhookUrl" : "String",
 "webhookSecret" : "String",
 "signStatus" : true,
 "status" : true,
 "createName" : "String",
 "createDate" : "DateTime",
 "modifyName" : "String",
 "modifyDate" : "DateTime"
 }]
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
