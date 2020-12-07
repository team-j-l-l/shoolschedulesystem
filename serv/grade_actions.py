from aiohttp import web
import psycopg2.errors
from urllib.parse import urlencode
from .config import db_block, web_routes

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
		UPDATE gradetable SET grade=%(grade)s
		WHERE sno_gra = %(stu_sno_gra)s AND cno_gra = %(cou_cno_gra)s
		""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra,grade=grade))
	return web.HTTPFound(location="/grade_info")

@web_routes.post('/action/grade/delete/{stu_sno_gra}/{cou_cno_gra}')
def delete_grade_action(request):
	stu_sno_gra = request.match_info.get("stu_sno_gra")
	cou_cno_gra = request.match_info.get("cou_cno_gra")
	if stu_sno_gra is None or cou_cno_gra is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra,must be required")
	with db_block() as db:
		db.execute("""
		DELETE FROM gradetable
			WHERE sno_gra = %(stu_sno_gra)s AND cno_gra = %(cou_cno_gra)s
		""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra))
		return web.HTTPFound(location="/grade_info")

@web_routes.post('/action/grade/add')
async def action_grade_add(request):
	params = await request.post()
	stu_sno_gra = params.get("stu_sno")
	cou_cno_gra = params.get("cou_cno")
	grade = params.get("grade")

	if stu_sno_gra is None or cou_cno_gra is None or grade is None:
		return web.HTTPBadRequest(text="stu_sno_gra,cou_cno_gra,grade must be required")
	try:
		stu_sno_gra = int(stu_sno_gra)
		cou_cno_gra = str(cou_cno_gra)
		grade = float(grade)
	except ValueError:
		return web.HTTPBadRequest(text="invalid value")
	try:
		with db_block() as db:
			db.execute("""
			INSERT INTO gradetable(sno_gra,cno_gra,grade)
			VALUES(%(stu_sno_gra)s,%(cou_cno_gra)s,%(grade)s)
			""",dict(stu_sno_gra=stu_sno_gra,cou_cno_gra=cou_cno_gra,grade=grade)
			)
	except psycopg2.errors.UniqueViolation:
		query = urlencode({
			"message":"已经添加该学生的该课程成绩",
			"return":"/grade"
		})
		return web.HTTPFound(location=f"/error?{query}")
	except psycopg2.errors.ForeignKeyViolation as ex:
		return web.HTTPBadRequest(text=f"无此学生或课程：{ex}")
	return web.HTTPFound(location='/grade_info')