from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import AsyncSessionLocal
from app.routes import (
    accounts_router,
    auth_router,
    invoices_router,
    memberships_router,
    payments_router,
    permissions_router,
    reports_router,
    roles_router,
    transactions_router,
    users_router,
)
from app.services.seed_service import seed_roles_permissions
from app.config import settings

app = FastAPI(
    title="MemberSync API",
    description="Backend del sistema de administración y control de prepago",
    version="1.0.0",
)

allowed_origins = []
if settings.CORS_ALLOWED_ORIGINS:
    allowed_origins = [origin.strip() for origin in settings.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=settings.CORS_ALLOW_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_seed():
    async with AsyncSessionLocal() as session:
        await seed_roles_permissions(session)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(permissions_router)
app.include_router(memberships_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(invoices_router)
app.include_router(payments_router)
app.include_router(reports_router)
