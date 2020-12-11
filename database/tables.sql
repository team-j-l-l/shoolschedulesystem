-- 学生信息表
DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student(
    sn       INTEGER,     --序号
    sno       VARCHAR(10), --学号
    sname     TEXT,        --姓名
    sgender   CHAR(1),     --性别(F/M/O)
    sage      INTEGER,     --年龄
    enrolled DATE,        --入学时间
    major    TEXT,        --专业
    scode    VARCHAR(10),  --学生登录密码
    PRIMARY KEY(sn)
);
-- 给序号sn创建一个自增序号seq_student_sn
CREATE SEQUENCE seq_student_sn 
    START 10000 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
ALTER TABLE student ALTER scode
    SET DEFAULT ('000000');
-- 给学号sno创建一个唯一索引idx_student_sno
CREATE UNIQUE INDEX idx_student_sno ON student(sno);


-- 课程信息表
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course(
    cn        INTEGER, --序号
    cno       VARCHAR(10), --课程号
    cname     TEXT,        --课程名称
    credit    DECIMAL,      --课程学分
    ctype     TEXT,       --课程属性
    PRIMARY KEY(cn)
);
-- 给序号cn创建一个自增序号seq_course_cn
CREATE SEQUENCE seq_course_cn 
    START 10000 INCREMENT 1 OWNED BY course.cn;
ALTER TABLE course ALTER cn 
    SET DEFAULT nextval('seq_course_cn');
-- 给课程号cno创建一个唯一索引idx_course_cno
CREATE UNIQUE INDEX idx_course_cno ON course(cno);


--教师信息表
DROP TABLE IF EXISTS teacher;
CREATE TABLE IF NOT EXISTS teacher(
    tn       INTEGER, --序号
    tno      VARCHAR(10), --教师号
    tname    TEXT,       --教师姓名
    tgender  CHAR(1),   --教师性别
    tage     INTEGER,   --教师年龄
    tcode    VARCHAR(10), --教师登录密码
    PRIMARY KEY(tn)
);
--给序号tn创建一个自增序号seq_teacher_tn
CREATE SEQUENCE seq_teacher_tn
    START 10000 INCREMENT 1 OWNED BY teacher.tn;
ALTER TABLE teacher ALTER tn
    SET DEFAULT nextval('seq_teacher_tn');
--给教师号tno创建一个唯一索引idx_teacher_tno
CREATE UNIQUE INDEX idx_teacher_tno ON teacher(tno);


-- 教学计划表
DROP TABLE IF EXISTS courseplan;
CREATE TABLE IF NOT EXISTS courseplan(
    pla_cno   VARCHAR(10), --计划课程号
    semester  TEXT, -- 学期
    week      TEXT, --教学周
    time      TEXT, -- 上课时间
    site      TEXT, -- 上课地点
    PRIMARY KEY(pla_cno,semester,site)
);
ALTER TABLE courseplan
    ADD CONSTRAINT cno_pla_fk FOREIGN KEY (pla_cno) REFERENCES course(cno);


--学生课程表
DROP TABLE IF EXISTS studentcourse;
CREATE TABLE IF NOT EXISTS studentcourse(
    sno_cou VARCHAR(10), --学生学号
    cno_cou VARCHAR(10), --课程号
    semester_cou TEXT, --上课学期
    week TEXT, --周次
    time TEXT, --时间
    site TEXT, --上课地点
    grade INTEGER DEFAULT null, --课程成绩
    PRIMARY KEY(sno_cou,cno_cou)
)
ALTER TABLE studentcourse
    ADD CONSTRAINT sno_cou_fk FOREIGN KEY (sno_cou) REFERENCES student(sno);
ALTER TABLE studentcourse
    ADD CONSTRAINT cno_cou_fk FOREIGN KEY (cno_cou) REFERENCES course(cno);

---- 成绩信息表
--DROP TABLE IF EXISTS gradetable;
--CREATE TABLE IF NOT EXISTS gradetable(
--    sno_gra VARCHAR(10), -- 学号
--    cno_gra VARCHAR(10), -- 课程号
--    grade INTEGER, --成绩
--    PRIMARY KEY(sno_gra,cno_gra)
--);
---- 创建外键引用课程计划表的cno和学生表的sno
--ALTER TABLE gradetable 
--    ADD CONSTRAINT sno_gra_fk FOREIGN KEY (sno_gra) REFERENCES student(sno);
--ALTER TABLE gradetable 
--    ADD CONSTRAINT cno_gra_fk FOREIGN KEY (cno_gra) REFERENCES course(cno);