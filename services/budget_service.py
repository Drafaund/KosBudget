from config.database import DatabaseManager
from datetime import datetime

class BudgetService:
    @staticmethod
    def create_or_update_budget(user_id, monthly_budget):
        """
        Create or update monthly budget
        
        Args:
            user_id (int): User ID
            monthly_budget (float): Monthly budget amount
        """
        budget_month = datetime.now().strftime('%Y-%m-01')
        query = """
        INSERT INTO budgets (user_id, monthly_budget, budget_month)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, budget_month) 
        DO UPDATE SET monthly_budget = EXCLUDED.monthly_budget
        RETURNING budget_id;
        """
        params = (user_id, monthly_budget, budget_month)
        return DatabaseManager.execute_query(query, params)
    
    @staticmethod
    def get_current_budget(user_id):
        """Get current month's budget"""
        budget_month = datetime.now().strftime('%Y-%m-01')
        query = """
        SELECT monthly_budget
        FROM budgets
        WHERE user_id = %s AND budget_month = %s;
        """
        return DatabaseManager.execute_query(query, (user_id, budget_month), fetch=True)
