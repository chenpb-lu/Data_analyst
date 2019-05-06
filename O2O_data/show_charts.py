"""
file：
author：
date：
"""
from pyecharts import Bar, Pie, Line
import pandas as pd
name1 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']
dfoff = pd.read_csv('data/ccf_offline_stage1_train.csv',names=name1)
#判断是否为满减折扣
dfoff['is_manjian'] = dfoff['Discount_rate'].map(lambda x : 1 if ':' in str(x) else 0)
#找出优惠的最低消费
dfoff['min_pay_of_manjian'] = dfoff['Discount_rate'].map(lambda x : -1 if ":" not in str(x) else int(str(x).split(':')[0]))
#将满减的优惠也转换成折扣率
dfoff['discount_rate'] = dfoff['Discount_rate'].map(lambda x : float(x) if ':' not in str(x) else (float(str(x).split(':')[0]) - float(str(x).split(':')[1]))/float(str(x).split(':')[0]))

#设置一列为datel类型发日期数据领取优惠券日期数据
dfoff['date_received'] = pd.to_datetime(dfoff['Date_received'],format='%Y%m%d')
#设置一列为datel类型发日期数据的消费日期数据
dfoff['date'] = pd.to_datetime(dfoff['Date'],format='%Y%m%d')

# 查看缺省值
# print(dfoff.isnull().any())
# 统计缺省值的比例
# print(dfoff.isnull().sum() / len(dfoff))

# 将距离为空的数据进行处理
dfoff['Distance'].fillna(-1,inplace= True)
# 标记距离是否为空
dfoff['null_Distance'] = dfoff['Distance'].map(lambda x : 1 if x == -1 else 0)

# 将日期转换成周几，便于分析
dfoff['weekday_Receive'] = dfoff['date_received'].apply(lambda  x : x.isoweekday())

# 保存处理后的训练集
# dfoff.to_csv('./data2/offline_data.csv',index=False,header=True)

dfoff['label'] = list(map(lambda x ,y : 1 if (x - y).total_seconds()/60*60*24 <= 15 else 0 ,dfoff['date'],dfoff['date_received']))

# drill_section = dfoff[dfoff['date_received'].isin(pd.date_range('2016/3/2', periods= 60))]
#
# verify_section = dfoff[dfoff['date_received'].isin(pd.date_range('2016/1/16', periods=


# df1 = dfoff[dfoff['Date_received'].notna()]
# tmp = df1.groupby('Date_received',as_index=False)['Coupon_id'].count()
# bar1 = Bar("每天被领券的数量",width=1500,height=600)
# bar1.add('',list(tmp['Date_received']),list(tmp['Coupon_id']),xaxis_interval=1,xaxis_rotate=60,mark_line=['max'])
# bar1.render('bar1.html')

#构建领取月份与消费月份、使用消费券月份
# dfoff['recived_month'] = dfoff['date_received'].apply(lambda x :x.month)
# consume_coupn = dfoff[dfoff['label'] == 1]['recived_month'].value_counts(sort=False)
# received = dfoff['recived_month'].value_counts(sort=False)
#
# dfoff['date_month'] = dfoff['date'].apply(lambda  x :x.month)
# consume = dfoff["date_month"].value_counts(sort=False)
#
# consume_coupn.sort_index(inplace= True)
# consume.sort_index(inplace= True)
# received.sort_index(inplace= True)
#
#
# line1 = Line('每月消费折线图')
# line1.add('核销',list(range(1,7)),list(consume_coupn.values))
# line1.add('领取',list(range(1,7)),list(received.values))
# line1.add('消费',list(range(1,7)),list(consume.values))
# line1.render('line1.html')


# dis = dfoff[dfoff["Distance"] != -1]['Distance'].value_counts()
# dis.sort_index(inplace= True)
# bar2 = Bar("消费距离柱状图")
# bar2.add('',list(dis.index),list(dis.values))
# bar2.render('bar2.html')
#
#
# rate = [dfoff[dfoff["Distance"] == i]['label'].value_counts()[1]/dfoff[dfoff['Distance'] == i]['label'].value_counts().sum() for i in range(11)]
# bar3 = Bar("消费距离与核销率柱状图")
# bar3.add('核销率',list(range(11)),rate)
# bar3.render("bar3.html")

# pie1 = Pie("各类优惠券占比饼图")
# pie1.add('',['折扣','满减'],list(dfoff[dfoff['Date_received'].notna()]['is_manjian'].value_counts(sort=False).values),is_label_show=True)
# pie1.render("pie1.html")

# pie2 = Pie("核销优惠券数量占比饼图")
# pie2.add('',['折扣','满减'],list(dfoff[dfoff['label'].notna()]['is_manjian'].value_counts(sort=False).values),is_label_show=True)
# pie2.render("pie2.html")

# bar4 = Bar("各种折扣率优惠券领取与核销柱状图")
# receied =dfoff['discount_rate'].value_counts(sort=False)
# consume_coupon = dfoff[dfoff['label'] ==1]['discount_rate'].value_counts(sort=False)
# receied.sort_index(inplace=True)
# consume_coupon.sort_index(inplace=True)
# bar4.add('领取',[float("%.4f"%x) for x in receied.index], list(receied.values),xaxis_rotate=50)
# bar4.add('核销',[float("%.4f"%x) for x in consume_coupon.index], list(consume_coupon.values),xaxis_rotate=50)
# bar4.render("bar4.html")

consume_coupon = dfoff[dfoff['label'] == 1]['weekday_Receive'].value_counts()
received = dfoff['weekday_Receive'].value_counts()
received.sort_index(inplace=True)
consume_coupon.sort_index(inplace=True)
line2 = Line("每周优惠券领取数与核销数折线图")
line2.add("领取",list(range(1,8)),list(received.values),is_label_show=True)
line2.add("核销",list(range(1,8)),list(consume_coupon.values),is_label_show=True)
line2.render("line2.html")