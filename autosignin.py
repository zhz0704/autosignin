import time
import keyboard as kb
import pyperclip
import ctypes
import pygetwindow as gw
import mouse
import argparse


SW_MINIMIZE = 6
SW_MAXIMIZE = 3
SW_HIDE = 0
SW_SHOW = 5
SW_RESTORE = 9

# SetWindowPos constants:
HWND_TOP = 0

# Window Message constants:
WM_CLOSE = 0x0010

delay_modifier = 0


def send(key: str, times=1, delay=0):
    for _ in range(times):
        kb.send(key)
        sleep(delay * delay_modifier)

def write(s: str):
    for c in s:
        send(c, 1, 0.05)

def sleep(t):
    time.sleep(t * delay_modifier)

def get_edge():
    t = time.time()
    while time.time() - t < 10:
        all_windows = gw.getAllWindows()
        for w in all_windows:
            title = str(w.title)
            # print(title)
            words = ['New', 'tab', 'Microsoft', 'Edge']
            if all([w in title for w in words]):
                return w
    return None
    
def tab_enter(count: int, delay=0):
    send('tab', count, delay)
    send('enter', 1, delay)

def shift_tab_enter(count: int, delay=0):
    kb.press('shift')
    send('tab', count, delay)
    kb.release('shift')
    send('enter', 1, delay)

def main():
    original = pyperclip.paste()
    # open edge
    send('win', 1, 1)
    pyperclip.copy('Microsoft Edge')
    send('ctrl+v', 1, 0.5)
    send('enter')

    # wait for the window to open
    edge = get_edge()
    if edge is None:
        print('Edge not found')
        exit()
    
    edge = gw.Win32Window(edge._hWnd)
    ctypes.windll.user32.SetForegroundWindow(edge._hWnd)
    # maximize the window
    edge.maximize()
    sleep(0.5)

    # go to the website
    pyperclip.copy('https://duty21.microsoftintern.com/')
    send('ctrl+v', 1, 0.5)
    send('enter')
    pyperclip.copy(original)
    sleep(1)

    # 登入
    tab_enter(2, 0.05)
    sleep(1)

    # TODO 新增今日班表
    tab_enter(3, 0.05)
    edge.restore()
    edge.moveTo(0, 0)
    edge.resizeTo(650, 650)
    sleep(0.5)

    # set zoom to 100%
    kb.press('ctrl')
    send('-', 7)
    send('=', 7)
    kb.release('ctrl')

    # 班表 end
    return
    shift_tab_enter(2, 0.05)
    sleep(0.5)
    tab_enter(2, 0.05)


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Sign in')
    parser.add_argument('-d', '--delay-modifier', type=float, default=1, help='Multiply the delay between key presses by this value.')
    args = parser.parse_args()
    delay_modifier = args.delay_modifier
    main()