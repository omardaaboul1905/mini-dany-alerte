import json, os, sys, time, urllib.request

PRODUCT = "https://gerarddarel.com/products/sac-mini-dany_425"
TOPIC = os.environ.get("NTFY_TOPIC", "")
UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def in_stock():
    try:
        data = json.loads(get(PRODUCT + ".js"))
        return any(v.get("available") for v in data.get("variants", []))
    except Exception as e:
        print("JSON KO:", e, file=sys.stderr)
    try:
        html = get(PRODUCT).lower()
        if "produit épuisé" in html or "out of stock" in html:
            return False
        if "ajouter au panier" in html or "add to cart" in html:
            return True
    except Exception as e:
        print("HTML KO:", e, file=sys.stderr)
    return None


def notify(title, msg):
    if not TOPIC:
        print("NTFY_TOPIC manquant")
        return
    req = urllib.request.Request(
        "https://ntfy.sh/" + TOPIC,
        data=msg.encode("utf-8"),
        headers={"Title": title, "Click": PRODUCT, "Priority": "urgent", "Tags": "handbag,rotating_light"},
    )
    urllib.request.urlopen(req, timeout=20)


state = in_stock()
print(time.strftime("%H:%M:%S"), "stock =", state)
if state :
    notify("MINI DANY EN STOCK", "Le sac est dispo, fonce : " + PRODUCT)
