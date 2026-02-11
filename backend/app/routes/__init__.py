from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.roles import router as roles_router
from app.routes.permissions import router as permissions_router
from app.routes.memberships import router as memberships_router
from app.routes.accounts import router as accounts_router
from app.routes.transactions import router as transactions_router
from app.routes.invoices import router as invoices_router
from app.routes.payments import router as payments_router
from app.routes.reports import router as reports_router

__all__ = [
    "auth_router",
    "users_router",
    "roles_router",
    "permissions_router",
    "memberships_router",
    "accounts_router",
    "transactions_router",
    "invoices_router",
    "payments_router",
    "reports_router",
]
