import pandas as pd
from utils import computeTime
from utils import readDataFromMysql

pre1 = pd.read_csv("data_test/pre1.csv")
pre2 = pd.read_csv("data_test/pre2.csv")

vip1 = pd.read_csv("data_test/vip1.csv")
vip2 = pd.read_csv("data_test/vip2.csv")
vip3 = pd.read_csv("data_test/vip3.csv")

sql = 'select zjc_supplier.name,zjc_supplier.province,zjc_supplier_param.attach_count,zjc_supplier.type,zjc_supplier.fund,zjc_supplier_param.service_level_average,zjc_supplier_param.instock_service_average,zjc_supplier_param.instock_product_average,zjc_supplier_param.instock_deliverspeed_average,zjc_supplier_param.iswin_count,zjc_supplier_param.price_level_average,zjc_supplier_param.tender_count,zjc_supplier_param.semester_tender_count,zjc_supplier_param.bidconcern_count,zjc_supplier_param.semester_bidconcern_count,zjc_supplier_param.login_days,zjc_supplier_param.semester_login_days,zjc_supplier_param.integrity_count,zjc_supplier_param.contract_rate,zjc_supplier_param.instock_honesty_average,zjc_supplier.regchecktime,zjc_supplier.createtime from zjc_supplier INNER JOIN zjc_supplier_param on zjc_supplier.id=zjc_supplier_param.supplier_id where zjc_supplier.state=2;'
# all_supplier:所有供应商，包括训练用的正负样本
all_supplier = readDataFromMysql(sql)
all_supplier.columns = ['name', 'province', 'attach_count', 'type', 'fund', 'service_average', 'instock_service', 'instock_product', 'instock_deliverspeed', 'win', 'price',
                        'tender', 'se_tender', 'bidconcern', 'se_bidconcern', 'login', 'se_login', 'integrity', 'contract_rate', 'instock_honesty', 'regchecktime', 'createtime']
all_supplier = all_supplier.drop_duplicates(keep=False, subset=['name'])
# 最后两列是注册和审核时间，用于计算已经成为平台用户的时长
time_all = computeTime(all_supplier.iloc[:, -2:])
time_all.columns = ['years']
all_supplier = pd.concat([all_supplier.iloc[:, :-2], time_all], axis=1)

vip_time = all_supplier[all_supplier['name'].isin(
    vip3['name'])].reset_index(drop=True)
vip_time.query('years>0.5')


vip3[vip3['name'].isin(pre2['name'])].reset_index(drop=True)

top1000 = pd.read_csv("data_test/pre_positive_sort.csv")
vip1[vip1['name'].isin(top1000['name'])].reset_index(drop=True)
vip2[vip2['name'].isin(top1000['name'])].reset_index(drop=True)

last = pd.read_csv('data/last.csv', sep='\t')
this = pre_positive[~pre_positive['name'].isin(
    last['name'])].reset_index(drop=True)
this = this.sort_values('probability', ascending=False).reset_index(drop=True)
this.iloc[:230, :].to_csv('./pre.csv', index=None)


new_add = pd.read_csv('data/new_add.csv')
new_add_new_supplier = new_supplier[new_supplier['name'].isin(
    new_add['name'])].reset_index(drop=True)
new_add_old_supplier = old_supplier[old_supplier['name'].isin(
    new_add['name'])].reset_index(drop=True)

all_supplier[all_supplier['name'].isin(
    new_add['name'])].reset_index(drop=True)

total = pd.read_csv('dataResult/total.csv')
this = pd.read_csv('dataResult/this.csv')

xy = new_add_old_supplier[new_add_old_supplier['name'].isin(
    total['name'])].reset_index(drop=True)

new_add_old_supplier[new_add_old_supplier['name'].isin(
    this['name'])].reset_index(drop=True)

data_refuse = pd.read_csv("./data/vip_0.csv")
data_refuse = data_refuse.drop_duplicates()

xy[xy['name'].isin(
    data_refuse['name'])].reset_index(drop=True)

new = pd.read_csv("./dataDump/vip_new_supplier.csv")
data_df[data_df['name'].isin(old_supplier['name'])].reset_index(drop=True)