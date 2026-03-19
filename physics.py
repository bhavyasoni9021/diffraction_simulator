import numpy as np


def single_slit_intensity(theta, wavelength, slit_width):
    """
    Single slit diffraction intensity.
    I = (sin(beta)/beta)^2
    beta = (pi * a * sin(theta)) / lambda
    """

    beta = (np.pi * slit_width * np.sin(theta)) / wavelength

    beta[beta == 0] = 1e-10

    intensity = (np.sin(beta) / beta) ** 2

    return intensity


def double_slit_intensity(theta, wavelength, slit_width, slit_distance):
    """
    Double slit interference with diffraction envelope
    """

    beta = (np.pi * slit_width * np.sin(theta)) / wavelength
    delta = (np.pi * slit_distance * np.sin(theta)) / wavelength

    beta[beta == 0] = 1e-10

    envelope = (np.sin(beta) / beta) ** 2
    interference = np.cos(delta) ** 2

    intensity = envelope * interference

    return intensity


def diffraction_grating_intensity(theta, wavelength, slit_distance, N):
    """
    Diffraction grating intensity
    """

    alpha = (np.pi * slit_distance * np.sin(theta)) / wavelength

    alpha[alpha == 0] = 1e-10

    intensity = (np.sin(N * alpha) / np.sin(alpha)) ** 2

    intensity = intensity / np.max(intensity)

    return intensity


def diffraction_angle(order, wavelength, slit_distance):
    """
    d sin(theta) = m lambda
    """

    value = order * wavelength / slit_distance

    if abs(value) > 1:
        return None

    theta = np.arcsin(value)

    return np.degrees(theta)


def resolution_limit(wavelength, slit_width):
    """
    theta = lambda / a
    """

    theta = wavelength / slit_width

    return np.degrees(theta)


def grating_resolving_power(order, N):
    """
    R = mN
    """

    return order * N


def fringe_spacing(wavelength, screen_distance, slit_distance):
    """
    fringe spacing y = lambda L / d
    """

    return (wavelength * screen_distance) / slit_distance


def fringe_orders(wavelength, slit_distance, max_order=3):

    orders = []

    for m in range(-max_order, max_order + 1):

        value = m * wavelength / slit_distance

        if abs(value) <= 1:
            theta = np.arcsin(value)
            orders.append((m, np.degrees(theta)))

    return orders