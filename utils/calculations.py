import streamlit as st
from config.settings import DECISION_WEIGHTS, SCORE_WEIGHTS, SESSION_KEYS
from services.budget_service import BudgetService
from services.category_service import CategoryService
from config.database import DatabaseManager
from decimal import Decimal

def safe_float_conversion(value):
    """Safely convert any numeric value to float"""
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    elif isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return 0.0
    else:
        return 0.0

def calculate_decision_score(urgency, frequency, impact):
    """Calculate decision score based on weighted criteria"""
    # Convert all inputs to float safely
    urgency_f = safe_float_conversion(urgency)
    frequency_f = safe_float_conversion(frequency)
    impact_f = safe_float_conversion(impact)
    
    # Convert weights to float safely
    urgency_weight = safe_float_conversion(DECISION_WEIGHTS["urgency"])
    frequency_weight = safe_float_conversion(DECISION_WEIGHTS["frequency"])
    impact_weight = safe_float_conversion(DECISION_WEIGHTS["impact"])
    
    decision_score = (urgency_f * urgency_weight + 
                     frequency_f * frequency_weight + 
                     impact_f * impact_weight)
    return decision_score

def calculate_allocation(user_id):
    """Calculate allocation based on priority and decision scores"""
    try:
        # Get budget
        success, budget_result = BudgetService.get_current_budget(user_id)
        
        if not success or not budget_result:
            st.warning("Budget tidak ditemukan. Silakan set budget terlebih dahulu.")
            return False
        
        monthly_budget = safe_float_conversion(budget_result[0]['monthly_budget'])
        
        if monthly_budget <= 0:
            st.warning("Budget harus lebih dari Rp 0.")
            return False
        
        # Get categories
        success, categories = CategoryService.get_categories(user_id)
        
        if not success or not categories:
            st.info("Belum ada kategori untuk dialokasikan.")
            return False
        
        # Convert weights to float safely
        priority_weight = safe_float_conversion(SCORE_WEIGHTS["priority"])
        decision_weight = safe_float_conversion(SCORE_WEIGHTS["decision"])
        
        # Calculate combined scores for all categories
        total_combined_score = 0.0
        category_scores = []
        
        for cat in categories:
            # Get values and convert to float
            priority = safe_float_conversion(cat.get('priority', 3))
            urgency = safe_float_conversion(cat.get('urgency', 3))
            frequency = safe_float_conversion(cat.get('frequency', 3))
            impact = safe_float_conversion(cat.get('impact', 3))
            
            # Normalize scores to 0-1 range
            priority_normalized = priority / 5.0
            urgency_normalized = urgency / 5.0
            frequency_normalized = frequency / 5.0
            impact_normalized = impact / 5.0
            
            # Calculate decision score
            decision_score = calculate_decision_score(
                urgency_normalized,
                frequency_normalized,
                impact_normalized
            )
            
            # Combined score with weights
            combined_score = (priority_normalized * priority_weight) + (decision_score * decision_weight)
            
            category_scores.append({
                'category_id': cat['category_id'],
                'name': cat['name'],
                'combined_score': combined_score
            })
            
            total_combined_score += combined_score
        
        # Calculate and update allocations
        if total_combined_score > 0:
            updated_count = 0
            
            for cat_score in category_scores:
                weight = cat_score['combined_score'] / total_combined_score
                allocation = monthly_budget * weight
                
                # Update allocation in database
                try:
                    query = """
                    UPDATE categories
                    SET allocation = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE category_id = %s;
                    """
                    # Convert to Decimal for database storage
                    allocation_decimal = Decimal(str(round(allocation, 2)))
                    params = (allocation_decimal, cat_score['category_id'])
                    
                    success, _ = DatabaseManager.execute_query(query, params)
                    if success:
                        updated_count += 1
                    else:
                        st.error(f"Gagal mengupdate alokasi untuk kategori {cat_score['name']}")
                        
                except Exception as e:
                    st.error(f"Error saat mengupdate alokasi untuk {cat_score['name']}: {str(e)}")
            
            if updated_count == len(category_scores):
                st.success(f"✅ Berhasil menghitung alokasi untuk {updated_count} kategori")
                return True
            else:
                st.warning(f"⚠️ Hanya {updated_count} dari {len(category_scores)} kategori yang berhasil diupdate")
                return False
        else:
            st.warning("Total combined score adalah 0. Periksa kembali nilai prioritas dan kriteria keputusan.")
            return False
            
    except Exception as e:
        st.error(f"Error dalam calculate_allocation: {str(e)}")
        return False

def get_financial_summary(user_id=None):
    """Get summary of financial data from database"""
    try:
        if not user_id:
            # Fallback to session state if no user_id provided
            categories = st.session_state.get(SESSION_KEYS["CATEGORIES"], [])
            monthly_budget = safe_float_conversion(st.session_state.get(SESSION_KEYS["MONTHLY_BUDGET"], 0))
        else:
            # Get data from database
            success, budget_result = BudgetService.get_current_budget(user_id)
            monthly_budget = safe_float_conversion(budget_result[0]['monthly_budget']) if success and budget_result else 0
            
            success, categories = CategoryService.get_categories(user_id)
            if not success:
                categories = []
        
        if not categories:
            return {
                'total_allocated': 0.0,
                'total_spent': 0.0,
                'remaining_budget': monthly_budget,
                'monthly_budget': monthly_budget
            }
        
        total_allocated = sum([safe_float_conversion(cat.get('allocation', 0)) for cat in categories])
        total_spent = sum([safe_float_conversion(cat.get('spent', 0)) for cat in categories])
        remaining_budget = monthly_budget - total_spent
        
        return {
            'total_allocated': total_allocated,
            'total_spent': total_spent,
            'remaining_budget': remaining_budget,
            'monthly_budget': monthly_budget
        }
        
    except Exception as e:
        st.error(f"Error dalam get_financial_summary: {str(e)}")
        return {
            'total_allocated': 0.0,
            'total_spent': 0.0,
            'remaining_budget': 0.0,
            'monthly_budget': 0.0
        }

def validate_category_data(category_data):
    """Validate category data before processing"""
    required_fields = ['name', 'priority', 'urgency', 'frequency', 'impact']
    
    for field in required_fields:
        if field not in category_data:
            return False, f"Field {field} is required"
        
        if field != 'name':
            value = safe_float_conversion(category_data[field])
            if value < 1 or value > 5:
                return False, f"Field {field} must be between 1 and 5"
    
    if not category_data['name'] or not category_data['name'].strip():
        return False, "Category name cannot be empty"
    
    return True, "Valid"