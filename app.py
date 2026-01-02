import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="RFM Customer Segmentation Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Global page tweaks */
    body {
        background: linear-gradient(to bottom right, #ffffff, #0d0d0d00);
        color: #EAEAEA;
        font-family: 'Poppins', sans-serif;
    }

    /* ******************** PENINGKATAN VISUAL BARU ******************** */
    .stApp {
        background-color: #0D0D0D; /* Memastikan background utama aplikasi gelap */
    }

    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        color: #F6C90E;
        margin-top: -30px;
        padding: 18px;
        background: linear-gradient(90deg, rgba(40,40,40,0.9), rgba(10,10,10,0.8));
        border-radius: 12px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.45);
        border: 2px solid #F6C90E; /* BINGKAI EMAS */
    }

    .metric-box {
        background-color: #1A1A1A; /* Sedikit lebih terang dari background utama */
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.8); /* Shadow yang lebih gelap */
        text-align: center;
        margin-bottom: 16px;
        transition: transform 0.2s ease;
        border: 1px solid rgba(246,201,14,0.3); /* Border Emas yang lebih jelas */
    }
    .metric-box:hover { 
        transform: scale(1.02); 
        box-shadow: 0 6px 20px rgba(246,201,14,0.15); /* Efek hover yang lebih elegan */
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
        color: #F6C90E;
    }
    .metric-label {
        font-size: 14px;
        color: #CFCFCF;
    }

    section[data-testid="stSidebar"] {
        background-color: #121212 !important; /* Sidebar sedikit lebih terang */
        border-right: 1px solid #333333;
    }
    /* Mengubah warna teks di seluruh sidebar */
    section[data-testid="stSidebar"] {
        color: white !important;
    }

    /* Mengubah warna teks pada semua elemen di dalam sidebar */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .summary-box {
        background-color: #1F1F1F; /* Warna yang berbeda dari background utama */
        border-left: 5px solid #F6C90E; /* Menggunakan warna Emas utama */
        padding: 18px;
        border-radius: 10px;
        font-size: 14px;
        margin-top: 12px;
        color: #DDD;
        box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }

    /* === GOLD + BLACK PREMIUM TABLE THEME (custom-table used for HTML tables) === */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 12px;
        overflow: hidden;
        background-color: #0D0D0D; /* Deep black */
        color: #EAEAEA;
        border: 1px solid #3A3A3A;
        font-family: 'Poppins', sans-serif;
        font-size: 13px;
    }

    /* 🔥 PERBAIKAN STICKY HEADER FINAL 🔥 */
    .custom-table th {
        background: linear-gradient(90deg, #D4A017, #F6C90E); /* Gradient Emas yang lebih halus */
        color: #1B1B1B;
        font-weight: 700;
        padding: 10px;
        text-align: center;
        border-bottom: 2px solid #D4A017;
        position: sticky; /* Membuat header tetap */
        top: 0;          /* Menempel di bagian atas scroll-table */
        z-index: 1000;    /* Z-index ditingkatkan agar tidak tertutup elemen Streamlit lain */
    }

    .custom-table td {
        padding: 8px 12px;
        border: 1px solid #262626;
        color: #EAEAEA;
    }

    .custom-table tr:nth-child(odd) {
        background-color: #121212;
    }
    .custom-table tr:nth-child(even) {
        background-color: #1A1A1A;
    }

    .custom-table tr:hover {
        background-color: rgba(246, 201, 14, 0.2); /* Efek hover lebih jelas */
        transition: 0.15s ease-in-out;
    }

    /* Plot container tweaks - PENTING: Untuk memastikan Plotly mengikuti tema gelap */
    .stPlotlyChart {
         /* Memastikan semua plot berada dalam container yang konsisten */
         border-radius: 10px;
         background-color: #1A1A1A; 
         padding: 10px;
         box-shadow: 0 2px 10px rgba(0,0,0,0.7);
         margin-bottom: 20px;
    }
    
    /* MENYESUAIKAN TINGGI TABEL DAN SCROLL */
    .scroll-table {
        max-height: 500px; /* Ditingkatkan agar kedua tabel sejajar vertikal */
        overflow-y: auto;
        padding-right: 6px;
        margin-bottom: 20px;
        border: 1px solid #333;
        border-radius: 10px;
    }
    
    /* PERBAIKAN JUDUL: MENGATASI JUDUL BERTABRAKAN DI STREAMLIT */
    [data-testid="stMarkdownContainer"] h4 {
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        padding-top: 0;
        color: #F6C90E;
    }
    
    /* CSS Khusus untuk selectbox di kolom tabel 2, agar tidak menggeser tabel RFM mentah */
    [data-testid="stForm"] > div:nth-child(1) {
        margin-bottom: 0px !important; 
    }
    
    /* Mengatur judul section Streamlit untuk tema gelap */
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Hanya memuat file RFM 
    try:
        df_rfm = pd.read_csv("rfm_tanpa_outlier.csv")
        df_norm = pd.read_csv("rfm_minmax_scaled.csv")
        df_clustered = pd.read_csv("rfm_clustered.csv")
        return df_rfm, df_norm, df_clustered 
    except FileNotFoundError:
        st.error("Pastikan file CSV (rfm_tanpa_outlier.csv, rfm_minmax_scaled.csv, rfm_clustered.csv) berada di lokasi yang benar.")
        empty_df = pd.DataFrame()
        return empty_df, empty_df, empty_df

df_rfm, df_norm, df_clustered = load_data() 

cluster_names = {
    0: "Low Value Customer",
    1: "Regular Customer",
    2: "High Value Customer"
}

# Hanya lanjutkan jika df_clustered tidak kosong
if not df_clustered.empty:
    df_clustered["Cluster_Label"] = df_clustered["Cluster"].map(cluster_names)

PALETTE = {
    "gold": "#F6C90E",
    "gold_mid": "#DDB308",
    "bronze": "#A67C52",
    "navy": "#1F3A5F",
    "black": "#0D0D0D",
    "charcoal": "#2E2E2E",
    "white_text": "#EAEAEA",
    "dark_bg": "#1A1A1A"
}

color_map = {
    "Low Value Customer": PALETTE["navy"],
    "Regular Customer": PALETTE["gold"],
    "High Value Customer": PALETTE["bronze"]
}

# Membuat template Plotly 
plotly_dark_theme = dict(
    font=dict(color=PALETTE["white_text"], family="Poppins"),
    plot_bgcolor=PALETTE["dark_bg"],
    paper_bgcolor=PALETTE["dark_bg"],
    title_font=dict(size=20, color=PALETTE["gold_mid"]),
    xaxis=dict(showgrid=True, gridcolor=PALETTE["charcoal"], zerolinecolor=PALETTE["charcoal"], tickfont=dict(color=PALETTE["white_text"]), title_font=dict(color=PALETTE["white_text"])),
    yaxis=dict(showgrid=True, gridcolor=PALETTE["charcoal"], zerolinecolor=PALETTE["charcoal"], tickfont=dict(color=PALETTE["white_text"]), title_font=dict(color=PALETTE["white_text"])),
    legend=dict(font=dict(color=PALETTE["white_text"])),
    colorway=[PALETTE["gold"], PALETTE["navy"], PALETTE["bronze"]]
)

def gold_table(df: pd.DataFrame, index=False):
    """Convert DataFrame to HTML table with custom class 'custom-table'."""
    df2 = df.copy()
    df2.columns = [str(c) for c in df2.columns]
    html = df2.to_html(classes='custom-table', index=index, border=0, justify='center', na_rep='')
    return html

# SIDEBAR & HEADER
st.sidebar.title("📂 Menu Dashboard")
data_loaded_successfully = not df_clustered.empty

if data_loaded_successfully:
    menu = st.sidebar.radio("Pilih Menu:", ["Analisis Deskriptif", "Analisis Clustering"])
else:
    st.sidebar.markdown("⚠️ **Data tidak dapat dimuat, harap periksa file CSV Anda.**")
    menu = "Data Error"

st.markdown('<div class="dashboard-title">✨ Dashboard - PT. AJM Global Pratama ✨</div>', unsafe_allow_html=True)
st.write("")

if not data_loaded_successfully:
    st.warning("Tidak ada data untuk ditampilkan. Harap periksa apakah file CSV Anda sudah dimuat dengan benar.")

# # Analisis Deskriptif
elif menu == "Analisis Deskriptif":
    st.subheader("📊 Analisis Deskriptif Pelanggan")
    st.markdown("---") 

    # Metrics
    colA, colB, colC, colD = st.columns(4)
    with colA:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{len(df_clustered):,}</div>
            <div class="metric-label">Total Pelanggan</div>
        </div>
        """, unsafe_allow_html=True)
    with colB:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{round(df_clustered['Recency'].mean(), 2)} Hari</div>
            <div class="metric-label">Rata-rata Recency</div> 
        </div>
        """, unsafe_allow_html=True)
    with colC:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{round(df_clustered['Frequency'].mean(), 2)} Transaksi</div>
            <div class="metric-label">Rata-rata Frequency</div>
        </div>
        """, unsafe_allow_html=True)
    with colD:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">Rp {round(df_clustered['Monetary'].mean()):,}</div>
            <div class="metric-label">Rata-rata Monetary</div> 
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---") 

    # summary box
    st.markdown("""
        <div class="summary-box">
            <p><strong>💡 Sekilas Tentang RFM:</strong> Analisis ini mengukur nilai pelanggan berdasarkan <strong>Recency</strong> (kapan terakhir kali pelanggan membeli), <strong>Frequency</strong> (seberapa sering pelanggan membeli), dan <strong>Monetary</strong> (berapa banyak uang yang dibelanjakan pelanggan). Data di bawah ini memberikan pandangan dasar sebelum dilakukan clustering.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    
    # pie chart dan violin 
    col_plot1, col_plot2 = st.columns([1, 1])

    with col_plot1:
        st.markdown("#### Distribusi Cluster Pelanggan 🥧") 
        ordered_labels = ["High Value Customer", "Regular Customer", "Low Value Customer"] 
        cluster_counts = df_clustered["Cluster_Label"].value_counts().reindex(ordered_labels, fill_value=0)

        fig_pie = px.pie(
            names=cluster_counts.index,
            values=cluster_counts.values,
            color=cluster_counts.index,
            color_discrete_map=color_map,
        )
        fig_pie.update_traces(
            textinfo='percent+label',
            textfont=dict(size=10, family="Poppins", color="white"),
            pull=[0.06]*len(cluster_counts),
            hoverlabel=dict(font_size=13),
            marker=dict(line=dict(color='black', width=2))
        )
        fig_pie.update_layout(plotly_dark_theme, 
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5),
            height=620, 
            margin=dict(t=30, b=10, l=10, r=10), 
            plot_bgcolor=PALETTE["dark_bg"], 
            paper_bgcolor=PALETTE["dark_bg"],
            title='' 
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_plot2:
        st.markdown("#### Distribusi Recency, Frequency, Monetary📉") 

        # 1. Recency 
        fig_r = px.violin(df_norm, y='Recency_Scaled', 
                          box=True, points="all", title="Recency (Scaled)", 
                          color_discrete_sequence=[PALETTE["navy"]])
        fig_r.update_layout(plotly_dark_theme, height=170, title_font=dict(size=14), margin=dict(t=20, b=10, l=10, r=10)) 
        st.plotly_chart(fig_r, use_container_width=True)
        
        # 2. Frequency
        fig_f = px.violin(df_norm, y='Frequency_Scaled', 
                          box=True, points="all", title="Frequency (Scaled)", 
                          color_discrete_sequence=[PALETTE["gold"]])
        fig_f.update_layout(plotly_dark_theme, height=170, title_font=dict(size=14), margin=dict(t=20, b=10, l=10, r=10)) 
        st.plotly_chart(fig_f, use_container_width=True)

        # 3. Monetary 
        fig_m = px.violin(df_norm, y='Monetary_Scaled', 
                          box=True, points="all", title="Monetary (Scaled)", 
                          color_discrete_sequence=[PALETTE["bronze"]])
        fig_m.update_layout(plotly_dark_theme, height=170, title_font=dict(size=14), margin=dict(t=20, b=10, l=10, r=10)) 
        st.plotly_chart(fig_m, use_container_width=True)

    st.markdown("---")
    st.subheader("🥇 Peringkat Perusahaan Berdasarkan Metrik RFM")

    # 2. Bar Chart
    col_bar1, col_bar2, col_bar3 = st.columns(3)

    with col_bar1:
        # Top 10 companies recency 
        top_companies_recency = (
            df_rfm[['perusahaan', 'Recency']]
            .sort_values(by='Recency', ascending=True) 
            .head(10)
            .set_index('perusahaan')['Recency'] 
        )
        fig_rec = px.bar(
            top_companies_recency,
            x=top_companies_recency.index,
            y=top_companies_recency.values,
            title="Top 10 Recency (Hari Terendah)",
            color_discrete_sequence=[PALETTE["navy"]] 
        )
        fig_rec.update_traces(text=top_companies_recency.values, textposition='outside')
        fig_rec.update_layout(plotly_dark_theme, height=450)
        st.plotly_chart(fig_rec, use_container_width=True)

    with col_bar2:
        # Top 10 Frequency
        top_companies_freq = df_clustered.groupby('perusahaan')['Frequency'].sum().sort_values(ascending=False).head(10)
        fig_hist_company = px.bar(
            top_companies_freq,
            x=top_companies_freq.index,
            y=top_companies_freq.values,
            title="Top 10 Total Frequency",
            color_discrete_sequence=[PALETTE["gold"]] 
        )
        fig_hist_company.update_layout(plotly_dark_theme, height=450)
        st.plotly_chart(fig_hist_company, use_container_width=True)

    with col_bar3:
        # Top 10 Monetary
        top10_company_monetary = df_clustered.groupby('perusahaan')['Monetary_Scaled'].sum().sort_values(ascending=False).head(10)
        fig_top10 = px.bar(
            top10_company_monetary,
            x=top10_company_monetary.index,
            y=top10_company_monetary.values,
            title="Top 10 Total Monetary",
            color_discrete_sequence=[PALETTE["bronze"]]
        )
        fig_top10.update_layout(plotly_dark_theme, height=450)
        st.plotly_chart(fig_top10, use_container_width=True)


    st.markdown("---") 
    st.subheader("📋 Data Perusahaan & Cluster")
    
    # 3. Tabel Data
    col_tabel1, col_tabel2 = st.columns([1, 1])

    with col_tabel1:
        st.markdown("#### Data RFM")
        # Pilih hanya kolom yang diminta: perusahaan, Recency, Frequency, Monetary
        df_rfm_subset = df_rfm[['perusahaan', 'Recency', 'Frequency', 'Monetary']]
        
        # Tabel RFM
        st.markdown(f"""
        <div class="scroll-table">
            {gold_table(df_rfm_subset)} 
        </div>
        """, unsafe_allow_html=True)
    
    with col_tabel2:
        st.markdown("#### Daftar Cluster")
        
        selected_table_cluster = st.selectbox(
            "Pilih Cluster untuk Ditampilkan:",
            ["Semua"] + list(df_clustered["Cluster_Label"].unique()),
            key="table_cluster_filter_deskriptif"
        )

        if selected_table_cluster == "Semua":
            df_table = df_clustered[["perusahaan", "Cluster", "Cluster_Label"]].sort_values("Cluster")
        else:
            df_table = df_clustered[df_clustered["Cluster_Label"] == selected_table_cluster][
                ["perusahaan", "Cluster", "Cluster_Label"]
            ].sort_values("Cluster")

        st.markdown(f"**Jumlah perusahaan ditampilkan: {len(df_table)}**")
        st.markdown(f"""
        <div class="scroll-table">
            {gold_table(df_table.reset_index(drop=True))}
        </div>
        """, unsafe_allow_html=True)

# # Analisis Clustering 
elif menu == "Analisis Clustering":
    st.subheader("🤖 Analisis Clustering RFM (K-Means)")
    st.markdown("---") 

    col1, col2 = st.columns([2, 3])
    with col1:
        selected_cluster = st.selectbox(
            "🧭 Pilih Cluster:",
            ["Semua"] + list(df_clustered["Cluster_Label"].unique())
        )
    with col2:
        search_query = st.text_input("🔍 Cari nama perusahaan:")
    
    st.markdown("---") 

    df_filtered = df_clustered.copy()
    if selected_cluster != "Semua":
        df_filtered = df_filtered[df_filtered["Cluster_Label"] == selected_cluster]
    if search_query:
        df_filtered = df_filtered[df_filtered["perusahaan"].str.contains(search_query, case=False, na=False)]

    # 3D SCATTER
    st.subheader("🌌 Visualisasi 3D RFM Clustering")
    fig_3d = px.scatter_3d(
        df_filtered,
        x='Recency_Scaled',
        y='Frequency_Scaled',
        z='Monetary_Scaled',
        color='Cluster_Label',
        color_discrete_map=color_map,
        title="Visualisasi 3D RFM Clustering",
        hover_name='perusahaan',
        hover_data={
            'Cluster_Label': True,
            'Recency': ':.0f',
            'Frequency': ':.0f',
            'Monetary': ':, .2f'
        }
    )
    fig_3d.update_layout(
        plotly_dark_theme, 
        width=1000,
        height=700,
        scene=dict(
            xaxis_title='Recency_Scaled',
            yaxis_title='Frequency_Scaled',
            zaxis_title='Monetary_Scaled',
            xaxis=dict(backgroundcolor="#1A1A1A", gridcolor="#333", zerolinecolor="#333"),
            yaxis=dict(backgroundcolor="#1A1A1A", gridcolor="#333", zerolinecolor="#333"),
            zaxis=dict(backgroundcolor="#1A1A1A", gridcolor="#333", zerolinecolor="#333"),
            aspectratio=dict(x=1, y=1, z=0.8)
        ),
        margin=dict(l=0, r=0, b=0, t=60),
        paper_bgcolor=PALETTE["dark_bg"], 
        plot_bgcolor=PALETTE["dark_bg"]
    )

    fig_3d.update_traces(
        hovertemplate="""
        <b>Perusahaan: %{customdata[0]}</b><br><br>
        <b>Cluster: %{customdata[1]}</b><br>
        Recency (Hari): %{customdata[2]:.0f}<br>
        Frequency (Total): %{customdata[3]:.0f}<br>
        Monetary (Rp): Rp %{customdata[4]:, .0f}<extra></extra>
        """,
        customdata=df_filtered[['perusahaan', 'Cluster_Label', 'Recency', 'Frequency', 'Monetary']].values
    )

    st.plotly_chart(fig_3d, use_container_width=False)
    st.markdown("---") 
    
    # Heatmap
    st.subheader("🔥 Heatmap Korelasi RFM")
    corr = df_filtered[['Recency_Scaled', 'Frequency_Scaled', 'Monetary_Scaled']].corr()
    fig_heat = px.imshow(
        corr,
        color_continuous_scale=["#FFF7E0", "#F6C90E", "#D4A017", "#8C5A10"],
        title="Heatmap Korelasi RFM (Gold Palette)",
        text_auto=True,
        aspect="auto"
    )
    fig_heat.update_layout(plotly_dark_theme, 
        coloraxis_colorbar=dict(title="Corr", tickfont=dict(color=PALETTE["white_text"]))
    )
    fig_heat.update_xaxes(side="top")
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("---") 

    st.subheader("📈 Ringkasan Cluster")
    
    cluster_summary = df_filtered.groupby('Cluster_Label').agg({
        'Recency_Scaled': 'mean',
        'Frequency_Scaled': 'mean',
        'Monetary_Scaled': 'mean'
    }).round(4)
    cluster_summary['Jumlah Anggota'] = df_filtered['Cluster_Label'].value_counts()
    cluster_summary['Persentase (%)'] = (cluster_summary['Jumlah Anggota'] / len(df_filtered) * 100).round(2)
    st.markdown(gold_table(cluster_summary.reset_index()), unsafe_allow_html=True)
    
    st.markdown("""
        <div class="summary-box">
            <p><strong>Ringkasan Metrik:</strong> Tabel ini menunjukkan nilai rata-rata <strong>Recency, Frequency, dan Monetary</strong> per cluster. Angka yang lebih **tinggi** pada Frequency dan Monetary, serta **lebih rendah** pada Recency (karena Recency yang diskalakan adalah kebalikan dari Recency mentah), menunjukkan cluster yang lebih bernilai. </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---") 
    
    # Histogram
    col_clust_hist1, col_clust_hist2 = st.columns(2)

    with col_clust_hist1:
        st.plotly_chart(px.histogram(df_filtered, x='Cluster_Label', y='Frequency_Scaled', color='Cluster_Label',
                                     barmode='group', title="Sebaran Cluster vs Frequency",
                                     color_discrete_map=color_map).update_layout(plotly_dark_theme),
                       use_container_width=True)
    with col_clust_hist2:
        st.plotly_chart(px.histogram(df_filtered, x='Cluster_Label', y='Monetary_Scaled', color='Cluster_Label',
                                     barmode='group', title="Sebaran Cluster vs Monetary",
                                     color_discrete_map=color_map).update_layout(plotly_dark_theme),
                       use_container_width=True)

    st.markdown("---") 

    # Top 10 Perusahaan
    st.subheader("🏆 Top 10 Perusahaan Berdasarkan Cluster & Metrik RFM")
    
    for cluster in df_filtered["Cluster_Label"].unique():
        st.markdown(f"#### **{cluster}**")
        subset = df_filtered[df_filtered["Cluster_Label"] == cluster]

        col1, col2, col3 = st.columns(3)
        with col1:
            top10_r = subset.groupby("perusahaan")["Recency_Scaled"].mean().sort_values(ascending=True).head(10)
            fig_r = px.bar(top10_r, x=top10_r.values, y=top10_r.index, orientation="h",
                           title="Top 10 Recency Terendah", 
                           color_discrete_sequence=[PALETTE["navy"]])
            fig_r.update_layout(plotly_dark_theme, height=400, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_r, use_container_width=True)

        with col2:
            top10_f = subset.groupby("perusahaan")["Frequency_Scaled"].sum().sort_values(ascending=False).head(10)
            fig_f = px.bar(top10_f, x=top10_f.values, y=top10_f.index, orientation="h",
                           title="Top 10 Frequency Tertinggi",
                           color_discrete_sequence=[PALETTE["gold"]]) 
            fig_f.update_layout(plotly_dark_theme, height=400, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_f, use_container_width=True)

        with col3:
            top10_m = subset.groupby("perusahaan")["Monetary_Scaled"].sum().sort_values(ascending=False).head(10)
            fig_m = px.bar(top10_m, x=top10_m.values, y=top10_m.index, orientation="h",
                           title="Top 10 Monetary Tertinggi", 
                           color_discrete_sequence=[PALETTE["bronze"]]) 
            fig_m.update_layout(plotly_dark_theme, height=400, yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_m, use_container_width=True)