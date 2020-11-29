from aiohttp import web
from .config import db_block, web_routes,render_html

@web_routes.get("/courseplan_info")
async def view_list_courseplan(request):
	with db_block() as db:
		db.execute('''
		SELECT cou_cno as cou_cno, cou_cname as cou_cname,
		credit as credit, semester as semester, 
		teacher as teacher, week as week, 
		time as time, site as site FROM courseplan 
		''')
		items = list(db)

	return render_html("courseplan_info.html",items=items)