from aiohttp import web
from .config import db_block, web_routes,render_html


@web_routes.get("/grade_info")
async def view_list_grade(request):
	with db_block() as db:
		db.execute('''
		SELECT sno AS stu_sno, sname AS stu_sname FROM student ORDER BY sname
		''')
		students = list(db)
		db.execute("""
		SELECT cno AS cou_cno, cname AS cou_cname, credit AS cou_credit FROM course ORDER BY cname
		""")
		courses = list(db)
		db.execute("""
		SELECT g.sno_gra as stu_sno,
			g.cno_gra as cou_cno,
			s.sname as stu_sname,
			c.cname as cou_cname,
			c.credit as cou_credit,
			g.grade
		FROM gradetable as g
			INNER JOIN student as s ON g.sno_gra=s.sno
			INNER JOIN course as c ON g.cno_gra=c.cno
		ORDER BY sno_gra,cno_gra;
		""")
		items = list(db)
	return render_html(request,"grade_info.html",students=students,
	courses = courses, items=items)

@web_routes.get("/grade/edit/{stu_sno_gra}/{cou_cno_gra}")
def view_grade_editor(request):
	stu_sno_gra = request.match_info.get("stu_sno_gra")
	cou_cno_gra = request.match_info.get("cou_cno_gra")
	if stu_sno_gra is None or cou_cno_gra is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra, must be required")
	with db_block() as db:
		db.execute("""
		SELECT grade FROM gradetable
			WHERE sno_gra = %(stu_sno_gra)s AND cno_gra = %(cou_cno_gra)s;
		""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra))
		record = db.fetch_first()
	if record is None:
		return web.HTTPNotFound(text=f"no such grade:stu_sno_gra={stu_sno_gra},cou_cno_gra={cou_cno_gra}")
	return render_html(request,"grade_edit.html",stu_sno_gra=stu_sno_gra,
                        cou_cno_gra=cou_cno_gra,grade=record.grade)

@web_routes.get("/grade/delete/{stu_sno_gra}/{cou_cno_gra}")
def grade_deletion_dialog(request):
    stu_sno_gra = request.match_info.get("stu_sno_gra")
    cou_cno_gra = request.match_info.get("cou_cno_gra")
    if stu_sno_gra is None or cou_cno_gra is None:
        return web.HTTPBadRequest(text="stu_sno_gra, cou_cno_gra, must be required")
    with db_block() as db:
        db.execute("""
        SELECT g.sno_gra as stu_sno,
		 	g.cno_gra as cou_cno,
            s.sname as stu_sname, 
            c.cname as cou_cname, 
			c.credit as cou_credit,
            g.grade 
        FROM gradetable as g
            INNER JOIN student as s ON g.sno_gra = s.sno
            INNER JOIN course as c  ON g.cno_gra = c.cno
        WHERE sno_gra = %(stu_sno_gra)s AND cno_gra = %(cou_cno_gra)s;
        """, dict(stu_sno_gra=stu_sno_gra, cou_cno_gra=cou_cno_gra))
        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sno_gra}, cou_sn={cou_cno_gra}")
    return render_html(request,'grade_delete.html', record=record)