#encoding=utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Position, Parking, Billing
from django.urls import reverse
from django.utils import timezone
# from django.template import loader
from django.shortcuts import render, get_object_or_404
#view class
from django.views import generic


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    position_list = Position.objects.all()[:10]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
        'position_list': position_list,
    }

    # output = ',  '.join([q.question_text for q in latest_question_list])


    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {
        'question': question
    })


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {
        'question': question
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoseNotExist ):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 100
        # question.choice_set.create(choice_text='auto added', votes=0)
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


def parkdetail(request, position_id):
    position = get_object_or_404(Position, pk=position_id)

    return render(request, 'polls/posdetail.html', {
        'position': position
    })

def dopark(request, park_id):
    position = get_object_or_404(Position, pk=park_id)
    p = position.parking_set.create(
        user=request.POST['uid']
    )

    return HttpResponseRedirect(reverse('polls:parks', args=(p.position.id,)))

def parks(request, pos_id):
    p = get_object_or_404(Position, pk=pos_id)
    # parking_list = get_object_or_404(Parking, 'position'=p).order_by('-starttime')[:10]
    parking_list = Parking.objects.filter(position=p).exclude(isend=True).order_by('-starttime')[:10]
    context = {
        'parking_list': parking_list,
    }

    return render(request, 'polls/parks.html', context)


def endpark(request, park_id):
    parking = get_object_or_404(Parking, pk=park_id)
    parking.end_parking()
    parking.save()
    x = (timezone.now() - parking.starttime).total_seconds()
    bill = parking.billing_set.create(
        amount=int(x/60),
        charger=parking.user
    )

    return render(request, 'polls/billrecords.html', { 'billing': bill})
