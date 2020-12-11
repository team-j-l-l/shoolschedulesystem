import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps
from .config import db_block, web_routes

@web_routes.get("/api/student/info")
async def get_student_info(request):
    with db_block() as db:
        db.execute("""
        SELECT sn as stu_sn, sno as stu_sno, sname as stu_sname, sgender as stu_sgender, 
        sage as stu_sage, enrolled as stu_enrolled, major as stu_major FROM student
        """)
        data = list(asdict(r) for r in db)
    return web.Response(text=json_dumps(data),content_type="application/json")

@web_routes.get("/api/student/{stu_sn:\d+}")
async def get_student_profile(request):
    stu_sn = request.match_info.get("stu_sn")
    with db_block() as db:
        db.execute("""
       SELECT sn as stu_sn, sno as stu_sno, sname as stu_sname, sgender as stu_sgender, 
        sage as stu_sage, enrolled as stu_enrolled, major as stu_major FROM student
        WHERE sn=%(stu_sn)s
        """, dict(stu_sn=stu_sn))
        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such student: stu_sn={stu_sn}")
    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")

@web_routes.post("/api/student")
async def new_student(request):
    student = await request.json()
    if not student.get('enrolled'):
        student['enrolled'] = datetime.date(1900, 1, 1)

    with db_block() as db:
        db.execute("""
        INSERT INTO student (sno, sname, sgender, sage, enrolled, major)
        VALUES(%(stu_sno)s, %(stu_sname)s, %(stu_sgender)s, %(stu_sage)s, %(stu_enrolled)s,%(stu_major)s) RETURNING sn;
        """, student)
        record = db.fetch_first()
        student["stu_sn"] = record.sn
    return web.Response(text=json_dumps(student), content_type="application/json")

@web_routes.put("/api/student/{stu_sn:\d+}")
async def update_student(request):
    stu_sn = request.match_info.get("stu_sn")
    student = await request.json()
    if not student.get('enrolled'):
        student['enrolled'] = datetime.date(1900, 1, 1)
    student["stu_sn"] = stu_sn
    with db_block() as db:
        db.execute("""
        UPDATE student SET
            sno=%(stu_sno)s, sname=%(stu_sname)s, sgender=%(stu_sgender)s, sage=%(stu_sage)s, enrolled=%(stu_enrolled)s, major=%(stu_major)s
        WHERE sn=%(stu_sn)s;
        """, student)
    return web.Response(text=json_dumps(student), content_type="application/json")

@web_routes.delete("/api/student/{stu_sn:\d+}")
async def delete_student(request):
    stu_sn = request.match_info.get("stu_sn")
    with db_block() as db:
        db.execute("""
        SELECT sno FROM student WHERE sn = %(stu_sn)s; 
        """,dict(stu_sn=stu_sn))
        stu_sno = db.fetch_first().sno
    with db_block() as db:
        db.execute("""
        DELETE FROM studentcourse WHERE sno_cou=%(stu_sno)s;
        DELETE FROM student WHERE sn=%(stu_sn)s;
        """, dict(stu_sn=stu_sn,stu_sno=stu_sno))
    return web.Response(text="", content_type="text/plain")