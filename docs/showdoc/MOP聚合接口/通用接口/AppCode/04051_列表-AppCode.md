---
page_id: "4051"
page_title: "列表-AppCode"
item_id: "6"
cat_id: "531"
catalog_path:
  - "通用接口"
  - "AppCode"
author_username: "chongwulin@reabam.com"
addtime: "2021-06-10 13:46:57"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=4051"
---
# 列表-AppCode

**请求URL：** 
- `/config/appCode/v2/list `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|optionName|否|String| 配置编码|
|companyId|否|String| 门店标识|

###请求参数Json格式
 
```
{
 "optionName" : "String",
 "companyId" : "String"
}
```

###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|List| 主数据|
|--fid|否|String| 主键标识|
|--version|否|Integer| 版本号|
|--optionName|否|String| 配置选项|
|--code|否|String| 配置选项值编码|
|--content|否|String| 配置选项值内容|
|--memo|否|String| 扩展配置选项|
|--extinfo|否|String| 扩展配置选项|
|--extinfo2|否|String| 扩展配置选项|
|--extinfo3|否|String| 扩展配置选项|
|--extinfo4|否|String| 扩展配置选项|
|--extinfo5|否|String| 扩展配置选项|
|--orderNo|否|Double| 扩展配置选项|
|--extvalue|否|Double| 扩展配置选项|
|--extvalue2|否|Double| 扩展配置选项|
|--extvalue3|否|Double| 扩展配置选项|
|--extvalue4|否|Double| 扩展配置选项|
|--extvalue5|否|Double| 扩展配置选项|
|--extimage|否|String| 扩展配置选项|
|--isvalid|否|Integer| 是否可用，取值：1 - 是，0-否|
|--upLoadFile|否|String| 扩展配置选项|
|--extinfo6|否|String| 扩展配置选项|
|--extinfo7|否|String| 扩展配置选项|
|--extvalue6|否|Double| 扩展配置选项|
|--extvalue7|否|Double| 扩展配置选项|
|--companyId|否|String| 门店商户ID，与商户表syscompany相关联|
|--createDate|否|DateTime| 创建时间|
|--createName|否|String| 创建人名称|
|--createId|否|String| 创建人ID|
|--exception1|否|Integer| 业务扩展字段,不存在数据库|
|--exception2|否|Integer| 业务扩展字段,不存在数据库|
|--allowDelete|否|Integer||
|--extendedParams|否|Map||
|--dbKey|否|Integer| 分库标识|
|--groupId|否|String| 品牌商id|
|msg|否|String| 消息|
|code|否|String| 业务代码|
|exceptionStackInfo|否|String| 异常堆栈信息|
|monitorRequestId|否|String| 请求监控ID|


###返回参数Json格式
 
```
{
 "data" : [{
 "fid" : "String",
 "version" : 0,
 "optionName" : "String",
 "code" : "String",
 "content" : "String",
 "memo" : "String",
 "extinfo" : "String",
 "extinfo2" : "String",
 "extinfo3" : "String",
 "extinfo4" : "String",
 "extinfo5" : "String",
 "orderNo" : 0,
 "extvalue" : 0,
 "extvalue2" : 0,
 "extvalue3" : 0,
 "extvalue4" : 0,
 "extvalue5" : 0,
 "extimage" : "String",
 "isvalid" : 0,
 "upLoadFile" : "String",
 "extinfo6" : "String",
 "extinfo7" : "String",
 "extvalue6" : 0,
 "extvalue7" : 0,
 "companyId" : "String",
 "createDate" : "DateTime",
 "createName" : "String",
 "createId" : "String",
 "exception1" : 0,
 "exception2" : 0,
 "allowDelete" : 0,
 "extendedParams" : null,
 "dbKey" : 0,
 "groupId" : "String"
 }],
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "monitorRequestId" : "String"
}
```
