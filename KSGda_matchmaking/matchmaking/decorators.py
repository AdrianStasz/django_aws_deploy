from django.shortcuts import redirect

from .models import Promoter

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def check_promoter(view_func):
    def wrapper_func(request, *args, **kwargs): 

        all_promoters = Promoter.objects.all()

        for promoter in all_promoters:
            if promoter.user.player == request.user.player:

                return view_func(request, *args, **kwargs)
            
        return redirect('create_match_error')
    return wrapper_func


