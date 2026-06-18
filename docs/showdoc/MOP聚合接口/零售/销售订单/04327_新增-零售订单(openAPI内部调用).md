---
page_id: "4327"
page_title: "新增-零售订单(openAPI内部调用)"
item_id: "6"
cat_id: "158"
catalog_path:
  - "零售"
  - "销售订单"
author_username: "675355567@qq.com"
addtime: "2023-11-07 15:08:43"
source_url: "https://showdoc.reabam.com/web/#/6?page_id=4327"
---
# openAPI新增订单

**请求URL：** 
- `/app/sales/order/dock/rpc/add`

**请求方式：**
- POST
- RequestBody


### 请求参数<业务参数>
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|docType|否|String| 单据业务类型编码，为空时默认为零售:Booking("预售"),Retail("零售"),Wx("商城销售"),Integral("积分兑换"),CreditSale("赊销")|
|orderDocType|否|String| 单据类型编码，为空时默认为零售:Booking("预售"),Retail("零售"),Wx("商城销售"),Integral("积分兑换"),CreditSale("赊销"),MeiTuan("美团"),Ele("饿了么"),Meal("点单订单");|
|orderDocTypeName|否|String| 单据类型名称|
|deliveryType|否|String| 提货方式，为空时默认为到店自提 xcth("到店自提"),shsm("快递配送")|
|deliveryExpressType|否|Integer| 快递配送方式 0默认快递配送 1同城配送|
|autoDelivery|否|Boolean| 是否自动配送|
|companyId|否|String| 门店标识 美团ePoiId|
|companyName|否|String| 门店名|
|deliveryWarehouseName|否|String| 发货仓库店名|
|deliveryCompanyName|否|String| 发货店名|
|groupId|否|String| 品牌标识|
|dockOrderId|否|String| 外卖订单标识 美团orderId|
|dockOrderNo|否|String| 外卖订单号 美团orderIdView|
|remark|否|String| 外卖订单备注 美团caution|
|createDate|否|DateTime| 订单时间 美团ctime(时间戳，需反算日期)|
|modifyDate|否|DateTime| 订单时间 美团utime(时间戳，需反算日期)|
|delivery|否|Object| 配送信息|
|--dinnersNumber|否|Integer| 预计用餐人数(-1) 用餐人数 用餐人数（0：用户没有选择用餐人数；1-10：用户选择的用餐人数；-10：10人以上用餐；88：用户需要餐具；99：用户不需要餐具），该信息默认不推送，如有需求可在开发者中心订阅|
|--deliveryTime|否|DateTime| 用户预计送达时间 美团deliveryTime(时间戳，需反算)|
|--provinceCode|否|String| 省级编码|
|--provinceName|否|String| 省份|
|--cityCode|否|String| 市级编码|
|--cityName|否|String| 城市|
|--regionCode|否|String| 区级编码|
|--regionName|否|String| 区|
|--recipientAddress|否|String| 收货地址|
|--recipientName|否|String| 收货人|
|--recipientPhone|否|String| 收货人电话|
|--backupRecipientPhone|否|String| 备份隐私号|
|--shipperPhone|否|String| 配送员电话|
|--shippingFee|否|Double| 配送费|
|--dockShippingFee|否|Double| 外部配送费(仅记录，Dorder不记录也不计算运费，仅DorderDock记录外部配送费用)|
|--isSelfShipping|否|Boolean| true： 商家自主配送 false：第三方配送 没有配置，即默认为：第三方配送|
|--takeTimeQuantums|否|String| 提货配送时间段|
|orderAmount|否|Double| 订单金额 美团originalPrice|
|realOrderAmount|否|Double| 用户实际支付金额 美团total|
|products|否|List| 商品列表|
|--specId|否|String| 商品规格ID 美团sku_id ERP商品ID|
|--salesPrice|否|Double| 商品单价/销售价 美团price|
|--salesPriceAmount|否|Double| 销售行小计|
|--productType|否|String| 商品类型|
|--totalRealAmount|否|Double| 行实付金额 美团自行计算结果|
|--quantity|否|Double| 数量|
|--unit|否|String| 单位|
|--discount|否|Double| 商品折扣 美团food_discount|
|--packingCharge|否|Double| 包装费小计 美团box_price*box_num|
|--packingQuantity|否|Double| 包装个数|
|--dockItemId|否|String| 外卖商品ID 美团mt_spu_id|
|--dockSpecId|否|String| 外卖规格ID 美团mt_sku_id|
|--remark|否|String| 行备注|
|--batchList|否|List| 批次信息|
|----batchCode|否|String| 批次号|
|----productionDate|否|DateTime| 生产日期|
|----quantity|否|Double| 出库数量|
|----specId|否|String| 商品规格ID|
|----validDays|否|Integer| 保质期|
|----sourceDocItemId|否|String| 来源单据明细行ID|
|--barcodeList|否|List| 唯一码信息|
|----barcode|否|String| 唯一码|
|----attachBarcode|否|String| 附加码|
|----attrs|否|List| 唯一码属性|
|------attrId|否|String| 唯一id|
|------code|否|Integer| 编码|
|------alias|否|String| 别名|
|------value|否|String| 值|
|------isRequired|否|Integer| 是否必填 1 - 必填, 0 - 不必填|
|------valueType|否|Integer| 0 任何值 1 序列|
|------content|否|String| 内容值,多个值时|
|------contentArr|否|Object||
|----isOpenUniqueCodeAttr|否|Integer| 启用唯一码属性- 行业属性|
|----specId|否|String| 规格ID|
|----remark|否|String| 唯一码备注|
|----mentityCardsResult|否|Object||
|------mid|否|String||
|------denomination|否|Double| 面额|
|------salesAdvice|否|Double| 售价|
|--shopCartItemType|否|Integer| 购物车Item类型 0-普通 2-行自定义优惠 7自定义套餐|
|--thirdProductName|否|String| 第三方商品名称|
|--thirdProductTagName|否|String| 第三方商品标签名称|
|--thirdProductLineId|否|String| 第三方商品行标识|
|--attributes|否|List| 第三方菜品属性名称（用于匹配标签）|
|--isGift|否|Boolean| 是否赠品 true是 false否|
|--searchBarcode|否|String| 目前快麦用于存储商品tid|
|--isCustomSuit|否|Boolean| 是否为自定义套装|
|--customSuitPorudctDTOS|否|List| 自定义套装商品|
|----splitPriceAmount|否|Double| 套餐商品的平摊金额：优惠券分摊的金额|
|----mianProduct|否|Boolean| 是否为主商品|
|----specId|否|String| 商品规格ID 美团sku_id ERP商品ID|
|----salesPrice|否|Double| 商品单价/销售价 美团price|
|----salesPriceAmount|否|Double| 商品单价/销售价行小计|
|----totalRealAmount|否|Double| 行实付金额 美团自行计算结果|
|----quantity|否|Double| 数量|
|----unit|否|String| 单位|
|----dockItemId|否|String| 外卖商品ID 美团mt_spu_id|
|----dockSpecId|否|String| 外卖规格ID 美团mt_sku_id|
|----remark|否|String| 行备注|
|----batchList|否|List| 批次信息|
|------batchCode|否|String| 批次号|
|------productionDate|否|DateTime| 生产日期|
|------quantity|否|Double| 出库数量|
|------specId|否|String| 商品规格ID|
|------validDays|否|Integer| 保质期|
|------sourceDocItemId|否|String| 来源单据明细行ID|
|----barcodeList|否|List| 唯一码信息|
|------barcode|否|String| 唯一码|
|------attachBarcode|否|String| 附加码|
|------attrs|否|List| 唯一码属性|
|--------attrId|否|String| 唯一id|
|--------code|否|Integer| 编码|
|--------alias|否|String| 别名|
|--------value|否|String| 值|
|--------isRequired|否|Integer| 是否必填 1 - 必填, 0 - 不必填|
|--------valueType|否|Integer| 0 任何值 1 序列|
|--------content|否|String| 内容值,多个值时|
|--------contentArr|否|Object||
|------isOpenUniqueCodeAttr|否|Integer| 启用唯一码属性- 行业属性|
|------specId|否|String| 规格ID|
|------remark|否|String| 唯一码备注|
|------mentityCardsResult|否|Object||
|--------mid|否|String||
|--------denomination|否|Double| 面额|
|--------salesAdvice|否|Double| 售价|
|----thirdProductName|否|String| 第三方商品名称|
|----thirdProductTagName|否|String| 第三方商品标签名称|
|----thirdProductLineId|否|String| 第三方商品行标识|
|----attributes|否|List| 第三方菜品属性名称（用于匹配标签）|
|----packingCharge|否|Double| 商品包装费(小计)|
|----packingQuantity|否|Double| 商品包装数量|
|----deductionAmount|否|Double| 折扣金额|
|--cartId|否|Integer| 口袋号|
|discounts|否|List| 外卖优惠列表|
|--thirdType|否|String| 第三方优惠活动类型|
|--remark|否|String| 优惠说明|
|--compAmount|否|Double| 商户承担金额|
|--thirdAmount|否|Double| 第三方承担金额|
|--acId|否|String| 活动ID，有就填|
|--deliveryFeeDiscount|否|Boolean| 是否为运费承担|
|specifyOrderStatus|否|String| 指定订单状态|
|commission|否|Double| 佣金|
|dockCompAddress|否|String| 门店地址(外卖需传)|
|taskId|否|Long| 任务处理状态id|
|memberId|否|String| 会员id|
|staffId|否|String| 导购id|
|billDay|否|Integer| 账期（赊销类型时必传）|
|isPay|否|Boolean| 是否支付(不传则默认使用现金支付)|
|payParam|否|Object| 支付对象|
|--offlinePayParameter|否|Object| 线下支付参数|
|----guestPayment|否|Double| 客付款|
|----guestPaymentInOtherCurrency|否|Double| 客付款-非主货币|
|----changePayment|否|Double| 找零|
|----changePaymentInOtherCurrency|否|Double| 找零-非主货币|
|----unionPayCode|否|String| 银联/通联/刷卡支付，支付编码，刷卡支付旧编码为：cardNumber|
|----sumiPayParameter|否|Object| 在线刷卡|
|------transactionDate|否|String| 交易日期|
|------referenceNo|否|String| 参考编号|
|----cardNo|否|String| 实体卡券号|
|----cardNoList|否|List| 实体卡券批量支持 券号列表|
|----microPayParameter|否|Object| 刷卡支付参数|
|------authCode|否|String| 支付授权码|
|------attach|否|String| 附加值 微信原生反扫支付attach=WXPAY|
|------serialNum|否|String| 收银终端mac地址|
|----payChannelCode|否|String| 支付渠道 -> WXP微信(默认值) ALP支付宝 YLP云闪付|
|----groupCouponCode|否|String| 团购券编码(美团团购支付必填)|
|----groupCouponUseQty|否|Integer| 团购券使用张数|
|----customizePayUseQty|否|Integer| 自定义金额支付使用张数|
|----items|否|List| 商品信息|
|------id|否|String| 购物车行id|
|------suitType|否|Integer| 套餐类型|
|------suitSpecId|否|String| 套餐规格id 如果不是套餐传普通商品规格id|
|------itemId|否|String| 商品id|
|------itemCode|否|String| 商品编码|
|------itemName|否|String| 商品名称|
|------specId|否|String| 规格id|
|------skuBarcode|否|String| sku|
|------specName|否|String| 规格名称|
|------quantity|否|Double| 数量|
|------realPrice|否|Double| 商品单价|
|------totalRealPrice|否|Double| 商品实付总价|
|------totalPaidAmount|否|Double| 商品已付金额|
|------seriesId|否|String| 系列id|
|------brandId|否|String| 品牌id|
|------itemTypeIds|否|List| 分类id|
|------suitQuantity|否|Double| 套餐数量|
|------entityCardDiscountAmount|否|Double| 实体卡支付折扣优惠|
|------payRate|否|Double| 支付比例|
|----specialFastThPay|否|Object| 快速订单第三方支付|
|------dgatheringId|否|String| 收银记录表行id|
|----version|否|String| 版本|
|----realCreateDate|否|DateTime| 实际支付时间(允许为空，为空时默认取服务端当前时间)|
|----speedOfflineOrder|否|Object| 无来源订单参数|
|------memberId|否|String| 会员id|
|------realMoney|否|Double| 订单实付总金额|
|------items|否|List| 商品信息|
|--------id|否|String| 购物车行id|
|--------suitType|否|Integer| 套餐类型|
|--------suitSpecId|否|String| 套餐规格id 如果不是套餐传普通商品规格id|
|--------itemId|否|String| 商品id|
|--------itemCode|否|String| 商品编码|
|--------itemName|否|String| 商品名称|
|--------specId|否|String| 规格id|
|--------skuBarcode|否|String| sku|
|--------specName|否|String| 规格名称|
|--------quantity|否|Double| 数量|
|--------realPrice|否|Double| 商品单价|
|--------totalRealPrice|否|Double| 商品实付总价|
|--------totalPaidAmount|否|Double| 商品已付金额|
|--------seriesId|否|String| 系列id|
|--------brandId|否|String| 品牌id|
|--------itemTypeIds|否|List| 分类id|
|--------suitQuantity|否|Double| 套餐数量|
|--------entityCardDiscountAmount|否|Double| 实体卡支付折扣优惠|
|--------payRate|否|Double| 支付比例|
|------fastPayInfoJson|否|String| 离线版支付后参数信息|
|------haveUseCustomDiscount|否|Boolean| 是否有用行优惠或者自定义折扣|
|------haveUsePromotion|否|Boolean| 是否有用促销|
|------haveUseCoupon|否|Boolean| 是否有用券|
|------haveUseMemberPrice|否|Boolean| 是否有使用会员价|
|--openId|否|String||
|--wxSn|否|String||
|--groupId|否|String||
|--tradeNo|否|String| 外部单号(MOP给外部)|
|--notCheckCustomPay|否|Boolean| 不用校验自定义收银设置|
|--controllerSource|否|String| 支付入口|
|--payType|是|String| 支付方式|
|--orderType|是|String| 订单类型，order订单 card储值卡充值单 memberBenefitBuyOrder会员权益充值单|
|--orderId|是|String| 订单标识|
|--orderNo|否|String| 订单编码|
|--payAmount|是|Double| 支付金额|
|--currencyId|否|String| 货币id|
|--exchangeRate|否|Double| 汇率|
|--currencyScale|否|Integer| 货币保留小数位|
|--smallestSize|否|Double| 最小币值|
|--orderPrepay|否|Boolean| 下订单预先支付|
|--entityCardPayDetail|否|Map| 实体卡券对订单行的支付明细（每行支付多少钱）|
|--groupId|否|String| 品牌id|
|--benefitsPayParameter|否|Object| 会员权益支付参数|
|----payPwdType|否|String| 密码验证类型，Password支付密码 Captcha手机验证码 QrCode会员二维码|
|----payPwd|否|String| 支付密码|
|----fromUser|否|Integer| 是否为用户选择，fromUser=1代表需要验证会员身份|
|--statementId|否|Long| 结算单标识|
|--postingDate|否|DateTime| 指定过账时间|
|--remark|否|String| 支付备注|
|--payDate|否|DateTime| 指定过账时间|
|--offlineCashierType|否|Integer| 收银类型|
|--memberBenefitsVerify|否|DateTime| 购物车会员权益验证时间|
|--merchantNo|否|String| 支付的商户号|
|--tradeNo|否|String| 外部单号(MOP给外部)|
|--useStoredValueCardDiscount|否|Boolean| 是否享用储值卡折扣优惠|
|--replaceSysNo|否|String| 用于支持点单商城访问会员商城接口|
|--requestId|否|String| 收银请求id|
|payParamList|否|List| 支付对象列表|
|--offlinePayParameter|否|Object| 线下支付参数|
|----guestPayment|否|Double| 客付款|
|----guestPaymentInOtherCurrency|否|Double| 客付款-非主货币|
|----changePayment|否|Double| 找零|
|----changePaymentInOtherCurrency|否|Double| 找零-非主货币|
|----unionPayCode|否|String| 银联/通联/刷卡支付，支付编码，刷卡支付旧编码为：cardNumber|
|----sumiPayParameter|否|Object| 在线刷卡|
|------transactionDate|否|String| 交易日期|
|------referenceNo|否|String| 参考编号|
|----cardNo|否|String| 实体卡券号|
|----cardNoList|否|List| 实体卡券批量支持 券号列表|
|----microPayParameter|否|Object| 刷卡支付参数|
|------authCode|否|String| 支付授权码|
|------attach|否|String| 附加值 微信原生反扫支付attach=WXPAY|
|------serialNum|否|String| 收银终端mac地址|
|----payChannelCode|否|String| 支付渠道 -> WXP微信(默认值) ALP支付宝 YLP云闪付|
|----groupCouponCode|否|String| 团购券编码(美团团购支付必填)|
|----groupCouponUseQty|否|Integer| 团购券使用张数|
|----customizePayUseQty|否|Integer| 自定义金额支付使用张数|
|----items|否|List| 商品信息|
|------id|否|String| 购物车行id|
|------suitType|否|Integer| 套餐类型|
|------suitSpecId|否|String| 套餐规格id 如果不是套餐传普通商品规格id|
|------itemId|否|String| 商品id|
|------itemCode|否|String| 商品编码|
|------itemName|否|String| 商品名称|
|------specId|否|String| 规格id|
|------skuBarcode|否|String| sku|
|------specName|否|String| 规格名称|
|------quantity|否|Double| 数量|
|------realPrice|否|Double| 商品单价|
|------totalRealPrice|否|Double| 商品实付总价|
|------totalPaidAmount|否|Double| 商品已付金额|
|------seriesId|否|String| 系列id|
|------brandId|否|String| 品牌id|
|------itemTypeIds|否|List| 分类id|
|------suitQuantity|否|Double| 套餐数量|
|------entityCardDiscountAmount|否|Double| 实体卡支付折扣优惠|
|------payRate|否|Double| 支付比例|
|----specialFastThPay|否|Object| 快速订单第三方支付|
|------dgatheringId|否|String| 收银记录表行id|
|----version|否|String| 版本|
|----realCreateDate|否|DateTime| 实际支付时间(允许为空，为空时默认取服务端当前时间)|
|----speedOfflineOrder|否|Object| 无来源订单参数|
|------memberId|否|String| 会员id|
|------realMoney|否|Double| 订单实付总金额|
|------items|否|List| 商品信息|
|--------id|否|String| 购物车行id|
|--------suitType|否|Integer| 套餐类型|
|--------suitSpecId|否|String| 套餐规格id 如果不是套餐传普通商品规格id|
|--------itemId|否|String| 商品id|
|--------itemCode|否|String| 商品编码|
|--------itemName|否|String| 商品名称|
|--------specId|否|String| 规格id|
|--------skuBarcode|否|String| sku|
|--------specName|否|String| 规格名称|
|--------quantity|否|Double| 数量|
|--------realPrice|否|Double| 商品单价|
|--------totalRealPrice|否|Double| 商品实付总价|
|--------totalPaidAmount|否|Double| 商品已付金额|
|--------seriesId|否|String| 系列id|
|--------brandId|否|String| 品牌id|
|--------itemTypeIds|否|List| 分类id|
|--------suitQuantity|否|Double| 套餐数量|
|--------entityCardDiscountAmount|否|Double| 实体卡支付折扣优惠|
|--------payRate|否|Double| 支付比例|
|------fastPayInfoJson|否|String| 离线版支付后参数信息|
|------haveUseCustomDiscount|否|Boolean| 是否有用行优惠或者自定义折扣|
|------haveUsePromotion|否|Boolean| 是否有用促销|
|------haveUseCoupon|否|Boolean| 是否有用券|
|------haveUseMemberPrice|否|Boolean| 是否有使用会员价|
|--openId|否|String||
|--wxSn|否|String||
|--groupId|否|String||
|--tradeNo|否|String| 外部单号(MOP给外部)|
|--notCheckCustomPay|否|Boolean| 不用校验自定义收银设置|
|--controllerSource|否|String| 支付入口|
|--payType|是|String| 支付方式|
|--orderType|是|String| 订单类型，order订单 card储值卡充值单 memberBenefitBuyOrder会员权益充值单|
|--orderId|是|String| 订单标识|
|--orderNo|否|String| 订单编码|
|--payAmount|是|Double| 支付金额|
|--currencyId|否|String| 货币id|
|--exchangeRate|否|Double| 汇率|
|--currencyScale|否|Integer| 货币保留小数位|
|--smallestSize|否|Double| 最小币值|
|--orderPrepay|否|Boolean| 下订单预先支付|
|--entityCardPayDetail|否|Map| 实体卡券对订单行的支付明细（每行支付多少钱）|
|--groupId|否|String| 品牌id|
|--benefitsPayParameter|否|Object| 会员权益支付参数|
|----payPwdType|否|String| 密码验证类型，Password支付密码 Captcha手机验证码 QrCode会员二维码|
|----payPwd|否|String| 支付密码|
|----fromUser|否|Integer| 是否为用户选择，fromUser=1代表需要验证会员身份|
|--statementId|否|Long| 结算单标识|
|--postingDate|否|DateTime| 指定过账时间|
|--remark|否|String| 支付备注|
|--payDate|否|DateTime| 指定过账时间|
|--offlineCashierType|否|Integer| 收银类型|
|--memberBenefitsVerify|否|DateTime| 购物车会员权益验证时间|
|--merchantNo|否|String| 支付的商户号|
|--tradeNo|否|String| 外部单号(MOP给外部)|
|--useStoredValueCardDiscount|否|Boolean| 是否享用储值卡折扣优惠|
|--replaceSysNo|否|String| 用于支持点单商城访问会员商城接口|
|--requestId|否|String| 收银请求id|
|couponTable|否|Object| 优惠券|
|createId|否|String| 创建人ID|
|createName|否|String| 创建人名称|
|orderCreateDate|否|DateTime| 自定义订单创建时间|
|expressFeeNoTotal|否|Boolean| 运费不累计在实收金额|
|hasCustomDiscount|否|Boolean| 是否一口价|
|specifyItemTotalRealAmount|否|Boolean| 是否指定行实收总价|
|takeOutDTO|否|Object| 外卖参数|
|--daySeq|否|String| 订单流水号|
|--orderMode|否|Integer| 订单模式 0顾客模式 1商家模式|
|--userPayAmount|否|Double| 用户实际支付金额|
|--companyIncomeAmount|否|Double| 店铺实收|
|platformType|否|Integer| 平台类型 0-美团 1-饿了么 2-快麦 3-openapi|
|orderType|否|Integer| 第三方销售订单类型快麦:1-货到付款;3-平台订单;4-线下订单;6-预售订单;7-合并订单;8-拆分订单; 9-加急订单;10-空包订单;11-合单提示;12-门店订单;13-换货订单;14-补发订单; 16-海外仓订单;17-Lazada;18-报损单;19-领用单;20-调整单;21-客户订单;22-天猫直送;23-平台预售;24-京东直发;33-分销订单;34-供销订单;35-京配订单;36-平台分销;99-出库单;|
|performanceServiceFee|否|Double| 履约服务费|
|technicalServiceFee|否|Double| 技术服务费|
|timeIntervalMarkUpFee|否|Double| 时段服务费|
|distanceIncreaseFee|否|Double| 距离加价费|
|pricePremiums|否|Double| 价格加价|
|coldBoxFee|否|Double| 冷链加价费|
|sourceOrder|否|Object| 原订单数据|
|isBook|否|Boolean| 是否为预订单|
|outSysName|否|String| 外部系统名称|
|outOrderNo|否|String| 外部系统单号,建议与dockOrderNo同值|
|outQueueNumber|否|String| 外部取单号|
|thMemberCoupons|否|List| 第三方会员优惠券|
|--id|否|Long| 购物车id|
|--couponAmount|否|Double| 优惠券优惠金额|
|--couponSku|否|String| 优惠券SKU|
|--couponId|否|String| 优惠券ID|
|--title|否|String| 优惠券标题|
|--couponType|否|Integer| 商品券类型，取值：0 - 现金券，1 - 折扣券，2 - 兑换券 ,3 - 运费券, 4-其他|
|--templeId|否|String| 模板id|
|--sourceType|否|Integer| 第三方优惠券的原始类型|
|--couponTypeName|否|String| 优惠券类型名称|
|--channel|否|String| 渠道|
|--billingKind|否|String| 财务属性编码|
|speedOrderDiscountSplits|否|List| 优惠平摊数据|
|--thirdProductLineId|否|String| 第三方订单商品行标识|
|--id|否|Long| 购物车订单行(开放API不用填)|
|--skuBarCode|否|String| 商品SKU编码|
|--itemTotalCount|否|Integer| 订单行总数量|
|--itemSplitCount|否|Integer| 本次被分摊商品数量|
|--splitPriceAmount|否|Double| 本次被分摊商品金额|
|--salePriceAmount|否|Double| 销售金额|
|--deductionAmount|否|Double| 参与抵扣的金额|
|--splitType|否|Integer| 分摊类型：1-优惠券 2-平台券 3-订单促销 4-整单优惠 5、标记支付 6-抹零|
|--spiltSource|否|String| 分摊来源（根据不同分摊类型，记录对应业务的唯一编码）：优惠券-券码 平台券-券码 促销-促销编码|
|--channel|否|Integer| 渠道 0：自营 1：美团 2：抖音 3：口碑(默认0)|
|--activityId|否|String| 活动id 平台券：券模板id、企迈券：券模板id、促销：促销编码|
|--activityName|否|String| 活动名称 平台券：券模板名称、企迈券：券模板名称、促销：促销名称|
|--remark|否|String| 备注|
|--billingKind|否|String| 财务属性编码|
|blessing|否|Object| 祝福语 (外卖)|
|--giverPhone|否|String| 赠送人手机号|
|--greeting|否|String| 祝福语|
|identityCard|否|String| 身份证号|
|name|否|String| 名称|


### 请求参数Json格式
 
```
{
 "docType" : "String",
 "orderDocType" : "String",
 "orderDocTypeName" : "String",
 "deliveryType" : "String",
 "deliveryExpressType" : 0,
 "autoDelivery" : true,
 "companyId" : "String",
 "companyName" : "String",
 "deliveryWarehouseName" : "String",
 "deliveryCompanyName" : "String",
 "groupId" : "String",
 "dockOrderId" : "String",
 "dockOrderNo" : "String",
 "remark" : "String",
 "createDate" : "DateTime",
 "modifyDate" : "DateTime",
 "delivery" : {
 "dinnersNumber" : 0,
 "deliveryTime" : "DateTime",
 "provinceCode" : "String",
 "provinceName" : "String",
 "cityCode" : "String",
 "cityName" : "String",
 "regionCode" : "String",
 "regionName" : "String",
 "recipientAddress" : "String",
 "recipientName" : "String",
 "recipientPhone" : "String",
 "backupRecipientPhone" : "String",
 "shipperPhone" : "String",
 "shippingFee" : 0,
 "dockShippingFee" : 0,
 "isSelfShipping" : true,
 "takeTimeQuantums" : "String"
 },
 "orderAmount" : 0,
 "realOrderAmount" : 0,
 "products" : [{
 "specId" : "String",
 "salesPrice" : 0,
 "salesPriceAmount" : 0,
 "productType" : "String",
 "totalRealAmount" : 0,
 "quantity" : 0,
 "unit" : "String",
 "discount" : 0,
 "packingCharge" : 0,
 "packingQuantity" : 0,
 "dockItemId" : "String",
 "dockSpecId" : "String",
 "remark" : "String",
 "batchList" : [{
 "batchCode" : "String",
 "productionDate" : "DateTime",
 "quantity" : 0,
 "specId" : "String",
 "validDays" : 0,
 "sourceDocItemId" : "String"
 }],
 "barcodeList" : [{
 "barcode" : "String",
 "attachBarcode" : "String",
 "attrs" : [{
 "attrId" : "String",
 "code" : 0,
 "alias" : "String",
 "value" : "String",
 "isRequired" : 0,
 "valueType" : 0,
 "content" : "String",
 "contentArr" : null
 }],
 "isOpenUniqueCodeAttr" : 0,
 "specId" : "String",
 "remark" : "String",
 "mentityCardsResult" : {
 "mid" : "String",
 "denomination" : 0,
 "salesAdvice" : 0
 }
 }],
 "shopCartItemType" : 0,
 "thirdProductName" : "String",
 "thirdProductTagName" : "String",
 "thirdProductLineId" : "String",
 "attributes" : null,
 "isGift" : true,
 "searchBarcode" : "String",
 "isCustomSuit" : true,
 "customSuitPorudctDTOS" : [{
 "splitPriceAmount" : 0,
 "mianProduct" : true,
 "specId" : "String",
 "salesPrice" : 0,
 "salesPriceAmount" : 0,
 "totalRealAmount" : 0,
 "quantity" : 0,
 "unit" : "String",
 "dockItemId" : "String",
 "dockSpecId" : "String",
 "remark" : "String",
 "batchList" : [{
 "batchCode" : "String",
 "productionDate" : "DateTime",
 "quantity" : 0,
 "specId" : "String",
 "validDays" : 0,
 "sourceDocItemId" : "String"
 }],
 "barcodeList" : [{
 "barcode" : "String",
 "attachBarcode" : "String",
 "attrs" : [{
 "attrId" : "String",
 "code" : 0,
 "alias" : "String",
 "value" : "String",
 "isRequired" : 0,
 "valueType" : 0,
 "content" : "String",
 "contentArr" : null
 }],
 "isOpenUniqueCodeAttr" : 0,
 "specId" : "String",
 "remark" : "String",
 "mentityCardsResult" : {
 "mid" : "String",
 "denomination" : 0,
 "salesAdvice" : 0
 }
 }],
 "thirdProductName" : "String",
 "thirdProductTagName" : "String",
 "thirdProductLineId" : "String",
 "attributes" : null,
 "packingCharge" : 0,
 "packingQuantity" : 0,
 "deductionAmount" : 0
 }],
 "cartId" : 0
 }],
 "discounts" : [{
 "thirdType" : "String",
 "remark" : "String",
 "compAmount" : 0,
 "thirdAmount" : 0,
 "acId" : "String",
 "deliveryFeeDiscount" : true
 }],
 "specifyOrderStatus" : "String",
 "commission" : 0,
 "dockCompAddress" : "String",
 "taskId" : 0,
 "memberId" : "String",
 "staffId" : "String",
 "billDay" : 0,
 "isPay" : true,
 "payParam" : {
 "offlinePayParameter" : {
 "guestPayment" : 0,
 "guestPaymentInOtherCurrency" : 0,
 "changePayment" : 0,
 "changePaymentInOtherCurrency" : 0,
 "unionPayCode" : "String",
 "sumiPayParameter" : {
 "transactionDate" : "String",
 "referenceNo" : "String"
 },
 "cardNo" : "String",
 "cardNoList" : null,
 "microPayParameter" : {
 "authCode" : "String",
 "attach" : "String",
 "serialNum" : "String"
 },
 "payChannelCode" : "String",
 "groupCouponCode" : "String",
 "groupCouponUseQty" : 0,
 "customizePayUseQty" : 0,
 "items" : [{
 "id" : "String",
 "suitType" : 0,
 "suitSpecId" : "String",
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "specId" : "String",
 "skuBarcode" : "String",
 "specName" : "String",
 "quantity" : 0,
 "realPrice" : 0,
 "totalRealPrice" : 0,
 "totalPaidAmount" : 0,
 "seriesId" : "String",
 "brandId" : "String",
 "itemTypeIds" : null,
 "suitQuantity" : 0,
 "entityCardDiscountAmount" : 0,
 "payRate" : 0
 }],
 "specialFastThPay" : {
 "dgatheringId" : "String"
 },
 "version" : "String",
 "realCreateDate" : "DateTime",
 "speedOfflineOrder" : {
 "memberId" : "String",
 "realMoney" : 0,
 "items" : [{
 "id" : "String",
 "suitType" : 0,
 "suitSpecId" : "String",
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "specId" : "String",
 "skuBarcode" : "String",
 "specName" : "String",
 "quantity" : 0,
 "realPrice" : 0,
 "totalRealPrice" : 0,
 "totalPaidAmount" : 0,
 "seriesId" : "String",
 "brandId" : "String",
 "itemTypeIds" : null,
 "suitQuantity" : 0,
 "entityCardDiscountAmount" : 0,
 "payRate" : 0
 }],
 "fastPayInfoJson" : "String",
 "haveUseCustomDiscount" : true,
 "haveUsePromotion" : true,
 "haveUseCoupon" : true,
 "haveUseMemberPrice" : true
 }
 },
 "openId" : "String",
 "wxSn" : "String",
 "groupId" : "String",
 "tradeNo" : "String",
 "notCheckCustomPay" : true,
 "controllerSource" : "String",
 "payType" : "String",
 "orderType" : "String",
 "orderId" : "String",
 "orderNo" : "String",
 "payAmount" : 0,
 "currencyId" : "String",
 "exchangeRate" : 0,
 "currencyScale" : 0,
 "smallestSize" : 0,
 "orderPrepay" : true,
 "entityCardPayDetail" : null,
 "groupId" : "String",
 "benefitsPayParameter" : {
 "payPwdType" : "String",
 "payPwd" : "String",
 "fromUser" : 0
 },
 "statementId" : 0,
 "postingDate" : "DateTime",
 "remark" : "String",
 "payDate" : "DateTime",
 "offlineCashierType" : 0,
 "memberBenefitsVerify" : "DateTime",
 "merchantNo" : "String",
 "tradeNo" : "String",
 "useStoredValueCardDiscount" : true,
 "replaceSysNo" : "String",
 "requestId" : "String"
 },
 "payParamList" : [{
 "offlinePayParameter" : {
 "guestPayment" : 0,
 "guestPaymentInOtherCurrency" : 0,
 "changePayment" : 0,
 "changePaymentInOtherCurrency" : 0,
 "unionPayCode" : "String",
 "sumiPayParameter" : {
 "transactionDate" : "String",
 "referenceNo" : "String"
 },
 "cardNo" : "String",
 "cardNoList" : null,
 "microPayParameter" : {
 "authCode" : "String",
 "attach" : "String",
 "serialNum" : "String"
 },
 "payChannelCode" : "String",
 "groupCouponCode" : "String",
 "groupCouponUseQty" : 0,
 "customizePayUseQty" : 0,
 "items" : [{
 "id" : "String",
 "suitType" : 0,
 "suitSpecId" : "String",
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "specId" : "String",
 "skuBarcode" : "String",
 "specName" : "String",
 "quantity" : 0,
 "realPrice" : 0,
 "totalRealPrice" : 0,
 "totalPaidAmount" : 0,
 "seriesId" : "String",
 "brandId" : "String",
 "itemTypeIds" : null,
 "suitQuantity" : 0,
 "entityCardDiscountAmount" : 0,
 "payRate" : 0
 }],
 "specialFastThPay" : {
 "dgatheringId" : "String"
 },
 "version" : "String",
 "realCreateDate" : "DateTime",
 "speedOfflineOrder" : {
 "memberId" : "String",
 "realMoney" : 0,
 "items" : [{
 "id" : "String",
 "suitType" : 0,
 "suitSpecId" : "String",
 "itemId" : "String",
 "itemCode" : "String",
 "itemName" : "String",
 "specId" : "String",
 "skuBarcode" : "String",
 "specName" : "String",
 "quantity" : 0,
 "realPrice" : 0,
 "totalRealPrice" : 0,
 "totalPaidAmount" : 0,
 "seriesId" : "String",
 "brandId" : "String",
 "itemTypeIds" : null,
 "suitQuantity" : 0,
 "entityCardDiscountAmount" : 0,
 "payRate" : 0
 }],
 "fastPayInfoJson" : "String",
 "haveUseCustomDiscount" : true,
 "haveUsePromotion" : true,
 "haveUseCoupon" : true,
 "haveUseMemberPrice" : true
 }
 },
 "openId" : "String",
 "wxSn" : "String",
 "groupId" : "String",
 "tradeNo" : "String",
 "notCheckCustomPay" : true,
 "controllerSource" : "String",
 "payType" : "String",
 "orderType" : "String",
 "orderId" : "String",
 "orderNo" : "String",
 "payAmount" : 0,
 "currencyId" : "String",
 "exchangeRate" : 0,
 "currencyScale" : 0,
 "smallestSize" : 0,
 "orderPrepay" : true,
 "entityCardPayDetail" : null,
 "groupId" : "String",
 "benefitsPayParameter" : {
 "payPwdType" : "String",
 "payPwd" : "String",
 "fromUser" : 0
 },
 "statementId" : 0,
 "postingDate" : "DateTime",
 "remark" : "String",
 "payDate" : "DateTime",
 "offlineCashierType" : 0,
 "memberBenefitsVerify" : "DateTime",
 "merchantNo" : "String",
 "tradeNo" : "String",
 "useStoredValueCardDiscount" : true,
 "replaceSysNo" : "String",
 "requestId" : "String"
 }],
 "couponTable" : null,
 "createId" : "String",
 "createName" : "String",
 "orderCreateDate" : "DateTime",
 "expressFeeNoTotal" : true,
 "hasCustomDiscount" : true,
 "specifyItemTotalRealAmount" : true,
 "takeOutDTO" : {
 "daySeq" : "String",
 "orderMode" : 0,
 "userPayAmount" : 0,
 "companyIncomeAmount" : 0
 },
 "platformType" : 0,
 "orderType" : 0,
 "performanceServiceFee" : 0,
 "technicalServiceFee" : 0,
 "timeIntervalMarkUpFee" : 0,
 "distanceIncreaseFee" : 0,
 "pricePremiums" : 0,
 "coldBoxFee" : 0,
 "sourceOrder" : null,
 "isBook" : true,
 "outSysName" : "String",
 "outOrderNo" : "String",
 "outQueueNumber" : "String",
 "thMemberCoupons" : [{
 "id" : 0,
 "couponAmount" : 0,
 "couponSku" : "String",
 "couponId" : "String",
 "title" : "String",
 "couponType" : 0,
 "templeId" : "String",
 "sourceType" : 0,
 "couponTypeName" : "String",
 "channel" : "String",
 "billingKind" : "String"
 }],
 "speedOrderDiscountSplits" : [{
 "thirdProductLineId" : "String",
 "id" : 0,
 "skuBarCode" : "String",
 "itemTotalCount" : 0,
 "itemSplitCount" : 0,
 "splitPriceAmount" : 0,
 "salePriceAmount" : 0,
 "deductionAmount" : 0,
 "splitType" : 0,
 "spiltSource" : "String",
 "channel" : 0,
 "activityId" : "String",
 "activityName" : "String",
 "remark" : "String",
 "billingKind" : "String"
 }],
 "blessing" : {
 "giverPhone" : "String",
 "greeting" : "String"
 },
 "identityCard": "440582199xxxxxxxxx",
 "name": "郭先生",
}
```

### 返回参数
 
|参数名|必选|类型|说明|
|:---- |:---|:----- |----- |
|data|否|Object||
|--orderId|否|String| 订单id|
|--orderNo|否|String| 订单编号|
|--queueNumber|否|String| 取单号|
|msg|否|String||
|code|否|String||
|exceptionStackInfo|否|String||
|traceId|否|String||


### 返回参数Json格式
 
```
{
 "data" : {
 "orderId" : "String",
 "orderNo" : "String",
 "queueNumber" : "String"
 },
 "msg" : "String",
 "code" : "String",
 "exceptionStackInfo" : "String",
 "traceId" : "String"
}
```
