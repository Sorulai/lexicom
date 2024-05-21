from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from .api.routers import router
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.get("/", include_in_schema=False)
def homepage():
    return RedirectResponse(url="/docs/")


app.include_router(router)
