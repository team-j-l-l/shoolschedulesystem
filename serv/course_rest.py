import datetime
from aiohttp import web
from dataclasses import asdict
from serv.json_util import json_dumps
from .config import db_block, web_routes

@web_routes.get("/api/course/info")
async def get_course_info(request):
    with db_block() as db:
        db.execute("""
        SELECT cn as cou_cn, cno as cou_cno, cname as cou_cname, credit as cou_credit, 
        ctype as cou_ctype FROM course
        """)
        data = list(asdict(r) for r in db)
    return web.Response(text=json_dumps(data),content_type="application/json")

@web_routes.get("/api/course/{cou_cn:\d+}")
async def get_course_profile(request):
    cou_cn = request.match_info.get("cou_cn")
    with db_block() as db:
        db.execute("""
       SELECT cn as cou_cn, cno as cou_cno, cname as cou_cname, credit as cou_credit, 
        ctype as cou_ctype FROM course
        WHERE cn=%(cou_cn)s
        """, dict(cou_cn=cou_cn))
        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such course: cou_cn={cou_cn}")
    data = asdict(record)
    return web.Response(text=json_dumps(data), content_type="application/json")

@web_routes.post("/api/course")
async def new_course(request):
    course = await request.json()

    with db_block() as db:
        db.execute("""
        INSERT INTO course (cno, cname, credit, ctype)
        VALUES(%(cou_cno)s, %(cou_cname)s, %(cou_credit)s, %(cou_ctype)s) RETURNING cn;
        """, course)
        record = db.fetch_first()
        course["cou_cn"] = record.cn
    return web.Response(text=json_dumps(course), content_type="application/json")

@web_routes.put("/api/course/{cou_cn:\d+}")
async def update_course(request):
    cou_cn = request.match_info.get("cou_cn")
    course = await request.json()
    course["cou_cn"] = cou_cn
    with db_block() as db:
        db.execute("""
        UPDATE course SET
            cno=%(cou_cno)s, cname=%(cou_cname)s, credit=%(cou_credit)s, ctype=%(cou_ctype)s
        WHERE cn=%(cou_cn)s;
        """, course)
    print(course)
    return web.Response(text=json_dumps(course), content_type="application/json")

@web_routes.delete("/api/course/{cou_cn:\d+}")
async def delete_course(request):
    cou_cn = request.match_info.get("cou_cn")
    with db_block() as db:
        db.execute("""
        SELECT cno FROM course WHERE cn = %(cou_cn)s; 
        """,dict(cou_cn=cou_cn))
        cou_cno = db.fetch_first().cno
    with db_block() as db:
        db.execute("""
        DELETE FROM courseplan WHERE pla_cno=%(cou_cno)s;
        DELETE FROM studentcourse WHERE cno_cou=%(cou_cno)s;
        DELETE FROM course WHERE cn=%(cou_cn)s;
        """, dict(cou_cn=cou_cn,cou_cno=cou_cno))
    return web.Response(text="", content_type="text/plain")