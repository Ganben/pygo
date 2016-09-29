#-*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import Rform, UploadForm, UploadForm2P, Rform2P
from .models import User, Pic, Tag
from .config import nogit, makeimgurl
import logging, datetime
import random
import oss2
import math, requests, json
from PIL import Image
import PIL

# Create your views here.

# Get an instance of a logger
logger = logging.getLogger('django')
#here define the wechat api parameters.
#user and auth both use wechat pub xxx
WECHAT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1d3cfcf816c87d8b&redirect_uri=https%3A%2F%2Fwww.aishe.org.cn%2Fphodo%2Flogin&response_type=code&scope=snsapi_base&state=123#wechat_redirect'
WECHAT_AUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/'
RANDOM = 4

def auto_resize(picture):     #maybe this method is a wrong place!
    p = Image.open(picture)
    #get size
    width, height = p.size
    logger.debug('incomming a picture with %s with %s ' % p.size)
    if width > height:
        #return a resized picture, depends on its originally vertical or horizontal
        ratio = 1600 / width
        rh = int(height * ratio)
        size = (1600, rh)
        # return p.resize(size, PIL.Image.ANTIALIAS)
        p1 = p.resize(size, PIL.Image.ANTIALIAS)
        # fp = '{0}/{1}/{2}'.format(str(datetime.date.year), str(datetime.date.month), str(datetime.time)).join('.jpg')
        # p.save(fp)
        return p1
    else:
        ratio = 1000 / height
        rw = int( width * ratio)
        size = (rw, 1000)
        # return p.resize(size, PIL.Image.ANTIALIAS)
        p1 = p.resize(size, PIL.Image.ANTIALIAS)
        # fp = '{0}/{1}/{2}'.format(str(datetime.date.year), str(datetime.date.month), str(datetime.time)).join('.jpg') attemps to generate filepath
        # p.save(fp)
        return p1

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

            list = Pic.objects.order_by('-rated')[:40]
            n = len(list)
            #random 2 in 20
            n1 = random.randrange(0,n,2)
            n2 = random.randrange(1,n-1,2)
            pics = [
                list[n1],
                list[n2]
            ]

            formchoices = [
                {
                    'value': pics[0].id,
                    'url': pics[0].picture,
                    'tag': pics[0].tag.name,
                    'id': 'id_choice_%s' % 0
                },
                {
                    'value': pics[1].id,
                    'url': pics[1].picture,
                    'tag': pics[1].tag.name,
                    'id': 'id_choice_%s' % 1
                }
            ]
            #render page and return forms for rate
            #form first and then fill with pic object.
            form = Rform(pics=pics, initial={'hidden_pic1': pics[0].id, 'hidden_pic2': pics[1].id})    #should be a list OMG
            # form.hidden_pic1 = pics[0].id
            # form.hidden_pic2 = pics[1].id
            logger.warning('form fields %s', str(form.fields['hidden_pic1']))
            #fill context with forms and other variables#maybe it should direct assign instead of use fields method
            context = {
                'form': form,
                'formchoices': formchoices
            }
            #TODO re build rate form by abandon choice field, generate another option, a complicated context! fill img url manuelly
            #Reason: impossible to use customized style in build in widgets like choice field.
            return render(request, 'rate.html', context)

    def post(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)  # redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        else:
            form = Rform2P(request.POST)
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
            k1 = float(300/(5+pic1.rated) + 20)
            k2 = float(300/(5+pic2.rated) + 20)
            win = form.cleaned_data['choice']
            #rated + 1 and update elo rating and save;
            if win == id1:
                #1 wins ,update the both rating:
                pic1.rating += int(k1*(1 - 1/(math.pow(10, float(pic2.rating - pic1.rating)/400) + 1)))
                pic2.rating += int(k2*(0 - 1/(math.pow(10, float(pic1.rating - pic2.rating)/400) + 1)))
                pic1.save()
                pic2.save()
            else:
                delta = float(pic2.rating - pic1.rating)
                pic1.rating += int(k1*(0 - 1/(math.pow(10,  delta/400) + 1)))
                pic2.rating += int(k2*(1 - 1/(math.pow(10, -delta/400) + 1)))
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
            formchoices = [
                {
                    'value': pics[0].id,
                    'url': pics[0].picture,
                    'tag': pics[0].tag.name,
                    'id': 'id_choice_%s' % 0
                },
                {
                    'value': pics[1].id,
                    'url': pics[1].picture,
                    'tag': pics[1].tag.name,
                    'id': 'id_choice_%s' % 1
                }
            ]
            #render and return form with initial for rate
            form = Rform(pics=pics, initial={'hidden_pic1': pic_id, 'hidden_pic2': item2.id})
            # form.fields['hidden_pic1'] = pic_id
            # form.fields['hidden_pic2'] = item2.pk
            context = {
                'form': form,
                'formchoices': formchoices
            }
            return render(request, 'rate.html', context)

class UploadView(View):
    # form_class = UploadForm()
    op_cache = {'key': 'value'} #is this a dict
    op_q = []
    tags = Tag.objects.filter(active=True)
    auth = oss2.Auth(nogit.AccessKeyID, nogit.AccessKeySecret)
    service = oss2.Service(auth, nogit.OSSENDPOINT, connect_timeout=15)
    bucket = oss2.Bucket(auth, nogit.OSSENDPOINT, nogit.BUCKET)
    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        logger.warning('welcome user %s' % openid)
        #lets make a choice field in upload form;
        # tags = Tag.objects.filter(active=True)
        tags = Tag.objects.filter(active=True)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)  # redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        o_id = random.randint(1, 300) #how long is this random? need review???
        self.op_cache[openid] = o_id #put the user and unique operation id to this dict, every post will chech the cache if this op is valide or duplicated
        #or use update: .update({openid: o_id})
        id_form = UploadForm(tags=tags, initial={'o_id': o_id})
        logger.warning('return o_id = %s ' % o_id)
        formchoice = []
        #generate choice array
        n = 0
        for tg in tags:
            formchoice.append({'value': tg.id, 'name': tg.name, 'id': 'id_choice_%s' % n })
            n += 1

        # form_class.fields['o_id'] = random.randint()
        return render(request, 'upload.html', {'form': id_form, 'formchoice': formchoice})

    def post(self, request, *args, **kwargs):
        # form = UploadForm2post(self.tags)
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)
        logger.debug('post uploaded triggered by {0}'.format(openid))
        uploaded = UploadForm2P(request.POST, request.FILES)
        if uploaded.is_valid():
            # openid = uploaded.cleaned_data['openid']
            # o_id = uploaded.cleaned_data['o_id']
            #above i get the data from the form and then goes to that dict
            # logger.warning('o_id equals %s' % o_id)
            # if self.op_cache.get(openid) == o_id:  debug not pass unique checking
            if True:
                pic = Pic()
                # pic.user = uploaded.cleaned_data['openid'] #change with no user connect
                pic.user = request.session.get('openid', 'anoymous')
                # pic.picture = uploaded.cleaned_data['picture'] #DONE size adjust, scale limit, tages auto generate; replace by models save rewrite;
                # see source: http: // stackoverflow.com / questions / 24745857 / python - pillow - how - to - scale - an - image
                # pic.picture = auto_resize(picture)  #must rewrite save method due to http://stackoverflow.com/questions/30434323/django-resize-image-before-upload
                pic.text = uploaded.cleaned_data['text']
                tag = uploaded.cleaned_data['choice']
                pic.tag = get_object_or_404(Tag, pk=tag)
                #no tag no permit
                if not pic.tag.active == True:
                    return render(request, 'rate.html')
                #try upload to oss and return path
                filebyte = makeimgurl.uploadImgHandler(request.FILES['picture'])
                if not filebyte:
                    logger.debug('=========================== wrong file byte ==============================')
                    return render(request, 'result.html', {'success': False})
                # resized = auto_resize(filebyte) #still not possible to use auto resize, must save to do it.
                try:

                    o_id = random.randint(1, 10000)
                    self.op_q.append(o_id)
                    logger.debug('----------------------------------------------o_id generated: {0}'.format(o_id))
                    pname = makeimgurl.imagename(request.FILES['picture'])
                    logger.debug('----------------------------------------------see pname: {0}'.format(pname))
                    result = self.bucket.put_object(pname, filebyte)
                    logger.debug('----------------------------------------------oss result {0}'.format(result.status))
                    print('http status: {0}'.format(result.status))
                    print('request_id: {0}'.format(result.request_id))
                    print('ETag: {0}'.format(result.etag))
                    print('date: {0}'.format(result.headers['date']))

                    pic.picture = 'http://{0}/{1}'.format(nogit.OSSEND2, pname)
                # pic.tag = 'default'
                    pic.save()
                    request.session['uploaded'] = True
                    picobj = {
                        'url': pic.picture,
                        'rating': pic.rating,
                        'rated': pic.rated,
                        'text': pic.text,
                        'tag': pic.tag.name
                    }

                    return render(request, 'result.html', {'success': True, 'picture': picobj})
                except:
                    logger.debug('----------------------------------------------exception unknow here')
                    return render(request, 'result.html', {'success': False})

            else:
                return render(request, 'result.html', {'success': False})
        else:
            return render(request, 'result.html', {'success': False})



class ResultView(View):
    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pic', False)
        if pk:
            pic = get_object_or_404(Pic, pk=pk)
            picobj = {
                'url': pic.picture,
                'rating': pic.rating,
                'rated': pic.rated,
                'text': pic.text,
                'tag': pic.tag.name
            }
            return render(request, 'result.html', {'mode': True, 'picture': picobj})
        else:
            pic = Pic.objects.all()[:1]
            picobj = {
                'url': pic[0].picture,
                'rating': pic[0].rating,
                'rated': pic[0].rated,
                'text': pic[0].text,
                'tag': pic[0].tag.name
            }
            return render(request, 'result.html', {'mode': True, 'picture': picobj})