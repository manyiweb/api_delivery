---
page_id: "4994"
page_title: "获取GlueSet配置"
item_id: "6"
cat_id: "115"
catalog_path:
  - "系统设置"
  - "零售"
author_username: "jianyuwang@reabam.com"
addtime: "2022-01-10 21:15:53"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=4994"
---
# 获取牌号设置相关信息
 

**请求URL：** 
- `core-retail/app/Business/getGlueSetInfo `

**请求方式：**
- POST
- RequestBody


###请求参数<业务参数>
 
无参数


###返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|showRecharge|是|Integer|是否展示换旧卡或充值功能 0不展示 1展示
|takeCardNo|是|Integer|获取牌号|
|openCard|是|Integer|按桌号/牌号挂单或取单|
|autoCard|是|Integer|自动编号|

###返回参数Json格式
 
```
{
 "takeCardNo": "0",
 "autoCard": 0,
 "openCard": 0,
 "ErrorCode": "",
 "ResultString": "操作成功",
 "showRecharge": 0,
 "ResultInt": 0
}
```
