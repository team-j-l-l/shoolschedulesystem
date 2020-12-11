from aiohttp import web
from .config import db_block, web_routes,render_html
from .login_actions import get_username

@web_routes.get("/stu_main")
async def view_login(request):
	username = get_username()
	with db_block() as db:
		db.execute("""
		SELECT sno, sname, sgender, sage, enrolled, major FROM student
		WHERE sno = %(username)s
		""",dict(username=username))
		items = list(db)
	return render_html(request,'stu_main.html')

@web_routes.get("/tea_main")
async def view_login(request):
	username = get_username()
	with db_block() as db:
		db.execute("""
		SELECT tno, tname, tgender, tage FROM teacher
		WHERE tno = %(username)s
		""",dict(username=username))
		items = list(db)
	return render_html(request,'tea_main.html')

@web_routes.get("/login")
async def view_login(request):
	return render_html(request,'login.html')