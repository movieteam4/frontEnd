from myapp.models import Dreamreal,createAccount,verifiedAccount,Favorite
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.templatetags.static import static
from django import forms
from .models import Dreamreal
from myapp.forms import LoginForm
import re
from django.urls import reverse
from django.middleware import csrf
import pandas as pd
import datetime
import base64
import mysql.connector
from django.core.cache import cache
# from myapp.call_dataframe import call_dataframe
from myapp.html_show import html_show
from django.http import JsonResponse
'123111121233'
show_data='暫無資料'
db_config = {
    'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',         # 資料庫伺服器地址 (可以是 IP 或域名)
    'user': 'dhv81sqnky35oozt',     # 資料庫使用者名稱
    'password': 'rrdv8ehsrp8pdzqn', # 資料庫密碼
    'database': 'xltc236odfo1enc9',  # 要使用的資料庫名稱
}
# if 'logged_in' in request.session:
#     mail=request.session['logged_in']
#     account=verifiedAccount.objects.get(mail=mail)
def user_more(request):
    if request.method =='POST':
        from myapp.call_dataframe import address
        df=address()
        dict_road = {}
        dict_town = {}
        same_list=[]
        list_city = ['選擇縣市']+list(df["縣市名稱"].unique())
        # 讀取所有縣市
        for city_name in list_city:
            dict_town[city_name] = list(df[(df["縣市名稱"] == city_name)]["鄉鎮市區"].unique())
            for n,town_name in enumerate(dict_town[city_name]):
                if town_name in same_list:
                    town_name=city_name[:-1]+town_name
                    dict_town[city_name][n]=town_name
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name[2:])]["街路聚落名稱"].unique())
                else:
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name)]["街路聚落名稱"].unique())
                same_list.append(town_name)
        mail=request.POST.get('email_address')
        account = verifiedAccount.objects.get(mail=mail)
        account.name=request.POST.get('name')
        if request.POST.get('date_of_birth'):
            try:
                account.date_of_birth=request.POST.get('date_of_birth')
            except:
                account.date_of_birth=datetime.strptime(request.POST.get('date_of_birth'),'%Y-%m-%d')
        account.mobile_phone=request.POST.get('mobile_phone')
        account.national_id=request.POST.get('national_id')
        account.occupation=request.POST.get('occupation')
        account.favorite_cinema=request.POST.get('favorite_cinema')
        account.marital_status=request.POST.get('marital_status')
        account.household_income=request.POST.get('household_income')
        account.gender=request.POST.get('sex')
        account.education=request.POST.get('education')
        account.favorite_genres=request.POST.getlist('f_genres')
        account.preferences=request.POST.getlist('seat')
        try:
            account.address=request.POST.get('city')+request.POST.get('district')+request.POST.get('road')+request.POST.get('address')
        except:
            pass
        detail='資料輸入完成'
        account.save()
        mail=request.session['logged_in']
        account=verifiedAccount.objects.get(mail=mail)
        name=account.name
        date_of_birth=str(account.date_of_birth)
        mobile_phone=account.mobile_phone
        national_id=account.national_id
        address=account.address
        occupation=account.occupation
        favorite_cinema=account.favorite_cinema
        marital_status=account.marital_status
        household_income=account.household_income
        sex=account.gender
        education=account.education
        favorite_genres=account.favorite_genres
        print(favorite_genres)
        seat=account.preferences
        print(seat)
        return render(request,'user_more.html',locals())

    if 'logged_in' in request.session:
        df = cache.get('address')
        if df is None:
            print('沒有暫存')
            from myapp.call_dataframe import address
            df=address()
            cache.set('address',df)
        else:
            print('找到了暫存')
        dict_road = {}
        dict_town = {}
        same_list=[]
        list_city = ['選擇縣市']+list(df["縣市名稱"].unique())
        # 讀取所有縣市
        for city_name in list_city:
            dict_town[city_name] = list(df[(df["縣市名稱"] == city_name)]["鄉鎮市區"].unique())
            for n,town_name in enumerate(dict_town[city_name]):
                if town_name in same_list:
                    town_name=city_name[:-1]+town_name
                    dict_town[city_name][n]=town_name
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name[2:])]["街路聚落名稱"].unique())
                else:
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name)]["街路聚落名稱"].unique())
                same_list.append(town_name)
        mail=request.session['logged_in']
        account=verifiedAccount.objects.get(mail=mail)
        name=account.name
        date_of_birth=str(account.date_of_birth)
        mobile_phone=account.mobile_phone
        national_id=account.national_id
        address=account.address
        occupation=account.occupation
        favorite_cinema=account.favorite_cinema
        marital_status=account.marital_status
        household_income=account.household_income
        sex=account.gender
        favorite_genres=account.favorite_genres
        seat=account.preferences
        education=account.education
        return render(request,'user_more.html',locals())
    else:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入會員')
def Line(request):
    return render(request,'Line.html',locals())
def initialise(request):
    from myapp.call_dataframe import call_dataframe ,week_ranking
    final_data=week_ranking(call_dataframe())
    cache.set('dataframe',final_data)
    print('暫存已設置')
    res='暫存已設置'
    return render(request,'initialise.html', {'res': res})
def contact(request):
    return render(request,'contact.html')
def product_details(request):
    return render(request,'product_details.html')
def shop(request):
    Favorite_movies_list=[]
    mail=False
    favorite=request.GET.get('favorite','')
    status = request.GET.get('status','')
    detail = request.GET.get('detail','')
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        Favorite_movies=Favorite.objects.filter(mail=mail)
        for movie in Favorite_movies:
                Favorite_movies_list.append(movie.which_movie)
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
    csrf_token = csrf.get_token(request)
    form_action_url = reverse('Taiwan_movies_all')
    final_data = cache.get('dataframe')
    if final_data is None:
        from myapp.call_dataframe import call_dataframe ,week_ranking
        final_data=week_ranking(call_dataframe())
        cache.set('dataframe',final_data)  #暫存
    horrors_list=final_data[final_data['類型'].str.contains('恐', na=False)].sort_values(by='當周票房數', ascending=False)
    story_rich_list=final_data[final_data['類型'].str.contains('劇情', na=False)].sort_values(by='當周票房數', ascending=False)
    animation_list=final_data[(final_data['類型'].str.contains('動畫', na=False))|(final_data['類型'].str.contains('卡通',na=False))].sort_values(by='當周票房數', ascending=False)
    action_list=final_data[final_data['類型'].str.contains('動作', na=False)].sort_values(by='當周票房數', ascending=False)
    documentary_list=final_data[final_data['類型'].str.contains('紀錄', na=False)].sort_values(by='當周票房數', ascending=False)
    musical_list=final_data[final_data['類型'].str.contains('音樂', na=False)].sort_values(by='當周票房數', ascending=False)
    romance_list=final_data[final_data['類型'].str.contains('愛', na=False)].sort_values(by='當周票房數', ascending=False)
    my_favorite=final_data[final_data['中文片名'].isin(Favorite_movies_list)]
    from myapp.show_more_filter import filter_show
    res=filter_show(final_data,horrors_list,story_rich_list,animation_list,action_list,documentary_list,musical_list,romance_list,my_favorite,Favorite_movies_list,mail)
    return render(request,'shop.html',locals())
def Taiwan_movies_all(request):
    mail=False
    global show_data , db_config
    Favorite_movies_list=[]
    if request.method !='POST':
        status = request.GET.get('status','''<li><a href="/signin">Sign in</a></li>''' )
        detail = request.GET.get('detail','')
        create_e_mail = request.GET.get('create_e_mail','')
        if create_e_mail!='':
            request.session['logged_in']=create_e_mail
            user = createAccount.objects.filter(mail=create_e_mail).first()
            create_password=user.password
            name=user.name
            verifiedAccount(mail=create_e_mail,password=create_password,name=name).save()
        detail = request.GET.get('detail','' )
        if status=='sign_out':
            if 'logged_in' in request.session:
                del request.session['logged_in']
            return redirect('/Taiwan_movies_all/?detail=已登出')
        elif 'logged_in' in request.session:
            mail=request.session.get('logged_in')
            account=verifiedAccount.objects.filter(mail=mail).first()
            name=account.name
            Favorite_movies=Favorite.objects.filter(mail=mail)
            for movie in Favorite_movies:
                 Favorite_movies_list.append(movie.which_movie)
            if name=='' or name is None:
                name='無名的遊盪者'
            status=f''' <li><a href="https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/user_more"><i class="fas fa-user" style="font-size: 25px;" ></i><span style="font-weight: bold; color: #fff; font-size: 24px; text-transform: capitalize;">{name}</span></a></li>
                        <li><a href="/Taiwan_movies_all?status=sign_out">Sign out</a></li>
                        '''
        csrf_token = csrf.get_token(request)
        form_action_url = reverse('Taiwan_movies_all')

        final_data = cache.get('dataframe')
        if final_data is not None:
            print('找到了暫存')
            res=html_show(final_data,Favorite_movies_list,mail)
            number_1=final_data['宣傳照'].iloc[0]
            description=final_data['簡介'].iloc[0]
            number_1_name=final_data['中文片名'].iloc[0]
            number_1_name_eng=final_data['英文片名'].iloc[0]
            description=description[:len(description)//3]+'...'
            cache.set('dataframe',final_data)
            return render(request,'Taiwan_movie_all.html', locals())
        print('沒有暫存,要重新加載資料庫')
        from myapp.call_dataframe import call_dataframe ,week_ranking
        final_data=week_ranking(call_dataframe())
        cache.set('dataframe',final_data)
        res=html_show(final_data,Favorite_movies_list,mail)
        number_1=final_data['宣傳照'].iloc[0]
        description=final_data['簡介'].iloc[0]
        number_1_name=final_data['中文片名'].iloc[0]
        number_1_name_eng=final_data['英文片名'].iloc[0]
        description=description[:len(description)//3]+'...'
        return render(request,'Taiwan_movie_all.html', locals())
    else:
        status='''<li><a href="/signin">Sign in</a></li>'''
        if request.session.get('logged_in') =='logged_in':
            status='''<li><a href="/Taiwan_movies_all">Sign out</a></li>'''
        csrf_token = csrf.get_token(request)
        form_action_url = reverse('Taiwan_movies_all')
        final_data = cache.get('dataframe')
        if final_data is not None:
            print('找到了暫存')
            res=html_show(final_data,Favorite_movies_list,mail)
            number_1=final_data['宣傳照'].iloc[0]
            description=final_data['簡介'].iloc[0]
            number_1_name=final_data['中文片名'].iloc[0]
            number_1_name_eng=final_data['英文片名'].iloc[0]
            description=description[:len(description)//3]+'...'
            cache.set('dataframe',final_data)
            return render(request,'Taiwan_movie_all.html', locals())
        print('沒有暫存,要重新加載資料庫')
        from myapp.call_dataframe import call_dataframe ,week_ranking
        final_data=week_ranking(call_dataframe())
        cache.set('dataframe',final_data)
        res=html_show(final_data)
        number_1=final_data['宣傳照'].iloc[0]
        description=final_data['簡介'].iloc[0]
        number_1_name=final_data['中文片名'].iloc[0]
        number_1_name_eng=final_data['英文片名'].iloc[0]
        description=description[:len(description)//3]+'...'
        return render(request,'Taiwan_movie_all.html', locals())
def hello(request):
    if request.method=='POST':
        where_from=request.POST.get('where_from')
        if where_from=='create_account':
            return render(request,'create_account.html')
        elif where_from=='from_create':
            create_e_mail = request.POST.get('create_e_mail')
            name=request.POST.get('create_name')
            create_password_1 = request.POST.get('create_password_1')
            create_password_2 = request.POST.get('create_password_2')
            pattern=re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not re.match(pattern,create_e_mail):
                detail='信箱不正確'
                return render(request,'create_account.html',locals())
            pattern=re.compile(r'^(?=.*[A-Z])[A-Za-z0-9]{8,}$')
            if createAccount.objects.filter(mail=create_e_mail).exists()==False:
                if create_password_2 !=create_password_1 :
                    detail='密碼不一樣'
                    return render(request,'create_account.html',locals())
                elif not re.match(pattern,create_password_1):
                    detail='密碼強度不夠'
                    return render(request,'create_account.html',locals())
                createAccount(mail=create_e_mail,password=create_password_2,name=name).save()
                res = send_mail("驗證信", "comment tu vas?", "ian27368885@gmail.com", [create_e_mail], html_message=f'<a href="https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=帳號驗證完成&create_e_mail={create_e_mail}" class="button">點我驗證帳號</a>')
                detail='驗證信已寄出,請查收'
                return render(request,'hello.html',locals())
            else:
                 detail='信箱已註冊'
                 return render(request,'create_account.html',locals())
        elif where_from=='from_log_in':
            e_mail = request.POST.get('e_mail')
            password=request.POST.get('password')
            user=verifiedAccount.objects.filter(mail=e_mail)
            for i in user:
                if i.password==password:
                    request.session['logged_in']=i.mail
                    response=redirect('/Taiwan_movies_all')
                    response.set_cookie('e_mail',e_mail)
                    return response
                else:
                     detail='密碼錯誤'
                     return render(request,'hello.html',locals())
            user=createAccount.objects.filter(mail=e_mail)
            for i in user:
                res = send_mail("驗證信", "comment tu vas?", "ian27368885@gmail.com", [e_mail], html_message=f'<a href="https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=帳號驗證完成&create_e_mail={e_mail}" class="button">點我驗證帳號</a>')
                detail='驗證信已寄出,請查收'
                return render(request,'hello.html',locals())
            detail='無此帳號'
            return render(request,'hello.html',locals())
        elif where_from=='from_log_out':
            e_mail=request.COOKIES.get('e_mail')
            for i in verifiedAccount.objects.filter(mail=e_mail):
                password=i.password
            detail='已登出'
            del request.session['logged_in']
            return render(request,'hello.html',locals())
    else:
        if request.session.get('logged_in') =='logged_in':
            return redirect('/Taiwan_movies_all')
        detail=request.GET.get('detail')
        create_e_mail=request.GET.get('create_e_mail')
        if detail==None:
            return render(request,'hello.html')
        users = createAccount.objects.filter(mail=create_e_mail)
        for user in users:
            create_password=user.password
            name=user.name
        verifiedAccount(mail=create_e_mail,password=create_password,name=name).save()
        return render(request,'hello.html',locals())
    return render(request,'hello.html')
def check_email(request):
    email = request.GET.get('#id_email', None)
    email_exists = False   # 初始化檢查結果
    # 檢查信箱是否已存在
    if email:
        email_exists = createAccount.objects.filter(email_address=email).exists()
    # 返回 JSON 給前端
    return JsonResponse({'email_exists': email_exists})
def handle(request):
    if request.method =='POST':
        if 'logged_in' in request.session:
            liked = request.POST.get('liked')  # 取得是否勾選 (True or False)
            movie_title = request.POST.get('movie_title')  # 取得電影名稱
            mail=request.session['logged_in']
        else:
            detail='請先登入'
            return JsonResponse({
            'detail':detail
        })
        if liked =='true':
             Favorite(mail=mail,which_movie= movie_title).save()
             print('資料已新增')
        else:
            favorite = Favorite.objects.get(mail=mail,which_movie= movie_title)
            favorite.delete()
            print('資料已刪除')
        movie_title = request.POST.get('movie_title')  # 取得電影名稱
        print(movie_title)
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'movie_title': movie_title,
        })
def favorite_page(request):
    if 'logged_in' in request.session:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/shop/?favorite=favorite')
    else:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入')
def about_us(request):
    return render(request,'about_us.html')
