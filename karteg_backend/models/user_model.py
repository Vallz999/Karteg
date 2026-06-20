from database.db import fetch_one, fetch_all, execute_query


class UserModel:

    @staticmethod
    def find_by_username(username):
        return fetch_one(
            "SELECT * FROM user WHERE username=%s",
            (username,)
        )

    @staticmethod
    def find_by_id(user_id):
        return fetch_one(
            "SELECT * FROM user WHERE id_user=%s",
            (user_id,)
        )

    @staticmethod
    def get_all():
        return fetch_all(
            "SELECT id_user, username, role FROM user"
        )

    @staticmethod
    def create(username, password, role):
        return execute_query("""
            INSERT INTO user
            (username,password,role)
            VALUES (%s,%s,%s)
        """, (
            username,
            password,
            role
        ))

    @staticmethod
    def delete(user_id):
        return execute_query(
            "DELETE FROM user WHERE id_user=%s",
            (user_id,)
        )