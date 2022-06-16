### 基于知识图谱的会展知识问答系统
#### 项目环境
* Django==2.2.7
* django-ranged-response==0.2.0
* django-simple-captcha==0.5.12
* Pillow==6.2.1
* pytz==2019.3
* six==1.13.0
* sqlparse==0.3.0
* jinja2==2.10
* pyecharts==1.9.1
* py2neo== 2021.2.3
* matplotlib==3.0.2
* redis==2.10.6
* pyahocorasick==1.4.4


#### 环境
* JetBrains PyCharm 2019.2.3 
* MacBookPro14,1
* Python 3.7

#### 数据库设计
1、redis数据库设计 

使用Redis数据库存放了用户的用户名、密码、登陆状态、验证码失败次数和禁止登陆时间，其中密码使用md5加密算法中，sha256安全散列算法，以非明文方式存储。禁止登陆时间使用Redis数据库中expire函数，在用户禁止登陆后，生成倒计时。用户所有数据使用Redis中哈希这个数据结构来实现，详细设计情况如下所示。

字段名|含义|备注
-|-|-
username|	用户名|	用户唯一标识
password	|密码	|sha256安全散列算法加密
fail_time	|验证码失败次数|	失败次数大于5次禁止登陆
login_status|	登陆状态	|负责检验登陆状态和注入session
forbiddentime	|禁止登陆时间|	默认不存在，当禁止登陆后在当前用户哈希表中自动生成
send|	发送验证码次数	|10分钟内最多发送5次

2、ne4j数据库设计

Neo4j存储了7类实体节点，6类实体间的关系和11类实体属性。


实体名称|	实体含义	|示例
-|-|-
expo_name|	展会|	第六届中国(温州)机械装备展览会
expo_type|	展会类型|	机械/五金/工业
expo_place	|展览地点|	温州国际会议展览中心
expo_year|	年份	|2011
expo_month	|月份|	十一月
expo_country|	所在国家|	中国
expo_orgization|	组织机构|	中国机械工业联合会/温州市人民政府
rels_type|	展会类型|	<第六届中国(温州)机械装备展览会，展会类型，机械/五金/工业>
rels_country|	举办国家|	<第六届中国(温州)机械装备展览会，举办国家，中国>
rels_year|	举办年份|	<第六届中国(温州)机械装备展览会，举办年份，2011>
rels_hold_place|	举办地点|	<第六届中国(温州)机械装备展览会，举办地点，温州国际会议展览中心>
rels_month|	举办月份|	<第六届中国(温州)机械装备展览会，举办月份，十一月>
rels_orgization|	举办方|	<第六届中国(温州)机械装备展览会，举办方，中国机械工业联合会/温州市人民政府>

属性名称|	属性含义|	示例
-|-|-
name|	展会名称|	第六届中国(温州)机械装备展览会
start_time|	开始时间|	2011-10-21
end_time|	结束时间|	2011-10-23
introduction|	展会概况|	中国（温州）机械装备展览会（CWMEE）从2006年开始已经成功举办了五届
location1|	位置1|	33
location2|	位置2|	12
range|	展会范围|	数控金属切削机床、电加工及激光加工等
interested _count|	感兴趣人数|	3968
contact_information|	联系方式|	上海联络处 联系人:黄保生 18721254596  电话：021-54995114
precautions|	注意事项|	CNENA全站展会信息均由会员发布，网站已尽严格审核义务
cost|	参展费用|	标准展位：5500元/个（3米乘3米），标准展位包括：展出场地，三面或两面展板（高2.5米）


#### 实体与属性关系：
![image](https://user-images.githubusercontent.com/101266608/174006835-fad53925-2c11-41aa-ba60-c43713e4fb70.png)

#### 知识图谱统计（对数轴）
![image](https://user-images.githubusercontent.com/101266608/174006929-f32f1e06-4a10-4588-95ab-b0d8b2597722.png)
![image](https://user-images.githubusercontent.com/101266608/174006962-85de706f-5f93-4b9c-a6d8-b9b0656bf4da.png)




#### 运行
* python manage.py runserver


#### 注意事项
json数据比较大，所以无法上传至Github，请提交issue（留邮箱）或者联系本人获取2144533854@qq.com


#### 效果图
注册
![image](https://user-images.githubusercontent.com/101266608/174006230-247b427a-6fa3-4d2f-8215-413ccdc12352.png)
登陆
![7FD78805A8F70ECE0B4A6B19903F8B21](https://user-images.githubusercontent.com/101266608/174006152-a05ad0ea-0739-4d41-aab9-241f1c9ead9d.jpg)
推荐
![187DDF01-B230-4A35-858D-9B3D77B564EE](https://user-images.githubusercontent.com/101266608/174006344-9d300b2f-04cd-4d38-ac2f-0ea80b794328.png)

问答
![683F41DFD1CB18AD14D60C546FB1032E](https://user-images.githubusercontent.com/101266608/174006362-19fbd3cb-8dea-4991-8160-2a4a400ba016.jpg)

可视化
![5FC3B808-9E6C-4124-9768-BD2667F08655](https://user-images.githubusercontent.com/101266608/174006299-4e9810fc-2900-4cbf-b5e0-37bec9970be7.png)

查询缓存与查询neo4j比较
![A4AAA63BE35FA1A8BFFDCB0B9A7551EC](https://user-images.githubusercontent.com/101266608/174006379-82ce27ab-5485-4549-b977-c196f39d700c.jpg)
后台知识图谱
![191B7C2D60C9511E4FB70356E62529B2](https://user-images.githubusercontent.com/101266608/174006415-5f0588b5-55b0-42e2-9e61-7d37342bf193.jpg)





