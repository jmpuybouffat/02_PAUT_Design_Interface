import numpy as np
import numpy as np
from scipy.optimize import brentq

def interface_func(x, cr, df, dp, dpf):
    """Équation de Snell-Descartes"""
    return x / np.sqrt(x**2 + dp**2) - cr * (dpf - x) / np.sqrt((dpf - x)**2 + df**2)

def ferrari2(cr, DF, DT, DX):
    """Résolution exacte Snell-Descartes 3D (Moteur de Ferrari)"""
    if abs(cr - 1) < 1e-6:
        return DX * DT / (DF + DT)
    try:
        a, b = (0, DX) if DX >= 0 else (DX, 0)
        return brentq(interface_func, a, b, args=(cr, DF, DT, DX))
    except:
        return DX * DT / (DF + DT)

def discrete_windows(M, window_type='rect'):
    """Apodisation (Code 4)"""
    if M <= 1: return np.ones(1)
    m = np.arange(M)
    if window_type == 'Han': return (np.sin(np.pi * m / (M - 1)))**2
    if window_type == 'Ham': return 0.54 - 0.46 * np.cos(2 * np.pi * m / (M - 1))
    return np.ones(M)

