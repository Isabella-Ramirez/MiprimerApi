"""enable_rls_on_tables

Revision ID: 19d18a11eda4
Revises: 003_tables
Create Date: 2025-09-10 22:55:41.146003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19d18a11eda4'
down_revision: Union[str, Sequence[str], None] = '003_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Enable Row Level Security on all tables."""
    
    # List of all tables that need RLS enabled
    tables = [
        'alembic_version',
        'roles',
        'users', 
        'guests',
        'room_types',
        'rooms',
        'reservations',
        'reservation_guests',
        'reservation_rooms',
        'payments'
    ]
    
    # Enable RLS on each table
    for table in tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    
    # Create basic policies for each table
    # Note: These are permissive policies - you should customize them based on your security requirements
    
    # Policy for alembic_version (system table, usually read-only for authenticated users)
    op.execute("""
        CREATE POLICY "Allow read access to alembic_version" ON alembic_version
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    # Policies for roles (typically read-only for authenticated users)
    op.execute("""
        CREATE POLICY "Allow read access to roles" ON roles
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    # Policies for users (users can read their own data, admins can read all)
    op.execute("""
        CREATE POLICY "Users can view own profile" ON users
        FOR SELECT USING (auth.uid() = id OR auth.role() = 'service_role')
    """)
    
    op.execute("""
        CREATE POLICY "Users can update own profile" ON users
        FOR UPDATE USING (auth.uid() = id OR auth.role() = 'service_role')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can insert users" ON users
        FOR INSERT WITH CHECK (auth.role() = 'service_role')
    """)

    # Policies for guests (authenticated users can read, service role can manage)
    op.execute("""
        CREATE POLICY "Allow read access to guests" ON guests
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage guests" ON guests
        FOR ALL USING (auth.role() = 'service_role')
    """)
    
    # Policies for room_types (read-only for authenticated users)
    op.execute("""
        CREATE POLICY "Allow read access to room_types" ON room_types
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage room_types" ON room_types
        FOR ALL USING (auth.role() = 'service_role')
    """)
    
    # Policies for rooms
    op.execute("""
        CREATE POLICY "Allow read access to rooms" ON rooms
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage rooms" ON rooms
        FOR ALL USING (auth.role() = 'service_role')
    """)
    
    # Policies for reservations
    op.execute("""
        CREATE POLICY "Allow read access to reservations" ON reservations
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage reservations" ON reservations
        FOR ALL USING (auth.role() = 'service_role')
    """)
    
    # Policies for reservation_guests
    op.execute("""
        CREATE POLICY "Allow read access to reservation_guests" ON reservation_guests
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage reservation_guests" ON reservation_guests
        FOR ALL USING (auth.role() = 'service_role')
    """)
    
    # Policies for reservation_rooms
    op.execute("""
        CREATE POLICY "Allow read access to reservation_rooms" ON reservation_rooms
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage reservation_rooms" ON reservation_rooms
        FOR ALL USING (auth.role() = 'service_role')
    """)
    
    # Policies for payments
    op.execute("""
        CREATE POLICY "Allow read access to payments" ON payments
        FOR SELECT USING (auth.role() = 'authenticated')
    """)
    
    op.execute("""
        CREATE POLICY "Service role can manage payments" ON payments
        FOR ALL USING (auth.role() = 'service_role')
    """)


def downgrade() -> None:
    """Disable Row Level Security on all tables."""
    
    # List of all tables that need RLS disabled
    tables = [
        'alembic_version',
        'roles',
        'users', 
        'guests',
        'room_types',
        'rooms',
        'reservations',
        'reservation_guests',
        'reservation_rooms',
        'payments'
    ]
    
    # Drop all policies and disable RLS on each table
    for table in tables:
        # Drop all policies for the table
        op.execute(f"DROP POLICY IF EXISTS \"Allow read access to {table}\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Users can view own profile\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Users can update own profile\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can insert users\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage {table}\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage user_roles\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage guests\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage room_types\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage rooms\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage reservations\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage reservation_guests\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage reservation_rooms\" ON {table}")
        op.execute(f"DROP POLICY IF EXISTS \"Service role can manage payments\" ON {table}")
        
        # Disable RLS
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
