from aiohttp import web
from .config import db_block, web_routes,render_html
import psycopg2.errors
from urllib.parse import urlencode
from .login_actions import get_current_user

@web_routes.get("/passwordchange/teacher")
async def view_password_change1(request):
    return render_html(request,'tpasswordchange.html')

@web_routes.get("/passwordchange/student")
async def view_password_change2(request):
    return render_html(request,'spasswordchange.html')

@web_routes.post("/action/password/change/teacher")
async def edit_password(request):
    username = get_current_user(request)
    params = await request.post()
    newpassword = params.get("password")
    with db_block() as db:
        db.execute("""
        UPDATE teacher SET tcode = %(newpassword)s
        WHERE tno = %(username)s;
        """,dict(username=username,newpassword=newpassword))
    return web.HTTPFound(location="/tea_main")

@web_routes.post("/action/password/change/student")
async def edit_password(request):
    username = get_current_user(request)
    params = await request.post()
    newpassword = params.get("password")
    with db_block() as db:
        db.execute("""
        UPDATE student SET scode = %(newpassword)s
        WHERE sno = %(username)s;
        """,dict(username=username,newpassword=newpassword))
    return web.HTTPFound(location="/stu_main")