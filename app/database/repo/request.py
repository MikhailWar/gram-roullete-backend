from app.database.repo.base import BaseRepo
from app.database.repo.game import GameRepo
from app.database.repo.user import UserRepo


class RequestRepo(BaseRepo):

    @property
    def users(self):
        return UserRepo(self.session)

    @property
    def game(self):
        return GameRepo(self.session)




