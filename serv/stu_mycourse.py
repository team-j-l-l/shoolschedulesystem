from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode
from .config import db_block, web_routes, render_html
from .login_actions import get_username

@web_routes.get("/stu_mycourse")
async def view_list_courseplan(request):
    username = get_username()
    with db_block() as db:
        db.execute("""
        SELECT tc.sno_cou, tc.cno_cou as cou_cno, tc.semester_cou as cou_semester,
        tc.site as cou_site, tc.week as cou_week, tc.time as cou_time,
        c.cname as cou_cname, c.credit as cou_credit, c.ctype as cou_ctype FROM studentcourse as tc
        INNER JOIN course as c ON tc.cno_cou=c.cno
        WHERE sno_cou=%(username)s;
        """,dict(username = username))
        items = list(db)
    return render_html(request,"stu_mycourse.html",items = items)

@web_routes.get("/action/stu_mycourse/delete/{cou_cno}")
def delete_confirm_dialog(request):
    username = get_username()
    cou_cno = request.match_info.get("cou_cno")
    if cou_cno is None:
        return web.HTTPBadRequest(text="cou_cno must be required")
    with db_block() as db:
        db.execute("""
       SELECT tc.sno_cou, tc.cno_cou as cou_cno, tc.semester_cou as cou_semester,
        tc.site as cou_site, tc.week as cou_week, tc.time as cou_time,
        c.cname as cou_cname, c.credit as cou_credit, c.ctype as cou_ctype FROM studentcourse as tc
        INNER JOIN course as c ON tc.cno_cou=c.cno
        WHERE sno_cou=%(username)s AND cno_cou=%(cou_cno)s;
        """,dict(username=username,cou_cno=cou_cno))
        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such course：cou_cno={cou_cno}")
    return render_html(request,"stu_mycourse_delete.html",record=record)

@web_routes.post("/action/stu_mycourse/delete/{sno_cou}/{cou_cno}")
def cdelete_confirm_dialog(request):
    sno_cou = request.match_info.get("sno_cou")
    cou_cno = request.match_info.get("cou_cno")
    if cou_cno is None:
        return web.HTTPBadRequest(text="cou_cno must be required")
    with db_block() as db:
        db.execute("""
        DELETE FROM studentcourse WHERE sno_cou=%(sno_cou)s AND cno_cou=%(cou_cno)s
        """,dict(cou_cno=cou_cno,sno_cou=sno_cou))
    return web.HTTPFound(location="/stu_mycourse")

