import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Penilaian Mahasiswa Fuzzy", layout="wide")

st.title("📚 Sistem Penilaian Mahasiswa Menggunakan Logika Fuzzy")

st.write("Input berupa nilai ujian (0-100).")

# ===========================
# INPUT
# ===========================

nilai = st.slider(
    "Masukkan Nilai Ujian",
    0,
    100,
    70
)

# ===========================
# FUNGSI KEANGGOTAAN
# ===========================

def rendah(x):
    if x <= 40:
        return 1
    elif 40 < x < 60:
        return (60 - x) / 20
    else:
        return 0

def sedang(x):
    if x <= 40 or x >= 80:
        return 0
    elif 40 < x <= 60:
        return (x - 40) / 20
    elif 60 < x < 80:
        return (80 - x) / 20

def tinggi(x):
    if x <= 60:
        return 0
    elif 60 < x < 80:
        return (x - 60) / 20
    else:
        return 1

# ===========================
# HITUNG DERAJAT KEANGGOTAAN
# ===========================

mu_rendah = rendah(nilai)
mu_sedang = sedang(nilai)
mu_tinggi = tinggi(nilai)

st.header("Derajat Keanggotaan")

col1,col2,col3 = st.columns(3)

col1.metric("Rendah", f"{mu_rendah:.2f}")
col2.metric("Sedang", f"{mu_sedang:.2f}")
col3.metric("Tinggi", f"{mu_tinggi:.2f}")

# ===========================
# INTERPRETASI
# ===========================

nilai_max = max(mu_rendah, mu_sedang, mu_tinggi)

if nilai_max == mu_rendah:
    hasil = "RENDAH"
elif nilai_max == mu_sedang:
    hasil = "SEDANG"
else:
    hasil = "TINGGI"

st.success(f"Kategori Penilaian Mahasiswa : **{hasil}**")

# ===========================
# GRAFIK
# ===========================

x = np.linspace(0,100,500)

y_rendah = []
y_sedang = []
y_tinggi = []

for i in x:
    y_rendah.append(rendah(i))
    y_sedang.append(sedang(i))
    y_tinggi.append(tinggi(i))

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(x,y_rendah,label="Rendah",color="blue",linewidth=2)
ax.plot(x,y_sedang,label="Sedang",color="green",linewidth=2)
ax.plot(x,y_tinggi,label="Tinggi",color="red",linewidth=2)

# Titik input
ax.axvline(nilai,color='black',linestyle='--')
ax.scatter([nilai],[mu_rendah],color='blue')
ax.scatter([nilai],[mu_sedang],color='green')
ax.scatter([nilai],[mu_tinggi],color='red')

ax.set_xlabel("Nilai Ujian")
ax.set_ylabel("μ(x)")
ax.set_xlim(0,100)
ax.set_ylim(0,1.1)
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ===========================
# RULE
# ===========================

st.header("Rule Fuzzy")

st.write("""
**R1** : IF Nilai Rendah THEN Penilaian Rendah

**R2** : IF Nilai Sedang THEN Penilaian Sedang

**R3** : IF Nilai Tinggi THEN Penilaian Tinggi
""")

# ===========================
# TABEL HASIL
# ===========================

st.header("Hasil Perhitungan")

st.table({
    "Kategori":["Rendah","Sedang","Tinggi"],
    "Derajat Keanggotaan":[
        round(mu_rendah,2),
        round(mu_sedang,2),
        round(mu_tinggi,2)
    ]
})

st.info(f"""
Nilai Ujian = {nilai}

μ Rendah = {mu_rendah:.2f}

μ Sedang = {mu_sedang:.2f}

μ Tinggi = {mu_tinggi:.2f}

Kategori = {hasil}
""")
