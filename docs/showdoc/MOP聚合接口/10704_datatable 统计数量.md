---
page_id: "10704"
page_title: "datatable 统计数量"
item_id: "6"
cat_id: "0"
catalog_path:
author_username: "admin"
addtime: "2025-11-18 11:18:24"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=10704"
---
# datatable 统计数量
 

**请求URL：** 
- `/dock/third/synchronize/countQty`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|platform|是|Integer| 平台编码，手动传 0 美团 1 饿了么 6 京东|
|status|否|String| 状态 ALL 全部 UNCONNECT 未关联，传空默认取全部|
|companyId|是|String| 门店ID，手动传|
|sword|否|String| 搜索条件|
|createDate|否|Object| 同步时间|
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
 "platform" : 0,
 "status" : "String",
 "companyId" : "String",
 "sword" : "String",
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
|--allQty|否|Long| 全部|
|--unConnectQty|否|Long| 未关联|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : {
 "allQty" : 0,
 "unConnectQty" : 0
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
