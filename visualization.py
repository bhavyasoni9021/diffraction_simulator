import numpy as np
import plotly.graph_objects as go


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

    # Central maximum marker
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

def animated_intensity(theta, intensity_start, intensity_end):
    """
    Smooth transition animation between two intensity patterns
    """

    theta_deg = np.degrees(theta)

    steps = 40
    frames = []

    # 🔥 CRITICAL FIX: lock axis ranges
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
        height=450,

        # 🔥 THIS FIXES YOUR PROBLEM
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[0, y_max]),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.1,
                y=1.15,
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