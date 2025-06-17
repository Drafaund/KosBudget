from config.database import DatabaseManager

class ExpenseService:
    @staticmethod
    def add_expense(user_id, category_id, amount, description=None):
        try:
            query = """
                INSERT INTO expenses (user_id, category_id, amount, description)
                VALUES (%s, %s, %s, %s)
            """
            params = (user_id, category_id, amount, description)
            success, _ = DatabaseManager.execute_query(query, params)
            return success
        except Exception as e:
            print(f"[ERROR] add_expense: {e}")
            return False