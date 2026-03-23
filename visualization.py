import numpy as np
import plotly.graph_objects as go


# =====================================================
# 2D INTENSITY PLOT
# =====================================================

def intensity_plot(theta, intensity, wavelength_nm):

    theta_deg = np.degrees(theta)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=theta_deg,
            y=intensity,
            mode="lines",
            line=dict(width=3),
            name="Intensity"
        )
    )

    fig.add_vline(
        x=0,
        line_dash="dash",
        line_color="white"
    )

    fig.add_annotation(
        x=0,
        y=max(intensity),
        text="m = 0 (Central Maximum)",
        showarrow=True,
        arrowhead=2
    )

    fig.update_layout(
        title="Angular Diffraction Intensity Distribution",
        xaxis_title="Diffraction Angle (degrees)",
        yaxis_title="Normalized Intensity",
        template="plotly_dark",
        height=450
    )

    return fig


# =====================================================
# HEATMAP
# =====================================================

def heatmap_pattern(intensity, wavelength_nm):

    pattern = np.tile(intensity, (250, 1))

    fig = go.Figure(
        data=go.Heatmap(
            z=pattern,
            colorscale="Inferno",
            showscale=True
        )
    )

    fig.update_layout(
        title="Simulated Screen Diffraction Pattern",
        xaxis_title="Screen Position",
        yaxis_title="Screen Height",
        height=350
    )

    return fig


# =====================================================
# ANIMATION (FIXED)
# =====================================================

def animated_intensity(theta, intensity_start, intensity_end):

    theta_deg = np.degrees(theta)

    steps = 40
    frames = []

    y_max = max(np.max(intensity_start), np.max(intensity_end)) * 1.1
    x_min = np.min(theta_deg)
    x_max = np.max(theta_deg)

    for i in range(steps):
        alpha = i / (steps - 1)
        blended = (1 - alpha) * intensity_start + alpha * intensity_end

        frames.append(
            go.Frame(
                data=[
                    go.Scatter(
                        x=theta_deg,
                        y=blended,
                        mode="lines",
                        line=dict(width=3)
                    )
                ]
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter(
                x=theta_deg,
                y=intensity_start,
                mode="lines",
                line=dict(width=3),
                name="Intensity"
            )
        ],
        frames=frames
    )

    fig.update_layout(
        title="Animated Diffraction Pattern Evolution",
        xaxis_title="Diffraction Angle (degrees)",
        yaxis_title="Normalized Intensity",
        template="plotly_dark",
        height=600,
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[0, y_max]),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.5,                # center horizontally
                y=-0.2,               # move BELOW the graph
                xanchor="center",
                yanchor="top",
                buttons=[
                    dict(
                        label="▶ Play Animation",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {"duration": 40, "redraw": True},
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                                "mode": "immediate"
                            }
                        ],
                    ),
                    dict(
                        label="⏸ Pause",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate"
                            }
                        ],
                    )
                ],
            )
        ],
    )

    return fig


# =====================================================
# 🔥 3D SINGLE SLIT
# =====================================================

def single_slit_3d(theta, wavelength, slit_width):

    theta_small = np.linspace(theta.min(), theta.max(), 120)
    X, Y = np.meshgrid(theta_small, theta_small)

    beta = (np.pi * slit_width * np.sin(X)) / wavelength
    intensity = (np.sinc(beta / np.pi))**2

    # Normalize
    intensity = intensity / np.max(intensity)

    fig = go.Figure(
        data=[go.Surface(
            z=intensity,
            x=X,
            y=Y,
            colorscale="Turbo"
        )]
    )

    # 🎥 CAMERA ROTATION
    frames = []
    for angle in np.linspace(0, 2*np.pi, 60):
        frames.append(
            go.Frame(
                layout=dict(
                    scene=dict(
                        camera=dict(
                            eye=dict(
                                x=1.5*np.cos(angle),
                                y=1.5*np.sin(angle),
                                z=1.2
                            )
                        )
                    )
                )
            )
        )

    fig.frames = frames

    fig.update_layout(
        title="3D Single Slit Diffraction",
        template="plotly_dark",
        height=600,
        

        scene=dict(
            xaxis_title="Angle X",
            yaxis_title="Angle Y",
            zaxis_title="Intensity"
        ),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="▶ Rotate",
                        method="animate",
                        args=[None, {
                            "frame": {"duration": 120},
                            "transition": {"duration": 50}
                        }],
                    )
                ]
            )
        ]
    )
    return fig


# =====================================================
# 🔥 3D DOUBLE SLIT
# =====================================================

def double_slit_3d(theta, wavelength, slit_width, slit_distance):

    theta_small = np.linspace(theta.min(), theta.max(), 120)
    X, Y = np.meshgrid(theta_small, theta_small)
    beta = (np.pi * slit_width * np.sin(X)) / wavelength
    delta = (np.pi * slit_distance * np.sin(X)) / wavelength

    single = (np.sinc(beta / np.pi))**2
    interference = (np.cos(delta))**2

    intensity = single * interference

    # Normalize
    intensity = intensity / np.max(intensity)

    fig = go.Figure(
        data=[go.Surface(
            z=intensity,
            x=X,
            y=Y,
            colorscale="Turbo"
        )]
    )

    # 🎥 CAMERA ROTATION
    frames = []
    for angle in np.linspace(0, 2*np.pi, 60):
        frames.append(
            go.Frame(
                layout=dict(
                    scene=dict(
                        camera=dict(
                            eye=dict(
                                x=1.5*np.cos(angle),
                                y=1.5*np.sin(angle),
                                z=1.2
                            )
                        )
                    )
                )
            )
        )

    fig.frames = frames

    fig.update_layout(
        title="3D Double Slit Diffraction",
        template="plotly_dark",
        height=600,

        scene=dict(
            xaxis_title="Angle X",
            yaxis_title="Angle Y",
            zaxis_title="Intensity"
        ),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="▶ Rotate",
                        method="animate",
                        args=[None, {"frame": {"duration": 120}}],
                    )
                ]
            )
        ]
    )

    return fig


# =====================================================
# 🔥 3D DIFFRACTION GRATING
# =====================================================

def grating_3d(theta, wavelength, slit_distance, N):

    theta_small = np.linspace(theta.min(), theta.max(), 120)
    X, Y = np.meshgrid(theta_small, theta_small)

    delta = (np.pi * slit_distance * np.sin(X)) / wavelength

    numerator = np.sin(N * delta)
    denominator = np.sin(delta) + 1e-9  # avoid division by zero

    intensity = (numerator / denominator)**2

    # Normalize
    intensity = intensity / np.max(intensity)

    fig = go.Figure(
        data=[go.Surface(
            z=intensity,
            x=X,
            y=Y,
            colorscale="Turbo"
        )]
    )

    # 🎥 CAMERA ROTATION
    frames = []

    for angle in np.linspace(0, 2*np.pi, 60):
        frames.append(
            go.Frame(
                layout=dict(
                    scene=dict(
                        camera=dict(
                            eye=dict(
                                x=2*np.cos(angle),
                                y=2*np.sin(angle),
                                z=1.3  # 🔥 slightly higher = better view
                            )
                        )
                    )
                )
            )
        )

    fig.frames = frames

    fig.update_layout(
        title="3D Diffraction Grating",
        template="plotly_dark",
        height=600,

        scene=dict(
        xaxis_title="Angle X",
        yaxis_title="Angle Y",
        zaxis_title="Intensity",

        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.2),  # 🔥 balanced view
            center=dict(x=0, y=0, z=0)
        )
    ),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="▶ Rotate",
                        method="animate",
                        args=[None, {"frame": {"duration": 120}}],
                    )
                ]
            )
        ]
    )
    return fig