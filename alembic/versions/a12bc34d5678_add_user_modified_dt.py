"""Add modified timestamp to PostgreSQL users."""
from alembic import op
import sqlalchemy as sa

revision = "a12bc34d5678"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("modified_Dt", sa.TIMESTAMP(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_column("users", "modified_Dt")