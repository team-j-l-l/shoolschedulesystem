## log 1

#### 最简易的版本与11月29日提交

* 已实现的功能
  * 学生信息的展示
  * 课程计划的展示
  * 成绩信息的展示
  * 修改成绩信息
  * 添加成绩信息
  * 删除成绩信息
* 预计将来实现的功能
  * 注册登录功能的实现（用户分为教师和学生）
  * 教师可以添加课程计划
  * 教师修改课程计划
  * 教师按照课程计划查询和管理学生成绩
  * 学生可以查询个人成绩
  * 学生可以选择教学计划
  * 学生可以查看已选课程

## log2

#### 修改完善后的版本与12月7日提交

* 实现的功能
  * 教师和学生不同角色的用户登录
  * 实现了学生端展示某学生所有成绩的功能
  * 实现了教师端学生信息增删改查功能
  * 实现了教师端增删改查课程计划的功能。

* 预计还将实现的功能
  * 修改原有的教师端成绩管理功能（针对教学计划登记成绩）
  * 修改教师端的成绩查询功能（查询某课程在某学期所有学生的成绩）
  * 学生端增加学生选课功能。

可能遇到的问题：数据库中可能需要增加学生选课表，其余的表结构可能相应的需要修改

## log3

#### 实现简单界面设计的版本于12.11提交

对现有网页进行简单的页面设计。

## log4

#### 2020年12月12日此版本已实现所有功能

后续若有工作也仅仅是对于页面的渲染设计或操作异常反馈信息的处理

* 此版本实现的功能
  * 教师和学生的密码修改
  * 学生选课功能
  * 教师成绩查询与管理功能（基于课程计划）
  * 增加了个人主页，以便使页面间的转换更加方便
  * 学生可查看已选课程
* 一些重要变动
  * 表结构变化，增加了学生选课表
  * 表结构变化，成绩不再依赖于学生和课程，而是由学生和课程计划决定，所以取消了单独的成绩表给直接将成绩信息展示在学生选课表中。学生选课即意味着一定会有本课程计划对应的成绩，老师尚未给出成绩时，成绩显示为缺省值NULL
  * 完成了几个重要逻辑关系的实现，即必须教师添加了课程计划学生才可选课，学生必须选了课并且教师添加了成绩学生才可看到正常查看到成绩
* 缺陷：正值考试周，时间紧迫因此并未对细节进行深入处理具体有以下几点
  * 修改密码应添加修改成功提示
  * 密码十位太少，有必要扩展
  * 如果操作错误，仍然使用的系统自己的报错信息，应该设置更人性化的提示
  * 学生选课但未到考试周的课程成绩直接展示位NULL显得不符合人类思维，可以选择将其隐藏掉或变为”未考试“

本次主要功能是由第一版本实现，学生信息部分由第二版本实现。假期时间更充裕在修正上述缺点的基础上，还可试着对本系统从版本和功能上进一步升级

## log5

#### 2020年12月13日

## log6
#### 2020年12月13日对12日所列部分缺陷进行了修正
* 使用javascript为修改密码部分添加了密码修改成功的提示
* 对操作错误的信息增加了提示页面（最为重要的是提醒了教师补课增加同样的教学计划，提醒了学生不可以选同样的两个教学计划）
* 为给出成绩的科目成绩显示从None改为了尚未登记
#### 最后的一些思考
* 分了学生端和教师端，多些时间思考处理应该能再减少重复代码
* 目前时间和能力受限，对学校课程计划与学生成绩安排的理解不到位，当涉及多专业多学院时情况又需要改变
* 时间更充裕后，再研究研究JavaScript将本系统中功能升级为第二版本会更好，能有效减少页面间跳转







