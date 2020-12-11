from aiohttp import web
from .config import db_block, web_routes,render_html
from .grade_actions import get_cou_cno


@web_routes.get("/grademanage_info")
async def view_list_grade(request):
	with db_block() as db:
		db.execute('''
		SELECT sno AS stu_sno, sname AS stu_sname FROM student ORDER BY sname
		''')
		students = list(db)
		db.execute("""
		SELECT cp.pla_cno AS cou_cno, c.cname AS cou_cname, c.credit AS cou_credit
		FROM courseplan as cp INNER JOIN course as c ON cp.pla_cno=c.cno ORDER BY pla_cno;
				""")
		courses = list(db)
		db.execute("""
		SELECT g.sno_cou as stu_sno,
			g.cno_cou as cou_cno,
			s.sname as stu_sname,
			c.cname as cou_cname,
			c.credit as cou_credit,
			g.grade
		FROM studentcourse as g
			INNER JOIN student as s ON g.sno_cou=s.sno
			INNER JOIN course as c ON g.cno_cou=c.cno
		ORDER BY sno_cou,cno_cou;
		""")
		items = list(db)
	return render_html(request,"grademanage_info.html",students=students,
	courses = courses, items=items)

@web_routes.get("/grademanage/choose")
async def view_course_grade(request):
	cou_cno_gra = get_cou_cno()
	print(cou_cno_gra)
	with db_block() as db:
		db.execute("""
		SELECT g.sno_cou as stu_sno,
			g.cno_cou as cou_cno,
			s.sname as stu_sname,
			c.cname as cou_cname,
			c.credit as cou_credit,
			g.grade
		FROM studentcourse as g
			INNER JOIN student as s ON g.sno_cou=s.sno
			INNER JOIN course as c ON g.cno_cou=c.cno
		WHERE cno_cou=%(cou_cno_gra)s;
		""",dict(cou_cno_gra=cou_cno_gra))
		items = list(db)
	with db_block() as db:
		db.execute('''
		SELECT sno AS stu_sno, sname AS stu_sname FROM student ORDER BY sname
		''')
		students = list(db)
	return render_html(request,"grade_coursex_view.html",items=items,students=students)

@web_routes.get("/grade/edit/{stu_sno_gra}/{cou_cno_gra}")
def view_grade_editor(request):
	stu_sno_gra = request.match_info.get("stu_sno_gra")
	cou_cno_gra = request.match_info.get("cou_cno_gra")
	if stu_sno_gra is None or cou_cno_gra is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra, must be required")
	with db_block() as db:
		db.execute("""
		SELECT grade FROM studentcourse
			WHERE sno_cou = %(stu_sno_gra)s AND cno_cou = %(cou_cno_gra)s;
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
        SELECT g.sno_cou as stu_sno,
		 	g.cno_cou as cou_cno,
            s.sname as stu_sname, 
            c.cname as cou_cname, 
			c.credit as cou_credit,
            g.grade 
        FROM studentcourse as g
            INNER JOIN student as s ON g.sno_cou = s.sno
            INNER JOIN course as c  ON g.cno_cou = c.cno
        WHERE sno_cou = %(stu_sno_gra)s AND cno_cou = %(cou_cno_gra)s;
        """, dict(stu_sno_gra=stu_sno_gra, cou_cno_gra=cou_cno_gra))
        record = db.fetch_first()
    if record is None:
        return web.HTTPNotFound(text=f"no such grade: stu_sn={stu_sno_gra}, cou_sn={cou_cno_gra}")
    return render_html(request,'grade_delete.html', record=record)