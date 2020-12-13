from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode
from .config import db_block, web_routes

@web_routes.post('/action/tcourseplan/edit/{cou_cno}')
async def edit_courseplan_action(request):
    cou_cno = request.match_info.get("cou_cno")
    if cou_cno is None:
        return web.HTTPBadRequest(text="cou_cno, must be required")
    params = await request.post()
    semester = params.get("semester")
    week = params.get("week")
    time = params.get("time")
    site = params.get("site")
    try:
        cou_cno = str(cou_cno)
        cou_semester = str(semester)
        cou_week = str(week)
        cou_time = str(time)
        cou_site = str(site)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")
    with db_block() as db:
        db.execute("""
        UPDATE courseplan SET semester = %(semester)s, week = %(week)s,
        time = %(time)s, site = %(site)s WHERE pla_cno=%(cou_cno)s
        """,dict(semester=semester,week=week,time=time,site=site,cou_cno=cou_cno))
    return web.HTTPFound(location="/tcourseplan_info")

@web_routes.post('/action/tcourseplan/delete/{cou_cno}/{semester}/{site}')
def delete_courseplan_action(request):
    cou_cno = request.match_info.get("cou_cno")
    semester = request.match_info.get("semester")
    site = request.match_info.get("site")
    if cou_cno is None:
        return web.HTTPBadRequest(text="cou_cno,must be required")
    with db_block() as db:
        db.execute("""
        DELETE FROM courseplan WHERE pla_cno=%(cou_cno)s AND semester = %(semester)s AND site = %(site)s
        """,dict(cou_cno=cou_cno,semester=semester,site=site))
    return web.HTTPFound(location="/tcourseplan_info")

@web_routes.post('/action/tcourseplan/add')
async def action_courseplan_add(request):
    params = await request.post()
    cou_cno = params.get("cou_cno")
    semester = params.get("semester")
    week = params.get("week")
    time = params.get("time")
    site = params.get("site")
    if cou_cno is None or semester is None or week is None or time is None or site is None:
        return web.HTTPBadRequest(text="课程计划输入项不能为空")
    try:
        cou_cno = int(cou_cno)
        semester = str(semester)
        week = str(week)
        time = str(time)
        site = str(site)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")
    try: 
        with db_block() as db:
            db.execute("""
            INSERT INTO courseplan(pla_cno,semester,week,time,site)
            VALUES(%(cou_cno)s,%(semester)s,%(week)s,%(time)s,%(site)s)
            """,dict(cou_cno=cou_cno,semester=semester,week=week,time=time,site=site))
    except psycopg2.errors.UniqueViolation:
        query = urlencode({
            "message":"已经添加该课程计划",
            "return":"/tcourseplan_info"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except psycopg2.errors.ForeignKeyViolation as ex:
        return web.HTTPFound(text=f"无此课程：{ex}")
    return web.HTTPFound(location='/tcourseplan_info')