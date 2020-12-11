from aiohttp import web
from .config import db_block, web_routes, render_html


@web_routes.post('/action/login/')
async def login_student_action(request):
    params = await request.post()
    username = params.get('username')
    password = params.get('password')
    usertype = params.get('logintype')
    global x 
    x = username
    if username is None or password is None:
        return web.HTTPBadRequest(text="username,password, must be required")
    if usertype == "学生":
        with db_block() as db:
            db.execute("""
            SELECT sno, scode FROM student
            """)
            check = list(db)
        for items in check:
            username1 = items.sno
            if username1 == username:
                password1 = items.scode
                if password == password1:
                    return web.HTTPFound(location="/stu_main")
    if usertype == "教师":
        with db_block() as db:
            db.execute("""
            SELECT tno, tcode FROM teacher
            """)
            check = list(db)
        for items in check:
            username1 = items.tno
            if username1 == username:
                password1 = items.tcode
                if password == password1:
                    return web.HTTPFound(location="/tea_main")


def get_username():
    return x