from django.db import models

class CurrencyList(models.Model):
    name = models.CharField(max_length=100, blank=False)
    icon = models.CharField(max_length=100, blank=False)
    activate = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CurrentRate(models.Model):
    source = models.ForeignKey(CurrencyList, on_delete=models.CASCADE, related_name='source_rates')
    target = models.ForeignKey(CurrencyList, on_delete=models.CASCADE, related_name='target_rates')
    value = models.FloatField(default=0.00)
    time = models.CharField(max_length=50)
    datetime= models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source.name} to {self.target.name}"

    @staticmethod
    def get_conversion_rate(source_currency, target_currency):
        try:
            conversion_rate = CurrentRate.objects.get(
                source__name=source_currency,
                target__name=target_currency
            ).value
            return conversion_rate
        except CurrentRate.DoesNotExist:
            return None
        

class WebsiteList(models.Model):
    name=models.CharField(blank=False,max_length=100)
    fullname=models.CharField(max_length=200,blank=False)
    title=models.CharField(max_length=1000,blank=False)
    logo=models.ImageField(upload_to="WebsiteLogo",blank=False)
    max=models.CharField(blank=False,max_length=1000)        
    min=models.CharField(blank=False,max_length=1000)        
    sendby=models.CharField(blank=False,max_length=1000)        
    receiveby=models.CharField(blank=False,max_length=1000)        
    receiveby=models.CharField(blank=False,max_length=1000) 
    security=models.CharField(blank=False,max_length=1000)
    support=models.CharField(blank=False,max_length=1000)
    offer=models.CharField(blank=False,max_length=1000)
    offer=models.CharField(blank=False,max_length=1000)
    sendmoneyprocess=models.TextField(blank=False)
    fullreviewlink=models.CharField(blank=False,max_length=1000)

    def __str__(self):
        return self.name
    

class ReviewsAndRatting(models.Model):
    name=models.ForeignKey(WebsiteList,on_delete=models.CASCADE)
    reviews=models.CharField(max_length=100,blank=False)
    rating=models.CharField(max_length=100,blank=False)
    datetime=models.CharField(max_length=100,blank=False)


    def __str__(self):
        return self.name.fullname