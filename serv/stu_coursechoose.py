from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode
from .config import db_block, web_routes, render_html
from .login_actions import get_username

@web_routes.get("/stu_planchoose")
async def view_list_courseplan(request):
    with db_block() as db:
        db.execute("""
        SELECT cno as cou_cno, cname as cou_cname FROM course
        """)
        courses = list(db)
        db.execute("""
        SELECT p.pla_cno as cou_cno, p.semester as cou_semester, 
        p.week as cou_week, p.time as cou_time, p.site as cou_site,
        c.cname as cou_cname, c.credit as cou_credit, c.ctype as cou_ctype
        FROM courseplan as p
        INNER JOIN course as c ON p.pla_cno=c.cno ORDER BY pla_cno;
        """)
        items = list(db)
    return render_html(request,"stu_coursechoose.html",courses = courses,items = items)

@web_routes.get("/scourse/choose/{cou_cno}")
def choose_confirm_dialog(request):
    cou_cno = request.match_info.get("cou_cno")
    if cou_cno is None:
        return web.HTTPBadRequest(text="cou_cno must be required")
    with db_block() as db:
        db.execute("""
        SELECT p.pla_cno as cou_cno, p.semester as cou_semester, 
        p.week as cou_week, p.time as cou_time, p.site as cou_site,
        c.cname as cou_cname, c.credit as cou_credit, c.ctype as cou_ctype
        FROM courseplan as p
        INNER JOIN course as c ON p.pla_cno=c.cno 
        WHERE pla_cno = %(cou_cno)s;
        """,dict(cou_cno=cou_cno))
        record = db.fetch_first()
        print(record)
    if record is None:
        return web.HTTPNotFound(text=f"no such course：cou_cno={cou_cno}")
    return render_html(request,"stu_coursechoose_confirm.html",record=record)

@web_routes.post('/action/stu_planchoose/confirm/{cou_cno}/{semester}/{week}/{time}/{site}')
def confirm_courseplan_action(request):
    cou_cno = request.match_info.get("cou_cno")
    semester = request.match_info.get("semester")
    print(semester)
    site = request.match_info.get("site")
    print(site)
    week = request.match_info.get("week")
    time = request.match_info.get("time")
    username = get_username()
    if cou_cno is None:
        return web.HTTPBadRequest(text="cou_cno,must be required")
    with db_block() as db:
        db.execute("""
        INSERT INTO studentcourse(sno_cou,cno_cou,semester_cou,week,time,site) 
        VALUES(%(username)s,%(cou_cno)s,%(semester)s,%(week)s,%(time)s,%(site)s)""",
        dict(username=username,cou_cno=cou_cno,semester=semester,week=week,time=time,site=site))
    return web.HTTPFound(location="/stu_planchoose")