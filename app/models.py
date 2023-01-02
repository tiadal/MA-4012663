from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

DE = "DE"
EN = "EN"
IT = "IT"
ES = "ES"
class FormSurvey(models.Model):
    LANGUAGE = (
        (DE, 'German'),
        (EN, 'English'),
        (IT, 'Italian'),
        (ES, 'Spanish'),
    )
    DJANGO_FORM = (
        ("Radio5", 'Radio5'),
        ("Radio5EN", 'Radio5EN'),        
        ("Radio5ENCON", 'Radio5ENCON'),
        ("Radio5ITCON", 'Radio5ITCON'),
        ("Radio50EN", "Radio50EN"),
        ("Radio7", 'Radio7'),
        ("Text1", 'Text1'),
        ("NewSurveyUserEN", 'NewSurveyUserEN'),
        ("NewSurveyUserIT", 'NewSurveyUserIT'),
        ("Radio50", "Radio50"),
        ("EmptyForm", "EmptyForm"),
        ("NewSurveyUserDE", "NewSurveyUserDE"),
        ("Radio5DE", "Radio5DE"),
        ("Radio5DECON", "Radio5DECON"),
        ("Radio50DE", "Radio50DE")
    )
    name = models.CharField(max_length=32, default='Form')
    language = models.CharField(max_length=2, choices = LANGUAGE, default='EN')
    text = models.TextField(blank=True, default="Please fill the form", null=True) 
    django_form_name = models.CharField(max_length=32, choices = DJANGO_FORM, default='Text1')
    template_tag = models.CharField(max_length=32, default="", null=False, blank=True)
    is_start = models.BooleanField(default=False, null=False, blank=True)
    text_button = models.TextField(blank=True, default="Save", null=True) 
    def __str__(self):
        return str(self.name)  

class VariablesCategory(models.Model):
    tag = models.CharField(max_length=2)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=320,null=True,blank=True)
    max_segments = models.IntegerField(default=1)
    def __str__(self):
        return str(self.id)   
 

DE = "DE"
EN = "EN"
IT = "IT"
ES = "ES"
class Survey(models.Model):
    LANGUAGE = (
        (DE, 'German'),
        (EN, 'English'),
        (IT, 'Italian'),
        (ES, 'Spanish'),
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=160)
    language = models.CharField(max_length=2, choices = LANGUAGE, default='EN')
    description = models.CharField(max_length=320,null=True,blank=True)
    # survey zero stuff
    survey_zero = models.BooleanField(default=False, blank=True)
    suvery_var_cat_id = models.ForeignKey(VariablesCategory, on_delete=models.CASCADE, null=True, blank=True)
    # 
    external_title = models.CharField(max_length=160, null=False, blank=False, default="Survey")
    external_subtitle = models.CharField(max_length=320, null=True, blank=True)
    external_description = models.TextField(null=True, blank=True)
    external_faq = models.TextField(null=True, blank=True)
    external_privacy = models.TextField(null=True, blank=True)
    variables = models.JSONField(default=dict)
    form_start = models.ForeignKey(FormSurvey, on_delete=models.CASCADE, null=True, blank=True,related_name='form_start')#models.JSONField(default=dict)
    form_survey = models.ForeignKey(FormSurvey, on_delete=models.CASCADE, null=True, blank=True,related_name='form_survey')#models.JSONField(default=dict)
    redirect_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title_case = models.CharField(max_length=160, null=False, blank=False, default="Case")
    title_question =  models.CharField(max_length=160, null=False, blank=False, default="Questions")
    help_title = models.CharField(max_length=320, null=True, blank=True)
    help_text1 = models.CharField(max_length=320, null=True, blank=True)
    help_text2 = models.CharField(max_length=320, null=True, blank=True)
    # new fields:
    first_survey = models.BooleanField(default=False, blank=True)
    last_survey = models.BooleanField(default=False, blank=True)
    survey_end_text = models.TextField(null=True, blank=True)
    max_cases = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

class SurveyUser(models.Model):
    user_settings = models.JSONField(default=dict)
    survey_id = models.IntegerField(null=True, blank=True)
    user_choiche = models.JSONField(default=dict)
    def __str__(self):
        return str(self.id)   

class SurveyCase(models.Model):
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    survey_user_id = models.ForeignKey(SurveyUser, on_delete=models.CASCADE)
    case_id = models.IntegerField(default=0)
    case_settings = models.JSONField(default=dict)
    case_answer = models.JSONField(default=dict)
    def __str__(self):
        return str(self.id) 

DE = "DE"
EN = "EN"
IT = "IT"
ES = "ES"
class VariableTemplates(models.Model):
    LANGUAGE = (
        (DE, 'German'),
        (EN, 'English'),
        (IT, 'Italian'),
        (ES, 'Spanish'),
    )
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Others'),
    )
    # settings for randomizer
    language = models.CharField(max_length=2, choices = LANGUAGE, default='EN')
    gender = models.CharField(max_length=2, choices = GENDER, default='X')
    segment_id = models.IntegerField(null=True, blank=True, default=1)
    # other stuff
    variable_id = models.ForeignKey(VariablesCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default="Template", null=True, blank=True)
    settings = models.JSONField(default=dict)
    segment = models.JSONField(default=dict)
    text_internal = models.CharField(max_length=3200, default=None, null=True, blank=True)
    text_external = models.CharField(max_length=3200, default=None, null=True, blank=True)
    code_html = models.TextField(default=None, null=True, blank=True)
    code_css = models.TextField(default=None, null=True, blank=True)
    code_js = models.TextField(default=None, null=True, blank=True) 
    zero_template = models.BooleanField(default=False)
    counter = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)   

class CounterSurvey(models.Model):
    unique_id = models.IntegerField(default=0)
    co = models.BooleanField(null=True, blank=True)
    tr = models.BooleanField(null=True, blank=True)
    se = models.BooleanField(null=True, blank=True)
    # cm = models.BooleanField(null=True, blank=True)
    counter = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id)   

# final tables  ----------------------------------------------------------------

class FinalUsers(models.Model):
    user_id = models.IntegerField(null=True, blank=True, default=0)
    lang_de = models.IntegerField(null=True, blank=True, default=0)
    lang_it = models.IntegerField(null=True, blank=True, default=0)
    lang_en = models.IntegerField(null=True, blank=True, default=0)
    lang_es = models.IntegerField(null=True, blank=True, default=0)
    lang_ot = models.IntegerField(null=True, blank=True, default=0)
    gend_m = models.IntegerField(null=True, blank=True, default=0)
    gend_f = models.IntegerField(null=True, blank=True, default=0)
    gend_x = models.IntegerField(null=True, blank=True, default=0)
    age_range = models.IntegerField(null=True, blank=True, default=0)
    occupation = models.IntegerField(null=True, blank=True, default=0)
    academic = models.IntegerField(null=True, blank=True, default=0)
    privacy = models.IntegerField(null=True, blank=True, default=0)
    context = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.id)

class FinalUserNew(models.Model):
    user_id = models.IntegerField(null=True, blank=True, default=0)
    lang = models.CharField(max_length=2, null=True, blank=True, default=0)
    gender = models.CharField(max_length=1, null=True, blank=True, default=0)
    age_range = models.IntegerField(null=True, blank=True, default=0)
    occupation = models.IntegerField(null=True, blank=True, default=0)
    academic = models.IntegerField(null=True, blank=True, default=0)
    privacy = models.IntegerField(null=True, blank=True, default=0)
    context = models.IntegerField(null=True, blank=True, default=0)
    click_ads = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return str(self.id)  

class FinalSurveyZero(models.Model):
    user_id = models.IntegerField(null=True, blank=True, default=0)
    case_id = models.IntegerField(null=True, blank=True, default=0)
    variable_tested = models.IntegerField(null=True, blank=True, default=0)
    template_id = models.IntegerField(null=True, blank=True, default=0)
    lang = models.CharField(max_length=2, null=True, blank=True, default=0)
    gender = models.CharField(max_length=1, null=True, blank=True, default=0)
    dep_var = models.IntegerField(null=True, blank=True, default=0)
    answer_1 = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.id) 

class FinalSurvey(models.Model):
    user_id = models.IntegerField(null=True, blank=True, default=0)
    case_id = models.IntegerField(null=True, blank=True, default=0)

    sensitivity = models.IntegerField(null=True, blank=True, default=0)
    context = models.IntegerField(null=True, blank=True, default=0)
    transparency = models.IntegerField(null=True, blank=True, default=0)
    #contextual_matching = models.IntegerField(null=True, blank=True, default=0)
    template_sensitivity = models.IntegerField(null=True, blank=True, default=0)
    template_context = models.IntegerField(null=True, blank=True, default=0)
    template_transparency = models.IntegerField(null=True, blank=True, default=0)
    #template_contextual_matching = models.IntegerField(null=True, blank=True, default=0)

    answer_1 = models.IntegerField(null=True, blank=True, default=0)
    answer_2 = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.id) 