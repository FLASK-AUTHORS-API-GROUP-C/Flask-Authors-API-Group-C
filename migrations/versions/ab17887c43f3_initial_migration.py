"""initial migration

Revision ID: ab17887c43f3
Revises: 
Create Date: 2025-03-13 10:43:42.514104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab17887c43f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('last_name', sa.String(length=20), nullable=False),
    sa.Column('biography', sa.String(length=20), nullable=True),
    sa.Column('contact', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('contact'),
    sa.UniqueConstraint('email')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('origin', sa.String(length=10), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('unit_price', sa.String(length=10), nullable=False),
    sa.Column('image', sa.String(length=50), nullable=True),
    sa.Column('bio', sa.String(length=30), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('price', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('image', sa.String(length=50), nullable=True),
    sa.Column('publication_date', sa.Date(), nullable=False),
    sa.Column('isbn', sa.String(length=30), nullable=True),
    sa.Column('pages', sa.String(length=30), nullable=False),
    sa.Column('genre', sa.String(length=50), nullable=False),
    sa.Column('unit_price', sa.String(length=20), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Books')
    op.drop_table('companies')
    op.drop_table('authors')
    # ### end Alembic commands ###
