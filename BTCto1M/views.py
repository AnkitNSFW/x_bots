from django.shortcuts import redirect
from django.http import HttpResponse   
from dotenv import load_dotenv
import os
from .utils import *
from .models import BTCPost

load_dotenv()

def home(request):
    return redirect('https://x.com/BTCinMillion')

def cron_job_call_handler(request):
    secret = request.headers.get('Authorization', '')
    expected_secret = "Bearer "+os.getenv('CRON_SECRET')

    if secret != expected_secret:
        return HttpResponse('Unauthorized', status=401)



    global LAST_BTC_24hr_HIGH

    try:
        last_post = BTCPost.objects.latest('post_time')
        last_post_price = last_post.btc_price
    except BTCPost.DoesNotExist:
        last_post_price = 0
    
    last_price = max(LAST_BTC_24hr_HIGH, last_post_price)
    
    current_btc_24hr_high = btc_24h_high(api_key=os.getenv('CRYPTO_API_KEY'))
    current_btc_24hr_high_in_million = price_to_million(price=current_btc_24hr_high)
    LAST_BTC_24hr_HIGH = current_btc_24hr_high_in_million

    if current_btc_24hr_high_in_million > last_price:
        image_url = generate_progress_image(HCTI_API_ENDPOINT=os.getenv('HCTI_API_ENDPOINT'),
                                            HCTI_API_USER_ID=os.getenv('HCTI_API_USER_ID'),
                                            HCTI_API_KEY=os.getenv('HCTI_API_KEY'),
                                            current_btc_24hr_high_in_million=current_btc_24hr_high_in_million)

        if image_url:
            media_id = upload_image_to_X(CONSUMER_KEY=os.getenv('X_CONSUMER_KEY'),
                                        CONSUMER_SECRET=os.getenv('X_CONSUMER_SECRET'),
                                        ACCESS_TOKEN=os.getenv('X_ACCESS_TOKEN'),
                                        ACCESS_TOKEN_SECRET=os.getenv('X_ACCESS_TOKEN_SECRET'),
                                        image_url=image_url)
        else:
            return
        

        if media_id:
            tweet_metadata = upload_tweet_to_X(CONSUMER_KEY=os.getenv('X_CONSUMER_KEY'),
                                            CONSUMER_SECRET=os.getenv('X_CONSUMER_SECRET'),
                                            ACCESS_TOKEN=os.getenv('X_ACCESS_TOKEN'),
                                            ACCESS_TOKEN_SECRET=os.getenv('X_ACCESS_TOKEN_SECRET'),
                                            btc_price=current_btc_24hr_high_in_million,
                                            media_id=media_id)
        else:
            return
        

        if tweet_metadata:
            tweet_link = extract_tweet_link(tweet_metadata)
            
        
        BTCPost.objects.create(btc_price=current_btc_24hr_high_in_million,
                               image_link=image_url,
                               tweet_link=tweet_link)

    return HttpResponse('Task Succesfull', status=200)