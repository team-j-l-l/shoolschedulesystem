
from aiohttp import web
from serv.config import web_routes,home_path
import serv.login_view
import serv.login_actions
import serv.student_view
import serv.student_rest
import serv.grade_views
import serv.grade_actions
import serv.stu_gra_view
import serv.tcourseplan_view
import serv.tcourseplan_actions
import serv.mainpage_view
import serv.stu_coursechoose
import serv.stu_mycourse
import serv.password



app = web.Application()
app.add_routes(web_routes)
app.add_routes([web.static("/",home_path/"static")])

if __name__=="__main__":
	web.run_app(app,port=8080)