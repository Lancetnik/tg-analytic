from pathlib import Path
from functools import lru_cache

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


INDEX_DIR = Path(__file__).resolve().parent
TEMPLATE = INDEX_DIR / 'templates' / 'index.html'
STATIC_DIR = INDEX_DIR / 'static'

html_router = APIRouter()
static = StaticFiles(directory=STATIC_DIR)


@lru_cache(maxsize=1)
def get_html():
    return TEMPLATE.read_text()


@html_router.get("/", response_class=HTMLResponse)
async def get_index(html: str = Depends(get_html)):
    return html
