from django.shortcuts import  render,HttpResponseRedirect
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash

#from django.contrib.auth.models import  User
from django.core.mail import send_mail 
from django.conf import settings

import random
from .models import items,carted1,ordered,addressed,addimg,mov_ticket,cinema_hall,select_halls
from .forms import SignUpForm,EditUserProfileForm,address,addim

# Create your views here.
# THIS CODE IS TO UPDATE THE CART ITEM IN THE BROWSER
global ab_item
def cart_it(request):
    if request.user.is_authenticated:
        a  = carted1.objects.all().filter(user=request.user)
        return  len(a)
    else:
        return 0


#creating home page

def home(request):
    bw = items.objects.all().filter(itype='BW')[:10]
    tw = items.objects.all().filter(itype='TW',price__gte =9000)[:10]
    m =  items.objects.all().filter(itype='M',price__gte=25000)[:10]
    l =  items.objects.all().filter(itype='L')[:10]
    s =  items.objects.all().filter(itype='S')[:10]
    p =  items.objects.all().filter(itype='P')

    if request.user.is_authenticated:
        a  = carted1.objects.all().filter(user=request.user)
        ab_item = len(a)
    else:
        ab_item = 0
    return render(request,'home.html',{'bottom_wear':bw,'top_wear':tw,'mobile':m,'laptop':l,'cart':ab_item,'poster1':p,'shoe':s})

#home page finished

# this is customized registration form
def register(request):
    if request.method == "POST":
        global otqw
        otqw = random.randint(100000,999999)
        global sign_up_form
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            uemail = sign_up_form.cleaned_data['email']
            mess = "enter the otp" + str(otqw)
            send_mail("verify otp",mess,settings.EMAIL_HOST_USER,[uemail])
            return HttpResponseRedirect('/valid/')
        else:
            return HttpResponseRedirect('/register/')
            

    else:
        sign_up_form = SignUpForm() 
        return  render(request,'register.html',{'form':sign_up_form,'nam':'SIGN UP'})

def valid(request):
    return render (request,'validation.html',{'nam':"VALIDATION"})

def otp_validate(request):
    if request.method == "POST":
        aq = request.POST.get('otp1')
       
        if int(aq)==otqw:
            messages.success(request,'CONGRATULATIONS YOUR ACCOUNT HAS BEEN SUCCCEFULLY CREATED ')
            sign_up_form.save()
            #User(username= uname,password=upass,email=uemail).save()
            return HttpResponseRedirect('/login/')
        else:
            messages.success(request,' WRONG OTP REGISTER AGAIN ')
            return HttpResponseRedirect('/register/')

# customize registration form gets completed

# login

def user_login(request):
    if request.user.is_authenticated:
         return HttpResponseRedirect('/')
    if request.method == "POST":
        fm = AuthenticationForm(request=request ,data = request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            print(uname,upass)
            user = authenticate(username = uname, password =upass )
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
        else:
            messages.success(request,'you are not a valid user')
    else:
        fm = AuthenticationForm()
    return render(request,'login.html',{'form':fm,'nam':'LOGIN'})

#login completed

# logout

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        messages.success(request,'First login the page !!')
        return HttpResponseRedirect('/login/')

# logout completed

#user profile

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = EditUserProfileForm(request.POST,instance= request.user)
            if fm.is_valid():
                fm.save()
                #messages.success(request,'Updated successfully !!')
                return HttpResponseRedirect('/')
       
        else:
            fm = EditUserProfileForm(instance = request.user)
            pp = addimg.objects.all().filter(user = request.user)
            messages.success(request,'Please Enter The Correct Detail !!')
        return render(request,'profile.html',{'name':request.user,'form':fm,'nam':'PROFILE','profile':pp,'cart':cart_it(request)})
    else:
        return HttpResponseRedirect('/login/')


#user profile gets completeed

#user password change if the password is konwn in the advance 

def user_change_password(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect('/login/')
    if request.method == "POST":
        fm = PasswordChangeForm(user = request.user,data = request.POST)
        if fm.is_valid():
            fm.save()
            # in order to be on the page of our choice we have to use 
            #  update_session_auth_hash otherwise 
            #  it will redirect to login page automatically
            update_session_auth_hash(request,fm.user)
            return HttpResponseRedirect('/')
    else:
        fm = PasswordChangeForm(user = request.user)
    return render(request,'change_password.html',{'form':fm,'nam':'CHANGE PASSWORD','cart':cart_it(request)})

# user_password change completed


# product detail 

def product_detail(request,id):
    ab = items.objects.get(pk = id)
    return render(request,'product_detail.html',{'item':ab,'nam':'PRODUCT DETAIL','cart':cart_it(request)})

#product detail completed

# product according to demand like mobile top wear bottom wear laptop

def product(request,it):
    ab = items.objects.all().filter(itype = it).order_by('price')
    if it=='M':
        nam = "MOBILE"
    elif it=='L':
        nam = "LAPTOP"
    elif it == "TW":
        nam = "TOP WEAR"
    elif it == "BW":
        nam = "BOTTOM WEAR"
    elif it=="S":
        nam="SHOE"

    return render (request,'utilities.html',{'item':ab,'itype':it,'nam':nam,'cart':cart_it(request)})

#end product


#product filter

def product_filter(request,price,it,abc):
    if abc==2:
        ab = items.objects.all().filter(itype=it).order_by('price')
    elif abc==3:
        ab = items.objects.all().filter(itype=it).order_by('-price')
    elif abc==1:
        ab = items.objects.all().filter(price__gte = price,itype=it)
    else:    
        ab = items.objects.all().filter(price__lte = price,itype=it)
    if it=='M':
        nam = "MOBILE"
    elif it=='L':
        nam = "LAPTOP"
    elif it == "TW":
        nam = "TOP WEAR"
    elif it == "BW":
        nam = "BOTTOM WEAR"
    elif it =="S":
        nam = "SHOE"
    return render (request,'utilities.html',{'item':ab,'itype':it,'nam':nam,'cart':cart_it(request)})

#product filter gets completed



#add to cart functions

def add_to_cart(request,it):
    if request.user.is_authenticated:
        ab = carted1.objects.all().filter(user=request.user,sel=items.objects.get(id=it))

        if len(ab)>0:
            return HttpResponseRedirect('/cart/')
        else:
            reg = carted1(user=request.user,sel = items.objects.get(id = it))
            reg.save()
            return HttpResponseRedirect('/cart/')
    else:
        messages.success(request,'PLEASE LOGIN FIRST')
        return HttpResponseRedirect('/login/')

   
# add to cart completed
    

# cared item 
    
def carted_item(request):
    price1 = 0
    ab = carted1.objects.all().filter(user=request.user)
    pp = addimg.objects.all().filter(user=request.user)
    count = 0
    for i  in ab:
        price1 += i.sel.price
        count+=1
    nam = "CART"
    return render(request,'cart.html',{'item':ab,'total':price1,'count':count,'nam':nam,'profile':pp,'cart':cart_it(request)})

# carted item gets completed


#remove from cart

def remove_from_cart(request,id1):
    ab = carted1.objects.get(id=id1)
    ab.delete()
    return HttpResponseRedirect('/cart/')

#remove from cart completed



#status of the order
def order_status(request):
    ab = ordered.objects.all().filter(user= request.user)
    nam = "ORDERED"
    return render(request,'ordered.html',{'item':ab,'nam':nam,'cart':cart_it(request)})
#end status of the order


# cancel order which has been already made
def cancel_order(request,it):
    ab = ordered.objects.get(id = it)
    ab.delete()
    return HttpResponseRedirect('/ordered_placed/')

#end cancel order


# show all the address of the current user
def address_of_the_current_user(request):
    pp = addimg.objects.all().filter(user = request.user)
    ab = addressed.objects.all().filter(user = request.user)
    return render(request,'address.html',{'item':ab,'nam':"ADDRESS",'profile':pp,'cart':cart_it(request)})
# end of the show address

# remove the saved address of the user

def remove_address(request,it):
    ab = addressed.objects.get(pk=it)
    ab.delete()
    return HttpResponseRedirect('/address/')
# end of the remove saved address

# add address of the current user
def add_address(request):
    if request.method == "POST":
        fm = address(request.POST)
        if fm.is_valid():
            cit = fm.cleaned_data['city']
            sta = fm.cleaned_data['state']
            zip = fm.cleaned_data['zip_code']
            str1 = fm.cleaned_data['street']
            mob = fm.cleaned_data['mobile']
            ab = addressed(user=request.user,city=cit,state = sta,zip_code = zip,street=str1,mobile=mob)
            ab.save()
            return HttpResponseRedirect('/address/')
        else:
            messages.success(request,'you are not a valid user')
    else:
        fm = address()
    return render(request,'login.html',{'form':fm,'nam':'ADD ADDRESS','cart':cart_it(request)})

# end of the add address


from pdf_mail import sendpdf
# simple_demo.py
from fpdf import FPDF
def place_order(request,it):
    ab = carted1.objects.all().filter(user = request.user)
    pdf = FPDF()
    pdf.set_font("Arial", size=7)
    pdf.add_page()
        
    col_width = pdf.w / 5
    row_height = 5
    im_h = 26

    pr = 0
    data = [['S.NO','ITYPE_NAME','ITEM_TYPE','PRICE']]  
    count = 1
    for i in  ab:
        bc = ordered(user= request.user,ite = i.sel)
        bc.save()
        data.append([str(count),i.sel.iname,i.sel.itype,str(i.sel.price)])   
        pr+=i.sel.price  
        count+=1 
        #pdf.image(i.sel.pic, x=180, y=im_h, w=20,h=10)   
        im_h+=15
        abc = carted1.objects.get(id = i.id)
        abc.delete()

    for row in data:
        for item in row:
            pdf.cell(col_width, row_height,txt=item, border=1)
              
        pdf.ln(row_height)

    pdf.cell(col_width*3,row_height,txt = "TOTAL AMOUNT",border = 1 )
    pdf.cell(col_width,row_height,txt = str(pr),border=1)
    pdf.ln(3*row_height)

    pdf.cell(col_width*2,row_height,txt = "DELIVERY ADDRESS",border = 1 )
    pdf.ln(row_height)

    ab1 = addressed.objects.get(pk = it)

    pdf.cell(col_width,row_height,txt = "USER : ",border = 1 )
    pdf.cell(col_width,row_height,txt = str(request.user) ,border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "CITY",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.city),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "STATE",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.state),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "ZIP CODE",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.zip_code),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "STREET",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.street),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "MOBILE NO ",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.mobile),border = 1 )
    pdf.ln(row_height)


        
    pdf.output('simple_table.pdf') 

    k = sendpdf ('abhaypy3@gmail.com',request.user.email,'Benayangla','This mail is from ABHAY website','list the item you have bought','simple_table','./')
    k.email_send()
    return HttpResponseRedirect('/ordered_placed/')

    
def add_image(request):
    
    if request.method=='POST':
        ab = addim(request.POST,request.FILES)
        if ab.is_valid():
            qw = addimg.objects.all().filter(user=request.user)
            if len(qw)>0:
                qw.delete()
            ad = ab.cleaned_data['im']
            bc = addimg(user = request.user,im=ad)
            bc.save()
            return HttpResponseRedirect('/profile/')
    else:
        ab = addim()
        return render(request,'add_image.html',{'nam':'ADD IMAGE','form':ab,'cart':cart_it(request)})
    
    




   
def shop_now(request,it,shp):
    print(shp)
    ab = items.objects.get(id = shp)
    #ac = ordered(user = request.user,ite = ab)
    #ac.save()
    #ab = carted1.objects.all().filter(user = request.user)
    pdf = FPDF()
    pdf.set_font("Arial", size=7)
    pdf.add_page()
        
    col_width = pdf.w / 5
    row_height = 5
    im_h = 26

    pr = 0
    data = [['S.NO','ITYPE_NAME','ITEM_TYPE','PRICE']]  
    count = 1
    for i in  range(1):
        bc = ordered(user= request.user,ite =ab )
        bc.save()
        data.append([str(count),ab.iname,ab.itype,str(ab.price)])   
        pr+=ab.price  
        count+=1 
        #pdf.image(i.sel.pic, x=180, y=im_h, w=20,h=10)   
        im_h+=15

    for row in data:
        for item in row:
            pdf.cell(col_width, row_height,txt=item, border=1)
              
        pdf.ln(row_height)

    pdf.cell(col_width*3,row_height,txt = "TOTAL AMOUNT",border = 1 )
    pdf.cell(col_width,row_height,txt = str(pr),border=1)
    pdf.ln(3*row_height)

    pdf.cell(col_width*2,row_height,txt = "DELIVERY ADDRESS",border = 1 )
    pdf.ln(row_height)

    ab1 = addressed.objects.get(pk = it)

    pdf.cell(col_width,row_height,txt = "USER : ",border = 1 )
    pdf.cell(col_width,row_height,txt = str(request.user) ,border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "CITY",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.city),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "STATE",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.state),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "ZIP CODE",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.zip_code),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "STREET",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.street),border = 1 )
    pdf.ln(row_height)

    pdf.cell(col_width,row_height,txt = "MOBILE NO ",border = 1 )
    pdf.cell(col_width,row_height,txt = str(ab1.mobile),border = 1 )
    pdf.ln(row_height)


        
    pdf.output('simple_table.pdf') 

    k = sendpdf ('abhaypy3@gmail.com',request.user.email,'Benayangla','This mail is from ABHAY website','list the item you have bought','simple_table','./')
    k.email_send()
    return HttpResponseRedirect('/ordered_placed/')


def shop_now_address(request,it):
    if request.user.is_authenticated:
        add = addressed.objects.all().filter(user=request.user)
        return render(request,'shop_now_address.html',{'item':add,'nam': 'ADDRESS','shp':it,'cart':cart_it(request)})
    else:
        messages.success(request,'PLEASE LOGIN FIRST')
        return HttpResponseRedirect('/login/')



import datetime
from django.utils.timezone import utc
def movie(request):
    abhay_kumar = mov_ticket.objects.all().order_by('-utm')

    """
     lis = []
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    
    for i in abhay_kumar:
        ak = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second)
        b = datetime.datetime(i.dtf.year,i.dtf.month,i.dtf.day,i.dtf.hour,i.dtf.minute,i.dtf.second)
        c = ak-b 
        print('Difference: ', c)
        minutes = c.total_seconds() / 60
        print('Total difference in minutes: ', int(minutes))
        lis.append(int(minutes))

    """
   
    return render(request,'movie.html',{'pic':abhay_kumar,'nam':'MOVIE SHOW','cart':cart_it(request)})

def hall_name(request,it):
    ab = select_halls.objects.all().filter(movie=mov_ticket.objects.get(mname=it))
    return render(request,'hall_address.html',{'hall':ab,'cart':cart_it(request)})


def bookmovie(request,chall,movi,val):
    initail_ticket = select_halls.objects.get(movie = mov_ticket.objects.get(mname=movi),hall=cinema_hall.objects.get(hname=chall)).seat
    if initail_ticket >= int(val):
        # code to get the name of  the user who want to watch the movie
        user_list = []
        if request.method=="POST":
            for i in range(val):
                user_list.append(request.POST[str(i+1)])
            print(user_list)
        # end of the user list code
        pdf = FPDF()
        pdf.set_font("Arial", size=7)
        pdf.add_page()
            
        col_width = pdf.w / 5
        row_height = 5
        im_h = 26
        pdf.cell(col_width,row_height,txt = "*"*int(col_width)*5,border = 0 )
        pdf.ln(row_height)
        pdf.set_font("Arial", size=20)
        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "ABHAY KUMAR ONLINE WEBSITE ",border = 0 )
        pdf.ln(row_height)
        pdf.set_font("Arial", size=7)
        pdf.cell(col_width,row_height,txt = "*"*int(col_width)*5,border = 0 )
        pdf.ln(row_height)
        pdf.cell(col_width,row_height,txt = "BOOKING TIME : "+str(str(datetime.datetime.now())),border = 0 )
        pdf.cell(col_width*3,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "WE WELCOME YOU",border = 0 )
        pdf.ln(row_height)
        
        pdf.ln(row_height*3)

        ab = mov_ticket.objects.get(mname=movi)
        pdf.set_font("Arial", size=7)
        pr = 0
        data = [['S.NO','MOVIE_NAME','NAME','PRICE']]  
        count = 1
        for i in  range(val):
            data.append([str(count),ab.mname,user_list[i],str(ab.disp)])   
            pr+=ab.disp
            count+=1   
            im_h+=15

        for row in data:
            for item in row:
                pdf.cell(col_width, row_height,txt=item, border=1)
                
            pdf.ln(row_height)

        pdf.cell(col_width*3,row_height,txt = "TOTAL AMOUNT",border = 1 )
        pdf.cell(col_width,row_height,txt = str(pr),border=1)
        pdf.ln(3*row_height)


        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width*2,row_height,txt = "CINEMA HALL ADDRESS",border = 1 )
        pdf.ln(row_height)

        ab1 = cinema_hall.objects.get(hname = chall)
        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "USER : ",border = 1 )
        pdf.cell(col_width,row_height,txt = str(request.user) ,border = 1 )
        pdf.ln(row_height)

        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "HALL NAME : ",border = 1 )
        pdf.cell(col_width,row_height,txt = str(ab1.hname) ,border = 1 )
        pdf.ln(row_height)

        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "CITY",border = 1 )
        pdf.cell(col_width,row_height,txt = str(ab1.city),border = 1 )
        pdf.ln(row_height)

        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "STATE",border = 1 )
        pdf.cell(col_width,row_height,txt = str(ab1.state),border = 1 )
        pdf.ln(row_height)

        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "ZIP CODE",border = 1 )
        pdf.cell(col_width,row_height,txt = str(ab1.pin),border = 1 )
        pdf.ln(row_height)

        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "STREET",border = 1 )
        pdf.cell(col_width,row_height,txt = str(ab1.street),border = 1 )
        pdf.ln(row_height)

        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width,row_height,txt = "MOBILE NO ",border = 1 )
        pdf.cell(col_width,row_height,txt = str(ab1.contact),border = 1 )
        pdf.ln(row_height*5)

        pdf.cell(col_width,row_height,txt = "*"*int(col_width)*5,border = 0 )
        pdf.ln(row_height)
        pdf.set_font("Arial", size=12)
        pdf.cell(col_width,row_height,txt = " ",border = 0 )
        pdf.cell(col_width*3,row_height,txt = "OUR TEAM WELCOME YOU FROM BOTTOM OF MY HEART ",border = 0 )
        pdf.ln(row_height)
        pdf.cell(col_width,row_height,txt = "*"*int(col_width)*5,border = 0 )
        pdf.ln(row_height)


            
        pdf.output('movie_ticket.pdf') 
        print(request.user.email)

        k = sendpdf ('abhaypy3@gmail.com',request.user.email,'Benayangla','This mail is from ABHAY website','list the item you have bought','movie_ticket','./')
        k.email_send()
        final_ticket = select_halls.objects.get(movie = mov_ticket.objects.get(mname=movi),hall=cinema_hall.objects.get(hname=chall))
        final_ticket.seat = initail_ticket-int(val)
        final_ticket.save()
        return HttpResponseRedirect('/movie/')
    else:
        return HttpResponseRedirect('/cal/')


def no_of_user(request,chall,movi,val):
    if val == 1:
        qw = select_halls.objects.get(movie = mov_ticket.objects.get(mname=movi),hall=cinema_hall.objects.get(hname=chall))
        return render(request,'no_of_user.html',{'seat':qw.seat,'tame':datetime.datetime.now(),'chall':chall,'movi':movi})

    qw = select_halls.objects.get(movie = mov_ticket.objects.get(mname=movi),hall=cinema_hall.objects.get(hname=chall))
    if request.method=="POST":
        nuser = request.POST['nuser']
        qw = select_halls.objects.get(movie = mov_ticket.objects.get(mname=movi),hall=cinema_hall.objects.get(hname=chall))
        if int(nuser) <= qw.seat:
            al = []
            for i in range(int(nuser)):
                al.append(str(i+1))

            print(nuser)
            return render(request,'no_of_user.html',{'item':al,'val':int(nuser),'chall':chall,'movi':movi,'cart':cart_it(request),'seat':qw.seat})
        else:
            return render(request,'spin.html')
    return render(request,'no_of_user.html',{'seat':qw.seat,'tame':datetime.datetime.now(),'chall':chall,'movi':movi})

import requests
import bs4

#INDIAN CORORNA DAILY UPDATE
from requests_html import HTML
from selenium import  webdriver
from selenium.webdriver.chrome.options import Options
import time
def corona(request):
    results = []
    url = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(url)
    htmlcontent = response.content
    soup = bs4.BeautifulSoup(htmlcontent,'html.parser')
    ab = soup.find_all('div',attrs={'class':'maincounter-number'})
    lis = ['covid cases','death','recovered']
    text = ['danger','primary','dark']
    bac = ['info','warning','danger']
    for i in range(len(lis)):
        results.append({'first':lis[i],'second':ab[i].text,'text':text[i],'back':bac[i]})
    print(results)

    #INDIAN DAILY CORONA VIRUS REPORT
    options =Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome('C:/Users/abhay/Downloads/chromedriver_win32/chromedriver.exe',options=options)
    url = 'https://www.google.com/search?q=covid+cases+in+india&oq=covid&aqs=chrome.0.69i59l3j0i131i433i512l2j69i60l2j69i61.1702j0j7&sourceid=chrome&ie=UTF-8'
    driver.get(url)
    time.sleep(1)

    body_el = driver.find_element_by_css_selector("body")
    html_str = body_el.get_attribute("innerHTML")
    html_obj = HTML(html = html_str)

    date = html_obj.find('.c274Wb')
    for i in date:
        todays_date = i.text
    new_cases = html_obj.find('.GxwVnb')
    for j in new_cases:
        ab = j.find('span')
        new_case = ab[2].text
        avg_case = ab[5].text    

    return render(request,'corona.html',{'bd':results,'today_date':todays_date,'new_case':new_case,'avg':avg_case})

    
    


    





















#################################################################################################################
# THIS CODE IS OF NO USE 
#################################################################################################################
"""
def sendemail(request):
    if request.method == "POST":
        pass
        #to = request.POST.get('toemail')
        #content = request.POST.get('content')
        #print(request.user.email)
        #file = open(MEDIA_ROOT + os.path.sep + render_to_string('qw.txt'),'r')
        #content = file.read()
        #file.close()
        #send_mail("testting",content,settings.EMAIL_HOST_USER,['abhaykumar912244@gmail.com'])
    #return render(request,'email.html')

"""


#################################################################################################################
# THIS CODE IS OF NO USE 
#################################################################################################################
"""
#***************************************************************************************************
# this code is not the part of the programme
"""

"""

def sendemail():
    excelfile = BytesIO()

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheetname')

    ws.write(0, 0, 'Firstname')
    ws.write(0, 1, 'Surname')
    ws.write(1, 0, 'Hans')
    ws.write(1, 1, 'Muster')

    wb.save(excelfile)

    email = EmailMessage()
    email.subject = 'This subject'
    email.body = 'This context'
    email.from_email = 'abhaypy3@gmail.com'
    email.to = ['abhaykumar912244@gmail.com']
    email.attach('test_file.xls', excelfile.getvalue(), 'application/ms-excel')
    #email.send()

#sendemail()    


#**************************************************************************************************

"""



#################################################################################################################
# THIS CODE IS OF NO USE 
#################################################################################################################
"""
#place final order note this is replaced by the pdf form the code is written below

def wait_place_order(request):
    # sending the excel  attachement to the user email 
    excelfile = BytesIO()

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Product_detail')

    ws.write(0, 0, 'SERIAL NO ')
    ws.write(0, 1, 'ITEM NAME')
    ws.write(0, 2, 'ITEM TYPE')
    ws.write(0, 3, 'PRICE')
    # upto here 

    ab = carted1.objects.all().filter(user = request.user)
    count = 1
    for i in  ab:
        bc = ordered(user= request.user,ite = i.sel)
        bc.save()
        # attachement code
        ws.write(count,0,count)
        ws.write(count,1,i.sel.iname)
        ws.write(count,2,i.sel.itype)
        ws.write(count,3,i.sel.price)
        #attachement end
        count+=1
        
        abc = carted1.objects.get(id = i.id)
        abc.delete()
    wb.save(excelfile)

    email = EmailMessage()
    email.subject = 'ORDER DETAIL'
    email.body = 'LIST OF THE ITEM ORDERED'
    email.from_email = 'abhaypy3@gmail.com'
    abqwer = request.user.email
    email.to = [abqwer]
    email.attach('test_file.xls', excelfile.getvalue(), 'application/ms-excel')
    email.send()

    return HttpResponseRedirect('/ordered_placed/')

# order placed and the detail has been emailed

"""



#################################################################################################################
# THIS CODE IS OF NO USE 
#################################################################################################################
"""
# for sending the ms excel attachement 
from io import BytesIO
import xlwt
from django.core.mail import EmailMessage

"""



#################################################################################################################
# THIS CODE IS OF NO USE 
#################################################################################################################
"""


"""



#################################################################################################################
# THIS CODE IS OF NO USE 
#################################################################################################################
"""


"""

    
    