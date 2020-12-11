from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode
from .config import db_block, web_routes

@web_routes.post('/action/grademanage/course/')
async def choose_course_grade(request):
	params = await request.post()
	cou_cno_gra = params.get("cou_cno")
	global y
	y = cou_cno_gra
	return web.HTTPFound(location="/grademanage/choose")
	
def get_cou_cno():
	return y

@web_routes.post('/action/grade/edit/{stu_sno_gra}/{cou_cno_gra}')
async def edit_grade_action(request):
	stu_sno_gra = request.match_info.get("stu_sno_gra")
	cou_cno_gra = request.match_info.get("cou_cno_gra")
	if stu_sno_gra is None or cou_cno_gra is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra, must be required")
	params = await request.post()
	grade = params.get("grade")

	try:
		stu_sno_gra = str(stu_sno_gra)
		cou_cno_gra = str(cou_cno_gra)
		grade = float(grade)
	except ValueError:
		return web.HTTPBadRequest(text="invalid value")

	with db_block() as db:
		db.execute("""
		UPDATE studentcourse SET grade=%(grade)s
		WHERE sno_cou = %(stu_sno_gra)s AND cno_cou = %(cou_cno_gra)s
		""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra,grade=grade))
	return web.HTTPFound(location="/grademanage/choose")

@web_routes.post('/action/grade/delete/{stu_sno_gra}/{cou_cno_gra}')
def delete_grade_action(request):
	stu_sno_gra = request.match_info.get("stu_sno_gra")
	cou_cno_gra = request.match_info.get("cou_cno_gra")
	if stu_sno_gra is None or cou_cno_gra is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra,must be required")
	with db_block() as db:
		db.execute("""
		DELETE FROM studentcourse
			WHERE sno_cou = %(stu_sno_gra)s AND cno_cou = %(cou_cno_gra)s
		""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra))
		return web.HTTPFound(location="/grademanage/choose")