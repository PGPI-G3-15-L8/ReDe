from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'home/index.html')

def privacy_policy_view(request):
    return render(request, 'home/privacy_policy.html')

def about_us_view(request):
    return render(request, 'home/about_us.html')