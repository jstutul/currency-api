from django.http import JsonResponse

def home(request):
    # Your JSON data
    data = {
        'status':True,
        'message': 'Welcome to currency api'
    }
    # Returning JSON response
    return JsonResponse(data)
