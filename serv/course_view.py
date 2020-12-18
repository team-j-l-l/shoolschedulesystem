from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes,render_html

@web_routes.get("/course_info")
async def view_course_info(request):
	return render_html(request,'course_info.html')