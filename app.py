import streamlit as st
import numpy as np

from physics import *
from visualization import *
from utils import *

# --------------------------
# PAGE CONFIG
# --------------------------

st.set_page_config(
    page_title="Wave Optics Simulation Lab",
    layout="wide"
)

# --------------------------
# TITLE
# --------------------------

st.title("🔬 Interactive Wave Optics Simulation & Measurement Lab")

st.markdown("""
A physics-based interactive simulation platform to study:

• Single-Slit Diffraction  
• Double-Slit Interference  
• Diffraction Gratings  

Adjust physical parameters and observe real-time changes in intensity patterns.
""")

# --------------------------
# SIDEBAR
# --------------------------

st.sidebar.header("🧪 Experiment Selection")

experiment = st.sidebar.selectbox(
    "Choose Experiment",
    [
        "Single Slit Diffraction",
        "Double Slit Interference",
        "Diffraction Grating"
    ]
)

st.sidebar.header("⚙️ Physical Parameters")

wavelength_nm = st.sidebar.slider(
    "Wavelength (nm)",
    400,
    700,
    550
)

wavelength = wavelength_nm * 1e-9
color = wavelength_color(wavelength_nm)

st.sidebar.markdown(f"### 🌈 Color: **{color.upper()}**")

theta = np.linspace(-0.01, 0.01, 4000)

st.header(f"📊 {experiment}")

# =====================================================
# SINGLE SLIT
# =====================================================

if experiment == "Single Slit Diffraction":

    slit_width_um = st.sidebar.slider("Slit Width (µm)", 5, 100, 20)
    slit_width = slit_width_um * 1e-6

    intensity = single_slit_intensity(theta, wavelength, slit_width)

    fig = intensity_plot(theta, intensity, wavelength_nm)
    heatmap = heatmap_pattern(intensity, wavelength_nm)

    # Animation
    animated_fig = animated_intensity(theta, np.roll(intensity, 200), intensity)

    st.plotly_chart(animated_fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(heatmap, use_container_width=True)

    # Metrics
    st.subheader("📏 Extracted Physical Quantities")

    res = resolution_limit(wavelength, slit_width)

    col1, col2, col3 = st.columns(3)

    col1.metric("Wavelength", f"{wavelength_nm} nm")
    col2.metric("Slit Width", f"{slit_width_um} µm")
    col3.metric("Resolution Limit", f"{res:.4f}°")

    # Explanation
    st.info(f"""
🔍 Increasing slit width → narrower central peak  
🔍 Increasing wavelength → wider diffraction spread  

This follows θ ≈ λ / a
""")

# =====================================================
# DOUBLE SLIT
# =====================================================

elif experiment == "Double Slit Interference":

    slit_width_um = st.sidebar.slider("Slit Width (µm)", 5, 100, 20)
    slit_distance_um = st.sidebar.slider("Slit Separation (µm)", 50, 500, 200)
    screen_distance = st.sidebar.slider("Screen Distance (m)", 0.5, 5.0, 1.0)

    slit_width = slit_width_um * 1e-6
    slit_distance = slit_distance_um * 1e-6

    intensity = double_slit_intensity(theta, wavelength, slit_width, slit_distance)

    fig = intensity_plot(theta, intensity, wavelength_nm)
    heatmap = heatmap_pattern(intensity, wavelength_nm)

    animated_fig = animated_intensity(theta, intensity * 0.2, intensity)

    st.plotly_chart(animated_fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(heatmap, use_container_width=True)

    st.subheader("📏 Extracted Physical Quantities")

    fringe = fringe_spacing(wavelength, screen_distance, slit_distance)
    angle = diffraction_angle(1, wavelength, slit_distance)

    col1, col2, col3 = st.columns(3)

    col1.metric("Wavelength", f"{wavelength_nm} nm")
    col2.metric("Fringe Spacing", f"{fringe*1000:.4f} mm")

    if angle:
        col3.metric("First Order Angle", f"{angle:.4f}°")

    st.subheader("📐 Fringe Orders")

    orders = fringe_orders(wavelength, slit_distance)

    for m, ang in orders:
        st.write(f"m = {m} → θ ≈ {ang:.4f}°")

    st.info(f"""
🔍 Increasing slit separation → fringes get closer  
🔍 Increasing wavelength → fringes spread apart  

Relation: y = λL / d
""")

# =====================================================
# DIFFRACTION GRATING
# =====================================================

elif experiment == "Diffraction Grating":

    slit_distance_um = st.sidebar.slider("Grating Spacing (µm)", 5, 50, 10)
    N = st.sidebar.slider("Number of Slits", 2, 50, 10)

    slit_distance = slit_distance_um * 1e-6

    intensity = diffraction_grating_intensity(theta, wavelength, slit_distance, N)

    fig = intensity_plot(theta, intensity, wavelength_nm)
    heatmap = heatmap_pattern(intensity, wavelength_nm)

    animated_fig = animated_intensity(theta, intensity * 0.2, intensity)

    st.plotly_chart(animated_fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(heatmap, use_container_width=True)

    st.subheader("📏 Extracted Physical Quantities")

    angle = diffraction_angle(1, wavelength, slit_distance)
    resolving = grating_resolving_power(1, N)

    col1, col2, col3 = st.columns(3)

    col1.metric("Wavelength", f"{wavelength_nm} nm")

    if angle:
        col2.metric("First Order Angle", f"{angle:.4f}°")

    col3.metric("Resolving Power", f"{resolving}")

    st.info(f"""
🔍 Increasing number of slits → sharper peaks  
🔍 Higher order → better resolution  

Resolving Power R = mN
""")

# =====================================================
# GLOBAL PHYSICS EXPLANATION
# =====================================================

st.markdown("---")

st.subheader("🧠 Physical Interpretation")

st.markdown("""
Diffraction and interference arise due to the **wave nature of light**.

• Waves passing through apertures spread and overlap  
• Constructive interference → bright fringes  
• Destructive interference → dark regions  

The general condition for maxima:

**d sin(θ) = mλ**

This simulator allows real-time exploration of these principles.
""")

# =====================================================
# FOOTER
# =====================================================

st.success("""
💡 Applications:
• Spectroscopy  
• Optical instrument design  
• Laser systems  
• Wave optics experiments  
""")