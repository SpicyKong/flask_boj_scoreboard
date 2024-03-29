"""empty message

Revision ID: dbc97386db4b
Revises: 
Create Date: 2021-09-20 05:06:42.476610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbc97386db4b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('USERNAME', sa.String(length=40), nullable=False),
    sa.Column('TIMESTAMP', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('problem',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('USER_ID', sa.Integer(), nullable=False),
    sa.Column('B_ID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['USER_ID'], ['user.ID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('week_board',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('USER_ID', sa.Integer(), nullable=False),
    sa.Column('WEEK', sa.Integer(), nullable=False),
    sa.Column('MON', sa.Integer(), nullable=False),
    sa.Column('TUE', sa.Integer(), nullable=False),
    sa.Column('WED', sa.Integer(), nullable=False),
    sa.Column('THU', sa.Integer(), nullable=False),
    sa.Column('FRI', sa.Integer(), nullable=False),
    sa.Column('SAT', sa.Integer(), nullable=False),
    sa.Column('SUN', sa.Integer(), nullable=False),
    sa.Column('TOTAL', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['USER_ID'], ['user.ID'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('week_board')
    op.drop_table('problem')
    op.drop_table('user')
    # ### end Alembic commands ###
