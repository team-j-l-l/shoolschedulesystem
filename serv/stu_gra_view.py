from aiohttp import web
from .config import db_block, web_routes, render_html
from .login_actions import get_username

@web_routes.get("/stu_gra_info")
async def view_stu_gra_info(request):
    username = get_username()
    print(username)
    with db_block() as db:
        db.execute("""
        SELECT g.sno_gra, g.cno_gra, g.grade, c.cno, c.cname, c.credit,
        c.ctype FROM gradetable as g
        INNER JOIN course as c ON g.cno_gra = c.cno
        ORDER BY cno_gra;
        """)
        items = list(db)
        for item in items: 
            if item.sno_gra != username:
                items.remove(item)
    return render_html(request,"stu_gra_info.html",items=items)