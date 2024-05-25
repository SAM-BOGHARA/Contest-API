import concurrent.futures

import requests
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from rest_framework.renderers import JSONRenderer

from .models import *
from .serializers import *

TTL_TIME = 7200

# Create your views here.
def home(request):
    return HttpResponse("Hi, I am Shubham Boghara.")


def apipage(request):
    return HttpResponse(
        "Hey, this is my hobby project made for leetcoders around the world."
    )


@api_view(["GET"])
@ratelimit(key="ip", rate="10/m")
def weekly(request, contest_id, page):
    if cache.get(f"{contest_id}_{page}"):
        data = cache.get(f"{contest_id}_{page}")
        db = "redis"
        print("redis response")
    else:
        data = Weekly.objects.filter(contest_id=contest_id, page=page)
        if data.exists():
            cache.set(f"{contest_id}_{page}", data, timeout=TTL_TIME)
            db = "postgresql"
            print("postgresql response")
        else:
            fetch_language_map(contest=f"weekly-contest-{contest_id}", page=page)
            data = Weekly.objects.filter(contest_id=contest_id, page=page)
            cache.set(f"{contest_id}_{page}", data, timeout=TTL_TIME)
            db = "postgresql"
            print("postgresql response")

    serializer = WeeklySerializer(data, many=True)
    response_data = {
        "db": db,
        "data": serializer.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@ratelimit(key="ip", rate="10/m")
def biweekly(request, contest_id, page):
    if cache.get(f"{contest_id}_{page}"):
        data = cache.get(f"{contest_id}_{page}")
        db = "redis"
        print("redis response")
    else:
        data = BiWeekly.objects.filter(contest_id=contest_id, page=page)
        if data.exists():
            cache.set(f"{contest_id}_{page}", data, timeout=TTL_TIME)
            db = "postgresql"
            print("postgresql response")
        else:
            fetch_language_map(contest=f"biweekly-contest-{contest_id}", page=page)
            data = BiWeekly.objects.filter(contest_id=contest_id, page=page)
            cache.set(f"{contest_id}_{page}", data, timeout=TTL_TIME)
            db = "postgresql"
            print("postgresql response")
    serializer = WeeklySerializer(data, many=True)
    response_data = {
        "db": db,
        "data": serializer.data,
    }
    return Response(response_data, status=status.HTTP_200_OK)


def fetch_submission_language(submission_id):
    try:
        url = f"https://leetcode.com/api/submissions/{submission_id}/"
        response = requests.get(url)
        data = response.json()
        print(data)
        language = data.get("lang", "omit")
        return language
    except Exception:
        pass
    try:
        url = f"https://leetcode.cn/api/submissions/{submission_id}/"
        response = requests.get(url)
        data = response.json()
        print(data)
        language = data.get("lang", "omit")
        return language
    except Exception:
        pass


def fetch_language_map(contest, page):
    l_map = {}
    contest_name = contest.split("-")[0]
    contest_id = int(contest.split("-")[-1])
    url = f"https://leetcode.com/contest/api/ranking/{contest}/?pagination={page}&region=global"
    response = requests.get(url)
    data = response.json()
    print(data)

    submission_ids = [
        list(user.values())[0]["submission_id"] for user in data["submissions"]
    ]
    username_list = [user["username"] for user in data["total_rank"]]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        language_promises = executor.map(fetch_submission_language, submission_ids)

    l_map = {username_list[i]: language for i, language in enumerate(language_promises)}

    # Store data in the appropriate model
    print(contest_name)
    if contest_name == "weekly":
        ContestModel = Weekly
    elif contest_name == "biweekly":
        ContestModel = BiWeekly
    else:
        raise ValueError("Invalid contest name")

    for username, lang in l_map.items():
        entry = ContestModel(
            contest_id=contest_id, username=username, lang=lang, page=page
        )
        entry.save()

    return l_map
