"""add account_id and relationship_status columns in tasks table

Revision ID: 031a07fb0811
Revises: 885632ab6357
Create Date: 2021-04-14 17:48:33.958394

"""
from typing import List

import sqlalchemy as sa
from alembic import op
from sqlalchemy import text

from auth_api.models import Org
from auth_api.utils.enums import OrgStatus, TaskRelationshipStatus, TaskRelationshipType, TaskStatus, TaskTypePrefix


# revision identifiers, used by Alembic.
revision = '031a07fb0811'
down_revision = '885632ab6357'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('account_id', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('relationship_status', sa.String(length=100), nullable=True))

    conn = op.get_bind()
    org_res = conn.execute(f"SELECT * FROM orgs WHERE status_code in ('PENDING_STAFF_REVIEW', 'REJECTED', 'ACTIVE') AND "
                           f"access_type in ('REGULAR_BCEID', 'EXTRA_PROVINCIAL');")
    org_list: List[Org] = org_res.fetchall()

    for org in org_list:
        org_id = org.id
        user_id = org.created_by_id
        created_time = org.created
        date_submitted = org.created
        name = org.name
        status = TaskStatus.OPEN.value
        task_type = TaskTypePrefix.NEW_ACCOUNT_STAFF_REVIEW.value
        task_relationship_type = TaskRelationshipType.ORG.value

        # Let us seed Tasks table with the existing pending staff review accounts
        if org.status_code == OrgStatus.PENDING_STAFF_REVIEW.value:
            relationship_status = TaskRelationshipStatus.PENDING_STAFF_REVIEW.value
        # Let us seed Tasks table with the existing rejected accounts
        elif org.status_code == OrgStatus.REJECTED.value:
            relationship_status = TaskRelationshipStatus.REJECTED.value
            status = TaskStatus.COMPLETED.value
        # Let us seed Tasks table with the existing active accounts
        else:
            relationship_status = TaskRelationshipStatus.ACTIVE.value
            status = TaskStatus.COMPLETED.value

        # Insert into tasks
        insert_sql = text("INSERT INTO tasks(created, modified, name, date_submitted, relationship_type, "
                          "relationship_id, created_by_id, modified_by_id, related_to, status, type, "
                          "relationship_status) "
                          "VALUES (:created_time, :created_time, :name, :date_submitted, :task_relationship_type, "
                          ":org_id, :user_id, :user_id, :user_id, :status, :task_type, :relationship_status)") \
            .params(
            created_time=created_time, name=name, date_submitted=date_submitted,
            task_relationship_type=task_relationship_type, org_id=org_id, user_id=user_id, status=status,
            task_type=task_type, relationship_status=relationship_status)
        op.execute(insert_sql)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'account_id')
    op.drop_column('tasks', 'relationship_status')
    # Delete the tasks
    op.execute(f"DELETE FROM tasks")
    # ### end Alembic commands ###