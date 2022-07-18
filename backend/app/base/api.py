from ninja import NinjaAPI

from app.api.admin.admin import router_admin
from app.api.auth.auth import router_auth
from app.api.hackathons.hackathon import router_hackathons
from app.api.leaderboard.leaderboard import router_leaderboard
from app.api.users.user import router_users

api = NinjaAPI()

api.add_router(prefix='users', router=router_users, tags=["Users"])
api.add_router(prefix='jwt', router=router_auth, tags=["Auth"])
api.add_router(prefix='hackathons', router=router_hackathons, tags=["Hackathons"])
api.add_router(prefix='leaderboard', router=router_leaderboard, tags=["Leaderboard"])
api.add_router(prefix='admin', router=router_admin, tags=["Admin"])
