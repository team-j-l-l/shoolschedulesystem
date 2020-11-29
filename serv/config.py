from re import template
from aiohttp import web
import jinja2
from pathlib import Path
from .dbconn import register_db_block

home_path = Path(__file__).parent.parent

web_routes = web.RouteTableDef()
db_block = register_db_block(
    dsn = "host=localhost dbname=schoolschedule user=manager password=pass"
)
jinja_env = jinja2.Environment(
	loader=jinja2.FileSystemLoader(str(home_path/"templates"))
)
def render_html(template,**kwargs):
    html = jinja_env.get_template(template).render(**kwargs)
    return web.Response(text=html,content_type="text/html")