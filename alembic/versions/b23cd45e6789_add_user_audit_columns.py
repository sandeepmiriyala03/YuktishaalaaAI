"""Add createdby and modifiedby to users."""
from alembic import op
import sqlalchemy as sa

revision = "b23cd45e6789"
down_revision = "a12bc34d5678"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column(
            "createdby",
            sa.String(length=50),
            nullable=False,
            server_default="System",
        ),
    )
    op.add_column(
        "users",
        sa.Column("modifiedby", sa.String(length=50), nullable=True),
    )


def downgrade():
    op.drop_column("users", "modifiedby")
    op.drop_column("users", "createdby")