import ormar

from . import metadata, database


class User(ormar.Model):
    class Meta(ormar.ModelMeta):
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, index=True)
    full_name: str = ormar.Text(index=True)
    email: str = ormar.Text(unique=True, index=True, nullable=False)
    hashed_password: str = ormar.Text(nullable=False)
    is_active: bool = ormar.Boolean(default=True)
    is_superuser: bool = ormar.Boolean(default=False)
