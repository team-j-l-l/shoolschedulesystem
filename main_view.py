from aiohttp import web
from .config import db_block, web_routes,render_html

@web_routes.get("/")
async def view_main(request):
	return web.HTTPFound('/student_info')