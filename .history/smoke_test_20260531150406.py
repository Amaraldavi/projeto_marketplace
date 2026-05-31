import urllib.request, urllib.error, time
urls = [
    "http://127.0.0.1:8000/trocas/",
    "http://127.0.0.1:8000/trocas/1/",
    "http://127.0.0.1:8000/trocas/1/checkout/",
    "http://127.0.0.1:8000/login/",
    "http://127.0.0.1:8000/register/",
]

# wait a bit for server to start
for i in range(10):
    try:
        urllib.request.urlopen("http://127.0.0.1:8000/", timeout=2)
        break
    except Exception:
        time.sleep(0.5)

for u in urls:
    try:
        r = urllib.request.urlopen(u, timeout=5)
        status = r.getcode()
        body = r.read(400).decode('utf-8', 'replace')
        print(f"{u} -> {status}")
        print(body[:300])
    except Exception as e:
        print(f"{u} -> ERROR: {e}")
