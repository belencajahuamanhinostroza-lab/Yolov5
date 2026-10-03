from PIL import Image
import io
import streamlit as st
import numpy as np
import pandas as pd
import torch

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Secure Vision",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ESTILO — inspirado en la referencia de cámaras de seguridad
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --black: #080909;
    --black-2: #111313;
    --panel: #171a19;
    --panel-2: #202321;
    --white: #f5f5ef;
    --muted: #a4aaa4;
    --lime: #d8f47a;
    --lime-2: #bde85e;
    --line: #303532;
    --danger: #ff6b61;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 85% 0%, rgba(216,244,122,.08), transparent 25%),
        radial-gradient(circle at 5% 90%, rgba(255,255,255,.035), transparent 25%),
        var(--black);
    color: var(--white);
}

/* Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

header[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1250px !important;
    padding-top: 1.7rem !important;
    padding-bottom: 3rem !important;
}

/* ============================================================
   SIDEBAR
   ============================================================ */
[data-testid="stSidebar"] {
    background: #0d0f0e !important;
    border-right: 1px solid #242825 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--white) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stSidebar"] label {
    color: #c5c9c4 !important;
    font-size: .82rem !important;
}

[data-testid="stSidebar"] p {
    color: #949a95 !important;
}

/* sliders */
[data-testid="stSlider"] [data-baseweb="slider"] div {
    color: var(--lime) !important;
}

[data-testid="stSlider"] [role="slider"] {
    background: var(--lime) !important;
    border-color: var(--lime) !important;
}

/* ============================================================
   BRAND
   ============================================================ */
.brand {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}

.brand-left {
    display: flex;
    align-items: center;
    gap: 11px;
}

.brand-mark {
    width: 43px;
    height: 43px;
    border-radius: 50%;
    background: var(--lime);
    color: #10120f;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    box-shadow: 0 0 0 7px rgba(216,244,122,.07);
}

.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--white);
    font-size: 1rem;
    font-weight: 700;
}

.brand-sub {
    color: #7f8580;
    font-size: .7rem;
    margin-top: 1px;
}

.live-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(216,244,122,.09);
    border: 1px solid rgba(216,244,122,.23);
    color: var(--lime);
    border-radius: 999px;
    padding: 7px 11px;
    font-size: .7rem;
    font-weight: 700;
}

.live-dot {
    width: 7px;
    height: 7px;
    background: var(--lime);
    border-radius: 50%;
    box-shadow: 0 0 0 4px rgba(216,244,122,.08);
}

/* ============================================================
   HERO / WELCOME
   ============================================================ */
.hero {
    position: relative;
    overflow: hidden;
    min-height: 205px;
    border-radius: 25px;
    background:
        radial-gradient(circle at 85% 15%, rgba(216,244,122,.16), transparent 25%),
        linear-gradient(135deg, #e9eee4 0%, #d9e2d5 48%, #cfd8cb 100%);
    padding: 29px 34px;
    margin-bottom: 20px;
    box-shadow: 0 18px 40px rgba(0,0,0,.22);
}

.hero::before {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    right: -75px;
    top: -105px;
    border-radius: 50%;
    border: 1px solid rgba(15,18,16,.08);
    box-shadow: 0 0 0 28px rgba(15,18,16,.025),
                0 0 0 56px rgba(15,18,16,.018);
}

.hero-eyebrow {
    color: #626a61;
    font-size: .72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.1px;
}

.hero-title {
    position: relative;
    z-index: 2;
    max-width: 590px;
    color: #090b09;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.45rem;
    font-weight: 700;
    line-height: 1.02;
    letter-spacing: -1.5px;
    margin-top: 8px;
}

.hero-copy {
    position: relative;
    z-index: 2;
    max-width: 570px;
    color: #555c54;
    font-size: .88rem;
    line-height: 1.5;
    margin-top: 11px;
}

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    margin-top: 17px;
    padding: 8px 13px;
    border-radius: 999px;
    background: #0a0b0a;
    color: white;
    font-size: .7rem;
    font-weight: 700;
}

/* ============================================================
   CARDS / PANELS
   ============================================================ */
.card {
    background: linear-gradient(145deg, #181b19, #111312);
    border: 1px solid var(--line);
    border-radius: 19px;
    padding: 20px;
    box-shadow: 0 12px 30px rgba(0,0,0,.18);
    margin-bottom: 17px;
}

.card-title {
    color: var(--white);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
}

.card-subtitle {
    color: #858b86;
    font-size: .75rem;
    margin-top: 3px;
    margin-bottom: 14px;
}

/* camera frame */
.camera-card {
    background: #0c0e0d;
    border: 1px solid #303530;
    border-radius: 20px;
    padding: 13px;
    box-shadow: 0 14px 34px rgba(0,0,0,.26);
}

.camera-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4px 4px 11px;
}

.camera-title {
    color: var(--white);
    font-family: 'Space Grotesk', sans-serif;
    font-size: .84rem;
    font-weight: 700;
}

.camera-status {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--lime);
    font-size: .68rem;
    font-weight: 700;
}

.camera-status span {
    width: 6px;
    height: 6px;
    background: var(--lime);
    border-radius: 50%;
}

/* inputs */
input, textarea {
    background: #111413 !important;
    color: var(--white) !important;
    border: 1px solid #343936 !important;
    border-radius: 12px !important;
}

input:focus, textarea:focus {
    border-color: var(--lime) !important;
    box-shadow: 0 0 0 3px rgba(216,244,122,.10) !important;
}

/* ============================================================
   BUTTONS — estilo referencia
   ============================================================ */
.stButton > button {
    background: #050605 !important;
    color: #ffffff !important;
    border: 1px solid #333733 !important;
    border-radius: 999px !important;
    min-height: 45px !important;
    padding: .65rem 1.35rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: .8rem !important;
    font-weight: 700 !important;
    box-shadow: 0 7px 17px rgba(0,0,0,.20) !important;
    transition: all .18s ease !important;
}

.stButton > button:hover {
    background: var(--lime) !important;
    color: #11130f !important;
    border-color: var(--lime) !important;
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(216,244,122,.13) !important;
}

/* Camera input */
[data-testid="stCameraInput"] {
    border-radius: 15px !important;
}

[data-testid="stCameraInput"] section {
    background: #111312 !important;
    border: 1px dashed #454a46 !important;
    border-radius: 15px !important;
}

[data-testid="stCameraInput"] button {
    background: var(--lime) !important;
    color: #10120f !important;
    border: 0 !important;
    border-radius: 999px !important;
    font-weight: 700 !important;
}

/* ============================================================
   KPI CARDS
   ============================================================ */
.kpi {
    background: #171a18;
    border: 1px solid #2d322f;
    border-radius: 15px;
    padding: 16px;
}

.kpi-label {
    color: #838983;
    font-size: .67rem;
    text-transform: uppercase;
    letter-spacing: .8px;
    font-weight: 700;
}

.kpi-value {
    color: var(--white);
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin-top: 5px;
}

.kpi-note {
    color: #6e756f;
    font-size: .68rem;
    margin-top: 1px;
}

/* confidence score */
.score-card {
    background: linear-gradient(145deg, #dff19d, #c9e979);
    color: #10120f;
    border-radius: 20px;
    padding: 21px;
    min-height: 190px;
    position: relative;
    overflow: hidden;
}

.score-card::after {
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    right: -70px;
    top: -80px;
    border: 1px solid rgba(0,0,0,.08);
    border-radius: 50%;
    box-shadow: 0 0 0 24px rgba(0,0,0,.025),
                0 0 0 48px rgba(0,0,0,.018);
}

.score-label {
    color: #626b54;
    font-size: .68rem;
    font-weight: 700;
}

.score-value {
    color: #0d0f0d;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    line-height: 1;
    font-weight: 700;
    margin: 8px 0;
}

.score-tag {
    display: inline-block;
    background: #11130f;
    color: var(--lime);
    padding: 6px 10px;
    border-radius: 999px;
    font-size: .68rem;
    font-weight: 700;
}

/* result */
.result-card {
    background: #f0f2ec;
    color: #11130f;
    border-radius: 20px;
    padding: 21px;
    min-height: 190px;
}

.result-badge {
    display: inline-block;
    background: #11130f;
    color: var(--lime);
    border-radius: 999px;
    padding: 6px 10px;
    font-size: .66rem;
    font-weight: 700;
}

.result-title {
    color: #11130f;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    margin-top: 12px;
}

.result-text {
    color: #596057;
    font-size: .82rem;
    line-height: 1.5;
    margin-top: 7px;
}

/* table */
[data-testid="stDataFrame"] {
    border: 1px solid #303530 !important;
    border-radius: 13px !important;
    overflow: hidden !important;
}

/* expander */
div[data-testid="stExpander"] {
    background: #141715 !important;
    border: 1px solid #303530 !important;
    border-radius: 14px !important;
}

div[data-testid="stExpander"] summary {
    color: var(--white) !important;
}

/* alert */
[data-testid="stAlert"] {
    border-radius: 13px !important;
}

/* chart text */
svg text {
    fill: #aeb4ae !important;
}

/* divider */
hr {
    border-color: #292d2a !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# MODELO
# ============================================================
@st.cache_resource
def load_model():
    try:
        from ultralytics import YOLO
        model = YOLO("yolov5su.pt")
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {str(e)}")
        return None


# ============================================================
# BRAND
# ============================================================
st.markdown("""
<div class="brand">
    <div class="brand-left">
        <div class="brand-mark">◉</div>
        <div>
            <div class="brand-name">Secure Vision</div>
            <div class="brand-sub">AI object detection system</div>
        </div>
    </div>
    <div class="live-pill">
        <span class="live-dot"></span>
        CAMERA READY
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Smart camera · AI detection</div>
    <div class="hero-title">Secure your world with intelligent vision.</div>
    <div class="hero-copy">
        Detect people, vehicles and everyday objects directly from your camera
        using YOLO and real-time computer vision technology.
    </div>
    <div class="hero-pill">◉ &nbsp; YOLO Vision Engine &nbsp; ↗</div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# CARGA
# ============================================================
with st.spinner("Loading vision engine..."):
    model = load_model()


if model:

    # ========================================================
    # SIDEBAR
    # ========================================================
    with st.sidebar:
        st.markdown("""
        <div style="padding:8px 0 18px;">
            <div style="color:#d8f47a;font-size:.68rem;font-weight:700;
                        text-transform:uppercase;letter-spacing:1px;">
                Camera controls
            </div>
            <div style="color:#f5f5ef;font-family:'Space Grotesk';
                        font-size:1.2rem;font-weight:700;margin-top:5px;">
                Detection
            </div>
        </div>
        """, unsafe_allow_html=True)

        conf_threshold = st.slider(
            "Minimum confidence",
            0.0, 1.0, 0.25, 0.01
        )

        iou_threshold = st.slider(
            "IoU threshold",
            0.0, 1.0, 0.45, 0.01
        )

        max_det = st.number_input(
            "Maximum detections",
            10, 2000, 1000, 10
        )

        st.markdown("""
        <div style="margin-top:18px;padding:13px;border:1px solid #303530;
                    border-radius:13px;background:#151816;">
            <div style="color:#858c86;font-size:.66rem;text-transform:uppercase;
                        letter-spacing:.8px;font-weight:700;">Engine</div>
            <div style="color:#f5f5ef;font-family:'Space Grotesk';
                        font-weight:700;margin-top:4px;">YOLOv5su</div>
            <div style="color:#707770;font-size:.68rem;margin-top:3px;">
                PyTorch · Ultralytics
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ========================================================
    # CAMERA
    # ========================================================
    st.markdown("""
    <div class="camera-card">
        <div class="camera-head">
            <div class="camera-title">Live camera capture</div>
            <div class="camera-status">
                <span></span> READY
            </div>
        </div>
    """, unsafe_allow_html=True)

    picture = st.camera_input(
        "Capture image",
        key="camera",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ========================================================
    # DETECCIÓN
    # ========================================================
    if picture:
        bytes_data = picture.getvalue()

        pil_img = Image.open(
            io.BytesIO(bytes_data)
        ).convert("RGB")

        np_img = np.array(pil_img)[..., ::-1]

        with st.spinner("Analyzing camera image..."):
            try:
                results = model(
                    np_img,
                    conf=conf_threshold,
                    iou=iou_threshold,
                    max_det=int(max_det)
                )
            except Exception as e:
                st.error(f"Error during detection: {str(e)}")
                st.stop()

        result = results[0]
        boxes = result.boxes

        annotated = result.plot()
        annotated_rgb = annotated[:, :, ::-1]

        # ====================================================
        # RESULTADOS
        # ====================================================
        col1, col2 = st.columns([1.25, .75], gap="large")

        with col1:
            st.markdown("""
            <div class="card" style="padding-bottom:13px;">
                <div class="card-title">Detection feed</div>
                <div class="card-subtitle">
                    Objects detected in the captured frame
                </div>
            """, unsafe_allow_html=True)

            st.image(
                annotated_rgb,
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            if boxes is not None and len(boxes) > 0:

                label_names = model.names
                category_count = {}
                category_conf = {}

                for box in boxes:
                    cat = int(box.cls.item())
                    conf = float(box.conf.item())

                    category_count[cat] = (
                        category_count.get(cat, 0) + 1
                    )

                    category_conf.setdefault(cat, []).append(conf)

                total_objects = len(boxes)
                categories = len(category_count)
                avg_conf = float(
                    np.mean([
                        float(box.conf.item())
                        for box in boxes
                    ])
                )

                # KPIs
                k1, k2 = st.columns(2)

                with k1:
                    st.markdown(f"""
                    <div class="kpi">
                        <div class="kpi-label">Objects</div>
                        <div class="kpi-value">{total_objects}</div>
                        <div class="kpi-note">detected</div>
                    </div>
                    """, unsafe_allow_html=True)

                with k2:
                    st.markdown(f"""
                    <div class="kpi">
                        <div class="kpi-label">Classes</div>
                        <div class="kpi-value">{categories}</div>
                        <div class="kpi-note">categories</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:10px'></div>",
                            unsafe_allow_html=True)

                st.markdown(f"""
                <div class="score-card">
                    <div class="score-label">AVERAGE CONFIDENCE</div>
                    <div class="score-value">{avg_conf:.0%}</div>
                    <span class="score-tag">● Detection active</span>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height:10px'></div>",
                            unsafe_allow_html=True)

                st.markdown("""
                <div class="card">
                    <div class="card-title">Detected objects</div>
                    <div class="card-subtitle">
                        Category · quantity · confidence
                    </div>
                """, unsafe_allow_html=True)

                data = [
                    {
                        "Categoría": label_names[cat],
                        "Cantidad": count,
                        "Confianza promedio": f"{np.mean(category_conf[cat]):.2f}"
                    }
                    for cat, count in category_count.items()
                ]

                df = pd.DataFrame(data)

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="result-card">
                    <div class="result-badge">NO OBJECTS</div>
                    <div class="result-title">Nothing detected.</div>
                    <div class="result-text">
                        Try lowering the confidence threshold from the
                        camera controls.
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # ====================================================
        # CHART
        # ====================================================
        if boxes is not None and len(boxes) > 0:
            st.markdown("<div style='height:2px'></div>",
                        unsafe_allow_html=True)

            st.markdown("""
            <div class="card">
                <div class="card-title">Detection overview</div>
                <div class="card-subtitle">
                    Number of detected objects by category
                </div>
            """, unsafe_allow_html=True)

            st.bar_chart(
                df.set_index("Categoría")["Cantidad"],
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:36px 20px;">
            <div style="width:54px;height:54px;border-radius:50%;
                        background:#d8f47a;color:#10120f;
                        display:flex;align-items:center;justify-content:center;
                        margin:0 auto 13px;font-size:1.2rem;">◉</div>
            <div class="card-title">Camera ready</div>
            <div class="card-subtitle" style="margin-bottom:0;">
                Capture an image to start detecting objects with YOLO.
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error(
        "No se pudo cargar el modelo. "
        "Verifica las dependencias e inténtalo nuevamente."
    )
    st.stop()


# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="margin-top:30px;padding-top:18px;border-top:1px solid #292d2a;
            display:flex;justify-content:space-between;gap:20px;">
    <div style="color:#686f69;font-size:.68rem;">
        SECURE VISION · AI OBJECT DETECTION
    </div>
    <div style="color:#686f69;font-size:.68rem;">
        YOLOv5 · Streamlit · PyTorch
    </div>
</div>
""", unsafe_allow_html=True)
