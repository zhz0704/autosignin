import time
import keyboard as kb
import pyperclip
import ctypes
import pygetwindow as gw
import argparse
from datetime import datetime

SW_MINIMIZE = 6
SW_MAXIMIZE = 3
SW_HIDE = 0
SW_SHOW = 5
SW_RESTORE = 9

# SetWindowPos constants:
HWND_TOP = 0

# Window Message constants:
WM_CLOSE = 0x0010

speed = 1


def send(key: str, times=1, delay=0):
    for _ in range(times):
        kb.send(key)
        sleep(delay)

def write(s: str):
    for c in s:
        send(c, 1, 0.05)

def sleep(t):
    time.sleep(t / speed)

def get_edge():
    t = time.time()
    while time.time() - t < 5:
        all_windows = gw.getAllWindows()
        for w in all_windows:
            title = str(w.title)
            # print(title)
            words = ['New', 'tab', 'Microsoft', 'Edge']
            if all([w in title for w in words]):
                return w
            
            words = ['新索引標籤', 'Microsoft', 'Edge']
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
    send('win', 1, 0.5)
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
    sleep(1)

    # 登入
    tab_enter(2, 0.01)
    sleep(0.5)

    # 去新增班表頁面
    tab_enter(3, 0.01)
    sleep(0.5)

    # get html source
    send('ctrl+u', 1, 0.5)
    send('ctrl+a', 1, 0.1)
    send('ctrl+c', 1, 0.1)
    send('ctrl+w', 1, 0.05)

    # parse token
    html = pyperclip.paste()
    # print(html)
    for line in html.split('\n'):
        if '_token' in line:
            token = line.split('value="')[1].split('"')[0]
        elif '/user/' in line:
            userid = line.split('/user/')[1].split('/')[0]
    print('userid:', userid)
    print('token:', token)

    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')

    print(formatted_date)

    # js code
    js = '''
    fetch('https://duty21.microsoftintern.com/user/%s/duty', {
        method: 'POST', // Specify the method
        headers: {
        'Content-Type': 'application/x-www-form-urlencoded' // Specify the content type
        },
        body: new URLSearchParams({
        _token: '%s',
        date: '%s',
        type: 'A'
        }) // Format the payload as URL-encoded
    })
    .then(response => {
        // Log the status and headers
        console.log('Status:', response.status);
        console.log('Headers:', response.headers);

        console.log('data:', response.text().then(text => {
            // console.log(text);
        }))
    })
    .catch(error => console.error('Error:', error)); // Handle any errors
    ''' % (userid, token, formatted_date)

    # open console
    send('ctrl+shift+j', 1, 0.5)
    # kb.write('allow pasting')
    # time.sleep(0.1)
    # send('enter', 1, 0.1)
    pyperclip.copy(js)
    send('ctrl+v', 1, 0.1)
    send('enter', 1, 0.5)
    send('ctrl+shift+j', 1, 0.1)
    tab_enter(1, 0.05)
    sleep(0.5)
    # 簽到
    shift_tab_enter(2, 0.05)
    sleep(0.5)
    tab_enter(2, 0.05)

    pyperclip.copy(original)


    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Sign in')
    parser.add_argument('-s', '--speed', type=float, default=1, help='The speed of the script.')
    args = parser.parse_args()
    speed = args.speed
    speed *= 0.5
    main()