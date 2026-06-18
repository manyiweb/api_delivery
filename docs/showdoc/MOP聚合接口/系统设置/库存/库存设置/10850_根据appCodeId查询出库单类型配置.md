---
page_id: "10850"
page_title: "根据appCodeId查询出库单类型配置"
item_id: "6"
cat_id: "135"
catalog_path:
  - "系统设置"
  - "库存"
  - "库存设置"
author_username: "tonyyan"
addtime: "2026-01-06 15:05:32"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=10850"
---
# 根据appCodeId查询出库单类型配置
 

**请求URL：** 
- `/config/whsTypeConfig/query/getWhsOutTypeConfig`

**请求方式：** 
- `POST`
- `RequestBody`


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|appCodeId|是|String| appcode配置ID|

### 请求参数Json格式
 
```
{
 "appCodeId":"String"
}
```

### 响应参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|--appCodeId|否|String| appcode 配置ID|
|--enableDepartmentFillIn|否|Boolean| 是否启用部门填入|
|--requiredDepartmentFillIn|否|Boolean| 部门填入是否必填|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 响应参数Json格式
 
```
{
 "data":{
 "appCodeId":"String",
 "enableDepartmentFillIn":true,
 "requiredDepartmentFillIn":true
 },
 "msg":"String",
 "code":"String",
 "exceptionStackInfo":"String",
 "traceId":"String"
}
```
