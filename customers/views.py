from django.shortcuts import render


def lancaster_homepage(request):
    return render(
        request,
        'lancaster.html',
        {
            'title': 'Lancaster Home Page',
        }
    )
