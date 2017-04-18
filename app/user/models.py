# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from ..database import Column, Model, SurrogatePK, db, reference_col, relationship
from ..extensions import bcrypt


class Roles(SurrogatePK, Model):
    """Roles for a users."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.String(500), default="")
    def __init__(self, name="", **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)
    def __repr__(self):
        """Represent instance as a unique string."""
        return '{name}'.format(name=self.name)

class UserRoles(SurrogatePK, Model):
    """User to role relationship."""

    __tablename__ = 'userroles'
    user_id = reference_col('users')
    role_id = reference_col('roles')
    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)
    def __repr__(self):
        """Represent instance as a unique string."""
        return '<UserRoles(u{}/r{})>'.format(self.user_id,self.role_id)


class Permissions(SurrogatePK, Model):
    """Roles for a users."""

    __tablename__ = 'permissions'
    name = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.String(500), default="")
    roles = relationship('Roles', backref='permissions', secondary='permissionroles')
    def __init__(self, name="", **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)
    def __repr__(self):
        """Represent instance as a unique string."""
        return '{name}'.format(name=self.name)




class PermissionRoles(SurrogatePK, Model):
    """Permission to role relationship."""

    __tablename__ = 'permissionroles'
    permission_id = reference_col('permissions')
    role_id = reference_col('roles')
    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)
    def __repr__(self):
        """Represent instance as a unique string."""
        return '<PermissionRoles(u{}/r{})>'.format(self.user_id,self.role_id)




class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=True)
    #: The hashed password
    password = Column(db.Binary(128), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    name = Column(db.String(30), nullable=True)
    #last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    #role = Column(db.String(30), default='member')
    roles = relationship('Roles', backref='users', secondary='userroles')

    def __init__(self, username="missing", name=None, password=None, **kwargs):
        """Create instance."""
        if not name:
            name = username
        db.Model.__init__(self, username=username, name=name, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0}'.format(self.name)

    @property
    def rolenames(self):
        return [r.name for r in self.roles]

    @property
    def permissions(self):
        roles = self.roles
        permissions = []
        for role in roles:
            perm = Roles.get_by_id(role.id).permissions
            for p in perm:
                permissions.append(p.name)
        return list(set(permissions))

    def has(self, permission):
        if permission == None:
            return True
        return permission in self.permissions

    def has_permission(self, permission):
        return self.has(permission)

    def has_role(self, role):
        if role == None:
            return True
        return role in self.rolenames

    @classmethod
    def get_by_username(cls, username):
        """Get record by username."""
        try:
            return cls.query.filter_by(username=username).one()
        except:
            return AnonymousUser()

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

class AnonymousUser(User):
    @property
    def rolenames(self):
        roles = User.get_by_username('anonymous').roles
        return [r.name for r in roles]

    @property
    def permissions(self):
        roles = User.get_by_username('anonymous').roles
        permissions = []
        for role in roles:
            perm = Roles.get_by_id(role.id).permissions
            for p in perm:
                permissions.append(p.name)
        return list(set(permissions))

    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return

