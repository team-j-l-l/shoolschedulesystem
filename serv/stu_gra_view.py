from aiohttp import web
from .config import db_block, web_routes, render_html
from .login_actions import get_username

@web_routes.get("/stu_gra_info")
async def view_stu_gra_info(request):
    username = get_username()
    with db_block() as db:
        db.execute("""
        SELECT g.sno_cou, g.cno_cou, g.grade, c.cno, c.cname, c.credit,
        c.ctype FROM studentcourse as g
        INNER JOIN course as c ON g.cno_cou = c.cno
        ORDER BY cno_cou;
        """)
        items = list(db)
        for item in items: 
            if item.sno_cou != username:
                items.remove(item)
        for item in items:
            if item.grade == None:
                item.grade = "尚未登记"
    return render_html(request,"stu_gra_info.html",items=items)