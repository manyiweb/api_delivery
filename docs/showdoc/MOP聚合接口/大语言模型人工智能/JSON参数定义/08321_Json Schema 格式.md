---
page_id: "8321"
page_title: "Json Schema 格式"
item_id: "6"
cat_id: "1092"
catalog_path:
  - "大语言模型人工智能"
  - "JSON参数定义"
author_username: "tonyyan"
addtime: "2024-05-31 11:15:59"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=8321"
---
# Json Schema 格式


### JSON ARRAY 数组
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|items|是|Object| 字段明细|
|--type|是|String| 类型 例如：string、number、object、array、boolean、integer|
|--description|否|String| 描述|
|type|是|String| 类型 例如：string、number、object、array、boolean、integer|
|description|否|String| 描述|


```
{
 "items" : {
 "type" : "String",
 "description" : "String"
 },
 "type" : "String",
 "description" : "String"
}
```

### JSON Boolean 布尔值
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|type|是|String| 类型 例如：string、number、object、array、boolean、integer|
|description|否|String| 描述|


```
{
 "type" : "String",
 "description" : "String"
}
```

### JSON Numeric 数字类型
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|multipleOf|否|Integer| 倍数|
|maximum|否|Integer| 最大值|
|exclusiveMaximum|否|Boolean| 是否排除最大值|
|minimum|否|Integer| 最小值|
|exclusiveMinimum|否|Boolean| 是否排除最小值|
|type|是|String| 类型 例如：string、number、object、array、boolean、integer|
|description|否|String| 描述|


### 返回参数Json格式
 
```
{
 "multipleOf" : 0,
 "maximum" : 0,
 "exclusiveMaximum" : true,
 "minimum" : 0,
 "exclusiveMinimum" : true,
 "type" : "String",
 "description" : "String"
}
```



### JSON Object 对象
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|properties|否|Map| 属性|
|required|否|List| 必需的属性|
|type|是|String| 类型 例如：string、number、object、array、boolean、integer|
|description|否|String| 描述|


### 返回参数Json格式
 
```
{
 "properties" : {
 		"name" : {
			"type" : "string",
			"description " : "名字"
		}
 },
 "required" : ["name"],
 "type" : "String",
 "description" : "String"
}
```


### JSON String 字符串
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|enumValues|否|List| 枚举值|
|format|否|String| 字符串格式 date-time、email、hostname、ipv4、ipv6、uri、time、date、duration、uuid|
|pattern|否|String| 正则|
|minLength|否|Integer| 最小长度|
|maxLength|否|Integer| 最大长度|
|type|是|String| 类型 例如：string、number、object、array、boolean、integer|
|description|否|String| 描述|


### 返回参数Json格式
 
```
{
 "enumValues" : null,
 "format" : "String",
 "pattern" : "String",
 "minLength" : 0,
 "maxLength" : 0,
 "type" : "String",
 "description" : "String"
}
```
