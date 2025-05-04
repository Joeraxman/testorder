import requests
import logging

# Logging instellen voor Azure
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info("✅ Authenticatie geslaagd.")
        return data['result']['access_token']
    else:
        logger.error(f"❌ Authenticatie mislukt: {data}")
        raise Exception("Authenticatie mislukt.")

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
        'post_only': 'true'
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if 'result' in data:
        order = data['result']['order']
        logger.info("✅ Spot order succesvol geplaatst:")
        logger.info(f"  Order ID: {order['order_id']}")
        logger.info(f"  Status: {order['order_state']}")
        logger.info(f"  Prijs: {order['price']}")
        logger.info(f"  Hoeveelheid BTC: {order['amount']}")
    else:
        logger.error(f"❌ Fout bij order plaatsen: {data}")

if __name__ == "__main__":
    try:
        access_token = authenticate(client_id, client_secret)
        place_spot_order(access_token)
    except Exception as e:
        logger.exception(f"⚠️ Fout tijdens scriptuitvoering: {e}")
