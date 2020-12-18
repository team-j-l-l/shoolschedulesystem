from aiohttp import web
from .config import db_block, web_routes, render_html
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet

secret_key = Fernet.generate_key()
print(f"Generated Secure Key:{secret_key}")
fernet = Fernet(secret_key)

@web_routes.post('/action/login/')
async def login_action(request):
    params = await request.post()
    username = params.get('username')
    password = params.get('password')
    usertype = params.get('logintype')
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
                    resp = web.HTTPFound("/stu_main")
                    set_secure_cookie(resp,"session_id",str(username))
                    return resp
                
    if usertype == "教师":
        with db_block() as db:
            db.execute("""
            SELECT tno, tcode FROM teacher
            """)
            check = list(db)
        for items in check:
            username2 = items.tno
            if username2 == username:
                password2 = items.tcode
                if password == password2:
                    resp = web.HTTPFound("/tea_main")
                    set_secure_cookie(resp,"session_id",str(username))
                    return resp
    

def set_secure_cookie(response, name, value, **kwargs):
    value = fernet.encrypt(value.encode('utf-8')).decode('utf-8')
    response.set_cookie(name,value,**kwargs)

def get_secure_cookie(request,name):
    value = request.cookies.get(name)
    if value is None:
        return None
    try:
        buffer = value.encode('utf-8')
        buffer = fernet.decrypt(buffer)
        secured_value = buffer.decode('utf-8')
        return secured_value
    except InvalidToken:
        print("cannot decrypt cookie value")
        return None

def get_current_user(request):
    username = get_secure_cookie(request,"session_id")
    return username