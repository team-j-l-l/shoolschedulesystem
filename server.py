
from aiohttp import web
from serv.config import web_routes,home_path
import serv.course_actions
import serv.course_view
import serv.grade_actions
import serv.main_view
import serv.student_view
import serv.grade_views


app = web.Application()
app.add_routes(web_routes)

if __name__=="__main__":
	web.run_app(app,port=8080)