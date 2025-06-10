# pages/form_input.py - VERSI DENGAN AUTO ALLOCATION
import streamlit as st
import pandas as pd
from utils.state_manager import SessionManager
from utils.calculations import calculate_decision_score, calculate_allocation
from services.budget_service import BudgetService
from services.category_service import CategoryService
import time

def render_form_input():
    """Render the form input page"""
    st.markdown('<h1 class="title-gradient">📝 Input Keuangan & Decision Category</h1>', unsafe_allow_html=True)
    
    # Get current user ID
    user_id = SessionManager.get_user_id()
    if not user_id:
        st.error("Anda belum login!")
        return

    # Add debug section at the top
    with st.expander("🔧 Debug & Troubleshoot"):
        debug_categories(user_id)

    # Budget input section
    render_budget_input(user_id)
    
    # Decision Category Information
    render_decision_info()
    
    # Category management section
    render_category_form(user_id)
    
    # Categories display
    render_categories_display(user_id)

def debug_categories(user_id):
    """Debug section to check categories"""
    st.write(f"**User ID:** {user_id}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Check All Categories"):
            success, categories = CategoryService.debug_all_categories(user_id)
            if success and categories:
                st.write(f"**Found {len(categories)} categories:**")
                for cat in categories:
                    active_status = "✅ Active" if cat['is_active'] else "❌ Inactive"
                    allocation = float(cat.get('allocation', 0))
                    st.write(f"- {cat['name']} ({active_status}) - Rp {allocation:,.0f}")
            else:
                st.write("No categories found")
    
    with col2:
        if st.button("🔄 Force Refresh"):
            st.rerun()
    
    with col3:
        if st.button("💰 Recalculate All Allocations"):
            with st.spinner("Menghitung ulang alokasi..."):
                calculate_allocation(user_id)
                st.success("✅ Alokasi berhasil dihitung ulang!")
                time.sleep(1)
                st.rerun()

def render_budget_input(user_id):
    """Render budget input section"""
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">💰 Uang Bulanan</h3>', unsafe_allow_html=True)
    
    # Get current budget from database
    success, result = BudgetService.get_current_budget(user_id)
    current_budget = result[0]['monthly_budget'] if success and result else 0
    
    new_budget = st.number_input(
        "💵 Masukkan uang bulanan Anda (Rp)", 
        min_value=0, 
        step=10000, 
        value=int(current_budget),
        help="Masukkan total uang bulanan yang Anda terima"
    )
    
    # Save to database when changed
    if new_budget != current_budget:
        success, _ = BudgetService.create_or_update_budget(user_id, float(new_budget))
        if success:
            st.success("✅ Budget berhasil diperbarui")
            # Recalculate allocations when budget changes
            with st.spinner("Menghitung ulang alokasi berdasarkan budget baru..."):
                calculate_allocation(user_id)
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Gagal menyimpan budget")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_decision_info():
    """Render decision category information"""
    st.markdown('<div class="decision-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: black; font-weight: 600;">🎯 Panduan Decision Category</h3>', unsafe_allow_html=True)
    st.markdown('''
    <div style="color: black;">
    <p><strong>🚨 Urgensi (50%):</strong> Seberapa mendesak kategori ini (1=Tidak mendesak, 5=Sangat mendesak)</p>
    <p><strong>🔄 Frekuensi (30%):</strong> Seberapa sering dibutuhkan (1=Jarang, 5=Sangat sering)</p>
    <p><strong>💥 Dampak (20%):</strong> Dampak jika terlewati (1=Ringan, 5=Sangat berat)</p>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_category_form(user_id):
    """Render category form for adding/editing categories"""
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle-gradient">📂 Tambah Kategori Pengeluaran</h3>', unsafe_allow_html=True)
    
    with st.form(key="add_category_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            cat_name = st.text_input("🏷️ Nama Kategori", placeholder="Contoh: Makanan, Transport, dll")
            cat_priority = st.slider("⭐ Prioritas Personal", 1, 5, 3, help="1=Rendah, 5=Tinggi")
        
        with col2:
            st.markdown("🎯 Decision Category:")
            cat_urgency = st.slider("🚨 Urgensi", 1, 5, 3, help="Seberapa mendesak kategori ini")
            cat_frequency = st.slider("🔄 Frekuensi", 1, 5, 3, help="Seberapa sering dibutuhkan")
            cat_impact = st.slider("💥 Dampak jika Terlewati", 1, 5, 3, help="Dampak jika kategori ini diabaikan")
        
        submitted = st.form_submit_button("💾 Simpan Kategori", use_container_width=True)

    if submitted:
        if cat_name and cat_name.strip():
            with st.spinner("Menyimpan kategori dan menghitung alokasi..."):
                success = handle_category_submission(user_id, cat_name.strip(), cat_priority, cat_urgency, cat_frequency, cat_impact)
                if success:
                    # PENTING: Hitung ulang alokasi setelah kategori baru ditambah
                    calculate_allocation(user_id)
                    time.sleep(2)  # Give time for database to update
                    st.rerun()
        else:
            st.error("❌ Nama kategori tidak boleh kosong!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_category_submission(user_id, cat_name, cat_priority, cat_urgency, cat_frequency, cat_impact):
    """Handle category form submission"""
    try:
        # Check if category already exists
        success, existing_categories = CategoryService.get_categories(user_id)
        if success and existing_categories:
            existing_names = [cat['name'].lower() for cat in existing_categories]
            if cat_name.lower() in existing_names:
                st.warning(f"⚠️ Kategori '{cat_name}' sudah ada!")
                return False
        
        category_data = {
            'name': cat_name,
            'priority': cat_priority,
            'urgency': cat_urgency,
            'frequency': cat_frequency,
            'impact': cat_impact
        }
        
        # Save category
        success, message = CategoryService.create_or_update_category(user_id, category_data)
        
        if success:
            st.success(f"✅ Kategori '{cat_name}' berhasil disimpan!")
            return True
        else:
            st.error(f"❌ Gagal menyimpan kategori: {message}")
            return False
            
    except Exception as e:
        st.error(f"❌ Error saat menyimpan kategori: {str(e)}")
        return False

def render_categories_display(user_id):
    """Render categories display with decision scores"""
    st.markdown('<h3 class="subtitle-gradient">📋 Daftar Kategori</h3>', unsafe_allow_html=True)
    
    # Get categories from database
    success, categories = CategoryService.get_categories(user_id)
    
    if not success:
        st.error("❌ Gagal mengambil data kategori dari database")
        return
        
    if not categories:
        st.info("📝 Belum ada kategori yang ditambahkan. Silakan tambahkan kategori di atas.")
        return
    
    st.markdown('<div class="category-card">', unsafe_allow_html=True)
    
    # Show categories count
    st.write(f"**Total Kategori:** {len(categories)}")
    
    # Check if any category has zero allocation
    zero_allocation_count = sum(1 for cat in categories if float(cat.get('allocation', 0)) == 0)
    if zero_allocation_count > 0:
        st.warning(f"⚠️ {zero_allocation_count} kategori memiliki alokasi Rp 0. Klik tombol 'Recalculate All Allocations' di bagian Debug.")
    
    # Create dataframe for display
    df_categories = []
    for cat in categories:
        try:
            decision_score = calculate_decision_score(
                cat.get('urgency', 3) / 5.0,
                cat.get('frequency', 3) / 5.0,
                cat.get('impact', 3) / 5.0
            ) * 100
            
            allocation = float(cat.get('allocation', 0))
            
            df_categories.append({
                '📂 Kategori': cat.get('name', 'Unknown'),
                '⭐ Prioritas': cat.get('priority', 3),
                '🚨 Urgensi': cat.get('urgency', 3),
                '🔄 Frekuensi': cat.get('frequency', 3),
                '💥 Dampak': cat.get('impact', 3),
                '🎯 Decision Score': f"{decision_score:.1f}%",
                '💰 Alokasi': f"Rp {allocation:,.0f}"
            })
        except Exception as e:
            st.error(f"Error processing category {cat.get('name', 'Unknown')}: {str(e)}")
    
    if df_categories:
        df_display = pd.DataFrame(df_categories)
        st.dataframe(df_display, use_container_width=True)
        
        # Show total allocation summary
        total_allocation = sum(float(cat.get('allocation', 0)) for cat in categories)
        success, budget_result = BudgetService.get_current_budget(user_id)
        monthly_budget = float(budget_result[0]['monthly_budget']) if success and budget_result else 0
        
       
        
        # Delete category section
        render_delete_category_section(user_id, categories)
    else:
        st.warning("⚠️ Tidak ada data kategori yang dapat ditampilkan")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_delete_category_section(user_id, categories):
    """Render delete category section"""
    with st.expander("🗑️ Hapus Kategori"):
        if categories:
            cat_to_delete = st.selectbox(
                "Pilih kategori yang ingin dihapus", 
                [cat['name'] for cat in categories],
                key="delete_selectbox"
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("🗑️ Hapus", key="delete_cat"):
                    success, message = CategoryService.delete_category(user_id, cat_to_delete)
                    if success:
                        st.success(f"✅ Kategori '{cat_to_delete}' berhasil dihapus")
                        # Recalculate allocations after deletion
                        with st.spinner("Menghitung ulang alokasi..."):
                            calculate_allocation(user_id)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
            
            with col2:
                st.write("⚠️ **Peringatan:** Tindakan ini tidak dapat dibatalkan!")
        else:
            st.write("Tidak ada kategori untuk dihapus")