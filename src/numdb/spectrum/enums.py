from enum import Enum


class Spectrum(Enum):
    ABSORBANCE = 1
    AB = 1
    TRANSMITTANCE = 2
    TR = 2
    RAMAN = 3
    RM = 3

    SAMPLE_INTENSITY = 9
    SM = 9
    SAMPLE_INTERFEROGRAM = 10
    IGSM = 10
    SAMPLE_PHASE = 11
    PHSM = 11

    REFERENCE_INTENSITY = 17
    RF = 17
    REFERENCE_INTERFEROGRAM = 18
    IGRF = 18
    REFERENCE_PHASE = 19
    PHRF = 19


class XAxisType(Enum):
    Unknown = 0
    Wavelength_m = 0
    Wavelength_dm = -1
    Wavelength_cm = -2
    Wavelength_mm = -3
    Wavelength_um = -6
    Wavelength_nm = -9
    Wavelength_pm = -12

    Wavenumber_m = 100
    Wavenumber_dm = 100 - 1
    Wavenumber_cm = 100 - 2
    Wavenumber_mm = 100 - 3
    Wavenumber_um = 100 - 6
    Wavenumber_nm = 100 - 9
    Wavenumber_pm = 100 - 12
