from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import Rform, UploadForm
from .models import User, Pic
import random
# Create your views here.

#here define the wechat api parameters.
#user and auth both use wechat pub xxx
WECHAT_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx1d3cfcf816c87d8b&redirect_uri=https%3A%2F%2Fwww.aishe.org.cn%2Fpark%2Flogin&response_type=code&scope=snsapi_base&state=123#wechat_redirect'


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
            #fill context with forms and other variables
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
            k1 = 500/pic1.rated + 16
            k2 = 500/pic2.rated + 16
            win = form.cleaned_data
            #rated + 1 and update elo rating and save;



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
    op_cache = {'': ''} #is this a dict
    def get(self, request, *args, **kwargs):
        openid = request.session.get('openid', None)
        if openid == None:
            return HttpResponseRedirect(
                WECHAT_URL)  # redirect to wechat authorize page. see http://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
        o_id = random.randint #how long is this random? need review???
        self.op_cache.update(openid, o_id)  #here TODO I need put the user and unique operation id to this dict, every post will chech the cache if this op is valide or duplicated
        id_form = UploadForm(initial={'o_id': o_id, 'openid': openid})
        # form_class.fields['o_id'] = random.randint()
        return render(request, 'upload.html', {'form': id_form})

    def post(self, request, *args, **kwargs):
        uploaded = UploadForm(request.POST, request.FILES)
        if uploaded.is_valid():
            openid = uploaded.cleaned_data['openid']
            o_id = uploaded.cleaned_data['o_id']
            #above i get the data from the form and then goes to that dict
            if self.op_cache.get(openid) == o_id:
                pic = Pic()
                pic.picture = uploaded.cleaned_data['picture'] #TODO size adjust, scale limit, tages auto generate
                pic.text = uploaded.cleaned_data['text']
                pic.save()
                request.session['uploaded'] = True
                return render(request, 'result.html', {'success': True})
            else:
                return render(request, 'result.html', {'success': False})
        else:
            return render(request, 'result.html', {'success': False})




