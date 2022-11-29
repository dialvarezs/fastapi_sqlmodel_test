"""Added notes

Revision ID: 69d2c4c7c540
Revises: d0d637c10cd3
Create Date: 2022-11-28 12:30:21.848540

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "69d2c4c7c540"
down_revision = "d0d637c10cd3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notes",
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(length=32), nullable=False),
        sa.Column(
            "detail", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=False
        ),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("is_archived", sa.Boolean(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notes")
    # ### end Alembic commands ###
