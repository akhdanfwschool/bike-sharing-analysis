from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MAIN_DATA = ROOT / "dashboard" / "main_data.csv"

SEASON_LABELS = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
WEATHER_LABELS = {
    1: "Cerah / sedikit awan",
    2: "Berkabut / berawan",
    3: "Hujan ringan / salju ringan",
    4: "Cuaca ekstrem",
}
WEEKDAY_LABELS = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"}

st.set_page_config(page_title="Bike Sharing | Ringkasan Analisis", page_icon="🚲", layout="wide")
st.markdown("""
<style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1400px;}
    [data-testid="stMetric"] {border: 1px solid rgba(128,128,128,.24); padding: 14px 16px; border-radius: 12px;}
    .eyebrow {letter-spacing: .12em; text-transform: uppercase; font-size: .76rem; opacity: .72;}
</style>
""", unsafe_allow_html=True)


def load_data() -> pd.DataFrame:
    if MAIN_DATA.exists():
        df = pd.read_csv(MAIN_DATA)
    else:
        source = DATA_DIR / "day.csv"
        if not source.exists():
            st.error("Dataset belum ditemukan. Dari folder proyek, jalankan `python scripts/download_data.py`, lalu muat ulang dashboard.")
            st.code("python scripts/download_data.py\nstreamlit run dashboard/dashboard.py", language="bash")
            st.stop()
        df = pd.read_csv(source)
    if "dteday" not in df.columns and "date" in df.columns:
        df = df.rename(columns={"date": "dteday"})
    df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce")
    required = {"dteday", "season", "weathersit", "workingday", "casual", "registered", "cnt"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Kolom wajib tidak tersedia: {', '.join(sorted(missing))}")
        st.stop()
    df = df.dropna(subset=["dteday", "cnt"]).copy()
    df["year"] = df["dteday"].dt.year
    df["month"] = df["dteday"].dt.month
    df["season_name"] = df["season"].map(SEASON_LABELS).fillna(df["season"].astype(str))
    df["weather_name"] = df["weathersit"].map(WEATHER_LABELS).fillna(df["weathersit"].astype(str))
    df["day_type"] = df["workingday"].map({1: "Hari kerja", 0: "Akhir pekan / hari libur"}).fillna("Tidak diketahui")
    df["month_name"] = df["dteday"].dt.strftime("%b")
    return df


df = load_data()

st.markdown('<div class="eyebrow">Data storytelling · 2011–2012</div>', unsafe_allow_html=True)
st.title("Pola Peminjaman Sepeda")
st.write("Dashboard interaktif untuk mengevaluasi tren permintaan, tipe hari, musim, dan kondisi cuaca pada sistem bike sharing.")

with st.sidebar:
    st.header("Filter analisis")
    min_date = df["dteday"].min().date()
    max_date = df["dteday"].max().date()
    date_range = st.date_input("Periode", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    years = sorted(df["year"].dropna().astype(int).unique().tolist())
    selected_years = st.multiselect("Tahun", years, default=years)
    seasons = sorted(df["season_name"].dropna().unique().tolist())
    selected_seasons = st.multiselect("Musim", seasons, default=seasons)
    weathers = sorted(df["weather_name"].dropna().unique().tolist())
    selected_weather = st.multiselect("Kondisi cuaca", weathers, default=weathers)
    day_types = ["Hari kerja", "Akhir pekan / hari libur"]
    selected_day_types = st.multiselect("Tipe hari", day_types, default=day_types)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[filtered["dteday"].between(start, end)]
if selected_years:
    filtered = filtered[filtered["year"].isin(selected_years)]
else:
    filtered = filtered.iloc[0:0]
if selected_seasons:
    filtered = filtered[filtered["season_name"].isin(selected_seasons)]
else:
    filtered = filtered.iloc[0:0]
if selected_weather:
    filtered = filtered[filtered["weather_name"].isin(selected_weather)]
else:
    filtered = filtered.iloc[0:0]
if selected_day_types:
    filtered = filtered[filtered["day_type"].isin(selected_day_types)]
else:
    filtered = filtered.iloc[0:0]

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih. Perluas rentang tanggal atau pilih kategori lainnya.")
    st.stop()

metric_cols = st.columns(4)
metric_cols[0].metric("Total peminjaman", f"{filtered['cnt'].sum():,.0f}".replace(",", "."))
metric_cols[1].metric("Rata-rata per hari", f"{filtered['cnt'].mean():,.0f}".replace(",", "."))
metric_cols[2].metric("Hari dianalisis", f"{len(filtered):,}".replace(",", "."))
registered_share = (filtered["registered"].sum() / filtered["cnt"].sum() * 100) if filtered["cnt"].sum() else 0
metric_cols[3].metric("Porsi pengguna terdaftar", f"{registered_share:.1f}%")

st.divider()
left, right = st.columns(2, gap="large")
with left:
    st.subheader("01 · Tren bulanan")
    monthly = (filtered.assign(month_start=filtered["dteday"].dt.to_period("M").dt.to_timestamp())
               .groupby("month_start", as_index=False)["cnt"].mean())
    fig = px.line(monthly, x="month_start", y="cnt", markers=True,
                  labels={"month_start": "Bulan", "cnt": "Rata-rata peminjaman per hari"})
    fig.update_layout(margin=dict(l=10, r=10, t=15, b=10), height=350)
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("02 · Hari kerja vs non-hari kerja")
    day_summary = filtered.groupby("day_type", as_index=False)["cnt"].mean()
    fig = px.bar(day_summary, x="day_type", y="cnt", text_auto=".0f",
                 labels={"day_type": "Tipe hari", "cnt": "Rata-rata peminjaman per hari"})
    fig.update_layout(margin=dict(l=10, r=10, t=15, b=10), height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2, gap="large")
with left:
    st.subheader("03 · Permintaan menurut musim")
    by_season = (filtered.groupby("season_name", as_index=False)["cnt"].mean()
                 .sort_values("cnt", ascending=False))
    fig = px.bar(by_season, x="season_name", y="cnt", text_auto=".0f",
                 labels={"season_name": "Musim", "cnt": "Rata-rata peminjaman per hari"})
    fig.update_layout(margin=dict(l=10, r=10, t=15, b=10), height=320, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("04 · Permintaan menurut cuaca")
    by_weather = (filtered.groupby("weather_name", as_index=False)["cnt"].mean()
                  .sort_values("cnt", ascending=False))
    fig = px.bar(by_weather, x="weather_name", y="cnt", text_auto=".0f",
                 labels={"weather_name": "Kondisi cuaca", "cnt": "Rata-rata peminjaman per hari"})
    fig.update_layout(margin=dict(l=10, r=10, t=15, b=10), height=320, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Temuan untuk ditindaklanjuti")
peak = monthly.loc[monthly["cnt"].idxmax()] if not monthly.empty else None
low = monthly.loc[monthly["cnt"].idxmin()] if not monthly.empty else None
best_season = by_season.iloc[0] if not by_season.empty else None
worst_weather = by_weather.iloc[-1] if not by_weather.empty else None
notes = []
if peak is not None:
    notes.append(f"Periode dengan rata-rata peminjaman tertinggi pada filter aktif adalah {peak['month_start']:%B %Y} ({peak['cnt']:.0f} peminjaman/hari). Siapkan ketersediaan sepeda dan pemeliharaan menjelang periode tersebut.")
if low is not None:
    notes.append(f"Periode dengan rata-rata terendah adalah {low['month_start']:%B %Y} ({low['cnt']:.0f} peminjaman/hari). Uji promosi atau paket harga pada periode permintaan rendah.")
if best_season is not None:
    notes.append(f"Musim dengan rata-rata peminjaman tertinggi pada filter aktif adalah {best_season['season_name']} ({best_season['cnt']:.0f} per hari).")
if worst_weather is not None:
    notes.append(f"Kategori cuaca dengan rata-rata peminjaman terendah adalah {worst_weather['weather_name']} ({worst_weather['cnt']:.0f} per hari); pertimbangkan pesan keselamatan dan perencanaan operasional yang fleksibel.")
for note in notes:
    st.markdown(f"- {note}")
st.caption("Catatan: data mencakup 2011–2012 dan kode cuaca/musim mengikuti dokumentasi dataset. Temuan bersifat deskriptif, bukan bukti sebab-akibat.")
with st.expander("Lihat data terfilter"):
    st.dataframe(filtered.sort_values("dteday", ascending=False), use_container_width=True, hide_index=True)
    st.download_button("Unduh data hasil filter (CSV)", filtered.to_csv(index=False).encode("utf-8"), file_name="bike_sharing_filtered.csv", mime="text/csv")
