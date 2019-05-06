"""
file：
author：
date：
"""
import pandas as pd
from feature import get_feature
import xgboost as xgb
from pretreatment import pre
name1 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received','Date']
name3 = ["User_id",'Merchant_id','Coupon_id','Discount_rate','Distance','Date_received']
dfoff = pd.read_csv('data/ccf_offline_stage1_train.csv',names=name1)
dftest = pd.read_csv('data/ccf_offline_stage1_test_revised.csv',names=name3)

dfoff = pre(dfoff)
dfoff['date'] = pd.to_datetime(dfoff['Date'], format='%Y%m%d')
dfoff['label'] = list(map(lambda x ,y : 1 if (x - y).total_seconds()/60*60*24 <= 15 else 0 ,dfoff['date'],dfoff['date_received']))
dftest = pre(dftest)

train_field = dfoff[dfoff['date_received'].isin(pd.date_range('2016/3/2',periods= 60))]
validate_field = dfoff[dfoff['date_received'].isin(pd.date_range('2016/1/16',periods= 60))]
test_field = dfoff[dfoff['date_received'].isin(pd.date_range('2016/4/17',periods= 60))]
#构造训练集、验证集、与测试集
train = get_feature(train_field)[["User_id", "Coupon_id", "Date_received","is_manjian","discount_rate",
                                  "min_pay_of_manjian","null_Distance","label","simple_User_id_received_cnt",
                                  "simple_User_id_Coupon_id_received_cnt","simple_User_id_Date_received_received_cnt",
                                  "simple_User_id_Coupon_id_Date_received_received_cnt",
                                  "simple_User_id_Coupon_id_Date_received_repeat_received"]]
validate = get_feature(validate_field)[["User_id", "Coupon_id", "Date_received","is_manjian","discount_rate",
                                  "min_pay_of_manjian","null_Distance","label","simple_User_id_received_cnt",
                                  "simple_User_id_Coupon_id_received_cnt","simple_User_id_Date_received_received_cnt",
                                  "simple_User_id_Coupon_id_Date_received_received_cnt",
                                  "simple_User_id_Coupon_id_Date_received_repeat_received"]]
test = get_feature(test_field)[["User_id", "Coupon_id", "Date_received","is_manjian","discount_rate",
                                  "min_pay_of_manjian","null_Distance","simple_User_id_received_cnt",
                                  "simple_User_id_Coupon_id_received_cnt","simple_User_id_Date_received_received_cnt",
                                  "simple_User_id_Coupon_id_Date_received_received_cnt",
                                  "simple_User_id_Coupon_id_Date_received_repeat_received"]]

dtrain = xgb.DMatrix(train.drop(["User_id", "Coupon_id", "Date_received",'label'], axis= 1) ,label= train['label'])
dtest = xgb.DMatrix(test.drop(["User_id", "Coupon_id", "Date_received"],axis= 1))
params = {
    'booster':'gbtree',
    'objective':'binary:logistic',
    'eval_metric': 'auc',
    'slient':1,
    'eta':0.01,
    'max_depth':5,
    'min_child_weight':1,
    'gamma':0,
    'lambda':1,
    'colsample_bylevel':0.7,
    'colsample_bytree':0.7,
    'subsample':0.9,
    'scale_pos_weight':1
}
model = xgb.train(params,dtrain,num_boost_round=50)

pedict = model.predict(dtest)

pedict = pd.DataFrame(pedict,columns= ['prob'])
result = pd.concat([test[["User_id", "Coupon_id", "Date_received"]],pedict],axis= 1)
feat_importance = pd.DataFrame(columns= ['feature_name','importance'])
feat_importance['feature_name'] = model.get_score().keys()
feat_importance['importance'] = model.get_score().keys()
feat_importance.sort_values(['importance'],ascending= False, inplace= True)

result.to_csv('result.csv',index= False ,header= False)

