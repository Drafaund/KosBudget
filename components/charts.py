# components/charts.py

import streamlit as st
import pandas as pd
import altair as alt
from config.settings import SESSION_KEYS

import altair as alt
import pandas as pd
import streamlit as st

def render_expense_chart(categories):
    if not categories:
        st.info("Belum ada data kategori untuk grafik.")
        return

    df = pd.DataFrame(categories)
    df['Label'] = df['name'].str.title()

    chart_data = pd.DataFrame({
        'Label': df['Label'],
        'Alokasi': df['allocation'],
        'Pengeluaran': df['total_spent']
    })

    chart_data['Status'] = chart_data.apply(
        lambda row: 'Aman' if row['Pengeluaran'] <= row['Alokasi'] else 'Overbudget', axis=1
    )
    chart_data['Warna Pengeluaran'] = chart_data['Status'].map({
        'Aman': '#4ECDC4',
        'Overbudget': '#FF6B6B'
    })
    chart_data['Warna Alokasi'] = '#90caf9'

    chart_data_long = pd.concat([
        chart_data[['Label', 'Alokasi']].rename(columns={'Alokasi': 'Jumlah'}).assign(
            Tipe='Alokasi', Warna='#90caf9', Status=''
        ),
        chart_data[['Label', 'Pengeluaran', 'Warna Pengeluaran', 'Status']].rename(
            columns={'Pengeluaran': 'Jumlah', 'Warna Pengeluaran': 'Warna'}
        ).assign(Tipe='Pengeluaran')
    ])

    chart = alt.Chart(chart_data_long).mark_bar().encode(
        x=alt.X('Label:N', title=None, axis=alt.Axis(labelAngle=0)),
        xOffset='Tipe:N',
        y=alt.Y('Jumlah:Q', title='Jumlah (Rp)'),
        color=alt.Color('Warna:N', scale=None, legend=None),
        tooltip=[
            alt.Tooltip('Label:N', title='Kategori'),
            alt.Tooltip('Tipe:N'),
            alt.Tooltip('Jumlah:Q', format=','),
            alt.Tooltip('Status:N')
        ]
    ).properties(
        height=350
    )

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