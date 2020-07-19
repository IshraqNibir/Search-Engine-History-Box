from django.shortcuts import render
from .models import History
from django.http import JsonResponse
from django.db.models import Q
from datetime import date
from datetime import timedelta
# Create your views here.



def home(request):
    
    all_data = History.objects.all()
    users = sorted(list(set([data.user for data in all_data])))
    keywords = sorted(list(set([data.keyword for data in all_data])))
    durations = sorted(list(set([data.duration for data in all_data])))
    locations = sorted(list(set([data.location for data in all_data])))
    dates = sorted(list([data.date for data in all_data]))

    '''
        IGNORE THIS SECTION // dev,debug purpose
    
    user_search_results = []
    if request.method == 'POST':
        user_checks = request.POST.getlist("user_check")

        for user in user_checks:
            final_results = History.objects.filter(Q(user__contains=str(user)))
            user_search_results.append(final_results)
    '''
        
    return render(request,'history/index.html', {'users': users, 'keywords': keywords, 'durations': durations, 'locations': locations})


def search(request):
    '''
        IGNORE THIS SECTION // dev,debug purpose
    
    user = request.session.get('user_search_list', None)
    final_results = History.objects.filter(Q(user__contains="Ishraq") & Q(location__contains="Chittagong"))
    print(user_search_results)
    return JsonResponse({'results': list(user_search_results)}, status=200)
    '''
    
    user_search_results = {}
    keyword_search_results = {}
    duration_search_results = {}
    location_search_results = {}
    previous_browsing_results = {}
    before_search_results = {}

    Total_Objects = History.objects.all()
    length = len(Total_Objects)

    if request.method == 'POST':

        #Checking if any user is checked
        user_checks = request.POST.getlist("user_check")
        block = 0
        chk = False
        for user in user_checks:
            final_results = History.objects.filter(Q(user__contains=str(user)))
            single = {user:list(final_results.values())}
            lst = list(final_results.values())
            if len(lst) > 0 and chk == False:
                block += 1
                chk = True
            user_search_results.update(single)

        #Checking if any keyword is checked
        keywords_checks = request.POST.getlist("keyword_check")
        chk = False
        for keyword in keywords_checks:
            final_results = History.objects.filter(Q(keyword__contains=str(keyword)))
            single = {keyword:list(final_results.values())}
            lst = list(final_results.values())
            if len(lst) > 0 and chk == False:
                block += 1
                chk = True
            keyword_search_results.update(single)

        #Checking if any duration is checked
        durations_checks = request.POST.getlist("duration_check")
        chk = False
        for duration in durations_checks:
            final_results = History.objects.filter(Q(duration__lte=int(duration)))
            single = {duration:list(final_results.values())}
            lst = list(final_results.values())
            if len(lst) > 0 and chk == False:
                block += 1
                chk = True
            duration_search_results.update(single)

        #Checking if any location is checked
        locations_checks = request.POST.getlist("location_check")
        chk = False
        for location in locations_checks:
            final_results = History.objects.filter(Q(location__contains=str(location)))
            single = {location:list(final_results.values())}
            lst = list(final_results.values())
            if len(lst) > 0 and chk == False:
                block += 1
                chk = True
            location_search_results.update(single)

        #Checking if any time_period is checked
        time_checks = request.POST.getlist("time_check")
        if len(time_checks) > 0:
            block += 1
            today = date.today()
            skip = False
            if 'Last Month' in time_checks and skip == False:
               picked_date = today - timedelta(days=30)
               final_results = History.objects.filter(date__gt=(picked_date))
               single = {'previous':list(final_results.values())}
               previous_browsing_results.update(single)
               skip = True
            if 'Last Week' in time_checks and skip == False:
               picked_date = today - timedelta(days=7)
               final_results = History.objects.filter(date__gt=(picked_date))
               single = {'previous':list(final_results.values())}
               previous_browsing_results.update(single)
               skip = True
            if 'Today' in time_checks and skip == False:
               picked_date = today
               final_results = History.objects.filter(date__contains=(picked_date))
               single = {'previous':list(final_results.values())}
               previous_browsing_results.update(single)
 
        #Checking if any date is checked or not
        before_checks = request.POST.get("before_check")
        if before_checks != '':
            block += 1
            final_results = History.objects.filter(Q(date__lt=(before_checks)))
            single = {'prvs':list(final_results.values())}
            before_search_results.update(single)
  
        #Checking how many times an user id is selected among all the fields
        cnt = dict()
        cnt=dict.fromkeys(range(length+5),0)
        for key in user_search_results:
            for l in range(len(user_search_results[key])):
                cnt[user_search_results[key][l]['id']] += 1

        for key in keyword_search_results:
            for l in range(len(keyword_search_results[key])):
                cnt[keyword_search_results[key][l]['id']] += 1

        for key in duration_search_results:
            for l in range(len(duration_search_results[key])):
                cnt[duration_search_results[key][l]['id']] += 1
        
        for key in location_search_results:
            for l in range(len(location_search_results[key])):
                cnt[location_search_results[key][l]['id']] += 1

        for key in previous_browsing_results:
            for l in range(len(previous_browsing_results[key])):
                cnt[previous_browsing_results[key][l]['id']] += 1

        for key in before_search_results:
            for l in range(len(before_search_results[key])):
                cnt[before_search_results[key][l]['id']] += 1
        
        
    fin_putput = {}

    #If only one field is selected
    if block == 1:
        for i in range(length+1):
            if cnt[i] == 1:
                final_results = History.objects.filter(id=i)
                single = {i:list(final_results.values())}
                fin_putput.update(single)
    
    #If two field is selected
    elif block == 2:
        for i in range(length+1):
            if cnt[i] == 2:
                final_results = History.objects.filter(id=i)
                single = {i:list(final_results.values())}
                fin_putput.update(single)

    #If three field is selected
    elif block == 3:
        for i in range(length+1):
            if cnt[i] == 3:
                final_results = History.objects.filter(id=i)
                single = {i:list(final_results.values())}
                fin_putput.update(single)

    #If four field is selected
    elif block == 4:
        for i in range(length+1):
            if cnt[i] == 4:
                final_results = History.objects.filter(id=i)
                single = {i:list(final_results.values())}
                fin_putput.update(single)
    
    #If five field is selected
    elif block == 5:
        for i in range(length+1):
            if cnt[i] == 5:
                final_results = History.objects.filter(id=i)
                single = {i:list(final_results.values())}
                fin_putput.update(single)

    #If six field is selected
    elif block == 6:
        for i in range(length+1):
            if cnt[i] == 6:
                final_results = History.objects.filter(id=i)
                single = {i:list(final_results.values())}
                fin_putput.update(single)
    
    return JsonResponse(fin_putput)

    
    