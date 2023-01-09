from ..models import User, Status, UserStatus


class UserListService:
    @staticmethod
    def get(option: str = None):
        if option == 'active':
            return UserListService.only_active()
        if option == 'waiting':
            return UserListService.only_waiting()
        if option == 'banned':
            return UserListService.only_banned()
        else:
            return UserListService.get_all()

    @staticmethod
    def get_all():
        return User.query.order_by(User.last_name).all()

    @staticmethod
    def only_waiting():
        return User.query \
            .join(Status, User.status_id == Status.status_id) \
            .filter(Status.name == UserStatus.WAITING.value) \
            .order_by(User.last_name) \
            .all()

    @staticmethod
    def only_active():
        return User.query \
            .join(Status, User.status_id == Status.status_id) \
            .filter(Status.name == UserStatus.ACTIVE.value) \
            .order_by(User.last_name) \
            .all()

    @staticmethod
    def only_banned():
        return User.query \
            .join(Status, User.status_id == Status.status_id) \
            .filter(Status.name == UserStatus.BANNED.value) \
            .order_by(User.last_name) \
            .all()
