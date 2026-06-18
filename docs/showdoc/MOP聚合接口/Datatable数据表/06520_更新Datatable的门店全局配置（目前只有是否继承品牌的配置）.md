---
page_id: "6520"
page_title: "更新Datatable的门店全局配置（目前只有是否继承品牌的配置）"
item_id: "6"
cat_id: "862"
catalog_path:
  - "Datatable数据表"
author_username: "tonyyan"
addtime: "2023-04-04 15:11:03"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=6520"
---
# 更新Datatable的门店全局配置（目前只有是否继承品牌的配置）
 

**请求URL：** 
- `/config/datatable/group/updateCompanySetting/{serviceId}`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|targetId|是|String| datatableId 或者 datatableId # exportId|
|companyId|是|String| 门店ID|
|inheritGroup|是|Boolean| 是否继承品牌|

### 请求参数Json格式
 
```
{
 "targetId" : "String",
 "companyId" : "String",
 "inheritGroup" : true
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object| 主数据|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|traceId|否|String| 链路跟踪id|


### 返回参数Json格式
 
```
{
 "data" : null,
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
