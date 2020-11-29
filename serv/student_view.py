from aiohttp import web
from .config import db_block, web_routes,render_html

@web_routes.get("/student_info")
async def view_list_student(request):
	with db_block() as db:
		db.execute('''
			SELECT sno as stu_no, sname as stu_name, gender as stu_gender, 
			enrolled as stu_enrolled, major as stu_major
			FROM student
			''')
		items = list(db)

	return render_html("student_info.html",items=items)