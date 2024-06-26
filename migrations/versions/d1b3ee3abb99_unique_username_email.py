"""Unique username, email

Revision ID: d1b3ee3abb99
Revises: b36272ee1c42
Create Date: 2024-06-01 01:07:07.656068

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d1b3ee3abb99"
down_revision: Union[str, None] = "b36272ee1c42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "user", ["email"])
    op.create_unique_constraint(None, "user", ["username"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    op.drop_constraint(None, "user", type_="unique")
    # ### end Alembic commands ###
