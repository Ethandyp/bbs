from django.shortcuts import render
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from blog import forms, models


# 自己生成验证码的登录
def login(request):
	# 初始化一个给AJAX返回的数据
	ret = {"status": 0, "msg": ""}
	if request.method == "POST":
		# 从提交过来的数据中 取到用户名和密码
		username = request.POST.get("username")
		pwd = request.POST.get("password")
		# 利用auth模块做用户名和密码的校验
		user = auth.authenticate(username=username, password=pwd)
		if user:
				# 用户名密码正确
				# 给用户做登录
			auth.login(request, user)
			ret["msg"] = "/index/"
		else:
			# 用户名密码错误
			ret["status"] = 1
			ret["msg"] = "用户名或密码错误！"
		return JsonResponse(ret)
	return render(request, "login.html")


def index(request):
	return render(request, "index.html")


# 注册函数
def register(request):
	ret = {'status': 0, "msg": []}
	if request.method == "POST":
		user_obj = forms.RegForm(request.POST)
		avatar_img = request.FILES.get("avatar")
		# 帮我做校验
		if user_obj.is_valid():
			# 剔除确认密码
			user_obj.cleaned_data.pop('re_password')
			models.UserInfo.objects.create_user(**user_obj.cleaned_data, avatar=avatar_img)
			ret['msg'] = "/index/"
			return JsonResponse(ret)
		else:
			print(user_obj.errors)
			ret['status'] = 1
			ret['msg'] = user_obj.errors
			return JsonResponse(ret)
	form_obj = forms.RegForm()
	return render(request, 'register.html', {"form_obj": form_obj})
