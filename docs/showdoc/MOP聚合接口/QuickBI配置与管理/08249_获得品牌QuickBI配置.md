---
page_id: "8249"
page_title: "获得品牌QuickBI配置"
item_id: "6"
cat_id: "1076"
catalog_path:
  - "QuickBI配置与管理"
author_username: "tonyyan"
addtime: "2024-07-23 09:42:19"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=8249"
---
# 获得品牌QuickBI配置
 

**请求URL：** 
- `/quickbi/setup/getGroupSetup`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|groupId|否|String| 品牌ID|

### 请求参数Json格式
 
```
{
 "groupId" : "String"
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|--setupId|否|Long| 设置记录ID|
|--dataPortalUrl|否|String| 品牌中台门户URL|
|--dataPortalId|否|String| 品牌中台门户ID|
|--workspaceId|否|String| 品牌中台工作空间ID|
|--groupId|否|String| 品牌ID|
|--guideDataPortalUrl|否|String| 店务助手门户URL|
|--guideDataPortalId|否|String| 店务助手门户ID|
|--analysisDataPortalUrl|否|String| 分析端门户URL|
|--analysisDataPortalId|否|String| 分析端门户ID|
|--analysisIndexUrl|否|String| 首页URL|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : {
 "setupId" : 0,
 "dataPortalUrl" : "String",
 "dataPortalId" : "String",
 "workspaceId" : "String",
 "groupId" : "String",
 "guideDataPortalUrl" : "String",
 "guideDataPortalId" : "String",
 "analysisDataPortalUrl" : "String",
 "analysisDataPortalId" : "String",
 "analysisIndexUrl" : "String"
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
