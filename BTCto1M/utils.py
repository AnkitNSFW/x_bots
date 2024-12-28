import requests, json, re
from requests_oauthlib import OAuth1

LAST_BTC_24hr_HIGH = 0


price_to_million = lambda price: (price//1_000)/1_000

def btc_24h_high(api_key):
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin'
    params = {
    'vs_currency': 'usd',
    'ids': 'bitcoin'
    }
    headers = {
        'x_cg_demo_api_key': api_key
    }

    raw_data = requests.get(url, headers=headers)
    print(raw_data.content)

    result = [json.loads(line) for line in raw_data.content.decode("utf-8").strip().split("\n")]
    return  result[0][0]["high_24h"]

def generate_progress_image(HCTI_API_ENDPOINT: str, 
                            HCTI_API_USER_ID: str,
                            HCTI_API_KEY: str,
                            btc_price: float):
    data = { 'html': f'''
        <script src="https://cdn.tailwindcss.com"></script>
        <div class="bg-white text-center h-[200px] w-[778px] p-[10px]">
            <div class="relative h-[158px] w-[758px] bg-black border-4 border-black">
                <span class="absolute inset-0 flex text- text-4xl text-white items-center justify-center z-10">
                    ${price_to_million(price=btc_price)}M
                </span>
                <div class="bg-[#F2A900] h-[150px] w-[{(btc_price/1_000_000)*750}px]">
                </div>
            </div>
            <div class="text-right mt-1">
                <span class="text-gray-500 ">@BTCinMillion</span>
            </div>
        </div>
    '''}

    image_response = requests.post(url = HCTI_API_ENDPOINT, 
                          data = data, 
                          auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    if image_response.status_code == 200:
        return image_response.json()['url']
    return False

def upload_image_to_X(CONSUMER_KEY: str, 
                      CONSUMER_SECRET: str,
                      ACCESS_TOKEN: str, 
                      ACCESS_TOKEN_SECRET: str,
                      image_url: str):
    
    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    url = "https://upload.twitter.com/1.1/media/upload.json"
    params = {"media_category": "tweet_image"}

    image_response = requests.get(image_url)
    files = {"media": image_response.content}

    response = requests.post(url, params=params, files=files, auth=auth)

    return response.json().get("media_id_string") if response.status_code == 200 else False

def upload_tweet_to_X(CONSUMER_KEY: str, 
                      CONSUMER_SECRET: str,
                      ACCESS_TOKEN: str, 
                      ACCESS_TOKEN_SECRET: str,
                      btc_price: float,
                      media_id: str):
    url = "https://api.twitter.com/2/tweets"
    
    payload = {
        "text": f"🚀 Bitcoin hits ${btc_price:,}",
        "media": {
            "media_ids": [media_id]
        }
    }

    auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    response = requests.post(url, json=payload, auth=auth,)
    
    # Using code 201 because that what is return on successful tweet
    if response.status_code == 201:
        return response.json()['data']['text']
    return False

extract_tweet_link = lambda tweet: re.search(r'https?://\S+$', tweet).group()