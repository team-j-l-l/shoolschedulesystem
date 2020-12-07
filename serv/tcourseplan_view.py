from aiohttp import web
from .config import db_block, web_routes, render_html

@web_routes.get("/tcourseplan_info")
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
    return render_html(request,"tcourseplan_info.html",courses = courses,items = items)

@web_routes.get("/tcourseplan/edit/{cou_cno}")
def view_courseplan_editor(request):
    cou_cno = request.match_info.get("cou_cno")
    with db_block() as db:
        db.execute("""
            SELECT semester,week,time,site FROM courseplan 
            WHERE pla_cno = %(cou_cno)s; 
        """,dict(cou_cno=cou_cno))
        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such course:cou_cno={cou_cno}")
    return render_html(request,"tcourseplan_edit.html",cou_cno=cou_cno,semester = record.semester,week=record.week,time=record.time,site=record.site) 

@web_routes.get("/tcourseplan/delete/{cou_cno}")
def grade_deletion_dialog(request):
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
    if record is None:
        return web.HTTPNotFound(text=f"no such course：cou_cno={cou_cno}")
    return render_html(request,"tcourseplan_delete.html",record=record)
