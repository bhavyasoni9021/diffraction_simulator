def wavelength_color(wavelength_nm):

    if wavelength_nm < 450:
        return "violet"
    elif wavelength_nm < 495:
        return "blue"
    elif wavelength_nm < 570:
        return "green"
    elif wavelength_nm < 590:
        return "yellow"
    elif wavelength_nm < 620:
        return "orange"
    else:
        return "red"