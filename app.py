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
st.caption("🚀 Interactive Physics Simulation | 2D + 3D | Real-Time Visualization")
if st.button("▶ Run Auto Demo"):
    if "demo_wavelength" not in st.session_state:
        st.session_state["demo_wavelength"] = 400
    else:
        st.session_state["demo_wavelength"] += 50
        if st.session_state["demo_wavelength"] > 700:
            st.session_state["demo_wavelength"] = 400

    st.rerun()
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
        "Single Slit Diffraction (2D)",
        "Double Slit Interference (2D)",
        "Diffraction Grating (2D)",
        "Single Slit Diffraction (3D)",
        "Double Slit Interference (3D)",
        "Diffraction Grating (3D)"

    ]
)

st.sidebar.header("⚙️ Physical Parameters")

wavelength_nm = st.sidebar.slider(
    "Wavelength (nm)",
    400,
    700,
    st.session_state.get("demo_wavelength", 550)
)

guided_mode = st.sidebar.checkbox("🎓 Guided Mode")

wavelength = wavelength_nm * 1e-9
color = wavelength_color(wavelength_nm)

st.sidebar.markdown(f"### 🌈 Color: **{color.upper()}**")

theta = np.linspace(-0.01, 0.01, 4000)

st.header(f"📊 {experiment}")

# =====================================================
# SINGLE SLIT
# =====================================================

if experiment == "Single Slit Diffraction (2D)":

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
    if guided_mode:
       st.markdown("### 🎓 Guided Learning")

       st.info("Step 1: Observe the central maximum at θ = 0")

       st.info("Step 2: Increase wavelength → diffraction spreads wider")

       st.info("Step 3: Increase slit width → central peak becomes sharper")

       st.info("Formula: θ ≈ λ / a")

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

elif experiment == "Double Slit Interference (2D)":

    slit_width_um = st.sidebar.slider("Slit Width (µm)", 5, 100, 20)
    slit_distance_um = st.sidebar.slider("Slit Separation (µm)", 50, 500, 200)
    screen_distance = st.sidebar.slider("Screen Distance (m)", 0.5, 5.0, 1.0)

    slit_width = slit_width_um * 1e-6
    slit_distance = slit_distance_um * 1e-6

    multi_mode = st.checkbox("🌈 Enable Multi-Wavelength (White Light Simulation)")
    if multi_mode:
        st.success("🌈 Multi-wavelength mode enabled: simulating white light interference")

    if multi_mode:
        wavelength_range = np.linspace(400e-9, 700e-9, 10)
        intensity = multi_wavelength_intensity(
            theta, wavelength_range, slit_width, slit_distance
        )
    else:
        intensity = double_slit_intensity(
            theta, wavelength, slit_width, slit_distance
        )
    fig = intensity_plot(theta, intensity, wavelength_nm)
    heatmap = heatmap_pattern(intensity, wavelength_nm)

    animated_fig = animated_intensity(theta, np.roll(intensity, 200), intensity)

    st.plotly_chart(animated_fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(heatmap, use_container_width=True)

    if guided_mode:
        st.markdown("### 🎓 Guided Learning")

        st.info("Step 1: Observe bright and dark fringes")

        st.info("Step 2: Increase slit separation → fringes get closer")

        st.info("Step 3: Increase wavelength → fringes spread apart")

        st.info("Formula: y = λL / d")

    # --------------------------
    # Metrics
    # --------------------------

    st.subheader("📏 Extracted Physical Quantities")

    fringe = fringe_spacing(wavelength, screen_distance, slit_distance)
    angle = diffraction_angle(1, wavelength, slit_distance)

    col1, col2, col3 = st.columns(3)

    col1.metric("Wavelength", f"{wavelength_nm} nm")
    col2.metric("Fringe Spacing", f"{fringe*1000:.4f} mm")

    if angle:
        col3.metric("First Order Angle", f"{angle:.4f}°")

    # --------------------------
    # Fringe Orders
    # --------------------------

    st.subheader("📐 Fringe Orders")

    orders = fringe_orders(wavelength, slit_distance)

    for m, ang in orders:
        st.write(f"m = {m} → θ ≈ {ang:.4f}°")

    # --------------------------
    # Inverse Solver
    # --------------------------

    st.markdown("---")
    st.subheader("🧠 Inverse Solver (Parameter Estimation)")

    measured_spacing_mm = st.number_input(
        "Enter measured fringe spacing (mm)",
        min_value=0.01,
        max_value=50.0,
        value=5.0
    )

    measured_spacing = measured_spacing_mm / 1000

    estimated_d = estimate_slit_distance(
        wavelength,
        screen_distance,
        measured_spacing
    )

    if estimated_d is not None:
        st.success(f"Estimated Slit Separation: {estimated_d*1e6:.2f} µm")
    
    st.info("""
This demonstrates solving the inverse problem:
Given observed fringe pattern → estimate system parameters.
""")

    # --------------------------
    # Sensitivity Analysis
    # --------------------------

    st.markdown("---")
    st.subheader("📊 Sensitivity Analysis")

    wavelength_range = np.linspace(400e-9, 700e-9, 50)
    fringe_values = [
        fringe_spacing(w, screen_distance, slit_distance)
        for w in wavelength_range
    ]

    import plotly.graph_objects as go

    fig_sens = go.Figure()

    fig_sens.add_trace(go.Scatter(
        x=wavelength_range * 1e9,
        y=np.array(fringe_values) * 1000,
        mode="lines",
        name="Fringe Spacing"
    ))

    fig_sens.update_layout(
        title="Fringe Spacing vs Wavelength",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Fringe Spacing (mm)",
        template="plotly_dark"
    )

    st.plotly_chart(fig_sens, use_container_width=True)
# =====================================================
# DIFFRACTION GRATING
# =====================================================

elif experiment == "Diffraction Grating (2D)":

    slit_distance_um = st.sidebar.slider("Grating Spacing (µm)", 5, 50, 10)
    N = st.sidebar.slider("Number of Slits", 2, 50, 10)

    slit_distance = slit_distance_um * 1e-6

    intensity = diffraction_grating_intensity(
        theta, wavelength, slit_distance, N
    )

    fig = intensity_plot(theta, intensity, wavelength_nm)
    heatmap = heatmap_pattern(intensity, wavelength_nm)

    animated_fig = animated_intensity(theta, np.roll(intensity, 200), intensity)

    st.plotly_chart(animated_fig, use_container_width=True)
    st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(heatmap, use_container_width=True)

    if guided_mode:
        st.markdown("### 🎓 Guided Learning")

        st.info("Step 1: Observe sharp bright peaks")

        st.info("Step 2: Increase number of slits → peaks become sharper")

        st.info("Step 3: Higher order → better resolution")

        st.info("Formula: d sin(θ) = mλ")

    # Metrics
    st.subheader("📏 Extracted Physical Quantities")

    angle = diffraction_angle(1, wavelength, slit_distance)
    resolving = grating_resolving_power(1, N)

    col1, col2, col3 = st.columns(3)

    col1.metric("Wavelength", f"{wavelength_nm} nm")

    if angle:
        col2.metric("First Order Angle", f"{angle:.4f}°")

    col3.metric("Resolving Power", f"{resolving}")

    st.info("""
🔍 Increasing number of slits → sharper and narrower peaks  
🔍 Higher order → better spectral resolution  
🔍 Increasing grating spacing → peaks move closer  

Grating equation: d sin(θ) = mλ  
Resolving Power: R = mN
""")
    
# =====================================================
# 3D MODES
# =====================================================

elif experiment == "Single Slit Diffraction (3D)":

    slit_width_um = st.sidebar.slider("Slit Width (µm)", 5, 100, 20)
    slit_width = slit_width_um * 1e-6

    fig3d = single_slit_3d(theta, wavelength, slit_width)
    st.plotly_chart(fig3d, use_container_width=True, theme=None)

    if guided_mode:
        st.markdown("### 🎓 Guided Learning")

        st.info("Observe the central peak in 3D surface")

        st.info("Increase slit width → surface narrows")

        st.info("Increase wavelength → surface spreads")

    # --------------------------
    # FORMULA + PHYSICS
    # --------------------------

    st.markdown("### 📐 Governing Equation")

    st.latex(r"I(\theta) = I_0 \left(\frac{\sin \beta}{\beta}\right)^2")
    st.latex(r"\beta = \frac{\pi a \sin\theta}{\lambda}")

    st.info("""
    📌 The intensity pattern follows a sinc-squared distribution.

    • Central maximum at θ = 0  
    • First minima when β = ±π  

    👉 Increasing slit width → narrower peak  
    👉 Increasing wavelength → wider spread  
    """)
    st.success("""
    🎯 Why this matters:

    • Used in spectroscopy  
    • Helps design optical instruments  
    • Fundamental to laser physics  

    👉 This connects simulation to real-world physics
    """)


elif experiment == "Double Slit Interference (3D)":

    slit_width_um = st.sidebar.slider("Slit Width (µm)", 5, 100, 20)
    slit_distance_um = st.sidebar.slider("Slit Separation (µm)", 50, 500, 200)

    slit_width = slit_width_um * 1e-6
    slit_distance = slit_distance_um * 1e-6

    fig3d = double_slit_3d(theta, wavelength, slit_width, slit_distance)
    st.plotly_chart(fig3d, use_container_width=True, theme=None)

    if guided_mode:
        st.markdown("### 🎓 Guided Learning")

        st.info("Notice alternating peaks (constructive interference)")

        st.info("Increase slit separation → peaks get closer")

        st.info("Fringe pattern appears in 3D surface")

    # --------------------------
    # FORMULA + PHYSICS
    # --------------------------

    st.markdown("### 📐 Governing Equation")

    st.latex(r"I(\theta) = I_0 \cos^2\left(\frac{\pi d \sin\theta}{\lambda}\right)")
    st.latex(r"\times \left(\frac{\sin \beta}{\beta}\right)^2")

    st.info("""
    📌 Interference arises from phase difference between waves.

    • Constructive: d sinθ = mλ  
    • Destructive: d sinθ = (m + 1/2)λ  

    👉 Larger slit separation → closer fringes  
    👉 Larger wavelength → wider fringes  
    """)
    st.success("""
    🎯 Why this matters:

    • Used in spectroscopy  
    • Helps design optical instruments  
    • Fundamental to laser physics  

    👉 This connects simulation to real-world physics
    """)


elif experiment == "Diffraction Grating (3D)":

    slit_distance_um = st.sidebar.slider("Grating Spacing (µm)", 5, 50, 10)
    N = st.sidebar.slider("Number of Slits", 2, 50, 10)

    slit_distance = slit_distance_um * 1e-6

    fig3d = grating_3d(theta, wavelength, slit_distance, N)
    st.plotly_chart(fig3d, use_container_width=True, theme=None)

    if guided_mode:
        st.markdown("### 🎓 Guided Learning")

        st.info("Sharp peaks represent diffraction orders")

        st.info("Increase number of slits → peaks sharpen")

        st.info("Higher order → better resolution")
    # --------------------------
    # FORMULA + PHYSICS
    # --------------------------

    st.markdown("### 📐 Grating Equation")

    st.latex(r"d \sin\theta = m\lambda")
    st.latex(r"R = mN")

    st.info("""
    📌 Diffraction grating produces sharp spectral peaks.

    • Higher order (m) → better separation  
    • More slits (N) → sharper peaks  

    👉 Used in spectroscopy for wavelength analysis  
    """)

    st.success("""
    🎯 Why this matters:

    • Used in spectroscopy  
    • Helps design optical instruments  
    • Fundamental to laser physics  

    👉 This connects simulation to real-world physics
    """)
# =====================================================
# GLOBAL PHYSICS EXPLANATION
# =====================================================

st.markdown("---")

with st.expander("🧠 Physics Theory (Click to Expand)"):

    st.markdown("""
Diffraction and interference arise due to the **wave nature of light**.

• Waves passing through apertures spread and overlap  
• Constructive interference → bright fringes  
• Destructive interference → dark regions  

### General Condition:
d sin(θ) = mλ

### Key Concepts:
- Larger wavelength → wider spread  
- Smaller slit → more diffraction  
- More slits → sharper peaks  

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