from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms.widgets import DateInput

    
class CreateSurvey(forms.Form):
    LANGUAGE = (
        ('DE', 'German'),
        ('EN', 'English'),
        ('IT', 'Italian'),
        ('ES', 'Spanish'),
    )
    name = forms.CharField(label="Name", max_length=160)
    language = forms.CharField(widget=forms.Select(choices=LANGUAGE))
    description = forms.CharField(label="Description", max_length=320)
    survey_end_text = forms.CharField(label="End Text", max_length=720)
    first_survey = forms.BooleanField(label="First Survey?", required=False)
    survey_zero = forms.BooleanField(label="Survey 0?", required=False)
    redirect_to = forms.ModelChoiceField(queryset=Survey.objects.filter(survey_zero=True),required=False)
    last_survey = forms.BooleanField(label="Last Survey?", required=False)

class NewSurveyUserEN(forms.Form):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Diverse'),
    )
    LANGUAGE = (
        ('EN', 'English'),
    )
    AGE_RANGE = (
        ('0', '18-24'),
        ('1', '25-34'),
        ('2', '35-44'),
        ('3', '45-54'),
        ('4', '55-64'),
        ('5', '65+'),
    )
    OCCUPATION = (
        ('0', 'Employed'),
        ('1', 'Unemployed'),
        ('2', 'Business owner'),
        ('3', 'Retired'),
        ('4', 'Student'),
        ('5', 'Other'),
    )
    ACADEMIC = (
        ('0', 'No schooling completed'),
        ('1', 'Primary school'),
        ('2', 'Secondary school'),
        ('3', 'High school'),
        ('4', 'University degree'),
    )
    CHOICES=[
        ('1','Never'),
        ('2','Rarely'),
        ('3','Sometimes'),
        ('4','Often'),
        ('5','Always')              
        ]
    CHOICES2=[
        ('1','Never'),
        ('2','Rarely'),
        ('3','Sometimes'),
        ('4','Often'),
        ('5','Always')                                
        ]
    CHOICES3=[
        ('0','Social media'),
        ('1',"News site"),
        ('2','Video games'),
        ('3','Entertainment websites'),
        ('4','E-Commerce'),
        ('5','Other')             
        ]
    gender = forms.CharField(widget=forms.Select(choices=GENDER))
    language = forms.CharField(widget=forms.Select(choices=LANGUAGE))
    age_range = forms.CharField(widget=forms.Select(choices=AGE_RANGE))
    occupation = forms.CharField(widget=forms.Select(choices=OCCUPATION))
    academic = forms.CharField(widget=forms.Select(choices=ACADEMIC))
    click_ads = forms.CharField(widget=forms.Select(choices=CHOICES))
    privacy = forms.CharField(widget=forms.Select(choices=CHOICES2))
    context = forms.CharField(widget=forms.Select(choices=CHOICES3))
    accept_terms = forms.BooleanField(required = True)

    def __init__(self, *args, **kwargs):
        super(NewSurveyUserEN, self).__init__(*args, **kwargs)
        self.fields['accept_terms'].label = 'Accept the data processing options'
        self.fields['gender'].label = "Gender"
        self.fields['language'].label = "Language"
        self.fields['occupation'].label = "Employment status"
        self.fields['academic'].label = "Level of education"
        self.fields['age_range'].label = "Age"
        self.fields['click_ads'].label = "How often do you click on online advertising?"
        self.fields['privacy'].label = "How often do you accept banners regarding cookies and personal data?"
        self.fields['context'].label = "What app/websites do you spend the most time on?"

class NewSurveyUserIT(forms.Form):
    GENDER = (
        ('M', 'Maschio'),
        ('F', 'Femmina'),
        ('X', 'Diverso'),
    )
    LANGUAGE = (
        ('IT', 'Italiano'),
    )
    AGE_RANGE = (
        ('1', '18-24'),
        ('2', '25-34'),
        ('3', '35-44'),
        ('4', '45-54'),
        ('5', '55-64'),
        ('6', '65+'),
    )
    OCCUPATION = (
        ('1', 'Dipendente'),
        ('2', 'Disoccupata/o'),
        ('3', 'Imprenditrice/ore'),
        ('4', 'Pensionata/o'),
    )
    ACADEMIC = (
        ('1', 'Scuole Elementari'),
        ('2', 'Scuole Medie'),
        ('3', 'Scuole Superiori'),
        ('4', 'Università'),
    )
    CHOICES=[
        ('1','Mai'),
        ('2','Raramente'),
        ('3','A volte'),
        ('4','Spesso'),
        ('5','Sempre')              
        ]
    CHOICES2=[
        ('1','Mai'),
        ('2','Raramente'),
        ('3','A volte'),
        ('4','Spesso'),
        ('5','Sempre')                                
        ]
    CHOICES3=[
        ('0','Social media'),
        ('1',"Siti di informazione"),
        ('2','Videogiochi'),
        ('3','Siti di intrattenimento'),
        ('4','Commercio Eletronico'),
        ('5','Altro')             
        ]
    gender = forms.CharField(widget=forms.Select(choices=GENDER))
    language = forms.CharField(widget=forms.Select(choices=LANGUAGE))
    age_range = forms.CharField(widget=forms.Select(choices=AGE_RANGE))
    occupation = forms.CharField(widget=forms.Select(choices=OCCUPATION))
    academic = forms.CharField(widget=forms.Select(choices=ACADEMIC))
    click_ads = forms.CharField(widget=forms.Select(choices=CHOICES))
    privacy = forms.CharField(widget=forms.Select(choices=CHOICES2))
    context = forms.CharField(widget=forms.Select(choices=CHOICES3))
    accept_terms = forms.BooleanField(required = True)

    def __init__(self, *args, **kwargs):
        super(NewSurveyUserIT, self).__init__(*args, **kwargs)
        self.fields['accept_terms'].label = 'Accetta le opzioni di trattamento dati'
        self.fields['gender'].label = "Genere"
        self.fields['language'].label = "Lingua"
        self.fields['occupation'].label = "Stato occupazionale"
        self.fields['academic'].label = "Livello di istruzione"
        self.fields['age_range'].label = "Fascia di età"
        self.fields['click_ads'].label = "Con che frequenza interagisci con pubblicità online?"
        self.fields['privacy'].label = "Con che frequenza accetti i banner riguardo ai cookies e dati personali?"
        self.fields['context'].label = "Su quale categoria di siti/app passi la maggior parte del tempo?"

class InternalTextSurvey(forms.Form):
    name = forms.CharField(label="Name", max_length=160)
    description = forms.CharField(label="Description", max_length=320)
    help_title = forms.CharField(label="help_title", max_length=320)
    help_text1 = forms.CharField(label="help_text1", max_length=320)
    help_text2 = forms.CharField(label="help_text2", max_length=320)

class SettingsSurvey(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['first_survey', 'last_survey', 'survey_zero', 'redirect_to', 'max_cases', 'language', 'suvery_var_cat_id']

class ExternalTextSurvey(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['external_title', 'external_subtitle', 'external_description', 'external_faq', 'external_privacy', 'title_case', 'title_question','survey_end_text']

class NewVariablesCategory(forms.ModelForm):
    class Meta:
        model = VariablesCategory
        fields = ['tag', 'name', 'description', 'max_segments']

class NewVariableTemplates(forms.ModelForm):
    class Meta:
        model = VariableTemplates
        fields = ['variable_id', 'name', 'text_internal', 'text_external', 'code_html', 'code_css', 'code_js', 'zero_template', 'language', 'segment_id', 'gender']

class NewForm(forms.ModelForm):
    class Meta:
        model = FormSurvey
        fields = '__all__'

class MultiChoiceForm(forms.Form):
        forms = forms.ModelChoiceField(queryset=FormSurvey.objects.filter(is_start=False),widget=forms.Select)

class FormStartChoice(forms.Form):
        forms = forms.ModelChoiceField(queryset=FormSurvey.objects.filter(is_start=True),widget=forms.Select)

class FormCounterSurvey(forms.ModelForm):
    class Meta:
        model = CounterSurvey
        fields = ['co', 'tr', 'se', 'unique_id']
# ----- forms survey templates

class EmptyForm(forms.Form):
    show = forms.BooleanField()

# en
class Radio5EN(forms.Form):
    CHOICES=[
        ('5','Strongly disagree'),
        ('4','Disagree'),
        ('3','Unsure'),
        ('2','Agree'),
        ('1','Strongly agree')           
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(Radio5EN, self).__init__(*args, **kwargs)
        self.fields['value'].label = "The content of this advertisement is sensitive"

class Radio5ENCON(forms.Form):
    CHOICES=[
        ('1','Strongly disagree'),
        ('2','Disagree'),
        ('3','Unsure'),
        ('4','Agree'),
        ('5','Strongly agree')           
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(Radio5ENCON, self).__init__(*args, **kwargs)
        self.fields['value'].label = "This website is trustworthy"

class Radio50EN(forms.Form):
    CHOICES=[
        ('1','Strongly disagree'),
        ('2','Disagree'),
        ('3','Unsure'),
        ('4','Agree'),
        ('5','Strongly agree')          
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    def __init__(self, *args, **kwargs):
        super(Radio50EN, self).__init__(*args, **kwargs)
        self.fields['value'].label = "I would like to click on the advertisement to get further information."

# it

class Radio5(forms.Form):
    CHOICES=[
        ('5','In completo disaccordo'),
        ('4','In disaccordo'),
        ('3','Incerto'),
        ('2','D`accordo'),
        ('1','Completamente d’accordo')           
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(Radio5, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Il contenuto di questa pubblicità è sensibile"

class Radio5ITCON(forms.Form):
    CHOICES=[
        ('1','In completo disaccordo'),
        ('2','In disaccordo'),
        ('3','Incerto'),
        ('4','D`accordo'),
        ('5','Completamente d’accordo')           
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(Radio5ITCON, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Questo sito è affidabile"

class Radio50(forms.Form):
    CHOICES=[
        ('1','In completo disaccordo'),
        ('2','In disaccordo'),
        ('3','Incerto'),
        ('4','D`accordo'),
        ('5','Completamente d’accordo')             
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    def __init__(self, *args, **kwargs):
        super(Radio50, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Vorrei fare clic sulla pubblicità per avere maggiori informazioni."

# de

class NewSurveyUserDE(forms.Form):
    GENDER = (
        ('M', 'Mann'),
        ('F', 'Frau'),
        ('X', 'Divers'),
    )
    LANGUAGE = (
        ('DE', 'Deutsch'),
    )
    AGE_RANGE = (
        ('0', '18-24'),
        ('1', '25-34'),
        ('2', '35-44'),
        ('3', '45-54'),
        ('4', '55-64'),
        ('5', '65+'),
    )
    OCCUPATION = (
        ('0', 'Angestellt'),
        ('1', 'Arbeitslos'),
        ('2', 'Selbständig'),
        ('3', 'Im Ruhestand'),
        ('4', 'Student'),
        ('5', 'Sonstige'),
    )
    ACADEMIC = (
        ('0', 'Kein Schulabschluss'),
        ('1', 'Grundschule'),
        ('2', 'Mittlerer Schulabschluss'),
        ('3', 'Abitur'),
        ('4', 'Universitätsabschluss'),
    )
    CHOICES=[
        ('1','Nie'),
        ('2','Selten'),
        ('3','gelegentlich'),
        ('4','Oft'),
        ('5','Immer')             
        ]
    CHOICES2=[
        ('1','Nie'),
        ('2','Selten'),
        ('3','gelegentlich'),
        ('4','Oft'),
        ('5','Immer')                                
        ]
    CHOICES3=[
        ('0','Social Media'),
        ('1',"Nachrichtenseite"),
        ('2','Videospiele'),
        ('3','Unterhaltung'),
        ('4','E-Commerce'),
        ('5','Sonstige')             
        ]
    gender = forms.CharField(widget=forms.Select(choices=GENDER))
    language = forms.CharField(widget=forms.Select(choices=LANGUAGE))
    age_range = forms.CharField(widget=forms.Select(choices=AGE_RANGE))
    occupation = forms.CharField(widget=forms.Select(choices=OCCUPATION))
    academic = forms.CharField(widget=forms.Select(choices=ACADEMIC))
    click_ads = forms.CharField(widget=forms.Select(choices=CHOICES))
    privacy = forms.CharField(widget=forms.Select(choices=CHOICES2))
    context = forms.CharField(widget=forms.Select(choices=CHOICES3))
    accept_terms = forms.BooleanField(required = True)

    def __init__(self, *args, **kwargs):
        super(NewSurveyUserDE, self).__init__(*args, **kwargs)
        self.fields['accept_terms'].label = 'Akzeptieren Sie die Datenverarbeitungsoptionen'
        self.fields['gender'].label = "Geschlecht"
        self.fields['language'].label = "Sprache"
        self.fields['occupation'].label = "Beschäftigungsverhältnis"
        self.fields['academic'].label = "Bildungsgrad"
        self.fields['age_range'].label = "Alter"
        self.fields['click_ads'].label = "Wie oft interagieren Sie mit Online-Werbung?"
        self.fields['privacy'].label = "Wie oft akzeptieren Sie Banner zu Cookies und personenbezogenen Daten?"
        self.fields['context'].label = "Auf welchen Apps/Websites verbringen Sie die meiste Zeit?"

class Radio5DE(forms.Form):
    CHOICES=[
        ('5','Stimmt nicht'),
        ('4','Stimmt wenig'),
        ('3','Stimmt mittelmässig'),
        ('2','Stimmt ziemlich'),
        ('1','Stimmt sehr')          
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(Radio5DE, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Der Inhalt dieser Anzeige ist sensibel oder unangemessen"

class Radio5DECON(forms.Form):
    CHOICES=[
        ('1','Stimmt nicht'),
        ('2','Stimmt wenig'),
        ('3','Stimmt mittelmässig'),
        ('4','Stimmt ziemlich'),
        ('5','Stimmt sehr')          
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(Radio5DECON, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Diese Seite ist zuverlässig"

class Radio50DE(forms.Form):
    CHOICES=[
        ('1','Stimmt nicht'),
        ('2','Stimmt wenig'),
        ('3','Stimmt mittelmässig'),
        ('4','Stimmt ziemlich'),
        ('5','Stimmt sehr')           
        ]
    value = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    def __init__(self, *args, **kwargs):
        super(Radio50DE, self).__init__(*args, **kwargs)
        self.fields['value'].label = "Ich möchte auf die Werbeanzeige klicken, um weitere Informationen zu erhalten."
