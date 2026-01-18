import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import math
from scipy.stats import norm

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="SmartStock AI Pro", layout="wide")
st.title("📦 SmartStock AI: Profesyonel Envanter Yönetimi")
st.markdown("---")

# --- 1. VERİ SİMÜLASYONU ---
@st.cache_data
def veri_uret():
    np.random.seed(42)
    baslangic = datetime(2024, 1, 1)
    gun_sayisi = 730
    tarihler = [baslangic + timedelta(days=i) for i in range(gun_sayisi)]
    satislar = 50 + 20 * np.sin(np.linspace(0, 8 * np.pi, gun_sayisi)) + np.random.normal(0, 10, gun_sayisi)
    return pd.DataFrame({'tarih': tarihler, 'satis': satislar.astype(int)})

df = veri_uret()

# --- 2. TALEP TAHMİNİ (AI) ---
df['gun_index'] = np.arange(len(df))
model = LinearRegression().fit(df[['gun_index']], df['satis'])
gelecek_gunler = np.array([[len(df) + i] for i in range(1, 31)])
tahminler = model.predict(gelecek_gunler)
aylik_talep = int(sum(tahminler))
gunluk_ortalama_talep = aylik_talep / 30
talep_standart_sapmasi = df['satis'].std()

# --- 3. MÜHENDİSLİK PARAMETRELERİ (SIDEBAR) ---
st.sidebar.header("⚙️ Operasyonel Ayarlar")
sip_maliyet = st.sidebar.number_input("Sipariş Maliyeti ($)", value=100)
elde_tutma = st.sidebar.number_input("Birim Tutma Maliyeti ($)", value=5)
tedarik_suresi = st.sidebar.slider("Tedarik Süresi (Gün)", 1, 14, 5)

st.sidebar.markdown("---")
st.sidebar.header("🛡️ Risk Yönetimi")
hizmet_seviyesi = st.sidebar.select_slider(
    "Hedef Hizmet Seviyesi (%)",
    options=[80, 85, 90, 95, 98, 99],
    value=95,
    help="Müşteriye 'yok çekmeme' olasılığınız."
)

# --- 4. HESAPLAMALAR (EOQ, SS, ROP) ---
# EOQ
yillik_talep = aylik_talep * 12
eoq = math.sqrt((2 * yillik_talep * sip_maliyet) / elde_tutma)

# Güvenlik Stoğu (Safety Stock) = Z * std_dev * sqrt(lead_time)
z_skoru = norm.ppf(hizmet_seviyesi / 100)
guvenlik_stogu = z_skoru * talep_standart_sapmasi * math.sqrt(tedarik_suresi)

# Yeniden Sipariş Noktası (ROP) = (D * L) + SS
rop = (gunluk_ortalama_talep * tedarik_suresi) + guvenlik_stogu

# --- 5. DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Gelecek Ay Tahmini", f"{aylik_talep} Adet")
c2.metric("İdeal Sipariş (EOQ)", f"{int(eoq)} Adet")
c3.metric("Güvenlik Stoğu", f"{int(guvenlik_stogu)} Adet")
c4.metric("Kritik Stok (ROP)", f"{int(rop)} Adet")

st.subheader("📈 Satış Projeksiyonu ve Stok Seviyeleri")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df['tarih'][-60:], df['satis'][-60:], label="Geçmiş Satışlar", color="#1f77b4", alpha=0.6)
gelecek_tarihler = [df['tarih'].iloc[-1] + timedelta(days=i) for i in range(1, 31)]
ax.plot(gelecek_tarihler, tahminler, label="Yapay Zeka Tahmini", color="#d62728", linestyle="--")
ax.axhline(y=rop, color='orange', linestyle=':', label="Yeni Sipariş Noktası (ROP)")
ax.fill_between(gelecek_tarihler, aylik_talep/30, rop, color='orange', alpha=0.1, label="Güvenlik Tamponu")
ax.legend()
st.pyplot(fig)

st.info(f"💡 **Mühendislik Analizi:** %{hizmet_seviyesi} hizmet seviyesini korumak için {int(guvenlik_stogu)} adet güvenlik stoğu tutulmaktadır. Toplam maliyet minimizasyonu için her siparişte {int(eoq)} adet ürün getirilmelidir.")