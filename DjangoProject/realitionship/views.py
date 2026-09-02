import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import Anketa as form_anketa
from .models import Anketa,Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        try:
            _=request.user.profile.anketa
        # BUG: can not load relationship
        except Exception:
            messages.warning(request, "Заполните анкету!")
    return render(request,"realitionship/index.html")


@login_required
def recomendation_search(request):
    mean_age = 2
    attempts = 0
    allowed_anketes = 0
    try:
        current_anketa = request.user.profile.anketa
    except Exception:
        messages.warning(request, "Заполните анкету!")
        return redirect("rl:anketa")
    anketes = []
    while len(anketes) == 0 and attempts < 20 and allowed_anketes<10:
        anketes = Anketa.objects.filter(
            age__gte=current_anketa.age - mean_age,
            age__lte=current_anketa.age + mean_age,
        )

        if current_anketa.find_gender != "both":
            anketes = anketes.filter(gender=current_anketa.find_gender)

        anketes = list(anketes)
        try:
            del anketes[anketes.index(request.user.profile.anketa)]
        except Exception:
            pass
        if not anketes:
            mean_age += 1
        else:
            allowed_anketes += len(anketes)
        attempts += 1
    print(anketes)
    anketes = [{
        "username":anketa.profile.user.username,
        "annotation":anketa.profile.annotation,
        "age":anketa.age,
        "user_icon":anketa.profile.user_icon.url,
        "user_id":request.user.pk
                } for anketa in anketes]
    anketes = json.dumps(anketes)
    print(anketes)
    return render(request, "realitionship/match.html", context={
        "anketes": anketes,
    })


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("rl:index")
    else:
        form = UserCreationForm()
    return render(request, "registration/sign_up.html", context={"form": form})


@login_required
def anketa(request):
    try:
        anketa = request.user.profile.anketa
    except Exception:
        anketa = None

    if request.method == "POST":
        form = form_anketa(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                anketa = request.user.profile.anketa
                anketa.gender=form_data.get("gender")
                anketa.age = form_data.get("age")
                print(anketa.age,type(anketa.age))
                if anketa.age <= 0:
                    messages.error(request,"Возраст не может быть отрицательным!")
                    return redirect("rl:anketa")
                anketa.find_gender = form_data.get("find_gender")
                anketa.save()
            except Exception as e:
                Anketa.objects.create(
                    gender=form_data.get("gender"),
                    age = form_data.get("age"),
                    find_gender = form_data.get("find_gender"),
                    profile=request.user.profile
                )
        return redirect("rl:profile")
    else:
        #POST
        initial = {}
        if anketa:
            initial = {
                "gender": anketa.gender,
                "age": anketa.age,
                "find_gender": anketa.find_gender,
            }
        form = form_anketa(initial=initial)
        return render(request,"realitionship/anketa.html", context={"form":form})


@login_required
def view_profile(request):
    if request.method == "GET":
        username = request.GET.get("username",None)

        if not username:
            profile = request.user.profile
            try:
                anketa = request.user.profile.anketa
            except Exception as e:
                anketa = None
                messages.warning(request, "Заполните анкету!")
        else:
            profile = Profile.objects.filter(user__username=username).first()
            if not profile:
                return HttpResponse("Такого профиля не существует, введён некорекктоный юзернейм")

        return render(
            request, "realitionship/profile.html", context=
            {
            "likes_count":profile.liked.count(),
            "dislikes_count":profile.disliked.count(),
            "annotation": profile.annotation,
            "age": profile.anketa.age if anketa else None,
            "user_icon": profile.user_icon,
            "username": profile.user.username,
            "is_user":True if request.user.username == username or username is None else False,
            "show_marked_items":profile.show_marked_items
            }
        )


def view_liked(request):
    liked_count = request.user.profile.liked.count()
    limit = int(request.GET.get("limit",2))
    current_page = int(request.GET.get("page",0))
    offset = limit*current_page
    end = limit+offset
    pages = [page for page in range(round(liked_count/limit))]
    next_page = current_page+1
    prev_page = current_page-1
    liked = request.user.profile.liked.all()[offset:end]
    if len(pages) > 0:
        show_next_btn = True if next_page <= pages[-1] else False
        show_prev_btn = True if prev_page >= 0 else False
    else:
        show_next_btn = False
        show_prev_btn = False

    return render(request,"realitionship/marked/liked.html",context={
                                                                     "liked":liked,
                                                                     "current_page":current_page,
                                                                     "pages":pages,
                                                                     "next_page":next_page,
                                                                     "prev_page":prev_page,
                                                                     "show_next_btn":show_next_btn,
                                                                     "show_prev_btn":show_prev_btn
                                                                     })


def view_disliked(request):
    disliked_count = request.user.profile.disliked.count()
    limit = int(request.GET.get("limit", 2))
    current_page = int(request.GET.get("page", 0))
    offset = limit * current_page
    end = limit + offset
    pages = [page for page in range(round(disliked_count / limit))]
    next_page = current_page + 1
    prev_page = current_page - 1
    disliked = request.user.profile.disliked.all()[offset:end]
    if len(pages) > 0:
        show_next_btn = True if next_page <= pages[-1] else False
        show_prev_btn = True if prev_page >= 0 else False
    else:
        show_next_btn = False
        show_prev_btn = False

    return render(request, "realitionship/marked/disliked.html", context={
        "disliked": disliked,
        "current_page": current_page,
        "pages": pages,
        "next_page": next_page,
        "prev_page": prev_page,
        "show_next_btn": show_next_btn,
        "show_prev_btn": show_prev_btn
    })

# BUG: get rid of csrf_exempt
@login_required
@csrf_exempt
def like(request, user_id:int):
    user = User.objects.filter(pk=user_id).first()
    if user:
        if user in request.user.profile.disliked.all():
            request.user.profile.disliked.remove(user)
        request.user.profile.liked.add(user)
    return JsonResponse({"status":"success"})

# BUG: get rid of csrf_exempt
@login_required
@csrf_exempt
def dislike(request, user_id:int):
    user = User.objects.filter(pk=user_id).first()
    if user:
        print(request.user.profile.liked)
        if user in request.user.profile.liked.all():
            request.user.profile.liked.remove(user)
        request.user.profile.disliked.add(user)
    return JsonResponse({"status":"success"})
