import streamlit as st
import pandas as pd
import joblib

# Səhifənin başlığı və dizaynı
st.set_page_config(page_title="Nasos Predictive Maintenance MVP", layout="centered")

st.title("⚙️ Nasosun Proqnozlaşdırıcı Baxım Paneli")
st.write("Bu panel sensor göstəricilərinə əsasən nasosun xarab olma riskini hesablayır.")

# 1. Modeli yaddaşdan yükləyirik
@st.cache_resource
def load_model():
    return joblib.load('pump_model.pkl')

try:
    model = load_model()
    st.success("✅ Model uğurla yükləndi!")
except:
    st.error("🚨 'pump_model.pkl' modeli tapılmadı! Zəhmət olmasa əvvəlcə modeli yadda saxladığınızdan əmin olun.")
    st.stop()

# 2. İstifadəçinin sensor dəyərlərini daxil etməsi üçün slayderlər (Sürgülər)
st.subheader("🎛️ Sensor Parametrlərini Tənzimləyin")

val_iso = st.slider("ISO Vibrasiya (value_ISO)", 0.0, 5.0, 0.3)
val_demo = st.slider("Demodulyasiya (value_DEMO)", 0.0, 0.5, 0.0003)
val_acc = st.slider("Ümumi Təcil (value_ACC)", 0.0, 0.6, 0.01)
val_p2p = st.slider("Pikdən-Pikə (value_P2P)", 0.0, 5.2, 0.04)
val_temp = st.slider("Temperatur (°C)", 15.0, 35.0, 24.0)

# 3. Hesablama düyməsi
if st.button("Risk Hesabla"):
    # Daxil edilən məlumatları modelə uyğunlaşdırırıq
    input_data = pd.DataFrame([[val_iso, val_demo, val_acc, val_p2p, val_temp]], 
                              columns=['value_ISO', 'value_DEMO', 'value_ACC', 'value_P2P', 'valueTEMP'])
    
    # Ehtimalı hesablayırıq
    probabilities = model.predict_proba(input_data)
    risk_percentage = probabilities[0][1] * 100
    
    st.markdown("---")
    st.subheader("📊 Analiz Nəticəsi:")
    
    # Nəticəyə görə ekranda rəngli xəbərdarlıq göstəririk
    if risk_percentage > 50:
        st.error(f"🚨 TƏHLÜKƏLİ! Nasosun xarab olma ehtimalı: **%{risk_percentage:.2f}**")
        st.warning("⚠️ Tövsiyə: Cihazda yüksək risk aşkarlandı, texniki baxış tələb olunur!")
    else:
        st.success(f"✅ NORMAL. Nasosun xarab olma ehtimalı: **%{risk_percentage:.2f}**")
        st.info("ℹ️ Cihaz normal iş rejimindədir.")
