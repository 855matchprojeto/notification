"""empty message

Revision ID: c146efd5d3c8
Revises: 
Create Date: 2021-11-16 00:40:04.358464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c146efd5d3c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_notificacao',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('guid_usuario', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('conteudo', sa.String(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('guid')
    )
    op.create_table('tb_permissao',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('descricao', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('descricao'),
        sa.UniqueConstraint('nome')
    )
    op.create_table('tb_usuario',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('email_verificado', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('guid'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table('tb_vinculo_permissao_funcao',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('id_permissao', sa.BigInteger(), nullable=True),
        sa.Column('id_funcao', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['id_permissao'], ['tb_permissao.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id_permissao', 'id_funcao')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_vinculo_permissao_funcao')
    op.drop_table('tb_usuario')
    op.drop_table('tb_permissao')
    op.drop_table('tb_notificacao')
    # ### end Alembic commands ###