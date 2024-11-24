from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pygwalker as pyg
import pandas as pd
from starlette.requests import Request

app = FastAPI()

# Ignore requests for favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(status_code=204)  # No Content



templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_pygwalker_view(request: Request):
    try:
        df = pd.read_csv("static/population.csv")

        gwalker = pyg.walk(df)
        gwalker_html = gwalker.to_html()  # Use the PyGWalker HTML output
    except Exception as e:
        print(f"Error generating PyGWalker plot: {e}")
        return f"Error generating PyGWalker plot: {e}"
    
    return templates.TemplateResponse("index.html", {"request": request, "plot": gwalker_html})

