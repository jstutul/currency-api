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
                        # print(item.get("Url"))
                        # Update reviews and rating here if needed
                        reviews.reviews = item.get("Reviews")
                        reviews.rating = item.get("Rating")
                        reviews.url = 'https://www.trustpilot.com/review/'+item.get("Url")
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

        allowedweb_names = [obj.name for obj in WebsiteList.objects.all()]
        
        data=[]
        for i in allowedweb_names:
            obj = WebsiteList.objects.get(name=i.lower())
            domain_url = request.build_absolute_uri('/')
            listdata={
                'name':obj.name,
                'fullname':obj.fullname,
                'title':obj.title,
                'logo':domain_url+obj.logo.url,
                'max':obj.max,      
                'min':obj.min, 
                'sendby':obj.sendby,    
                'receiveby':obj.receiveby,      
                'receiveby':obj.receiveby,
                'security':obj.security,
                'support':obj.support,
                'offer':obj.offer,
                'sendmoneyprocess':obj.sendmoneyprocess,
                'fullreviewlink':obj.fullreviewlink,
                'reviews':ReviewsAndRatting.objects.get(name=obj).reviews,
                'ratting':ReviewsAndRatting.objects.get(name=obj).rating,
                'reviewurl':ReviewsAndRatting.objects.get(name=obj).url,
                'sendurl':obj.sendUrl
            }
            data.append(listdata)    

        return JsonResponse({'source':source_currency.name,'target':target_currency.name,'rate':source_to_target,'amount': source_to_target*amount,'data':data}, status=200)
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
    

def parse_duration_to_days(duration_str):
    print(duration_str)
    total_hours=duration_str.split('.')[0].split('H')[0].split('S')[0].split('PT')[1]
    print(total_hours)
    days = int(int(total_hours) / 24)
    if days <= 1:
        return 0
    else:
        return days
    

# Combined function to format duration
def format_duration(duration):
    if duration:
        # print(duration['min'].split(".")[0])
        min_duration = parse_duration_to_days(duration['min'])
        max_duration = parse_duration_to_days(duration['max'])
        return f"{min_duration}-{max_duration} Days"
    else:
        return "0-0 Days"
    

def c_compare(request):
    allowedweb_names = [obj.name for obj in WebsiteList.objects.all()]
        # print(allowedweb_names)
    from_currency = request.GET.get('from')
    to_currency   = request.GET.get('to')
    currency   = request.GET.get('c')
    amount        = float(request.GET.get('value', 0))   
    rate          = float(request.GET.get('rate', 0))   
    
    symbol="USD",
    if currency==from_currency:
        symbol=from_currency
    else:    
        symbol=from_currency
    api_response = getcompare(from_currency, to_currency, amount, rate)
        # allowedweb_names = ['wise', 'xe', 'remitly', 'ofx', 'revolut', 'paypal']
    api_provider_names = [provider['name'].lower() for provider in api_response['providers']]
    allowedweb_names_lower = [name.lower() for name in allowedweb_names]
    filtered_providers = [provider for provider in api_response["providers"] if provider.get('name').lower() in allowedweb_names_lower]
    # print(allowedweb_names_lower)
    # print("tutul=",api_response)
    # Print the filtered providers
    # print("Filtered providers:", filtered_providers)
    data=[]
    for i in filtered_providers:
        # print(i.get("quotes"))
        name =i.get("name")
        fee =i.get("quotes")[0]["fee"]
        receivedAmount =i.get("quotes")[0]["receivedAmount"]
        rate=i.get("quotes")[0]["rate"]
        duration = format_duration(i.get("quotes")[0]['deliveryEstimation']['duration'])
        obj = WebsiteList.objects.get(name=name.lower())
        # print(name,fee,receivedAmount,rate,duration,obj)
        domain_url = request.build_absolute_uri('/')
        # print(name.lower())
        listdata={
            'name':obj.name,
            'fullname':obj.fullname,
            'title':obj.title,
            'logo':domain_url+obj.logo.url,
            'max':obj.max,      
            'min':obj.min, 
            'sendby':obj.sendby,    
            'receiveby':obj.receiveby,      
            'receiveby':obj.receiveby,
            'security':obj.security,
            'support':obj.support,
            'offer':obj.offer,
            'sendmoneyprocess':obj.sendmoneyprocess,
            'fullreviewlink':obj.fullreviewlink,
            'reviews':ReviewsAndRatting.objects.get(name=obj).reviews,
            'ratting':ReviewsAndRatting.objects.get(name=obj).rating,
            'reviewurl':ReviewsAndRatting.objects.get(name=obj).url,
            'rate':'{:.4f}'.format(rate),
            'fees':fee,
            'duration':duration,
            'receivedAmount':receivedAmount,
            'symbol':symbol
        }
        # print(listdata)
       
        data.append(listdata)
        # print(name,fee,receivedAmount,rate,duration)
    # print(data)    
    sorted_data = sorted(data, key=lambda x: x['rate'], reverse=True)

    return JsonResponse({'data': sorted_data, },status=200) 
    # try:
    #     allowedweb_names = [obj.name for obj in WebsiteList.objects.all()]
    #     # print(allowedweb_names)
    #     from_currency = request.GET.get('from')
    #     to_currency   = request.GET.get('to')
    #     currency   = request.GET.get('c')
    #     amount        = float(request.GET.get('value', 0))   
    #     rate          = float(request.GET.get('rate', 0))   
        
    #     symbol="USD",
    #     if currency==from_currency:
    #         symbol=from_currency
    #     else:    
    #         symbol=from_currency

    #     api_response = getcompare(from_currency, to_currency, amount, rate)
    #         # allowedweb_names = ['wise', 'xe', 'remitly', 'ofx', 'revolut', 'paypal']
    #     api_provider_names = [provider['name'].lower() for provider in api_response['providers']]
    #     allowedweb_names_lower = [name.lower() for name in allowedweb_names]
    #     filtered_providers = [provider for provider in api_response["providers"] if provider.get('name').lower() in allowedweb_names_lower]
    #     # print(allowedweb_names_lower)
    #     # print("tutul=",api_response)
    #     # Print the filtered providers
    #     # print("Filtered providers:", filtered_providers)
    #     data=[]
    #     for i in filtered_providers:
    #         # print(i.get("quotes"))
    #         name =i.get("name")
    #         fee =i.get("quotes")[0]["fee"]
    #         receivedAmount =i.get("quotes")[0]["receivedAmount"]
    #         rate=i.get("quotes")[0]["rate"]
    #         duration = format_duration(i.get("quotes")[0]['deliveryEstimation']['duration'])
    #         obj = WebsiteList.objects.get(name=name.lower())
    #         # print(name,fee,receivedAmount,rate,duration,obj)
    #         print(name.lower())
    #         listdata={
    #             'name':obj.name,
    #             'fullname':obj.fullname,
    #             'title':obj.title,
    #             'logo':obj.logo.url,
    #             'max':obj.max,      
    #             'min':obj.min, 
    #             'sendby':obj.sendby,    
    #             'receiveby':obj.receiveby,      
    #             'receiveby':obj.receiveby,
    #             'security':obj.security,
    #             'support':obj.support,
    #             'offer':obj.offer,
    #             'sendmoneyprocess':obj.sendmoneyprocess,
    #             'fullreviewlink':obj.fullreviewlink,
    #             'reviews':ReviewsAndRatting.objects.get(name=obj).reviews,
    #             'ratting':ReviewsAndRatting.objects.get(name=obj).rating,
    #             'rate':rate,
    #             'fees':fee,
    #             'duration':duration,
    #             'receivedAmount':receivedAmount,
    #             'symbol':symbol
    #         }
    #         # print(listdata)
           
    #         data.append(listdata)
    #         # print(name,fee,receivedAmount,rate,duration)
    #     # print(data)    
    #     return JsonResponse({'data': data, },status=200)   
    # except Exception as e:
    #         return JsonResponse({'error': str(e)}, status=400)    








def cc_compare(request):
    allowedweb_names = [obj.name for obj in WebsiteList.objects.all()]
    
    data=[]
    for i in allowedweb_names:
        obj = WebsiteList.objects.get(name=i.lower())
        domain_url = request.build_absolute_uri('/')
        listdata={
            'name':obj.name,
            'fullname':obj.fullname,
            'title':obj.title,
            'logo':domain_url+obj.logo.url,
            'max':obj.max,      
            'min':obj.min, 
            'sendby':obj.sendby,    
            'receiveby':obj.receiveby,      
            'receiveby':obj.receiveby,
            'security':obj.security,
            'support':obj.support,
            'offer':obj.offer,
            'sendmoneyprocess':obj.sendmoneyprocess,
            'fullreviewlink':obj.fullreviewlink,
            'reviews':ReviewsAndRatting.objects.get(name=obj).reviews,
            'ratting':ReviewsAndRatting.objects.get(name=obj).rating,
            'reviewurl':ReviewsAndRatting.objects.get(name=obj).url,
            
        }
        data.append(listdata)    

    return JsonResponse({'data': data, },status=200) 