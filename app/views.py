from ast import Pass
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib import messages
from django.db import connection
from django.db.models import Avg, Count, Min, Sum, Q
from django.core import serializers
from django.db.models import F

import json
import base64
import re
import ast
import itertools
import csv
import io
import urllib3
import string
import random

#print("VIEWS ARE IMPORTED")

# hompepage
#    path('', user_views.homepage, name="homepage"),
def homepage(request):
    return render(request, 'app/index.html')

# public test ----------------------------------------------------
#   path('survey/', views.picksurvey, name="test-picksurvey"),
def picksurvey(request):
    return render(request, 'app/picksurvey.html')

#   path('survey/<testid>/start/<int:userid>', views.teststart, name="test-start"),
def teststart(request, testid, userid ):
    # get url parameters
    testid = int(testid)
    init_userid = int(userid)
    # get survey info
    get_survey = Survey.objects.get(id=testid)
    # post request
    if request.method == 'POST':
        # get survey
        user = request.user
        # START USER CREATION
        #form = NewSurveyUser(request.POST)
        user_data = {}
        if init_userid == 0: #and form.is_valid():
            try:
                redirect_to = get_survey.redirect_to
                redirect_to_id = redirect_to.id
                # get form data 
                for key, value in request.POST.items():
                    if key == "csrfmiddlewaretoken":
                        pass
                    elif key == 'formAdd':
                        pass
                    else:
                        user_data[key] = value
                user_data_json = json.dumps(user_data)#(user_data, indent = 4) 
                # sql add survey
                create_survey_user = SurveyUser.objects.create(
                    user_settings=user_data_json,
                    survey_id = testid
                    )
                userid = create_survey_user.id
                return redirect('app:test-start', testid=redirect_to_id, userid=userid)
            except: 
                return redirect('app:homepage')
        elif init_userid != 0:
            try:
                get_survey_user = SurveyUser.objects.get(
                    id=userid
                    )
                userid = get_survey_user.id
                return redirect('app:test-case', testid=testid, userid=userid, caseid=1)
            except: 
                return redirect('app:homepage')
        else:
            return redirect('app:homepage')
        # END USER CREATION
    # get request
    try:
        form_start = FormSurvey.objects.get(id=get_survey.form_start.id)
        # foreign key version
        text = form_start.text
        text_button = form_start.text_button
        print("if stops here form is wrong")
        form = eval(form_start.template_tag) # DANGEROUS
        print("form worked")
        context = {
            'form': form,
            'text': text,
            'survey_info': get_survey,
            'text_button': text_button,
            'help_title': get_survey.help_title,
            'help_text1': get_survey.help_text1,
            'help_text2': get_survey.help_text2
        }
        return render(request, 'app/survey-start.html', context=context)
    except:
        messages.error(request, f'Link was not valid')
        return redirect('app:homepage')

#    path('survey/<testid>/<userid>/<caseid>', views.testcase, name="test-case"),
def testcase(request, testid, userid, caseid):
    # get url parameters
    testid = testid
    userid = userid
    caseid = caseid
    nextid = caseid + 1
    previd = caseid - 1
    info = {'testid': testid, 'userid': userid, 'caseid': caseid, 'nextid': nextid, 'previd': previd}
    # hanlde survey case
    if int(caseid) == 1: #CHANGED  below case_id=1
        # user
        get_user = SurveyUser.objects.get(id=userid)
        user_variables_dict = ast.literal_eval(get_user.user_settings)
        user_gender = user_variables_dict["gender"]
        # survey
        get_survey = Survey.objects.get(id=testid)
        suvery_language = get_survey.language
        survey_variables_dict =  ast.literal_eval(get_survey.variables)
        survey_lenght = int(survey_variables_dict["lenght"])
        survery_max_lenght = get_survey.max_cases
        survey_half = survery_max_lenght / 2
        survey_variables = survey_variables_dict["variables"]
        print("Check if its last survey: ")
        print(get_survey.last_survey)
        print("Check survey cases:")
        print(survery_max_lenght)
        # CREATE LOGIC FOR RANDOMIZER AND TEST creation
        # survey zero
        if get_survey.survey_zero: 
            #print("---------------------- survey_zero ----------------------------------")
            # calculate all possible cases
            survey_variables_list = []
            #print("init survey_zero cases")
            for key, value in survey_variables.items():
                #print(f'key: {key}, value: {value}')
                temp_list = []
                segment_1_list = []
                segment_2_list = []
                for k, v in value.items():
                    #print(f'INNER LOOP key: {k}, value: {v}')
                    if k == "templates":
                        for template_id in v:
                            # get template settings
                            get_template = VariableTemplates.objects.get(id=template_id)
                            template_language = get_template.language
                            template_gender = get_template.gender
                            template_segment_id = get_template.segment_id
                            template_counter = get_template.counter
                            template_zero = get_template.zero_template
                            #print(f'is zero: {template_zero} language: {template_language} gender: {template_gender} segment_id:{template_segment_id}')
                            # add if template matches survey settings
                            if template_zero == True:
                                temp_list.append(template_id)
                            elif (template_language == suvery_language) and (template_gender == user_gender or template_gender == "X"):
                                    if template_segment_id == 1:
                                        segment_1_list.append(template_id)
                                        #print(f'template id: {template_id} added to segment list 1')
                                    elif template_segment_id == 2:
                                        segment_2_list.append(template_id)
                                        #print(f'template id: {template_id} added to segment list 2')
                                    else:
                                        #print(f'passed, template_segment_id = {template_segment_id} ')
                                        pass   
                            else:
                                #print(f'template_segment_id = {template_segment_id} ')
                                pass
                #print("Segment list:")
                #print(segment_1_list)
                #print(segment_2_list)
                if len(segment_1_list) == 0 and len(segment_2_list) == 0:
                    pass
                else:
                    #print("Segment query result:")
                    query_segment_1 = VariableTemplates.objects.filter(id__in=segment_1_list).order_by('counter')[:survey_half].values_list('id', flat=True)
                    for template in query_segment_1:
                        temp_list.append(template)
                        template = VariableTemplates.objects.get(id=template)
                        template.counter = template.counter + 1
                        template.save()
                    #print(query_segment_1)
                    query_segment_2 = VariableTemplates.objects.filter(id__in=segment_2_list).order_by('counter')[:survey_half].values_list('id', flat=True)
                    for template in query_segment_2:
                        temp_list.append(template)
                        template = VariableTemplates.objects.get(id=template)
                        template.counter = template.counter + 1
                        template.save()
                    #print(query_segment_2)
                #print("Temp list:")
                #print(temp_list)  
                survey_variables_list.append(temp_list) 
            print(f'survey_variables_list: {survey_variables_list}')
            final_list = list(itertools.product(*survey_variables_list)) 
            #print(f'final list: {final_list}')
        # normal survey
        if get_survey.last_survey:
            print("---------------------- last_survey ----------------------------------")
            # calculate all possible cases
            survey_variables_list = []
            zero_variables_list = []
            # get which cases to cover
            value_list = CounterSurvey.objects.values('counter').distinct().count()
            print(f"value list: {int(value_list)}")
            if int(value_list) == 1:
                print("random cases----------------------")
                cases = random.choices(CounterSurvey.objects.all().values(), k=survery_max_lenght)
            else:
                print("db call cases----------------------")
                cases = CounterSurvey.objects.all().order_by('counter')[:survery_max_lenght].values()
            # get user selected templates
            user_settings_dict = ast.literal_eval(get_user.user_settings)
            print(user_settings_dict)
            print(get_user.user_choiche)
            print(type(get_user.user_choiche))
            user_choiche_dict = get_user.user_choiche
            for key, value in user_choiche_dict.items():
                if key == '3':
                    for k, v in value.items():
                        if k == '1':
                            case_se_true = v
                        else:
                            case_se_false = v
                if key == '4':
                    for k, v in value.items():
                        if k == '1':
                            case_co_true = v
                        else:
                            case_co_false = v
            # get survey templates
            for key, value in survey_variables.items():
                if key.lower() == 'tr':
                    for k, v in value.items():
                        if k == 'templates':
                            for id_template in v:
                                template_check = VariableTemplates.objects.get(id=id_template)
                                if template_check.segment_id == 1:
                                    case_tr_true = id_template
                                else:
                                    case_tr_false = id_template
                if key.lower() == 'cm':
                    for k, v in value.items():
                        if k == 'templates':
                            for id_template in v:
                                template_check = VariableTemplates.objects.get(id=id_template)
                                if template_check.segment_id == 1:
                                    case_cm_true = id_template
                                else:
                                    case_cm_false = id_template
            print("VARIABLES:")
            print(case_se_true)
            print(case_se_false)
            print(case_co_true)
            print(case_co_false)
            print(case_tr_true)
            print(case_tr_false)
            print("END VARIABLES")
            # hanlde cases
            final_list = []
            list_counter_id = []
            print(f'cases: {cases}')
            for case in cases:
                # init
                case_list = []
                case_id = case['id']
                case_unique_id = case['unique_id']
                case_co = case['co']
                case_tr = case['tr']
                case_se = case['se']
                #case_cm = case['cm']
                case_counter = case['counter']
                # update counter
                new_counter = int(case_counter) + 1
                update_counter = CounterSurvey.objects.filter(id=case_id).update(counter=new_counter)
                # define templates
                # co
                if case_co:
                    new_co = case_co_true
                else:
                    new_co = case_co_false
                case_list.append(new_co)
                # tr
                if case_tr:
                    new_tr = case_tr_true
                else:
                    new_tr = case_tr_false
                case_list.append(new_tr)
                # se
                if case_se:
                    new_se = case_se_true
                else:
                    new_se = case_se_false
                case_list.append(new_se)
                # cm
                #if case_cm:
                #    new_cm = case_cm_true
                #else:
                #    new_cm = case_cm_false
                #case_list.append(new_cm)
                # update lists
                list_counter_id.append(case_id)
                final_list.append(case_list)
                print(f'case_list: {case_list}')
            print(f'final_list: {final_list}') # result ex: [ [1,3,5,7], [2,4,6,8], [1,4,6,8], [2,3,5,7] ]
        # initialize case settings
        for i in range(1,survery_max_lenght+1):
            #print(f'i= {i}')
            variable_id_list = []
            template_id_list = []
            name_list = []
            settings_list = []
            segment_list = []
            text_internal_list = []
            text_external_list = []
            code_html_list = []
            code_css_list = []
            code_js_list = []
            template_id_list = []
            template_id_tested = 0
            counter_survey_id = 0
            case_settings = {
                    'variable_id': variable_id_list,
                    'template_id_list': template_id_list, 
                    'name': name_list,
                    'settings': settings_list,
                    'segment': segment_list,
                    'text_internal': text_internal_list,
                    'text_external': text_external_list,
                    'code_html':  code_html_list,
                    'code_css': code_css_list,
                    'code_js': code_js_list
                    }
            # print final list
            print(f'final list: {final_list}')
            case_list = final_list[i-1]
            for template_id in case_list:
                print(f'init template: {template_id}')
                template_settings = VariableTemplates.objects.get(id=template_id)
                variable_id_list.append(template_settings.variable_id.id)
                template_id_list.append(template_settings.id) # here
                try:
                    if template_settings.variable_id.id == get_survey.suvery_var_cat_id.id:
                        template_id_tested = template_settings.id
                except:
                    pass
                try:
                    counter_survey_id = list_counter_id[i-1]
                except:
                    pass
                name_list.append(template_settings.name)
                settings_list.append(template_settings.settings)
                segment_list.append(template_settings.segment)
                text_internal_list.append(template_settings.text_internal)
                code_html_list.append(template_settings.code_html)
                code_css_list.append(template_settings.code_css)
                code_js_list.append(template_settings.code_js)
            case_settings = {
                'variable_id': variable_id_list,
                'template_id_list': template_id_list,
                'template_id_tested': template_id_tested,
                'name': name_list,
                'settings': settings_list,
                'segment': segment_list,
                'text_internal': text_internal_list,
                'text_external': text_external_list,
                'code_html':  code_html_list,
                'code_css': code_css_list,
                'code_js': code_js_list,
                'counter_survey_id': counter_survey_id
                }
            case_answer = {}
            case_settings_json = json.dumps(case_settings)#, indent = 4)
            case_answer_json = json.dumps(case_answer)#, indent = 4)
            new_survey_case = SurveyCase.objects.create(
                survey_id = get_survey,
                survey_user_id = get_user,
                case_id = i,
                case_settings = case_settings_json,
                case_answer = case_answer_json,
                )
        # END LOGIC
        survey_case_settings = SurveyCase.objects.get(case_id=caseid, survey_id=testid, survey_user_id=userid)
        ##print(f'survey_case_settings: {survey_case_settings.case_settings}')
        case_settings =  ast.literal_eval(survey_case_settings.case_settings)
        survey = Survey.objects.get(id=testid)
        form_case = FormSurvey.objects.get(name=survey.form_survey)
        form = eval(form_case.template_tag)
        text = form_case.text
        text_button = form_case.text_button
        ads_link = ""
        # get length and save it to survey_settings 
        #survey_settings_dict =  ast.literal_eval(survey.variables)
        #survey_settings = survey_settings_dict["lenght"]
        survey_lenght = survey.max_cases
        # build the cases code
        for i in range(len(case_settings['code_html'])):
            if "ADLINK" in case_settings['code_html'][i]:
                ads_link = case_settings['code_html'][i]
                ads_link = ads_link.replace('ADLINK ', ' ')
                #print("adlink was found")
                case_settings['code_html'][i] = "<span style='display:none;'>ads was replaced correctly</span>"
        for i in range(len(case_settings['code_html'])):
            if "ADSPACE" in case_settings['code_html'][i]:
                case_settings['code_html'][i] = case_settings['code_html'][i].replace("ADSPACE", ads_link)
        context = {
            'variable_id': case_settings['variable_id'],
            'name': case_settings['name'],
            'settings': case_settings['settings'],
            'segment': case_settings['segment'],
            'text_internal': case_settings['text_internal'],
            'text_external': case_settings['text_external'],
            'code_html': case_settings['code_html'],
            'code_css': case_settings['code_css'],
            'code_js': case_settings['code_js'],
            'form': form,
            'text_button': text_button,
            'text': text,
            'info': info,
            'title_case': survey.title_case,
            'title_question': survey.title_question,
            'survey_lenght': survey_lenght,
            'help_title': survey.help_title,
            'help_text1': survey.help_text1,
            'help_text2': survey.help_text2
            }
        return render(request, 'app/survey-case.html', context=context)
    # post request
    elif request.method == 'POST':
        # get form data 
        case_answer_dict = {}
        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken":
                pass
            elif key == "formAnswer":
                pass
            else:
                case_answer_dict[key] = value
        survery_to_update = SurveyCase.objects.get(case_id=previd, survey_id=testid, survey_user_id=userid)
        case_answer_json = json.dumps(case_answer_dict)
        survery_to_update.case_answer = case_answer_json
        #print("CASE ANSWER DICT!!!")
        ##print(case_answer_dict)
        survery_to_update.save()
        check_survey = SurveyCase.objects.get(case_id=previd, survey_id=testid, survey_user_id=userid)
        # sql add survey
        get_survey = Survey.objects.get(id=testid)
        survey_user_id = SurveyUser.objects.get(id=userid)
        case_id = caseid
        # get form stuff
        survey_id = Survey.objects.get(id=testid)
        # get length and save it to survey_settings 
        #survey_settings_dict =  ast.literal_eval(survey_id.variables)
        #survey_settings = survey_settings_dict["lenght"]
        survey_lenght = survey_id.max_cases
        # ---
        survey_limit = survey_lenght + 1 #CHANGED
        if caseid <= survey_lenght:
            survey_case_settings = SurveyCase.objects.get(case_id=caseid, survey_id=testid, survey_user_id=userid)
            ##print(f'survey_case_settings: {survey_case_settings.case_settings}')
            case_settings =  ast.literal_eval(survey_case_settings.case_settings)
            survey = Survey.objects.get(id=testid)
            form_case = FormSurvey.objects.get(name=survey.form_survey)
            form = eval(form_case.template_tag)
            text = form_case.text
            text_button = form_case.text_button
            ads_link = ""
            for i in range(len(case_settings['code_html'])):
                if "ADLINK" in case_settings['code_html'][i]:
                    ads_link = case_settings['code_html'][i]
                    ads_link = ads_link.replace("ADLINK ","")
                    #print("adlink was found and replaced")
                    case_settings['code_html'][i] = "<span style='display:none;'>ads was replaced correctly</span>"
            for i in range(len(case_settings['code_html'])):
                if "ADSPACE" in case_settings['code_html'][i]:
                    case_settings['code_html'][i] = case_settings['code_html'][i].replace("ADSPACE", ads_link)
                    #print(f"adspace was found and replaced with {ads_link}")
            context = {
                'variable_id': case_settings['variable_id'],
                'name': case_settings['name'],
                'settings': case_settings['settings'],
                'segment': case_settings['segment'],
                'text_internal': case_settings['text_internal'],
                'text_external': case_settings['text_external'],
                'code_html': case_settings['code_html'],
                'code_css': case_settings['code_css'],
                'code_js': case_settings['code_js'],
                'form': form,
                'text_button': text_button,
                'text': text,
                'info': info,
                'title_case': survey.title_case,
                'title_question': survey.title_question,
                'survey_lenght': survey_lenght,
                'help_title': survey.help_title,
                'help_text1': survey.help_text1,
                'help_text2': survey.help_text2
                }
            return render(request, 'app/survey-case.html', context=context)
        elif caseid == survey_limit:
            return redirect('app:test-end', testid=testid, userid=userid)
        else:
            messages.error(request, f'Survey attempt was not valid, please start again')
            return redirect('app:test-start', testid=testid)
    else:
        messages.error(request, f'Survey attempt was not valid, please start again')
        return redirect('app:test-start', testid=testid)

#    path('survey/<testid>/<userid>/end', views.testend, name="test-case"),
def testend(request, testid, userid):
    # get url parameters
    testid = testid
    userid = userid
    # start calculation
    get_survey = Survey.objects.get(id=testid)
    get_user = SurveyUser.objects.get(id=userid)
    get_answers = SurveyCase.objects.filter(survey_user_id=userid, survey_id=testid).exclude(case_id=0)
    #for answer in get_answers:
        ##print(f"case_settings: {answer.case_settings}")
        ##print(f"case_answer: {answer.case_answer}")
        ##print("--------------------------------")
    # START TEST
    if get_survey.survey_zero == True:
        # INIT
        choices_dict = {}
        for answer in get_answers:
            case_settings = ast.literal_eval(answer.case_settings)
            case_answer =  ast.literal_eval(answer.case_answer)
            # get template id
            for key, value in case_settings.items():
                if key == "template_id_tested":
                    template_id = value
            # get value
            for key, value in case_answer.items():
                if key == "value":
                    answer_value = value
            choices_dict[template_id] = answer_value
        # find min and max_cases
        seg_1_template = max(choices_dict, key=choices_dict.get)
        seg_2_template = min(choices_dict, key=choices_dict.get)
        # put min and max in temp_dict
        temp_dict = {}
        temp_dict["1"] = str(seg_1_template)
        temp_dict["2"] = str(seg_2_template)
        # save user_choiche of user
        initial_dict = get_user.user_choiche
        initial_dict[get_survey.suvery_var_cat_id.id] = temp_dict
        get_user.user_choiche = initial_dict
        get_user.save()
        
        # create dict for user_choiche
        #segment_dict = {}
        #segment_dict[get_survey.suvery_var_cat_id.id] = temp_dict
        #segment_json = json.dumps(segment_dict, indent = 4) 
        #get_user.user_choiche = segment_json
        #get_user.save()
    # END
    # get templated IDs to update
    # CODE 3
    # end
    redirect = {
    'survey_end_text': get_survey.survey_end_text,
    'last_survey': get_survey.last_survey,
    'redirect_to': get_survey.redirect_to,
    'userid': userid
    }
    ##print(f'last_survey: {get_survey.last_survey}; redirect_to: {get_survey.redirect_to}; userid: {userid}.')
    # end caluclation
    answers_list = []
    for answer in get_answers:
        case_answer =  ast.literal_eval(answer.case_answer)
        answer_list= []
        for key, value in case_answer.items():
            answer_list.append(key + ": " + value + "; ")
        answers_list.append(answer_list)
    # update values
    context = {
        'answers_list': answers_list,
        'redirect': redirect
    }
    return render(request, 'app/survey-end.html', context=context)

# private test -----------------------------------------------------
#    path('survey/create', views.testcreate, name="test-create"), 
@login_required
def testcreate(request):
    # post request
    if request.method == 'POST':
        try:
            user = request.user
            form = CreateSurvey(request.POST)
            if form.is_valid(): 
                # get form data  
                name = form.cleaned_data['name']
                language = form.cleaned_data['language']
                description = form.cleaned_data['description']
                survey_end_text = form.cleaned_data['survey_end_text']
                first_survey = form.cleaned_data['first_survey']
                survey_zero = form.cleaned_data['survey_zero']
                redirect_to = form.cleaned_data['redirect_to']
                last_survey = form.cleaned_data['last_survey']
                # sql add survey
                if redirect_to == None:                    
                    add_survey_no_parent = Survey.objects.get_or_create(
                        user_id=user,
                        name=name, 
                        language=language,
                        description=description,
                        survey_end_text=survey_end_text,
                        first_survey=first_survey,
                        survey_zero= survey_zero,
                        last_survey=last_survey
                        )
                else:
                    redirect_to_id = Survey.objects.get(id=redirect_to.id)
                    add_survey_with_parent = Survey.objects.get_or_create(
                        user_id=user,
                        name=name, 
                        language=language,
                        description=description,
                        survey_end_text=survey_end_text,
                        first_survey=first_survey, 
                        survey_zero= survey_zero,
                        redirect_to=redirect_to,
                        last_survey=last_survey
                        )                   
                messages.success(request, f'Survey {name} created successfully')
                return redirect('app:test-create', )
            else:
                messages.error(request, f'Form was not valid')
                return redirect('app:test-create', )
        except:
            messages.error(request, f'Survey creation failed')
            return redirect('app:test-create', )
    # get request
    form = CreateSurvey()
    surveys = Survey.objects.all()
    context = {
        'form': form,
        'surveys': surveys,
    }
    return render(request, 'app/surveys.html', context=context)

#    path('create/settings/', views.testcreatesettings, name="test-createsettings"),
@login_required
def testcreatesettings(request):
    # post request
    if request.method == 'POST':
        # FORM => formNewVariablesCategory
        if 'deleteStuff' in request.POST:
            try:
                SurveyUser.objects.all().delete()
                SurveyCase.objects.all().delete()
                FinalUsers.objects.all().delete()
                FinalSurveyZero.objects.all().delete()
                FinalSurvey.objects.all().delete()
                messages.success(request, 'deleteStuff successfully')
                return redirect('app:test-createsettings', )
            except:
                messages.error(request, 'deleteStuff failed')
                return redirect('app:test-createsettings', )
        if 'addNewVariablesCategory' in request.POST:
            formNewVariablesCategory = NewVariablesCategory(request.POST)
            try:
                if formNewVariablesCategory.is_valid():
                    # get form data
                    tag = formNewVariablesCategory.cleaned_data['tag']
                    name = formNewVariablesCategory.cleaned_data['name']
                    description = formNewVariablesCategory.cleaned_data['description']
                    max_segments = int(formNewVariablesCategory.cleaned_data['max_segments'])
                    # sql add survey
                    add_variable = VariablesCategory.objects.create(
                        tag=tag,
                        name=name, 
                        description=description, 
                        max_segments=max_segments)
                    messages.success(request, f'Variable {name} created successfully')
                    return redirect('app:test-createsettings', )
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-createsettings', )
            except:
                messages.error(request, f'Variable creation failed')
                return redirect('app:test-createsettings', )
        if 'addNewVariableTemplate' in request.POST:
            form_edit_template = NewVariableTemplates(request.POST)
            try:
                if form_edit_template.is_valid():            
                    # get form data  
                    variable_id = form_edit_template.cleaned_data['variable_id']
                    name = form_edit_template.cleaned_data['name']
                    text_external = form_edit_template.cleaned_data['text_external']
                    text_internal = form_edit_template.cleaned_data['text_internal']
                    code_html = form_edit_template.cleaned_data['code_html']
                    code_css = form_edit_template.cleaned_data['code_css']
                    code_js = form_edit_template.cleaned_data['code_js']
                    zero_template = form_edit_template.cleaned_data['zero_template']
                    language = form_edit_template.cleaned_data['language']
                    segment_id = form_edit_template.cleaned_data['segment_id']
                    #print(variable_id, name)
                    # sql add survey
                    variable_obj = VariablesCategory.objects.get(id=variable_id.id)
                    create_template = VariableTemplates.objects.get_or_create(
                        variable_id = variable_obj,
                        name = name,  
                        text_external = text_external,
                        text_internal = text_internal,
                        code_html = code_html,
                        code_css = code_css,
                        code_js = code_js,
                        zero_template= zero_template,
                        language = language,
                        segment_id = segment_id
                        )
                    messages.success(request, f'Template created successfully')
                    return redirect('app:test-createsettings', ) 
                else:
                    messages.error(request, f'Form Template was not valid')
                    return redirect('app:test-createsettings', ) 
            except:
                messages.error(request, f'Create template failed')
                return redirect('app:test-createsettings', ) 
        if 'addFormCounter' in request.POST:
            form = FormCounterSurvey(request.POST)
            if form.is_valid():
                unique_id = form.cleaned_data['unique_id']
                co = form.cleaned_data['co']
                tr = form.cleaned_data['tr']
                se = form.cleaned_data['se']
                #cm = form.cleaned_data['cm'] 
                # sql add survey
                #print("FormCounterSurvey")
                add_form = CounterSurvey.objects.create(
                    unique_id = unique_id,
                    co = co,
                    tr = tr,
                    se = se,
                    #cm = cm,
                    )
                #print("IT WORKS!!!")
                messages.success(request, f'addFormCounter was updated ')
                return redirect('app:test-createsettings')
            else:
                messages.success(request, f'addFormCounter could not be updated ')
                return redirect('app:test-createsettings')      
        if 'formSurvey' in request.POST:
            formSurvey = NewForm(request.POST)
            try:
                if formSurvey.is_valid(): 
                    # get form data  
                    form_name = formSurvey.cleaned_data['name']
                    form_language = formSurvey.cleaned_data['language']
                    form_text = formSurvey.cleaned_data['text']
                    django_form_name = formSurvey.cleaned_data['django_form_name']
                    is_start = formSurvey.cleaned_data['is_start']
                    template_tag = formSurvey.cleaned_data['template_tag']
                    text_button = formSurvey.cleaned_data['text_button']
                    # sql add survey
                    add_form = FormSurvey.objects.create(
                        name=form_name,
                        language = form_language,
                        text = form_text,
                        django_form_name = django_form_name,
                        template_tag = template_tag,
                        is_start = is_start,
                        text_button = text_button
                        )
                    messages.success(request, f'Form was updated ')
                    return redirect('app:test-createsettings')
                else:
                    messages.success(request, f'Form could not be updated ')
                    return redirect('app:test-createsettings')
            except:
                messages.error(request, f'Edit forms failed')
                return redirect('app:test-createsettings') 
        else:
            messages.error(request, f'Form was not valid')
            return redirect('app:test-createsettings', )               
    # get request
    else:
        #forms
        formSurvey = NewForm()
        formNewVariableTemplates = NewVariableTemplates()
        formNewVariablesCategory = NewVariablesCategory()
        formCounterSurvey = FormCounterSurvey()
        # sql
        forms = FormSurvey.objects.all()
        templates = VariableTemplates.objects.all()
        variables_category = VariablesCategory.objects.all()
        counters = CounterSurvey.objects.all()
        context = {
            'formSurvey': formSurvey,
            'formNewVariableTemplates': formNewVariableTemplates,
            'formNewVariablesCategory': formNewVariablesCategory,
            'variables_category': variables_category,
            'templates': templates,
            'forms':forms,
            'formCounterSurvey': formCounterSurvey,
            'counters':counters
        }
        return render(request, 'app/main-settings.html', context=context)

#    path('survey/<testid>/settings', views.testsettings, name="test-settings"),
@login_required
def testsettings(request, testid):
    # get url parameters
    testid = testid
    # post request
    if request.method == 'POST':
        # FORM =>
        if 'formEditInternalText' in request.POST:
            user = request.user
            formEditInternalText = InternalTextSurvey(request.POST)
            try:
                if formEditInternalText.is_valid(): 
                    # get form data  
                    name = formEditInternalText.cleaned_data['name']
                    description = formEditInternalText.cleaned_data['description']
                    # sql add survey
                    edit_survey = Survey.objects.get(id=testid)
                    edit_survey.name = formEditInternalText.cleaned_data.get('name')
                    edit_survey.description = formEditInternalText.cleaned_data.get('description')
                    edit_survey.help_title = formEditInternalText.cleaned_data.get('help_title')
                    edit_survey.help_text1 = formEditInternalText.cleaned_data.get('help_text1')
                    edit_survey.help_text2 = formEditInternalText.cleaned_data.get('help_text2')
                    edit_survey.save()
                    messages.success(request, f'Internal text updated successfully')
                    return redirect('app:test-settings', testid=testid)
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-settings', testid=testid)
            except:
                messages.error(request, f'Edit internal text failed')
                return redirect('app:test-settings', testid=testid)
        elif 'formEditSettings' in request.POST:
            user = request.user
            formEditSettings = SettingsSurvey(request.POST)
            try:
                if formEditSettings.is_valid(): 
                    # get form data  
                    first_survey = formEditSettings.cleaned_data['first_survey']
                    last_survey = formEditSettings.cleaned_data['last_survey']
                    survey_zero = formEditSettings.cleaned_data['survey_zero']
                    redirect_to = formEditSettings.cleaned_data['redirect_to']
                    max_cases = formEditSettings.cleaned_data['max_cases']
                    language = formEditSettings.cleaned_data['language']
                    suvery_var_cat_id = formEditSettings.cleaned_data['suvery_var_cat_id']
                    # sql add survey
                    edit_survey = Survey.objects.get(id=testid)
                    edit_survey.first_survey = first_survey
                    edit_survey.last_survey = last_survey
                    edit_survey.survey_zero = survey_zero
                    edit_survey.redirect_to = redirect_to
                    edit_survey.max_cases = max_cases
                    edit_survey.language = language
                    edit_survey.suvery_var_cat_id = suvery_var_cat_id
                    edit_survey.save()
                    messages.success(request, f'Settings type survey updated successfully')
                    return redirect('app:test-settings', testid=testid)
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-settings', testid=testid)
            except:
                messages.error(request, f'Edit settings type failed')
                return redirect('app:test-settings', testid=testid)           
        elif 'formEditExternalText' in request.POST:
            user = request.user
            formEditExternalText = ExternalTextSurvey(request.POST)
            try:
                if formEditExternalText.is_valid(): 
                    # get form data  
                    external_title = formEditExternalText.cleaned_data['external_title']
                    external_subtitle = formEditExternalText.cleaned_data['external_subtitle']
                    external_description = formEditExternalText.cleaned_data['external_description']
                    external_faq = formEditExternalText.cleaned_data['external_faq']
                    external_privacy = formEditExternalText.cleaned_data['external_privacy']
                    title_question = formEditExternalText.cleaned_data['title_question']
                    title_case = formEditExternalText.cleaned_data['title_case']
                    survey_end_text = formEditExternalText.cleaned_data['survey_end_text']
                    # sql add survey
                    edit_survey = Survey.objects.get(id=testid)
                    edit_survey.external_title = external_title
                    edit_survey.external_subtitle = external_subtitle
                    edit_survey.external_description = external_description
                    edit_survey.external_faq = external_faq
                    edit_survey.external_privacy = external_privacy
                    edit_survey.title_case = title_case
                    edit_survey.title_question = title_question
                    edit_survey.survey_end_text = survey_end_text
                    edit_survey.save()
                    messages.success(request, f'External text updated successfully')
                    return redirect('app:test-settings', testid=testid)
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-settings', testid=testid)
            except:
                messages.error(request, f'Edit external text failed')
                return redirect('app:test-settings', testid=testid)
        elif 'formEditVariablesSubmit' in request.POST:
            formEditVariables = request.POST["formEditVariablesSubmit"]
            get_tags = VariablesCategory.objects.all()
            variable_dict = {}
            variable_dict["variables"] = {}
            counter_lenght_survey = 1
            try:
                survey_info = Survey.objects.get(id=testid)
                survey_language = survey_info.language
                if survey_info.survey_zero == False or survey_info.survey_zero == True:
                    for key in request.POST:
                        if key == "csrfmiddlewaretoken":
                            pass
                        elif key == "formEditVariablesSubmit":
                            pass
                        else:
                            new_dict = {}
                            new_dict["amount"] = request.POST[key]
                            new_dict["templates"] = []
                            variable_dict["variables"][key] = new_dict
                            if int(request.POST[key]) == 0:
                                pass
                            else:
                                counter_lenght_survey = counter_lenght_survey * int(request.POST[key])
                    # prepare json
                    variable_dict["lenght"] = counter_lenght_survey
                    new_variable_dict = variable_dict.copy()
                    for key, value in variable_dict["variables"].items():
                        # set parameters for search
                        parent_test = survey_info.redirect_to
                        amount = value["amount"]
                        templates = value["templates"]
                        # sql
                        if int(amount) > 0:
                            variable_id = VariablesCategory.objects.get(tag=key)
                            variable_templates = VariableTemplates.objects.filter(variable_id=variable_id, language=survey_language).exclude(zero_template=True)[0:int(amount)]
                            for template in variable_templates:
                                templates.append(str(template.id))
                        if int(amount) == 0:
                            variable_id = VariablesCategory.objects.get(tag=key)
                            zero_template = VariableTemplates.objects.get(variable_id=variable_id, zero_template=True)
                            templates.append(str(zero_template.id))
                    variables_json = json.dumps(variable_dict, indent = 4) 
                    # sql add survey
                    edit_survey = Survey.objects.get(id=testid)
                    edit_survey.variables = variables_json
                    edit_survey.save()
                    # new stuff hope :)
                    messages.success(request, f'Variables updated successfully')
                    return redirect('app:test-settings', testid=testid)
                else:
                    Pass
                    # new stuff hope :)
            except:
                messages.error(request, f'Edit forms  failed')
                return redirect('app:test-settings', testid=testid)               
        elif 'formEditForms' in request.POST:
            formEditForms = MultiChoiceForm(request.POST)
            try:
                if formEditForms.is_valid(): 
                    # get form data
                    #print("FORM 1")
                    form_survey = formEditForms.cleaned_data['forms']
                    # sql add survey
                    form_info = FormSurvey.objects.get(name=form_survey)
                    edit_survey = Survey.objects.get(id=testid)
                    #print("FORM 2")
                    #form_settings = {'form_id': form_info.id,'text': form_info.text,'template_tag': form_info.template_tag,}
                    #form_dict_json = json.dumps(form_settings, indent = 4)
                    #edit_survey.form_survey = form_dict_json
                    edit_survey.form_survey = form_info
                    edit_survey.save()
                    #print("FORM 3")
                    messages.success(request, f'Survey forms updated successfully')
                    return redirect('app:test-settings', testid=testid)
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-settings', testid=testid)
            except:
                messages.error(request, f'Form was not valid')
                return redirect('app:test-settings', testid=testid)
        elif 'formStart' in request.POST:
            formStart = FormStartChoice(request.POST)
            try:
                if formStart.is_valid(): 
                    # get form data  
                    form_start = formStart.cleaned_data['forms']
                    # sql add survey
                    form_info = FormSurvey.objects.get(name=form_start)
                    edit_survey = Survey.objects.get(id=testid)
                    #form_settings = {'form_id': form_info.id,'text': form_info.text,'template_tag': form_info.template_tag,}
                    #form_dict_json = json.dumps(form_settings, indent = 4)
                    #edit_survey.form_start = form_dict_json
                    edit_survey.form_start = form_info
                    edit_survey.save()
                    messages.success(request, f'Start form text updated successfully')
                    return redirect('app:test-settings', testid=testid)
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-settings', testid=testid)
            except:
                messages.error(request, f'Form was not valid')
                return redirect('app:test-settings', testid=testid)
        else:
            messages.error(request, f'Form was not valid')
            return redirect('app:test-settings', testid=testid)
    # get request
    else:
        # sql queries
        survey_info = Survey.objects.get(id=testid)
        if survey_info.first_survey == True:
            survey_cases = SurveyUser.objects.filter(survey_id=testid)
        else:
            survey_cases = SurveyCase.objects.filter(survey_id=testid)#.values('survey_user_id').annotate(dcount=Count('id'))
        settings_info = survey_info.variables
        if bool(settings_info) == False:
            settings_info = ""
        else:
            settings_info = ast.literal_eval(settings_info)
        # init forms
        formEditInternalText = InternalTextSurvey(initial={
            "name": survey_info.name, 
            "description": survey_info.description,
            "help_title": survey_info.help_title,
            "help_text1": survey_info.help_text1,
            "help_text2": survey_info.help_text2
            })
        formEditSettings = SettingsSurvey(initial={
            "first_survey": survey_info.first_survey, 
            "survey_zero": survey_info.survey_zero, 
            "redirect_to": survey_info.redirect_to,
            "last_survey": survey_info.last_survey,
            "max_cases": survey_info.max_cases,
            "language": survey_info.language,
            "suvery_var_cat_id": survey_info.suvery_var_cat_id
            })
        formEditExternalText = ExternalTextSurvey(initial={
            "external_title": survey_info.external_title, 
            "external_subtitle": survey_info.external_subtitle, 
            "external_description": survey_info.external_description,
            "external_faq": survey_info.external_faq, 
            "external_privacy": survey_info.external_privacy,
            "title_case": survey_info.title_case,
            "title_question": survey_info.title_question,
            "survey_end_text": survey_info.survey_end_text
            })
        variables = VariablesCategory.objects.all()
        formStart = FormStartChoice(initial={
            "forms": survey_info.form_start
        }
        )
        formEditForms = MultiChoiceForm(initial={
            "forms": survey_info.form_survey
        })
        context = {
            'formEditInternalText': formEditInternalText,
            'formEditSettings': formEditSettings,
            'formEditExternalText': formEditExternalText,
            'variables': variables,
            'formStart': formStart,
            'formEditForms': formEditForms,
            'survey_info': survey_info,
            'settings_info': settings_info,
            'survey_cases': survey_cases
        }
        return render(request, 'app/survey.html', context=context)

#    path('survey/<testid>/results', views.testresults, name="test-results"),
@login_required
def testresults(request, testid):
    testid = testid
    survey_data = SurveyCase.objects.filter(survey_id=testid)
    context = {
       'survey_data':survey_data 
    }
    return render(request, 'app/report.html', context=context)
    #survey_data_json = serializers.serialize('json', survey_data)
    #return HttpResponse(survey_data_json, content_type='application/json')

    #survey_data = list(SurveyCase.objects.filter(survey_id=testid).values())  # wrap in list(), because QuerySet is not JSON serializable
    #return JsonResponse(survey_data, safe=False)  # or JsonResponse({'data': data})

#   path('survey/<testid>/delete/', views.testdelete, name="test-delete"),
@login_required
def testdelete(request, testid):
    testid = testid
    try:
        delete_survey = Survey.objects.filter(id=testid).delete()
        messages.success(request, f'Survey {testid} deleted')
        return redirect('app:test-create')
    except:
        messages.error(request, f'Survey {testid} NOT deleted')
        return redirect('app:test-create')

# path('create/settings/variable/delete', views.settingsvariabledelete, name="test-settingsvariabledelete"),
@login_required
def settingsvariabledelete(request, variableid):
    variableid = variableid
    try:
        delete_variable = VariablesCategory.objects.filter(id=variableid).delete()
        messages.success(request, f'Survey {variableid} deleted')
        return redirect('app:test-createsettings')
    except:
        messages.error(request, f'Survey {variableid} NOT deleted')
        return redirect('app:test-createsettings')

@login_required
def templatepreview(request, templateid):
    templateid = templateid
    template = VariableTemplates.objects.get(id=templateid)
    context = {
        'text_internal': template.text_internal,
        'text_external': template.text_external,
        'code_html': template.code_html,
        'code_css': template.code_css,
        'code_js': template.code_js
    }
    return render(request, 'app/template-preview.html', context=context)


#    path('create/settings/template/<templateid>', views.testtemplateedit, name="test-templateedit")
@login_required
def testtemplateedit(request, templateid):
    templateid = templateid
    # post request
    if request.method == 'POST':
        # FORM =>
        if 'editTemplate' in request.POST:
            form_edit_template = NewVariableTemplates(request.POST)
            try:
                if form_edit_template.is_valid():
                    # get form data  
                    name = form_edit_template.cleaned_data['name']
                    text_internal = form_edit_template.cleaned_data['text_internal']
                    text_external = form_edit_template.cleaned_data['text_external']
                    code_html = form_edit_template.cleaned_data['code_html']
                    code_css = form_edit_template.cleaned_data['code_css']
                    code_js = form_edit_template.cleaned_data['code_js']
                    zero_template = form_edit_template.cleaned_data['zero_template']
                    language = form_edit_template.cleaned_data['language']
                    gender = form_edit_template.cleaned_data['gender']
                    segment_id = form_edit_template.cleaned_data['segment_id']
                    # sql add survey
                    edit_survey= VariableTemplates.objects.get(id=templateid)
                    edit_survey.name = name
                    edit_survey.text_internal = text_internal
                    edit_survey.text_external = text_external
                    edit_survey.code_html = code_html
                    edit_survey.code_css = code_css
                    edit_survey.code_js = code_js         
                    edit_survey.zero_template = zero_template
                    edit_survey.language = language
                    edit_survey.gender = gender
                    edit_survey.segment_id = segment_id                                
                    edit_survey.save()
                    messages.success(request, f'Template updated successfully')
                    return redirect('app:test-templateedit', templateid=templateid)
                else:
                    messages.error(request, f'Form was not valid')
                    return redirect('app:test-templateedit', templateid=templateid)
            except:
                messages.error(request, f'Edit template failed')
                return redirect('app:test-templateedit', templateid=templateid)
    # get request
    else:
        template = VariableTemplates.objects.get(id=templateid)
        form_edit_template = NewVariableTemplates(initial={
                'variable_id': template.variable_id, 
                'name': template.name, 
                'settings': template.settings, 
                'text_internal': template.text_internal,
                'text_external': template.text_external,
                'code_html': template.code_html,
                'code_css': template.code_css,
                'code_js': template.code_js,
                'zero_template': template.zero_template,
                'language': template.language,
                'gender': template.gender,
                'segment_id': template.segment_id,
                'counter': template.counter
            })
        context = {
        'form_edit_template': form_edit_template,
        'template': template,
        }
        return render(request, 'app/template-edit.html', context=context)

#     path('create/settings/template/<templateid>/delete', views.testtemplatedelete, name="test-templatedelete"),
@login_required
def testtemplatedelete(request, templateid):
    templateid = templateid
    # delete
    try:
        delete_variable = VariableTemplates.objects.filter(id=templateid).delete()
        messages.success(request, f'Template {templateid} deleted')
        return redirect('app:test-createsettings')
    except:
        messages.error(request, f'Template {templateid} NOT deleted')
        return redirect('app:test-createsettings')

#   path('create/settings/form/<formid>', views.formedit, name="test-formedit"),
@login_required
def formedit(request, formid):
    formid = formid
    if request.method == 'POST':
        formSurvey = NewForm(request.POST)
        try:
            if formSurvey.is_valid(): 
                #print("HERE I AM")
                form_name = formSurvey.cleaned_data['name']
                form_language = formSurvey.cleaned_data['language']
                form_text = formSurvey.cleaned_data['text']
                django_form_name = formSurvey.cleaned_data['django_form_name']
                is_start = formSurvey.cleaned_data['is_start']
                template_tag = formSurvey.cleaned_data['template_tag']
                text_button = formSurvey.cleaned_data['text_button']
                # sql add survey
                add_form = FormSurvey.objects.get(id=formid)    
                add_form.name=form_name
                add_form.language = form_language
                add_form.text = form_text
                add_form.django_form_name = django_form_name
                add_form.template_tag = template_tag
                add_form.is_start = is_start
                add_form.text_button = text_button
                add_form.save()
                #print("IT WORKS!!!")
                messages.success(request, f'Form updated successfully')
                return redirect('app:test-formedit', formid=formid)
            else:
                messages.error(request, f'Form was not updated')
                return redirect('app:test-formedit', formid=formid)
        except:
            messages.error(request, f'Form was not valid')
            return redirect('app:test-formedit', formid=formid)
    template = FormSurvey.objects.get(id=formid)
    formEdit = NewForm(initial={
            'name': template.name, 
            'text': template.text, 
            'language': template.language,
            'django_form_name': template.django_form_name,
            'template_tag': template.template_tag,
            'is_start': template.is_start,
            'text_button': template.text_button
        })
    context = {
    'formEdit': formEdit,
    'formid': formid,
    }
    return render(request, 'app/form-edit.html', context=context)

#     path('create/settings/form/<formid>/delete', views.formdelete, name="test-formdelete"),
@login_required
def formdelete(request, formid):
    formid = formid
    # delete
    try:
        #print("HERE I AM")
        delete_variable = FormSurvey.objects.filter(id=formid).delete()
        messages.success(request, f'Form {formid} deleted')
        return redirect('app:test-createsettings')
    except:
        messages.error(request, f'Form {formid} NOT deleted')
        return redirect('app:test-createsettings')



# path('reports/<reportid>/', views.testfinalresults, name="test-final-results"),
@login_required
def testfinalresults(request, reportid):
    reportid = reportid
    if reportid == 1: # user
        users = SurveyUser.objects.all().values()
        delete = FinalUserNew.objects.all().delete()
        # init users settings
        lang_de = 0
        lang_it = 0
        lang_en = 0
        lang_es = 0
        lang_ot = 0
        gend_m = 0
        gend_f = 0
        gend_x = 0
        age = 0
        lang = ""
        gender = ""
        # loop and assign new values                             
        for user in users:
            for k, v in user.items():
                ##print(f'key: {k} value: {v}')
                if k == 'id':
                    user_id = v
                if k == 'user_settings':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'gender':
                            if value == 'M':
                                gend_m = 1
                                gender = 'M'
                            elif value == 'F':
                                gend_f = 1
                                gender = 'F'
                            elif value == 'X':
                                gend_x = 1
                                gender = 'X'
                            else:
                                pass
                        if key == 'age_range':
                            age_range = value
                        if key == 'language':
                            if value == 'IT':
                                lang_de = 0
                                lang_it = 1
                                lang_en = 0
                                lang_es = 0
                                lang_ot = 0
                                lang = 'IT'
                            elif value == 'DE':
                                lang_de = 1
                                lang_it = 0
                                lang_en = 0
                                lang_es = 0
                                lang_ot = 0
                                lang = 'DE'
                            elif value == 'EN':
                                lang_de = 0
                                lang_it = 0
                                lang_en = 1
                                lang_es = 0
                                lang_ot = 0
                                lang = 'EN'
                            elif value == 'ES':
                                lang_de = 0
                                lang_it = 0
                                lang_en = 0
                                lang_es = 1
                                lang_ot = 0
                                lang = 'ES'
                            else:
                                lang_de = 0
                                lang_it = 0
                                lang_en = 0
                                lang_es = 1
                                lang_ot = 0
                                lang = 'OT'
                        if key == 'occupation':
                            if value == '1':
                                occupation = 1
                            elif value == '2':
                                occupation = 2
                            elif value == '3':
                                occupation = 3
                            elif value == '4':
                                occupation = 4
                            else:
                                occupation = 0
                        if key == 'academic':
                            if value == '1':
                                academic = 1
                            elif value == '2':
                                academic = 2
                            elif value == '3':
                                academic = 3
                            elif value == '4':
                                academic = 4
                            else:
                                academic = 0
                        if key == 'click_ads':
                            if value == '0':
                                click_ads = 0
                            elif value == '1':
                                click_ads = 1
                            elif value == '2':
                                click_ads = 2
                            elif value == '3':
                                click_ads = 3
                            elif value == '4':
                                click_ads = 4
                            else:
                                click_ads = 0
                        if key == 'privacy':
                            if value == '0':
                                privacy = 0
                            elif value == '1':
                                privacy = 1
                            elif value == '2':
                                privacy = 2
                            elif value == '3':
                                privacy = 3
                            elif value == '4':
                                privacy = 4
                            else:
                                privacy = 0
                        if key == 'context':
                            if value == '0':
                                context = 0
                            elif value == '1':
                                context = 1
                            elif value == '2':
                                context = 2
                            elif value == '3':
                                context = 3
                            elif value == '4':
                                context = 4
                            elif value == '5':
                                context = 5
                            else:
                                context = 0                                                                      
            # add to new table
            '''
            new_user = FinalUsers.objects.get_or_create (
                user_id = user_id,
                lang_de = lang_de,
                lang_it = lang_it,
                lang_en = lang_en,
                lang_es = lang_es,
                lang_ot = lang_ot,
                gend_m = gend_m,
                gend_f = gend_f,
                gend_x = gend_x,
                age_range = age_range,
                occupation = occupation,
                academic = academic,
                privacy = privacy,
                click_ads = click_ads,
                context = context
            )
            '''
            new_user_short = FinalUserNew.objects.get_or_create (
                user_id = user_id,
                lang = lang,
                gender = gender,
                age_range = age_range,
                occupation = occupation,
                academic = academic,
                privacy = privacy,
                click_ads = click_ads,
                context = context
            )
        # query table
        #survey_data = FinalUsers.objects.all()
        survey_data = FinalUserNew.objects.all()
        template = 1
    elif reportid == 2: # sensitive
        FinalSurveyZero.objects.all().delete()
        cases = SurveyCase.objects.filter(survey_id__survey_zero=True, survey_id__suvery_var_cat_id=4).values()
        # init users settings
        case_id = 0
        variable_tested = 4
        template_id = 0
        answer_1 = 0
        answer_2 = 0
        # loop and assign new values                             
        for case in cases:
            for k, v in case.items():
                #print(f'key: {k} value: {v}')
                if k == 'id':
                    user_id = v
                if k == 'case_id':
                    case_id = v
                if k == 'case_settings':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'template_id_tested':
                            template_id = value
                    template_info = VariableTemplates.objects.filter(id=template_id).values()[0]
                    language = template_info['language']
                    gender = template_info['gender']
                    segment_id = template_info['segment_id']
                if k == 'case_answer':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'value':
                            answer_1 = value              
            # add to new table
            new_survey_zero = FinalSurveyZero.objects.get_or_create (
                user_id = user_id,
                case_id = case_id,
                variable_tested = variable_tested,
                template_id = template_id,
                lang = language,
                gender = gender,
                dep_var = segment_id,
                answer_1 = answer_1
            )
        # query table
        survey_data = FinalSurveyZero.objects.filter(variable_tested=4)
        template = 2
    elif reportid == 3: # context
        cases = SurveyCase.objects.filter(survey_id__survey_zero=True, survey_id__suvery_var_cat_id=1).values()
        # init users settings
        case_id = 0
        variable_tested = 1
        template_id = 0
        answer_1 = 0
        answer_2 = 0
        # loop and assign new values                             
        for case in cases:
            for k, v in case.items():
                #print(f'key: {k} value: {v}')
                if k == 'id':
                    user_id = v
                if k == 'case_id':
                    case_id = v
                if k == 'case_settings':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'template_id_tested':
                            template_id = value
                    template_info = VariableTemplates.objects.filter(id=template_id).values()[0]
                    language = template_info['language']
                    gender = template_info['gender']
                    segment_id = template_info['segment_id']
                if k == 'case_answer':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'value':
                            answer_1 = value               
            # add to new table
            new_survey_zero = FinalSurveyZero.objects.get_or_create (
                user_id = user_id,
                case_id = case_id,
                variable_tested = variable_tested,
                template_id = template_id,
                lang = language,
                gender = gender,
                dep_var = segment_id,
                answer_1 = answer_1
            )
        # query table
        survey_data = FinalSurveyZero.objects.filter(variable_tested=4)
        template = 3
    elif reportid == 4: # final results
        cases = SurveyCase.objects.filter(survey_id__last_survey=True).values()
        # init users settings
        case_id = 0
        sensitivity = 0
        context = 0
        transparency = 0
        contextual_matching = 0
        template_sensitivity = 0
        template_context = 0
        template_transparency = 0
        template_contextual_matching = 0
        answer_1 = 0
        answer_2 = 0
        # loop and assign new values                             
        for case in cases:
            for k, v in case.items():
                #print(f'key: {k} value: {v}')
                if k == 'survey_user_id_id':
                    user_id = v
                if k == 'case_id':
                    case_id = v
                if k == 'case_settings':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'template_id_list':
                            for i in range(len(value)):
                                if i == 0:
                                    template_context = value[i]
                                elif i == 1:
                                    template_transparency = value[i]
                                elif i == 2:
                                    template_sensitivity = value[i]
                                elif i == 3:
                                    template_contextual_matching = value[i]
                                else:
                                    print("error")
                        if key == "counter_survey_id":
                            counter = CounterSurvey.objects.get(id=value)
                            #print("------------------counter -------")
                            #print(counter)
                            sensitivity = counter.se
                            context = counter.co
                            transparency = counter.tr
                            contextual_matching = counter.cm
                if k == 'case_answer':
                    v_dict = ast.literal_eval(v)
                    for key, value in v_dict.items():
                        if key == 'value':
                            answer_1 = value
                        if key == 'value2':
                            answer_2 = value  
            # add to new table
            new_final_survey = FinalSurvey.objects.get_or_create (
                user_id = user_id,
                case_id = case_id,
                sensitivity = sensitivity,
                context = context,
                transparency = transparency,
                contextual_matching = contextual_matching,
                template_sensitivity = template_sensitivity,
                template_context = template_context,
                template_transparency = template_transparency,
                template_contextual_matching = template_contextual_matching,
                answer_1 = answer_1,
                answer_2 = answer_2
            )
        # query table
        survey_data = FinalSurvey.objects.all()
        template = 4
    else:
        survey_data = ""
        template = 0
    context = {
       'survey_data': survey_data,
       'template': template 
    }
    return render(request, 'app/final-report.html', context=context)
# --------------- test ----------------------------------------------------
