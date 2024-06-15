import requests

font_name = 'NotoSansDevanagari-Regular'
version = '1'
text = 'नेपाल'
url = f'http://localhost:3000/{font_name}/{version}/{text}'

print('url', url)

response = requests.get(url)

print('status code', response.status_code)

if response.status_code == 200:
    for c in response.text:
        print(ord(c))
else:
    print(response.text)
