from django.shortcuts import render


def website(request):
    return render(request, 'setup/website.html', locals())


def personal(request):
    return render(request, 'setup/personal.html', locals())