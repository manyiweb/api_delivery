---
page_id: "6239"
page_title: "获得当前品牌是否 使用新的 Datatable 功能"
item_id: "6"
cat_id: "862"
catalog_path:
  - "Datatable数据表"
author_username: "tonyyan"
addtime: "2022-12-28 12:04:05"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6239"
---
# 获得当前品牌是否 使用新的 Datatable 功能
 

**请求URL：** 
- `/config/datatable/switch/getResult`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|datatableId|否|String| 数据表ID|

### 请求参数Json格式
 
```
{
 "datatableId" : "String"
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object| 主数据|
|--usingDatatable|否|Boolean| 是否使用 Datatable|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|traceId|否|String| 链路跟踪id|


### 返回参数Json格式
 
```
{
 "data" : {
 "usingDatatable" : true
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
