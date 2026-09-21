from sqlalchemy import text
from database.db import engine

class userRepository:

    @staticmethod
    def create_user(user):
       
        sql = text("""
            INSERT INTO users (username, password_hash, role)
            VALUES (:username, :password, :role)
            RETURNING id;
        """)
        
        with engine.connect() as conn:
            result = conn.execute(
                sql,
                {
                    "username": user.username,
                    "password": user.password,  # ప్లెయిన్ టెక్స్ట్ ఇన్‌పుట్
                    "role": user.role
                }
            )
            
            user_id = result.fetchone()[0]
            
            # డేటాబేస్ లో మార్పులను సేవ్ చేయడం (Commit)
            conn.commit()
            
        return user_id
    
    @staticmethod
    def get_users():
        """
        మొత్తం యూజర్ల లిస్ట్‌ను డిక్షనరీ ఫార్మాట్‌లో తెస్తుంది (FastAPI రూటర్ కోసం).
        """
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, username, password_hash, role FROM users"))
            users = []
            for row in result:
                users.append({
                    "id": row.id,
                    "username": row.username,
                    "password": row.password_hash,
                    "role": row.role
                })
        return users

    @staticmethod
    def get_user(user_id):
        with engine.connect() as conn:
            row = conn.execute(
                text("""
                    SELECT id, username, password_hash, role
                    FROM users
                    WHERE id = :user_id
                """),
                {"user_id": user_id}
            ).mappings().first()
            if not row:
                return None
            return {
                "id": row["id"],
                "username": row["username"],
                "password": row["password_hash"],
                "role": row["role"]
            }

    @staticmethod
    def update_user(user_id, user):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    UPDATE users
                    SET username = :username, password_hash = :password, role = :role
                    WHERE id = :user_id
                """),
                {
                    "user_id": user_id,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role
                }
            )
            return result.rowcount > 0

    @staticmethod
    def delete_user(user_id):
        with engine.begin() as conn:
            result = conn.execute(
                text("DELETE FROM users WHERE id = :user_id"),
                {"user_id": user_id}
            )
            return result.rowcount > 0