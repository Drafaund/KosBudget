# components/charts.py

import streamlit as st
import pandas as pd
import altair as alt
from config.settings import SESSION_KEYS

def render_expense_chart():
    """Render expense vs allocation chart"""
    categories = st.session_state.get(SESSION_KEYS["CATEGORIES"], [])
    
    if not categories:
        st.warning("⚠️ Belum ada data kategori untuk ditampilkan.")
        return
    
    df = pd.DataFrame(categories)
    df_chart = pd.DataFrame({
        'Kategori': df['name'],
        'Alokasi': df['allocation'],
        'Terpakai': df['spent']
    })
    df_chart_melted = df_chart.melt('Kategori', var_name='Tipe', value_name='Jumlah')

    chart = alt.Chart(df_chart_melted).mark_bar().encode(
        x=alt.X('Kategori:N', title='Kategori'),
        y=alt.Y('Jumlah:Q', title='Jumlah (Rp)'),
        color=alt.Color('Tipe:N', 
            scale=alt.Scale(domain=['Alokasi', 'Terpakai'], 
                          range=['#667eea', '#FF6B6B']))
    ).properties(height=400)

    st.altair_chart(chart, use_container_width=True)

def render_metric_cards(summary):
    """Render financial summary metric cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        budget = st.session_state.get(SESSION_KEYS["MONTHLY_BUDGET"], 0)
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="metric-value">Rp {budget:,.0f}</div>
            <div class="metric-label">💰 Budget Bulanan</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <div class="metric-value">Rp {summary["total_allocated"]:,.0f}</div>
            <div class="metric-label">📊 Total Alokasi</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);">
            <div class="metric-value">Rp {summary["total_spent"]:,.0f}</div>
            <div class="metric-label">💸 Total Terpakai</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        remaining = summary["remaining_budget"]
        color = "#11998e" if remaining >= 0 else "#ff416c"
        st.markdown(f'''
        <div class="metric-card" style="background: linear-gradient(135deg, {color} 0%, #38ef7d 100%);">
            <div class="metric-value">Rp {remaining:,.0f}</div>
            <div class="metric-label">💵 Sisa Budget</div>
        </div>
        ''', unsafe_allow_html=True)