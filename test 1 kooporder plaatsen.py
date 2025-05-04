import requests

# Vul hier je API-sleutels in
client_id = '3E9AgJj9'
client_secret = 'SW-P4YDsBO6KsGwo-YHh9xUu5g1Gr0iAoDGTp_HgXis'

def authenticate(client_id, client_secret):
    url = 'https://www.deribit.com/api/v2/public/auth'
    params = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.get(url, params=params)
    data = response.json()
    if 'result' in data:
        return data['result']['access_token']
    else:
        raise Exception(f"❌ Authenticatie mislukt: {data}")

def place_spot_order(access_token):
    url = 'https://www.deribit.com/api/v2/private/buy'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'instrument_name': 'BTC_USDC',
        'amount': 0.0001,
        'type': 'limit',
        'price': 66666,
        'post_only': 'true'  # ✅ als string (kleine letters)
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'result' in data:
        order = data['result']['order']
        print("✅ Spot order succesvol geplaatst:")
        print(f"  Order ID: {order['order_id']}")
        print(f"  Status: {order['order_state']}")
        print(f"  Prijs: {order['price']}")
        print(f"  Hoeveelheid BTC: {order['amount']}")
    else:
        print(f"❌ Fout bij order plaatsen: {data}")

# Uitvoeren
access_token = authenticate(client_id, client_secret)
place_spot_order(access_token)

