from aiohttp import web
from aiohttp.web_request import Request
from .config import db_block, web_routes,render_html

@web_routes.get("/student_info")
async def view_student_info(request):
	return render_html(request,'student_info.html')