from .. import db


class Permission:
    ACCESS = 1
    SELF_MANAGEMENT = 2
    SELLING = 4
    BUYING = 8
    USER_ADMINISTRATION = 16
    STATUS_CHANGING = 32
    ADD_WORKER = 64
    CHANGE_ROLE = 128


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    permissions = db.Column(db.Integer, default=0)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.ACCESS, Permission.SELF_MANAGEMENT, Permission.SELLING],
            'Worker': [Permission.ACCESS, Permission.SELF_MANAGEMENT, Permission.SELLING,
                       Permission.BUYING, Permission.USER_ADMINISTRATION, Permission.STATUS_CHANGING],
            'Administrator': [Permission.ACCESS, Permission.SELF_MANAGEMENT, Permission.SELLING,
                              Permission.BUYING, Permission.USER_ADMINISTRATION, Permission.STATUS_CHANGING,
                              Permission.ADD_WORKER, Permission.CHANGE_ROLE]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return f"<Role {self.name} (default {self.default})>"
