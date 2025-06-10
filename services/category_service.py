# services/category_service.py - VERSI SEDERHANA DAN STABIL
from config.database import DatabaseManager
import streamlit as st

class CategoryService:
    @staticmethod
    def create_or_update_category(user_id, category_data):
        """
        Create or update a category in database
        """
        try:
            # Debug info
            print(f"[DEBUG] Creating category: {category_data['name']} for user: {user_id}")
            
            # First, check if category exists
            check_query = "SELECT category_id FROM categories WHERE user_id = %s AND name = %s;"
            success, existing = DatabaseManager.execute_query(check_query, (user_id, category_data['name']), fetch=True)
            
            if existing:
                # Update existing category
                query = """
                UPDATE categories 
                SET priority = %s, urgency = %s, frequency = %s, impact = %s, 
                    is_active = TRUE, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s AND name = %s
                RETURNING category_id;
                """
                params = (
                    category_data['priority'],
                    category_data['urgency'],
                    category_data['frequency'],
                    category_data['impact'],
                    user_id,
                    category_data['name']
                )
            else:
                # Insert new category
                query = """
                INSERT INTO categories (user_id, name, priority, urgency, frequency, impact, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                RETURNING category_id;
                """
                params = (
                    user_id,
                    category_data['name'],
                    category_data['priority'],
                    category_data['urgency'],
                    category_data['frequency'],
                    category_data['impact']
                )
            
            success, result = DatabaseManager.execute_query(query, params, fetch=True)
            
            if success and result:
                print(f"[DEBUG] Category saved successfully with ID: {result[0]['category_id']}")
                return True, f"Category '{category_data['name']}' saved successfully"
            else:
                print(f"[DEBUG] Failed to save category")
                return False, "Failed to save category"
                
        except Exception as e:
            print(f"[DEBUG] Exception in create_or_update_category: {str(e)}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_categories(user_id):
        """Get all active categories for a user"""
        try:
            print(f"[DEBUG] Getting categories for user: {user_id}")
            
            query = """
            SELECT category_id, name, priority, urgency, frequency, impact, 
                   COALESCE(allocation, 0) as allocation
            FROM categories
            WHERE user_id = %s AND is_active = TRUE
            ORDER BY name;
            """
            
            success, result = DatabaseManager.execute_query(query, (user_id,), fetch=True)
            
            print(f"[DEBUG] Query result - Success: {success}, Count: {len(result) if result else 0}")
            
            if success:
                return True, result if result else []
            else:
                return False, []
                
        except Exception as e:
            print(f"[DEBUG] Exception in get_categories: {str(e)}")
            return False, []
    
    @staticmethod
    def delete_category(user_id, category_name):
        """Soft delete a category by name"""
        try:
            query = """
            UPDATE categories
            SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s AND name = %s
            RETURNING category_id;
            """
            
            success, result = DatabaseManager.execute_query(query, (user_id, category_name), fetch=True)
            
            if success and result:
                return True, f"Category '{category_name}' deleted successfully"
            else:
                return False, f"Failed to delete category"
                
        except Exception as e:
            print(f"[DEBUG] Exception in delete_category: {str(e)}")
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def debug_all_categories(user_id):
        """Debug method to see all categories"""
        try:
            query = """
            SELECT category_id, name, priority, urgency, frequency, impact, 
                   allocation, is_active, created_at
            FROM categories
            WHERE user_id = %s
            ORDER BY created_at DESC;
            """
            
            success, result = DatabaseManager.execute_query(query, (user_id,), fetch=True)
            return success, result
            
        except Exception as e:
            return False, str(e)