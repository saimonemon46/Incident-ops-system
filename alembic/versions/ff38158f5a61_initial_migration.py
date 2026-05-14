"""initial_migration

Revision ID: ff38158f5a61
Revises:
Create Date: 2026-05-10 21:41:33.047044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "ff38158f5a61"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role = postgresql.ENUM("ENGINEER", "MANAGER", "ADMIN", name="userrole")
severity = postgresql.ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL", name="severity")
status = postgresql.ENUM("OPEN", "IN_PROGRESS", "RESOLVED", name="status")
incident_category = postgresql.ENUM(
    "PAYMENT",
    "AUTH",
    "DATABASE",
    "NETWORK",
    "PERFORMANCE",
    "UNKNOWN",
    name="incidentcategory",
)

user_role_column = postgresql.ENUM("ENGINEER", "MANAGER", "ADMIN", name="userrole", create_type=False)
severity_column = postgresql.ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL", name="severity", create_type=False)
status_column = postgresql.ENUM("OPEN", "IN_PROGRESS", "RESOLVED", name="status", create_type=False)
incident_category_column = postgresql.ENUM(
    "PAYMENT",
    "AUTH",
    "DATABASE",
    "NETWORK",
    "PERFORMANCE",
    "UNKNOWN",
    name="incidentcategory",
    create_type=False,
)


def upgrade() -> None:
    """Create the application schema."""
    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    severity.create(bind, checkfirst=True)
    status.create(bind, checkfirst=True)
    incident_category.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_column, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    op.create_table(
        "incidents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", severity_column, nullable=False),
        sa.Column("status", status_column, nullable=False),
        sa.Column("assigned_to", sa.String(length=100), nullable=True),
        sa.Column("category", incident_category_column, nullable=True),
        sa.Column("suggested_fix", sa.Text(), nullable=True),
        sa.Column("ai_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("sla_deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sla_breached", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_incidents_id"), "incidents", ["id"], unique=False)


def downgrade() -> None:
    """Drop the application schema."""
    bind = op.get_bind()

    op.drop_index(op.f("ix_incidents_id"), table_name="incidents")
    op.drop_table("incidents")

    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    incident_category.drop(bind, checkfirst=True)
    status.drop(bind, checkfirst=True)
    severity.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
