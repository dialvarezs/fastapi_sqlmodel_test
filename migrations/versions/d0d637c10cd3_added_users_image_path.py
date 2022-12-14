"""Added users.image_path

Revision ID: d0d637c10cd3
Revises: 29004f6c303f
Create Date: 2022-10-25 14:49:41.728049

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "d0d637c10cd3"
down_revision = "29004f6c303f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "image_path", sqlmodel.sql.sqltypes.AutoString(length=256), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "image_path")
    # ### end Alembic commands ###
