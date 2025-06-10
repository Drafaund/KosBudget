import streamlit as st
import pandas as pd
from utils.calculations import calculate_decision_score, calculate_allocation
from utils.state_manager import initialize_session_state
from components.charts import render_expense_chart

def render_dashboard():
    """Render the dashboard page"""
    initialize_session_state()
    
    st.markdown('<h1 class="title-gradient">📊 Dashboard Keuangan</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p style="font-size: 1.2rem; color: black; margin-bottom: 2rem;">'
        f'Halo, <strong>{st.session_state.username}</strong> 👋, berikut ringkasan keuanganmu</p>', 
        unsafe_allow_html=True
    )

    # User avatar
    render_user_avatar()
    
    # Summary metrics
    render_summary_metrics()
    
    # Add expense section
    render_add_expense_section()
    
    # Charts and analysis
    render_charts_section()
    
    # Detailed breakdown
    render_detailed_breakdown()

def render_user_avatar():
    """Render user avatar"""
    st.markdown(
        f'<img class="avatar" src="https://ui-avatars.com/api/?name={st.session_state.username}'
        f'&background=667eea&color=fff&size=50" alt="avatar">', 
        unsafe_allow_html=True
    )

def render_summary_metrics():
    """Render summary metrics cards"""
    if not st.session_state.categories:
        st.info("📝 Belum ada kategori. Silakan buat kategori terlebih dahulu di Form Input.")
        return
    
    total_allocated = sum([cat['allocation'] for cat in st.session_state.categories])
    total_spent = sum([cat['spent'] for cat in st.session_state.categories])
    remaining_budget = st.session_state.monthly_budget - total_spent
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            value=st.session_state.monthly_budget,
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

def render_add_expense_section():
    """Render add expense section"""
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">➕ Tambah Pengeluaran</h3>', unsafe_allow_html=True)
    
    with st.form(key="expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.categories:
                selected_category = st.selectbox(
                    "📂 Pilih Kategori", 
                    [c['name'] for c in st.session_state.categories]
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
    """Handle expense form submission"""
    st.session_state.expenses.append({
        'category': selected_category,
        'amount': amount_spent
    })
    calculate_allocation()
    st.markdown(
        f'<div class="success-message">✅ Pengeluaran Rp{amount_spent:,.0f} '
        f'untuk kategori "{selected_category}" ditambahkan.</div>', 
        unsafe_allow_html=True
    )

def render_charts_section():
    """Render charts and analysis section"""
    if not st.session_state.categories:
        return
        
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">📈 Grafik Pengeluaran vs Alokasi</h3>', unsafe_allow_html=True)
    
    # Use chart component
    render_expense_chart(st.session_state.categories)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_detailed_breakdown():
    """Render detailed financial breakdown"""
    if not st.session_state.categories:
        return
        
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">💼 Detail Keuangan & Analisis Decision</h3>', unsafe_allow_html=True)
    
    # Enhanced dataframe with decision scores
    df_enhanced = []
    for cat in st.session_state.categories:
        decision_score = calculate_decision_score(
            cat.get('urgency', 3) / 5.0,
            cat.get('frequency', 3) / 5.0,
            cat.get('impact', 3) / 5.0
        ) * 100
        
        sisa = cat['allocation'] - cat['spent']
        persentase = (cat['spent'] / cat['allocation'] * 100) if cat['allocation'] > 0 else 0
        status = '✅ Aman' if sisa >= 0 else '⚠️ Over Budget'
        
        df_enhanced.append({
            '📂 Kategori': cat['name'],
            '🎯 Decision Score': f"{decision_score:.1f}%",
            '💰 Alokasi (Rp)': cat['allocation'],
            '💸 Terpakai (Rp)': cat['spent'],
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