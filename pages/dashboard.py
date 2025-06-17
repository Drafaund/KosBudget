import streamlit as st
import pandas as pd
from utils.calculations import calculate_decision_score, calculate_allocation
from utils.state_manager import SessionManager
from components.charts import render_expense_chart
from services.budget_service import BudgetService
from services.category_service import CategoryService
from services.expense_service import ExpenseService

def render_dashboard():
    """Render the dashboard page"""
    # Autorisasi user
    user_id = SessionManager.get_user_id()
    user_data = SessionManager.get_current_user()
    if not user_id or not user_data:
        st.error("Anda belum login!")
        return

    username = user_data.get("username", "User")

    # Ambil data kategori dari database
    success_cat, categories = CategoryService.get_categories(user_id)
    if not success_cat or not isinstance(categories, list):
        st.error("Gagal mengambil data kategori dari database.")
        categories = []
    
    # Konversi Decimal ke float
    for cat in categories:
        if 'allocation' in cat:
            cat['allocation'] = float(cat['allocation'])
        if 'total_spent' in cat:
            cat['total_spent'] = float(cat['total_spent'])
    st.session_state.categories = categories

    # Ambil budget bulanan dari database
    success_budget, budget_result = BudgetService.get_current_budget(user_id)
    monthly_budget = float(budget_result[0]['monthly_budget']) if success_budget and budget_result else 0
    st.session_state.monthly_budget = monthly_budget

    # Ambil data pengeluaran (jika ada service-nya, atau gunakan session_state.expenses)
    if "expenses" not in st.session_state:
        st.session_state.expenses = []

    st.markdown('<h1 class="title-gradient">📊 Dashboard Keuangan</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="font-size: 1.2rem; color: black; margin-bottom: 2rem;">'
        f'Halo, <strong>{username}</strong> 👋, berikut ringkasan keuanganmu</p>', 
        unsafe_allow_html=True
    )

    # User avatar
    render_user_avatar(username)

    # Summary metrics
    render_summary_metrics(monthly_budget, categories)

    # Add expense section
    render_add_expense_section(categories)

    # Charts and analysis
    render_charts_section(categories)

    # Detailed breakdown
    render_detailed_breakdown(categories)

def render_user_avatar(username):
    """Render user avatar"""
    st.markdown(
        f'<img class="avatar" src="https://ui-avatars.com/api/?name={username}'
        f'&background=667eea&color=fff&size=50" alt="avatar">', 
        unsafe_allow_html=True
    )

def render_summary_metrics(monthly_budget, categories):
    """Render summary metrics cards"""
    if not categories:
        st.info("📝 Belum ada kategori. Silakan buat kategori terlebih dahulu di Form Input.")
        return
    
    total_allocated = sum([cat['allocation'] for cat in categories])
    total_spent = sum([cat.get('total_spent', 0) for cat in categories])
    remaining_budget = monthly_budget - total_spent
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            value=monthly_budget,
            label="💰 Budget Bulanan",
            gradient="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"
        )
    
    with col2:
        render_metric_card(
            value=total_allocated,
            label="📊 Total Alokasi",
            gradient="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);"
        )
    
    with col3:
        render_metric_card(
            value=total_spent,
            label="💸 Total Terpakai",
            gradient="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);"
        )
    
    with col4:
        color = "#11998e" if remaining_budget >= 0 else "#ff416c"
        render_metric_card(
            value=remaining_budget,
            label="💵 Sisa Budget",
            gradient=f"background: linear-gradient(135deg, {color} 0%, #38ef7d 100%);"
        )

def render_metric_card(value, label, gradient):
    """Render individual metric card"""
    st.markdown(f'''
    <div class="metric-card" style="{gradient}">
        <div class="metric-value">Rp {value:,.0f}</div>
        <div class="metric-label">{label}</div>
    </div>
    ''', unsafe_allow_html=True)

def render_add_expense_section(categories):
    """Render add expense section"""
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">➕ Tambah Pengeluaran</h3>', unsafe_allow_html=True)
    
    with st.form(key="expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            if categories:
                selected_category = st.selectbox(
                    "📂 Pilih Kategori", 
                    [c['name'] for c in categories]
                )
            else:
                st.warning("⚠️ Belum ada kategori. Silakan buat kategori terlebih dahulu di Form Input.")
                selected_category = None
        
        with col2:
            amount_spent = st.number_input(
                "💰 Jumlah Pengeluaran (Rp)", 
                min_value=0, 
                step=1000
            )
        
        exp_submitted = st.form_submit_button("➕ Tambah Pengeluaran")

    if exp_submitted and selected_category:
        handle_expense_submission(selected_category, amount_spent)
    
    st.markdown('</div>', unsafe_allow_html=True)


def handle_expense_submission(selected_category, amount_spent):
    user_id = SessionManager.get_user_id()
    categories = st.session_state.categories
    category_id = next((cat['category_id'] for cat in categories if cat['name'] == selected_category), None)
    if category_id is None:
        st.error("Kategori tidak ditemukan.")
        return

    success = ExpenseService.add_expense(user_id, category_id, amount_spent)
    if success:
        st.success(f"✅ Pengeluaran Rp{amount_spent:,.0f} untuk kategori \"{selected_category}\" berhasil disimpan.")
        calculate_allocation(user_id)
        # Refresh kategori
        success_cat, categories = CategoryService.get_categories(user_id)
        if success_cat:
            st.session_state.categories = categories
        # Rerender grafik & tabel
        render_charts_section(categories)
        render_detailed_breakdown(categories)
    else:
        st.error("Gagal menyimpan pengeluaran ke database.")

def render_charts_section(categories):
    """Render charts and analysis section"""
    if not categories:
        return
        
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">📈 Grafik Pengeluaran vs Alokasi</h3>', unsafe_allow_html=True)
    
    # Use chart component
    render_expense_chart(categories)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_detailed_breakdown(categories):
    """Render detailed financial breakdown"""
    if not categories:
        return
        
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">💼 Detail Keuangan & Analisis Decision</h3>', unsafe_allow_html=True)
    
    # Enhanced dataframe with decision scores
    df_enhanced = []
    for cat in categories:
        decision_score = calculate_decision_score(
            cat.get('urgency', 3) / 5.0,
            cat.get('frequency', 3) / 5.0,
            cat.get('impact', 3) / 5.0
        ) * 100
        
        sisa = cat.get('allocation', 0) - cat.get('total_spent', 0)
        persentase = (cat.get('total_spent', 0) / cat.get('allocation', 0) * 100) if cat.get('allocation', 0) > 0 else 0
        status = '✅ Aman' if sisa >= 0 else '⚠️ Over Budget'
        
        df_enhanced.append({
            '📂 Kategori': cat['name'],
            '🎯 Decision Score': f"{decision_score:.1f}%",
            '💰 Alokasi (Rp)': cat['allocation'],
            '💸 Terpakai (Rp)': cat['total_spent'],
            '💵 Sisa (Rp)': sisa,
            '📊 Persentase (%)': f"{persentase:.1f}%",
            '🔍 Status': status
        })
    
    df_display_enhanced = pd.DataFrame(df_enhanced)
    st.dataframe(df_display_enhanced, use_container_width=True)
    
    # Render insights
    render_financial_insights(df_enhanced)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_financial_insights(df_enhanced):
    """Render financial insights based on data"""
    if not df_enhanced:
        return
    
    # Calculate insights
    over_budget_count = sum(1 for item in df_enhanced if '⚠️' in item['🔍 Status'])
    total_categories = len(df_enhanced)
    
    st.markdown('<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown('**💡 Insights Keuangan:**', unsafe_allow_html=True)
    
    if over_budget_count == 0:
        st.markdown('✅ Selamat! Semua kategori masih dalam batas budget yang dialokasikan.')
    else:
        st.markdown(f'⚠️ {over_budget_count} dari {total_categories} kategori melebihi budget yang dialokasikan.')
    
    # Find highest decision score category
    highest_score_cat = max(df_enhanced, key=lambda x: float(x['🎯 Decision Score'].replace('%', '')))
    st.markdown(f'🎯 Kategori dengan Decision Score tertinggi: **{highest_score_cat["📂 Kategori"]}** ({highest_score_cat["🎯 Decision Score"]})')
    
    st.markdown('</div>', unsafe_allow_html=True)