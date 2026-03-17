import random, time, numpy as np, ctypes, pygetwindow as gw, cv2

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
PW_RENDERFULLCONTENT = 0x00000002

WM_KEYDOWN, WM_KEYUP = 0x0100, 0x0101
PostMessage = ctypes.windll.user32.PostMessageW
KEY_MAP = {f'{i}': 0x30+i for i in range(1, 10)}

def captureWindow(hwnd):
    try:
        l, t, r, b = user32.GetWindowRect(hwnd)
        w, h = r - l, b - t
        hdc = user32.GetWindowDC(hwnd)
        mfc = gdi32.CreateCompatibleDC(hdc)
        bmp = gdi32.CreateCompatibleBitmap(hdc, w, h)
        gdi32.SelectObject(mfc, bmp)
        user32.PrintWindow(hwnd, mfc, PW_RENDERFULLCONTENT or 0)
        buf = ctypes.create_string_buffer(w * h * 4)
        gdi32.GetBitmapBits(bmp, w * h * 4, buf)
        gdi32.DeleteObject(bmp); gdi32.DeleteDC(mfc); user32.ReleaseDC(hwnd, hdc)
        img = np.frombuffer(buf, dtype=np.uint8).reshape((h, w, 4))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    except: return None

def findWin(title):
    try: return [{'handle': w._hWnd} for w in gw.getWindowsWithTitle(title)]
    except: return []

def sendKey(hwnd, key):
    vk = KEY_MAP.get(str(key), key)
    PostMessage(hwnd, WM_KEYDOWN, vk, 0x00000001 | (0x00000001 << 30))
    time.sleep(random.uniform(0.05, 0.09))
    PostMessage(hwnd, WM_KEYUP, vk, 0x00000001 | (0x00000003 << 30) | (0x1 << 31))

def getColors(img, y, x, w, h):
    return [tuple(int(c) for c in img[y][px]) for px in [x-5, x, x+5] if 0 <= px < w]

def getColor(img, y, x, h, w):
    return tuple(int(c) for c in img[y][x]) if 0 <= y < h and 0 <= x < w else None

def matchColor(c1, c2, tol=50):
    if not c1 or not c2: return False
    return all(all(abs(a-b) <= tol for a, b in zip(x, y)) for x, y in zip(c1, c2))

def isGreen(c, tol=30):
    return bool(c and c[1] > c[0] + tol and c[1] > c[2] + tol)

def isRed(c, tol=30):
    return bool(c and c[0] > c[1] + tol and c[0] > c[2] + tol)

def main():
    windows = findWin("魔兽世界")
    if not windows: print('未找到窗口'); return
    hwnd = windows[0]['handle']
    
    statusX, statusY = 18, 50
    sX, eX, sY, tX = 853, 1493, 1545, 1610
    
    cL, cT = min(statusX, sX), min(statusY, sY)
    cR, cB = max(statusX+1, tX+10, eX+10), max(statusY+1, sY+10)
    
    lSX, lSY = statusX - cL, statusY - cT
    lEX, lEY = eX - cL, sY - cT
    lTX = tX - cL
    
    print(f"区域: {cL},{cT}->{cR},{cB} | Ctrl+C停止\n")
    
    while True:
        img = captureWindow(hwnd)
        if img is None: time.sleep(0.1); continue
        h, w = img.shape[:2]
        
        c = getColor(img, int(lSY), int(lSX), h, w)
        if c:
            if isGreen(c): time.sleep(random.uniform(0.15, 0.3)); continue
            elif isRed(c):
                t = getColors(img, int(lEY), int(lTX), w, h)
                for x in range(int(lSX), int(lEX)+1):
                    if matchColor(getColors(img, int(lEY), x, w, h), t, 10):
                        k = max(1, min(9, (x-int(lSX))//71 + 1))
                        sendKey(hwnd, k); break
        time.sleep(random.uniform(0.15, 0.3))

if __name__ == "__main__": main()
