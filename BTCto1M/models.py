from django.db import models

class BTCPost(models.Model):
    btc_price = models.FloatField()
    post_time = models.DateTimeField(auto_now_add=True)
    image_link = models.URLField(max_length=100)
    tweet_link = models.URLField(max_length=100)

    def __str__(self):
        return f"{self.btc_price} - {self.post_time}\n{self.link}\n{self.tweet_link}"