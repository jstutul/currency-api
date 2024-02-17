from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apiapp.models import *
import json


def home(request):
    # Your JSON data
    data = {
        'status':True,
        'message': 'Welcome to currency api'
    }
    # Returning JSON response
    return JsonResponse(data)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CurrencyList, CurrentRate
import json

@csrf_exempt
def current_rate_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for entry in data:
                source_currency_name = entry.get('source')
                target_currency_name = entry.get('target')
                conversion_value = entry.get('value')
                time = entry.get('time')  # Extracting time from JSON data
                
                # Assuming CurrencyList model is already defined
                source_currency, _ = CurrencyList.objects.get_or_create(name=source_currency_name)
                target_currency, _ = CurrencyList.objects.get_or_create(name=target_currency_name)

                # Check if the conversion rate already exists in the database
                conversion_rate, created = CurrentRate.objects.get_or_create(
                    source=source_currency,
                    target=target_currency,
                    defaults={'value': conversion_value, 'time': time}  # Include time when creating new instance
                )
                if not created:
                    conversion_rate.value = conversion_value
                    conversion_rate.time = time  # Update time when conversion rate already exists
                    conversion_rate.save()
            return JsonResponse({'message': 'Data stored successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


# @csrf_exempt
# def insert_reviews_data(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             for item in data:
#                 name = item.get("Name")

#                 # Check if WebsiteList with the name already exists
#                 website, _ = WebsiteList.objects.get_or_create(name__iexact=name.lower())

#                 # Get or create ReviewsAndRatting object for the website
#                 reviews, created = ReviewsAndRatting.objects.get_or_create(name=website)

#                 if created:
#                     print("Created ReviewsAndRatting for:", name)
#                 else:
#                     print("Updated ReviewsAndRatting for:", name)
#                     # Update reviews and rating here if needed

#                 # Update or create ReviewsAndRatting instance
#                 if created:
#                     ReviewsAndRatting.objects.create(
#                         name=website,
#                         reviews=item.get("Reviews"),
#                         rating=item.get("Rating"),
#                         datetime=item.get("DateTime")
#                     )
#                 else:
#                     reviews.reviews = item.get("Reviews")
#                     reviews.rating = item.get("Rating")
#                     reviews.datetime = item.get("DateTime")
#                     reviews.save()

#             return JsonResponse({'message': 'Data processed successfully'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def insert_reviews_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                name = item.get("Name")

                # Check if WebsiteList with the name already exists
                website, created = WebsiteList.objects.get_or_create(name__iexact=name.lower())

                if not created:
                    # Get ReviewsAndRatting objects for the website
                    reviews_list = ReviewsAndRatting.objects.filter(name=website)

                    if reviews_list.exists():
                        # If there are existing reviews, update the first one
                        reviews = reviews_list.first()
                        print("Updated ReviewsAndRatting for:", name)
                    else:
                        # If no reviews exist, create a new one
                        reviews = ReviewsAndRatting(name=website)
                        print("Created ReviewsAndRatting for:", name)

                    # Update reviews and rating here if needed
                    reviews.reviews = item.get("Reviews")
                    reviews.rating = item.get("Rating")
                    reviews.datetime = item.get("DateTime")
                    reviews.save()
                else:
                    print("No WebsiteList instance found for name:", name)

            return JsonResponse({'message': 'Data processed successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    