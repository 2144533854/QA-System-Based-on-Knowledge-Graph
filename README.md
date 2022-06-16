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
#### 运行
* python manage.py runserver

#### 路由设计
URL|视图|模板|说明
-|-|-|-
index|login.views.index|index.html|主页
login|login.views.login|login.html|登录
register|login.views.register|register.html|注册
logout|login.views.logout|NAN|登出

