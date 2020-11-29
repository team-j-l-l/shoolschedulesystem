from aiohttp import web
from .config import db_block, web_routes,render_html


@web_routes.get("/grade_info")
async def view_list_grade(request):
	with db_block() as db:
		db.execute('''
		SELECT stu_sno_gra as stu_sno_gra, stu_sname_gra as stu_sname_gra,
		cou_cno_gra as cou_cno_gra, cou_cname_gra as cou_cname_gra,
		cou_credit_gra as cou_credit_gra, grade as grade FROM grade
		''')
		items = list(db)
	return render_html("grade_info.html",items=items)

@web_routes.get("/grade/edit/{stu_sno_gra}/{cou_cno_gra}")
def view_grade_editor(request):
	stu_sno_gra = request.match_info.get("stu_sno_gra")
	cou_cno_gra = request.match_info.get("cou_cno_gra")
	if stu_sno_gra is None or cou_cno_gra is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra, must be required")
	with db_block() as db:
		db.execute("""
		SELECT grade FROM grade
			WHERE stu_sno_gra = %(stu_sno_gra)s AND cou_cno_gra = %(cou_cno_gra)s;
		""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra))
		record = db.fetch_first()
	if record is None:
		return web.HTTPNotFound(text=f"no such grade:stu_sno_gra={stu_sno_gra},cou_cno_gra={cou_cno_gra}")
	return render_html("grade_edit.html",stu_sno_gra=stu_sno_gra,
                        cou_cno_gra=cou_cno_gra,grade=record.grade)
