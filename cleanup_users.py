import os
import sys
from pathlib import Path

# Add project workspace directory to python path
project_dir = str(Path(__file__).resolve().parent)
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from database import SessionLocal
import models
from sqlalchemy import text

def main():
    db = SessionLocal()
    try:
        # 1. Identify users to keep
        # - kty98116@naver.com
        # - Nickname containing "AI 사회자" or "Ai 사회자"
        keep_users = db.query(models.User).filter(
            (models.User.email == 'kty98116@naver.com') | 
            (models.User.nickname.like('%Ai 사회자%')) | 
            (models.User.nickname.like('%AI 사회자%'))
        ).all()
        
        print("Users to keep:")
        for u in keep_users:
            print(f"  - ID: {u.id} | Email: {u.email} | Nickname: {u.nickname}")
            
        keep_ids = [u.id for u in keep_users]
        if not keep_ids:
            print("Error: No matching users to keep found. Aborting.")
            return

        # 2. Delete all other users
        # This will cascade delete comments, ratings, and libraries of deleted users
        deleted_count = db.query(models.User).filter(~models.User.id.in_(keep_ids)).delete(synchronize_session=False)
        print(f"\nDeleted {deleted_count} users.")
        db.commit()

        # 3. Re-index surviving users starting from 1
        # Sort surviving users by current ID
        keep_users_sorted = sorted(keep_users, key=lambda x: x.id)
        
        # Check database dialect
        is_sqlite = "sqlite" in str(db.bind.url).lower()
        print(f"Database dialect is {'SQLite' if is_sqlite else 'MySQL/MariaDB'}")

        # Disable foreign key checks
        if is_sqlite:
            db.execute(text("PRAGMA foreign_keys = OFF;"))
        else:
            db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        id_mapping = {}
        for idx, u in enumerate(keep_users_sorted, start=1):
            old_id = u.id
            new_id = idx
            id_mapping[old_id] = new_id
            print(f"Mapping ID: {old_id} -> {new_id} for {u.email}")
            
            # Update user ID
            db.execute(text("UPDATE users SET id = :new_id WHERE id = :old_id"), {"new_id": new_id, "old_id": old_id})
            
            # Update referencing tables
            db.execute(text("UPDATE chat_messages SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
            db.execute(text("UPDATE ratings SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
            db.execute(text("UPDATE library SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
            db.execute(text("UPDATE candidate_books SET created_by = :new_id WHERE created_by = :old_id"), {"new_id": new_id, "old_id": old_id})
            db.execute(text("UPDATE past_chat_messages SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})

        # Enable foreign key checks
        if is_sqlite:
            db.execute(text("PRAGMA foreign_keys = ON;"))
        else:
            db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            # Reset auto-increment to next ID (length + 1)
            next_id = len(keep_users_sorted) + 1
            db.execute(text(f"ALTER TABLE users AUTO_INCREMENT = {next_id};"))
            print(f"Reset users AUTO_INCREMENT to {next_id}")

        db.commit()
        print("\nRe-indexing completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
