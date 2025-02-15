from fastapi import APIRouter

from app.api.v1.endpoints import (
    # auth,
    # dependents,
    # payments,
    # plans,
    # roles,
    # services,
    # statuses,
    # subscriptions,
    users,
)

api_router = APIRouter()

# Include all endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_router.include_router(
#     subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"]
# )
# api_router.include_router(plans.router, prefix="/plans", tags=["Plans"])
# api_router.include_router(services.router, prefix="/services", tags=["Services"])
# api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
# api_router.include_router(statuses.router, prefix="/statuses", tags=["Statuses"])
# api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
# api_router.include_router(dependents.router, prefix="/dependents", tags=["Dependents"])
