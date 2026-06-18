---
page_id: "4588"
page_title: "叫号屏刷新推送事件WebSocket"
item_id: "6"
cat_id: "626"
catalog_path:
  - "零售"
  - "餐饮"
author_username: "admin"
addtime: "2021-10-08 16:04:40"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=4588"
---
# 叫号屏刷新推送事件 WebSocket
 

**ACTION：**
- `/retail/queueNumberBoard/refresh`

**推送类型：**
- datagram-message

**推送定位：**
- 智慧收银
- 指定门店

###请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|companyId|是|String|门店ID|
|triggerByOrderNo|是|String|触发刷新的订单号|
|tableNumber|是|String| 牌号/桌号|
|queueNumber|是|String| 取餐码|


###请求参数Json格式
 
```
{
 "companyId" : "String",
 "triggerByOrderNo" : "String",
 "tableNumber" : "String",
 "queueNumber" : "String"
}
```


###注意
广播事件是非可靠的推送事件，所以客户端在断开链接重连时必须调用一次获得叫号屏信息的接口，另外如果在2分钟（阈值可调）没有任何叫号屏刷新事件到达时，应该自动刷新叫号屏；
