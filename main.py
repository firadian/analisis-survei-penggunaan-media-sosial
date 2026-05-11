import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# Initialize session state for login status if not already set
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


# --- Login Page ---
if not st.session_state.logged_in:
    st.title('Halaman Login Aplikasi Dashboard')
    st.write('Silakan login untuk mengakses dashboard.')

    username_input = st.text_input('Username')
    password_input = st.text_input('Password', type='password')

    if st.button('Login'):
        if username_input == 'kelompok 1' and password_input == 'Streamlit':
            st.session_state.logged_in = True
            st.success('Login Berhasil! Memuat dashboard...')
            st.rerun() # Rerun to show dashboard content
        else:
            st.error('Username atau password salah.')
else:
    # --- Main Application Content (only visible after successful login) ---
    st.set_page_config(layout="wide")

    st.markdown("### **1. Pengaturan Awal (Import Library, Konfigurasi, dan Judul Aplikasi)**")
    st.markdown("Bagian ini mengatur semua yang kita butuhkan: mengimpor pustaka penting seperti Streamlit, Pandas, Matplotlib, dan Seaborn, lalu mengatur tampilan aplikasi agar lebar dan memberikan judul yang jelas.")

    st.title('Dashboard Analisis Survei Penggunaan Media Sosial')
    st.write('Aplikasi interaktif ini menyajikan data survei tentang perilaku penggunaan media sosial dan dampaknya terhadap produktivitas.')
    st.markdown("### **2. Memuat Data Survei**")
    st.markdown("Fungsi ini bertugas memuat data dari file `Survei_Medsos.csv`. Kami menggunakan `st.cache_data` agar data hanya dimuat sekali dan aplikasi berjalan cepat. Jika file tidak ditemukan, akan ada pesan kesalahan.")

    @st.cache_data
    def load_data():
        try:
            data = pd.read_csv('Survei_Medsos.csv')
            return data
        except FileNotFoundError:
            st.error('File `Survei_Medsos.csv` tidak ditemukan. Pastikan file berada di folder yang sama.')
            return pd.DataFrame()

    data = load_data()

    # Lanjutkan hanya jika data berhasil dimuat
    if not data.empty:
        st.markdown("### **3. Navigasi Aplikasi (Sidebar)**")
        st.markdown("Sidebar ini berfungsi sebagai menu utama. Pengguna dapat memilih bagian analisis yang ingin ditampilkan, membuat presentasi Anda lebih terstruktur dan mudah diikuti.")
        st.sidebar.title('Pilih Bagian Analisis')
        analysis_selection = st.sidebar.radio(
            "Lihat:",
            ['Ringkasan Data', 'Dampak ke Produktivitas', 'Penggunaan Platform Medsos', 'Hubungan Medsos & Produktivitas']
        )
        if analysis_selection == 'Ringkasan Data':
            st.markdown("### **4. Bagian: Ringkasan Data**")
            st.markdown("Di sini kita bisa melihat gambaran umum data:")
            st.markdown("-   **Contoh Data:** Menampilkan beberapa baris pertama data.")
            st.markdown("-   **Ukuran Data:** Memberi tahu berapa banyak baris dan kolom yang ada.")
            st.markdown("-   **Informasi Kolom:** Menunjukkan tipe data dan apakah ada nilai yang kosong di setiap kolom.")
            st.subheader('Ringkasan Awal Dataset')
            st.dataframe(data.head())
            st.write(f"**Jumlah Responden:** {data.shape[0]} | **Jumlah Pertanyaan:** {data.shape[1]}")
            st.write('**Tipe Data dan Kelengkapan Kolom:**')
            buffer = io.StringIO()
            data.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)

            st.markdown('##### **Statistik Deskriptif Kolom Numerik**')
            st.dataframe(data.describe())

            st.markdown('##### **Ringkasan Kolom Kategorikal**')
            for col in data.select_dtypes(include='object').columns:
                st.write(f"**Kolom: {col}**")
                freq_table = data[col].value_counts().rename_axis('Kategori').reset_index(name='Jumlah Responden')
                freq_table['Persentase (%)'] = (freq_table['Jumlah Responden'] / freq_table['Jumlah Responden'].sum() * 100).round(2)
                st.dataframe(freq_table)
        elif analysis_selection == 'Dampak ke Produktivitas':
            st.markdown("### **5. Bagian: Dampak ke Produktivitas**")
            st.markdown("Fokus pada kolom 'Mengganggu_Produktivitas', bagian ini menyajikan:")
            st.markdown("-   **Distribusi:** Diagram batang menunjukkan bagaimana responden menilai dampak media sosial pada produktivitas mereka (skala 1-5).")
            st.markdown("-   **Keterangan Skala:** Penjelasan arti dari setiap angka pada skala (1: Tidak pernah sampai 5: Selalu).")
            st.markdown("-   **Deteksi Outlier:** Dua *boxplot* yang membandingkan data sebelum dan sesudah outlier dihapus (menggunakan metode IQR) untuk melihat apakah ada nilai ekstrem yang memengaruhi distribusi.")
            st.markdown("-   **Transformasi Log:** Dua histogram yang menunjukkan distribusi data sebelum dan sesudah transformasi logaritma (log1p). Ini biasa dilakukan untuk menormalisasi data.")
            st.subheader('Analisis Dampak Media Sosial terhadap Produktivitas')

            st.markdown('##### **Rangkuman Frekuensi Tingkat Gangguan Produktivitas**')
            freq_prod = data['Mengganggu_Produktivitas'].value_counts(sort=False).rename_axis('Tingkat Gangguan').reset_index(name='Jumlah Responden')
            freq_prod['Persentase (%)'] = (freq_prod['Jumlah Responden'] / freq_prod['Jumlah Responden'].sum() * 100).round(2)
            st.dataframe(freq_prod)

            st.markdown('#### **Distribusi Tingkat Gangguan Produktivitas**')
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.countplot(x='Mengganggu_Produktivitas', data=data, palette='viridis', ax=ax1)
            ax1.set_title('Frekuensi Tingkat Gangguan Produktivitas', fontsize=16)
            ax1.set_xlabel('Tingkat Gangguan (1 = Tidak Pernah, 5 = Selalu)', fontsize=14)
            ax1.set_ylabel('Jumlah Responden', fontsize=14)
            st.pyplot(fig1)

            st.markdown("""
            **Keterangan Skala 'Mengganggu_Produktivitas':**
            - (1): Tidak pernah
            - (2): Jarang
            - (3): Kadang
            - (4): Sering
            - (5): Selalu
            """)

            st.markdown('#### **Deteksi Outlier pada Tingkat Gangguan Produktivitas**')
            Q1 = data['Mengganggu_Produktivitas'].quantile(0.25)
            Q3 = data['Mengganggu_Produktivitas'].quantile(0.75)
            IQR = Q3 - Q1
            filtered_data = data[(data['Mengganggu_Produktivitas'] >= Q1 - 1.5 * IQR) & (data['Mengganggu_Produktivitas'] <= Q3 + 1.5 * IQR)].copy()

            fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(14, 6))
            sns.boxplot(x=data['Mengganggu_Produktivitas'], ax=ax2a, color='skyblue')
            ax2a.set_title('Sebelum Penghapusan Outlier')
            ax2a.set_xlabel('Tingkat Gangguan Produktivitas')
            sns.boxplot(x=filtered_data['Mengganggu_Produktivitas'], ax=ax2b, color='lightcoral')
            ax2b.set_title('Setelah Penghapusan Outlier')
            ax2b.set_xlabel('Tingkat Gangguan Produktivitas')
            plt.tight_layout()
            st.pyplot(fig2)

            st.markdown('#### **Transformasi Log untuk Normalisasi Data**')
            data_for_log = data.copy()
            data_for_log['Mengganggu_Produktivitas_log'] = np.log1p(data_for_log['Mengganggu_Produktivitas'])

            fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(14, 6))
            sns.histplot(data_for_log['Mengganggu_Produktivitas'], kde=True, ax=ax3a, color='dodgerblue')
            ax3a.set_title('Sebelum Transformasi Log')
            ax3a.set_xlabel('Tingkat Gangguan Produktivitas')
            sns.histplot(data_for_log['Mengganggu_Produktivitas_log'], kde=True, ax=ax3b, color='mediumseagreen')
            ax3b.set_title('Setelah Transformasi Log (np.log1p)')
            ax3b.set_xlabel('Tingkat Gangguan Produktivitas (Log Transformed)')
            plt.tight_layout()
            st.pyplot(fig3)
        elif analysis_selection == 'Penggunaan Platform Medsos':
            st.markdown("### **6. Bagian: Penggunaan Platform Medsos**")
            st.markdown("Bagian ini menampilkan dua diagram batang horizontal:")
            st.markdown("-   **Platform Sering Digunakan:** Menunjukkan platform media sosial mana yang paling sering digunakan oleh responden.")
            st.markdown("-   **Platform Membuat Lupa Waktu:** Menunjukkan platform mana yang paling sering membuat responden lupa waktu.")
            st.markdown("Kedua visualisasi ini ditampilkan berdampingan agar mudah dibandingkan.")
            st.subheader('Visualisasi Frekuensi Penggunaan Platform Media Sosial')

            col1, col2 = st.columns(2)

            with col1:
                st.markdown('##### **Rangkuman Platform Paling Sering Digunakan**')
                freq_sering = data['Sering'].value_counts().rename_axis('Platform Medsos').reset_index(name='Jumlah Responden')
                freq_sering['Persentase (%)'] = (freq_sering['Jumlah Responden'] / freq_sering['Jumlah Responden'].sum() * 100).round(2)
                st.dataframe(freq_sering)

                st.markdown('#### **Platform Paling Sering Digunakan**')
                fig_sering, ax_sering = plt.subplots(figsize=(10, 6))
                sns.countplot(y='Sering', data=data, order=data['Sering'].value_counts().index, palette='viridis', ax=ax_sering)
                ax_sering.set_title('Frekuensi Platform yang Sering Digunakan')
                ax_sering.set_xlabel('Jumlah Responden')
                ax_sering.set_ylabel('Platform Medsos')
                st.pyplot(fig_sering)

            with col2:
                st.markdown('##### **Rangkuman Platform yang Membuat Lupa Waktu**')
                freq_lupa = data['Lupa_Waktu'].value_counts().rename_axis('Platform Medsos').reset_index(name='Jumlah Responden')
                freq_lupa['Persentase (%)'] = (freq_lupa['Jumlah Responden'] / freq_lupa['Jumlah Responden'].sum() * 100).round(2)
                st.dataframe(freq_lupa)

                st.markdown('#### **Platform yang Membuat Lupa Waktu**')
                fig_lupawaktu, ax_lupawaktu = plt.subplots(figsize=(10, 6))
                sns.countplot(y='Lupa_Waktu', data=data, order=data['Lupa_Waktu'].value_counts().index, palette='magma', ax=ax_lupawaktu)
                ax_lupawaktu.set_title('Frekuensi Platform yang Membuat Lupa Waktu')
                ax_lupawaktu.set_xlabel('Jumlah Responden')
                ax_lupawaktu.set_ylabel('Platform Medsos')
                st.pyplot(fig_lupawaktu)
        elif analysis_selection == 'Hubungan Medsos & Produktivitas':
            st.markdown("### **7. Bagian: Hubungan Medsos & Produktivitas**")
            st.markdown("Bagian ini mengeksplorasi keterkaitan antara penggunaan media sosial dan tingkat gangguan produktivitas:")
            st.markdown("-   **Dampak dari Platform Sering Digunakan:** Diagram batang bertumpuk menunjukkan bagaimana tingkat gangguan produktivitas berbeda di antara platform yang paling sering digunakan.")
            st.markdown("-   **Dampak dari Platform yang Membuat Lupa Waktu:** Sama seperti di atas, tetapi fokus pada platform yang membuat responden lupa waktu. Ini membantu mengidentifikasi platform mana yang paling berpengaruh terhadap produktivitas.")
            st.subheader('Korelasi Antara Penggunaan Medsos dan Gangguan Produktivitas')

            st.markdown('#### **Tingkat Gangguan Produktivitas berdasarkan Platform Sering Digunakan**')
            fig_rel1, ax_rel1 = plt.subplots(figsize=(12, 7))
            sns.countplot(y='Sering', hue='Mengganggu_Produktivitas', data=data, palette='coolwarm', ax=ax_rel1,
                          order=data['Sering'].value_counts().index)
            ax_rel1.set_title('Gangguan Produktivitas berdasarkan Platform Sering Digunakan')
            ax_rel1.set_xlabel('Jumlah Responden')
            ax_rel1.set_ylabel('Platform Medsos (Sering Digunakan)')
            handles, labels = ax_rel1.get_legend_handles_labels()
            ax_rel1.legend(handles=handles, labels=['Tidak pernah (1)', 'Jarang (2)', 'Kadang (3)', 'Sering (4)', 'Selalu (5)'], title='Tingkat Gangguan')
            st.pyplot(fig_rel1)

            st.markdown('#### **Tingkat Gangguan Produktivitas berdasarkan Platform yang Membuat Lupa Waktu**')
            fig_rel2, ax_rel2 = plt.subplots(figsize=(12, 7))
            sns.countplot(y='Lupa_Waktu', hue='Mengganggu_Produktivitas', data=data, palette='Spectral', ax=ax_rel2,
                          order=data['Lupa_Waktu'].value_counts().index)
            ax_rel2.set_title('Gangguan Produktivitas berdasarkan Platform yang Membuat Lupa Waktu')
            ax_rel2.set_xlabel('Jumlah Responden')
            ax_rel2.set_ylabel('Platform Medsos (Membuat Lupa Waktu)')
            handles, labels = ax_rel2.get_legend_handles_labels()
            ax_rel2.legend(handles=handles, labels=['Tidak pernah (1)', 'Jarang (2)', 'Kadang (3)', 'Sering (4)', 'Selalu (5)'], title='Tingkat Gangguan')
            st.pyplot(fig_rel2)
