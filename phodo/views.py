#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import Rform, UploadForm
from .models import User, Pic
import logging, datetime
import random
import math, requests, json
from PIL import Image
import PIL

# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)
#here define the wechat api parameters.
#user and auth both use wechat pub xxx
WECHAT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1d3cfcf816c87d8b&redirect_uri=https%3A%2F%2Fwww.aishe.org.cn%2Fphodo%2Flogin&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
WECHAT_AUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/'

class IndexView(View):
    #this view is to do 1, redirect to auth page(commom method)
    #let me see if django has some common tool; mixins or method decorator, not comprehensible
    # i just decide to use manually verify sessions. of course before i use salt sign, it will not be safe.
    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(WECHAT_URL)   #redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        else:
            #call a view to draw 2 picture to phodo
            #r_id = 1 cancelled, let rate get auto generate # auto generate r_id, = photo id , its rating times, pull another picture to compare with it.
            return HttpResponseRedirect(reverse('phodo:rate'))

class LoginView(View):
    #this handle the redirected url from wechat;
    def get(self, request, *args, **kwargs):
        code = request.GET.get('CODE', 'X')  # path variable ?CODE=xxxxxxxx pass to code.
        if code == 'X':
            return render(request, 'result.html', {'success': False})
        else:
            res = requests.get(WECHAT_AUTH_URL.join(code).join(
                '&grant_type=authorization_code'))  # use wechat authorize api to fetch accesstoken, openid etc.
            data = json.loads(res)
            if data.get('errcode', 0) == 0:
                u = User(name=data.openid, openid=data.openid)
                # u.save()  # no user save needed! every thing comes from wechat user openid!
                request.session['login'] = True
                request.session['openid'] = data.openid
                return HttpResponseRedirect(reverse('phodo:rate'))

class RateView(View):
    #this view is to render the pic1 and pic2 to be rated by clicking
    #this page can get: generate random (none input) or given picture id (p_id)
    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)   #redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        else:
            #how to generate a random picture? its a auto updated list!
            #right now i just use a last 3 picture, for sqlite pk +1 or -1, ordered_by - rated times.
            list = Pic.objects.order_by('-rated')[:20]
            #random 2 in 20
            n1 = random.randrange(0,18,2)
            n2 = random.randrange(1,19,2)
            pics = [
                list[n1],
                list[n2]
            ]
            #render page and return forms for rate
            #form first and then fill with pic object.
            form = Rform(pics[0])
            form.fields['hidden_pic1'] = pics[0].id
            form.fields['hidden_pic2'] = pics[1].id
            logger.debug('form fields %s', str(form.hidden_pic1))
            #fill context with forms and other variables#maybe it should direct assign instead of use fields method
            context = {
                'form': form
            }
            return render(request, 'rate.html', context)

    def post(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)  # redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        else:
            form = Rform(request.POST)
        #here i will handle the posted form, first validate data, then calculate elo rate, then update to db.
        if form.is_valid():
            #query two pic objects
            id1 = form.cleaned_data['hidden_pic1']
            pic1 = get_object_or_404(Pic, pk=id1)
            id2 = form.cleaned_data['hidden_pic2']
            pic2 = get_object_or_404(Pic, pk=id2)
            pic1.addRate()
            pic2.addRate()
            #calculate floating index k according to its total rated times;
            k1 = 300/(5+pic1.rated) + 20
            k2 = 300/(5+pic2.rated) + 20
            win = form.cleaned_data['choice']
            #rated + 1 and update elo rating and save;
            if win == id1:
                #1 wins ,update the both rating:
                pic1.rating += int(k1(1 - 1/(math.pow(10, (pic2.rating - pic1.rating)/400) + 1)))
                pic2.rating += int(k2(0 - 1/(math.pow(10, (pic1.rating - pic2.rating)/400) + 1)))
                pic1.save()
                pic2.save()
            else:
                pic1.rating += int(k1(0 - 1 / (math.pow(10, (pic2.rating - pic1.rating) / 400) + 1)))
                pic2.rating += int(k2(1 - 1 / (math.pow(10, (pic1.rating - pic2.rating) / 400) + 1)))
                pic1.save()
                pic2.save()
            return render(request, 'result.html', {'success': True})

class PicRateView(View):
    #this view generate a rate of specific picture
    def get(self, request, pic_id, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)  # redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        else:
            item1 = get_object_or_404(Pic, pk=pic_id)  #find the pic
            user = get_object_or_404(User, openid = openid)  #identify the user
            #determine a pic to compare, rate = 0.6-1.8, text: no search. if mongodb try match
            #order_by upload
            #if there isn't return rate refuse page==get or 404

            item2 = Pic.objects.exclude(pk=pic_id).filter(rated__lte=10 + int(item1.rated*1.8))
            pics = [
                item1,
                item2
            ] #can be rewrite
            #fill the context with forms data and other variables
            #render and return form with initial for rate
            form = Rform(pics)
            form.fields['hidden_pic1'] = pic_id
            form.fields['hidden_pic2'] = item2.pk
            context = {
                'form': form
            }
            return render(request, 'rate.html', context)

class UploadView(View):
    # form_class = UploadForm()
    op_cache = {'key': 'value'} #is this a dict
    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        logger.warning('welcome user %s' % openid)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)  # redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        o_id = random.randint(1, 300) #how long is this random? need review???
        self.op_cache[openid] = o_id #put the user and unique operation id to this dict, every post will chech the cache if this op is valide or duplicated
        #or use update: .update({openid: o_id})
        id_form = UploadForm(initial={'o_id': o_id, 'openid': openid})
        logger.warning('return o_id = %s ' % o_id)
        # form_class.fields['o_id'] = random.randint()
        return render(request, 'upload.html', {'form': id_form})

    def post(self, request, *args, **kwargs):
        uploaded = UploadForm(request.POST, request.FILES)
        if uploaded.is_valid():
            # openid = uploaded.cleaned_data['openid']
            # o_id = uploaded.cleaned_data['o_id']
            #above i get the data from the form and then goes to that dict
            # logger.warning('o_id equals %s' % o_id)
            # if self.op_cache.get(openid) == o_id:  debug not pass unique checking
            if True:
                pic = Pic()
                # pic.user = uploaded.cleaned_data['openid'] #change with no user connect
                pic.user = request.session.get('openid')
                pic.picture = uploaded.cleaned_data['picture'] #DONE size adjust, scale limit, tages auto generate
                # see source: http: // stackoverflow.com / questions / 24745857 / python - pillow - how - to - scale - an - image
                # pic.picture = auto_resize(picture)
                pic.text = uploaded.cleaned_data['text']
                pic.save()

                request.session['uploaded'] = True
                return render(request, 'result.html', {'success': True})
            else:
                return render(request, 'result.html', {'success': False})
        else:
            return render(request, 'result.html', {'success': uploaded})

def auto_resize(picture):
    p = Image.open(picture)
    #get size
    width, height = p.size
    logger.debug('incomming a picture with %s with %s ' % p.size)
    if width > height:
        #return a resized picture, depends on its originally vertical or horizontal
        ratio = 1600 / width
        rh = int(height * ratio)
        size = (1600, 800)
        # return p.resize(size, PIL.Image.ANTIALIAS)
        p.resize(size, PIL.Image.ANTIALIAS)
        fp = '{0}/{1}/{2}'.format(str(datetime.date.year), str(datetime.date.month), str(datetime.time)).join('.jpg')
        p.save(fp)
        return fp
    else:
        ratio = 1000 / height
        rw = int( width * ratio)
        size = (600, 1000)
        # return p.resize(size, PIL.Image.ANTIALIAS)
        p.resize(size, PIL.Image.ANTIALIAS)
        fp = '{0}/{1}/{2}'.format(str(datetime.date.year), str(datetime.date.month), str(datetime.time)).join('.jpg')
        p.save(fp)
        return fp