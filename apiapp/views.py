from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apiapp.models import *
import json
import requests

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
                if WebsiteList.objects.filter(name__iexact=name.lower()).exists():
                    website = WebsiteList.objects.get(name__iexact=name.lower())
                    if website:
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



def current_rate(request):
    try:
        # Get the values from the URL parameters
        from_currency = request.GET.get('from')
        to_currency = request.GET.get('to')
        amount = float(request.GET.get('value', 0))  

        source_currency = CurrencyList.objects.get(name=from_currency)
        target_currency = CurrencyList.objects.get(name=to_currency)
        
        common_currency = CurrencyList.objects.get(name='USD')  
        rate_source_to_common = CurrentRate.objects.get(source=common_currency, target=source_currency)
        rate_common_to_target = CurrentRate.objects.get(source=common_currency, target=target_currency)
        # Calculate the converted amount
        source_to_usd = 1 / rate_source_to_common.value
        source_to_target = source_to_usd * rate_common_to_target.value

        return JsonResponse({'source':source_currency.name,'target':target_currency.name,'rate':source_to_target,'amount': source_to_target*amount}, status=200)
    except CurrencyList.DoesNotExist:
        return JsonResponse({'error': f"Currency not found"}, status=400)
    except CurrentRate.DoesNotExist:
        return JsonResponse({'error': f"Conversion rate not available for {from_currency} to {to_currency}"}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def getcompare(sc,tc,sa,mmr):
    source_currency = sc
    target_currency = tc
    send_amount = sa
    mid_market_rate = mmr

    url = f"https://api.wise.com/v3/comparisons?sourceCurrency={source_currency}&targetCurrency={target_currency}&sendAmount={send_amount}&midMarketRate={mid_market_rate}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()  # Return the JSON response as a Python dictionary
    else:
        return None


def c_compare(request):
    try:
        allowedweb_names = [obj.name for obj in WebsiteList.objects.all()]
        print(allowedweb_names)
        from_currency = request.GET.get('from')
        to_currency   = request.GET.get('to')
        currency   = request.GET.get('c')
        amount        = float(request.GET.get('value', 0))   
        rate          = float(request.GET.get('value', 0))   


        if from_currency == currency:
            api_response = getcompare(from_currency, to_currency, amount, rate)
            # allowedweb_names = ['wise', 'xe', 'remitly', 'ofx', 'revolut', 'paypal']
            api_provider_names = [provider['name'].lower() for provider in api_response['providers']]
            allowedweb_names_lower = [name.lower() for name in allowedweb_names]
            filtered_providers = [provider for provider in api_response["providers"] if provider.get('name').lower() in allowedweb_names_lower]

            # Print the filtered providers
            # print("Filtered providers:", filtered_providers)

            for i in filtered_providers:
                print(i.get("name"),i.get("quotes")[0]["rate"],i.get("receivedAmount"),i.get("markup"))
            return JsonResponse({'success': '2', },status=400)   
        else:
            pass
        return JsonResponse({'success': '1', },status=400)    
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)    