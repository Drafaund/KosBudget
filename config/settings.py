# config/settings.py

# Page Configuration
PAGE_CONFIG = {
    "page_title": "KosBudget - Manajemen Keuangan Anak Kos",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Decision Criteria Weights
DECISION_WEIGHTS = {
    "urgency": 0.5,
    "frequency": 0.3,
    "impact": 0.2
}

# Priority and Decision Score Weights
SCORE_WEIGHTS = {
    "priority": 0.5,
    "decision": 0.5
}

# Default Values
DEFAULTS = {
    "priority": 3,
    "urgency": 3,
    "frequency": 3,
    "impact": 3,
    "step_amount": 10000,
    "min_amount": 0
}

# Navigation Pages
PAGES = {
    "FORM_INPUT": "Form Input",
    "DASHBOARD": "Dashboard"
}

# Session State Keys
SESSION_KEYS = {
    "AUTHENTICATED": "authenticated",
    "USERNAME": "username",
    "USERS": "users",
    "CURRENT_PAGE": "current_page", 
    "MONTHLY_BUDGET": "monthly_budget",
    "CATEGORIES": "categories",
    "EXPENSES": "expenses"
}