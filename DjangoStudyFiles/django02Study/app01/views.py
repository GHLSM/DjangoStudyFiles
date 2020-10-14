from django.shortcuts import render, HttpResponse, redirect
from django.views import View


class MyLogin(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        return HttpResponse("ok")


def index(request):
    n = 123
    f = 11.11
    s = "ok"
    l = ["hhh", 12]
    t = ("jjj", 122,)
    d = {"name": 'jason', "age": 10}
    b = True
    se = {"hhh", "hhehehe"}
    return render(request, "index.html", locals())