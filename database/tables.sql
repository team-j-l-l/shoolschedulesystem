-- 学生信息表
DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student  (
    sn       INTEGER,     --序号
    sno       VARCHAR(10), --学号
    sname     TEXT,        --姓名
    gender   CHAR(1),     --性别(F/M/O)
    enrolled DATE,        --入学时间
    major    TEXT,        --专业
    PRIMARY KEY(sn)
);
-- 给序号sn创建一个自增序号seq_student_sn
CREATE SEQUENCE seq_student_sn 
    START 10000 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
-- 给学号sno创建一个唯一索引idx_student_sno
CREATE UNIQUE INDEX idx_student_sno ON student(sno);


-- 课程信息表
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course  (
    cn        INTEGER, --序号
    cno       VARCHAR(10), --课程号
    cname     TEXT,        --课程名称
    PRIMARY KEY(cn)
);
-- 给序号cn创建一个自增序号seq_course_cn
CREATE SEQUENCE seq_course_cn 
    START 10000 INCREMENT 1 OWNED BY course.cn;
ALTER TABLE course ALTER cn 
    SET DEFAULT nextval('seq_course_cn');
-- 给课程号cno创建一个唯一索引idx_course_cno
CREATE UNIQUE INDEX idx_course_cno ON course(cno);


-- 教学计划表
DROP TABLE IF EXISTS courseplan;
CREATE TABLE IF NOT EXISTS courseplan
(
    cou_cno   VARCHAR(10), -- 课程号
    cou_cname TEXT, -- 课程名称
    credit    DECIMAL, -- 学分
    semester  TEXT, -- 学期
    teacher   TEXT, -- 授课教师
    week      TEXT, -- 教学周
    time      TEXT, -- 上课时间
    site      TEXT, -- 上课地点
    PRIMARY KEY(semester,time,site)
);


-- 成绩信息表
DROP TABLE IF EXISTS grade;
CREATE TABLE IF NOT EXISTS grade
(
    stu_sno_gra VARCHAR(10), -- 学号
    stu_sname_gra TEXT, -- 姓名
    cou_cno_gra VARCHAR(10), -- 课程号
    cou_cname_gra TEXT, -- 课程名称
    cou_credit_gra DECIMAL, --学分
    grade INTEGER, --成绩
    PRIMARY KEY(stu_sno_gra,cou_cno_gra)
);
-- 创建外键引用课程计划表的cno和学生表的sno
ALTER TABLE grade 
    ADD CONSTRAINT stu_sno_gra_fk FOREIGN KEY (stu_sno_gra) REFERENCES student(sno);
ALTER TABLE grade 
    ADD CONSTRAINT cou_cno_gra_fk FOREIGN KEY (cou_cno_gra) REFERENCES course(cno);
ALTER TABLE grade ALTER COLUMN cou_credit_gra TYPE TEXT;

-- 登录信息表
CREATE TABLE IF NOT EXISTS log_in  (
    account    TEXT, 
    passwords  TEXT,        
    kind     CHAR(5),     
    PRIMARY KEY(account)
);