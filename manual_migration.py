from alembic import op
import sqlalchemy as sa

# Укажите уникальный идентификатор ревизии
revision = 'unique_revision_id'
down_revision = None  # или укажите предыдущую ревизию, если она есть
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("telegram_id", sa.BigInteger, unique=True, index=True),
        sa.Column("full_name", sa.String(255))
    )

    op.create_table(
        "groups",
        sa.Column("group_id", sa.BigInteger, primary_key=True, index=True),
        sa.Column("admin_id", sa.BigInteger, nullable=False)
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("groups")
