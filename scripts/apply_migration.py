#!/usr/bin/env python3
"""
Apply database migrations for QR Access PRO
"""
import sys
import os

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config.settings import config
from config.database import get_connection

def apply_migration():
    """Apply the fix_user_id_nullable migration."""
    migrations = [
        {
            "name": "Allow NULL user_id in accesos_log",
            "sql": "ALTER TABLE accesos_log MODIFY COLUMN user_id INT NULL;"
        },
        {
            "name": "Add detalles column to accesos_log",
            "sql": "ALTER TABLE accesos_log ADD COLUMN IF NOT EXISTS detalles TEXT NULL;"
        }
    ]
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        print("=" * 60)
        print("  QR Access PRO - Database Migration")
        print("=" * 60)
        print()
        
        for migration in migrations:
            print(f"[*] Applying: {migration['name']}")
            print(f"    SQL: {migration['sql']}")
            try:
                cursor.execute(migration['sql'])
                connection.commit()
                print(f"    ✅ OK")
            except Exception as e:
                print(f"    ❌ ERROR: {e}")
                connection.rollback()
                return False
            print()
        
        # Verify the changes
        print("[*] Verifying changes...")
        cursor.execute("SHOW COLUMNS FROM accesos_log WHERE Field IN ('user_id', 'detalles');")
        results = cursor.fetchall()
        
        for row in results:
            # Results are tuples: (Field, Type, Null, Key, Default, Extra)
            field_name = row[0]
            field_type = row[1]
            is_null = row[2]
            print(f"    Column: {field_name}, Type: {field_type}, Null: {is_null}")
        
        print()
        print("=" * 60)
        print("  ✅ Migration completed successfully!")
        print("=" * 60)
        print()
        print("You can now:")
        print("  1. Restart the Flask app")
        print("  2. Test QR scanning in the web interface")
        print()
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    success = apply_migration()
    sys.exit(0 if success else 1)
