import ctypes
import winreg

DWORD = ctypes.c_uint32
BOOL = ctypes.c_uint32
Dwmapi = ctypes.windll.LoadLibrary('Dwmapi.dll')


def getColorizationColor():
    pcrColorization = DWORD()
    pfOpaqueBlend = BOOL()
    result = Dwmapi.DwmGetColorizationColor(
        ctypes.byref(pcrColorization),
        ctypes.byref(pfOpaqueBlend))
    if result == 0:
        color = pcrColorization.value
        b = color & 0xff
        g = color >> 8 & 0xff
        r = color >> 16 & 0xff
        a = color >> 24 & 0xff
        return [a, r, g, b]
    else:
        return [0, 0, 0, 0]

# struct ColorizationParameters
#  COLORREF ColorizationColor
#  COLORREF ColorizationAfterglow
#  UINT     ColorizationColorBalance // 0-100
#  UINT     ColorizationAfterglowBalance
#  UINT     ColorizationBlurBalance
#  BOOL     EnableWindowColorization
#  UINT     ColorizationGlassAttribute

def setColorizationColor(r, g, b):
    # win10 always use RGB
    RGB = b + (g << 8) + (r << 16)
    # BGR = r + (g << 8) + (b << 16)

    # AccentColor should be changed first
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         'SOFTWARE\\Microsoft\\Windows\\DWM',
                         0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, 'AccentColor', 0, winreg.REG_DWORD, RGB + 0xff000000)

    t = ctypes.c_uint32 * 7
    p = t()
    Dwmapi.DwmpGetColorizationParameters(ctypes.byref(p))

    p[0] = RGB + 0xff000000
    p[1] = RGB + 0xc4000000
    p[2] = 100
    p[3] = 100
    p[4] = 1
    p[5] = 1
    p[6] = 1
    result = Dwmapi.DwmpSetColorizationParameters(
        ctypes.byref(p),
        BOOL(0))
    return result == 0
