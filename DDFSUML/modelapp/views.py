from django.shortcuts import render,redirect
from .models import Symp,DiseaseDesc,About,Profile,queryToDoc
import pickle
from datetime import datetime
import sklearn
from pytz import timezone
from django.template import defaultfilters
import numpy as np
from django.conf import settings

import warnings
from PyDictionary import PyDictionary
from django.contrib.auth.forms import UserCreationForm
import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import indian_names
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUser,QueryUser
warnings.filterwarnings("ignore")


valN = pickle.load(open(os.path.dirname(os.path.dirname(__file__))+'/model/nbmodel.pkl', 'rb'))
valR = pickle.load(open(os.path.dirname(os.path.dirname(__file__))+'/model/rfcmodel.pkl', 'rb'))


e_classes = ['(vertigo) Paroymsal  Positional Vertigo', 'AIDS', 'Acne',
 'Alcoholic hepatitis', 'Allergy', 'Arthritis', 'Bronchial Asthma',
 'Cervical spondylosis', 'Chicken pox', 'Chronic cholestasis', 'Common Cold',
 'Dengue', 'Diabetes ', 'Dimorphic hemmorhoids(piles)', 'Drug Reaction',
 'Fungal infection', 'GERD', 'Gastroenteritis', 'Heart attack', 'Hepatitis B',
 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Hypertension ',
 'Hyperthyroidism', 'Hypoglycemia', 'Hypothyroidism', 'Impetigo', 'Jaundice',
 'Malaria', 'Migraine', 'Osteoarthristis', 'Paralysis (brain hemorrhage)',
 'Peptic ulcer diseae', 'Pneumonia', 'Psoriasis', 'Tuberculosis', 'Typhoid',
 'Urinary tract infection', 'Varicose veins', 'hepatitis A']

xVal = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing',
 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity',
 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
 'spotting_urination', 'fatigue', 'weight_gain', 'anxiety',
 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness',
 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough',
 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration',
 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements',
 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid',
 'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech',
 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
 'swelling_joints', 'movement_stiffness', 'spinning_movements',
 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine',
 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain',
 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes',
 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum',
 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
 'stomach_bleeding', 'distention_of_abdomen',
 'history_of_alcohol_consumption', 'fluid_overload_1', 'blood_in_sputum',
 'prominent_veins_on_calf', 'palpitations', 'painful_walking',
 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

def index(request):
  if request.user.is_authenticated:
    return redirect('dashboard')
  symps = Symp.objects.all().order_by('name')
  return render(request,'index.html',{'symps':symps,'flag':False,'page': 'search'})


def dashboard(request):
  return render(request,'dashboard.html')

def predDis(request):
  symps = request.GET.get('allSymps')


  print(symps)
  symptoms_dict = {}
  for index, symptom in enumerate(xVal):
    symptoms_dict[symptom] = index

  def predictDisease(symptoms):
    labelled_data = [0 for _ in range(len(symptoms_dict))]
    symptoms = symptoms.split(',')
    for symptom in symptoms:
      symptom = '_'.join(symptom.lower().split())
      labelled_data[symptoms_dict[symptom]] = 1
    symptoms = sorted(list(set(symptoms)))
    labelled_data = np.array(labelled_data).reshape(1,-1)
    gnb_pred = e_classes[valN.predict(labelled_data)[0]]
    rfc_pred = e_classes[valR.predict(labelled_data)[0]]
    return(gnb_pred,rfc_pred,symptoms)


  
  disease1,disease2,symptoms = predictDisease(symps)
  disdesc1 = DiseaseDesc.objects.get(name=disease1.strip())
  disdesc2 = DiseaseDesc.objects.get(name=disease2.strip())
  if disease1==disease2:
    dds=disease1
  else:
    dds=disease1+" or "+disease2
  
  sform = ""
  for i in symptoms:
    if symptoms.index(i)==(len(symptoms)-1):
      sform+=i
    else:
      sform+=i+','


  form = QueryUser(initial={"nickname":indian_names.get_full_name(),"listosymp":sform,"predDiseases":dds})
  if request.method =='POST':
    form = QueryUser(request.POST)
    if  form.is_valid():
      form.save()
      mail = form.cleaned_data.get('mail')
      messages.success(request,'Check your mail ('+mail+') for detailed diagnosis from our expert, may take a day or two')
    else:
      print(form.errors)
    return redirect('home')




  context = {

    'symps': symptoms,
    'disease1': disease1,
    'disease2': disease2,
    'disdesc1': disdesc1,
    'disdesc2': disdesc2,
    'form':form,
    'page': 'result'
  }




  return render(request,'result.html',context=context)








def about(request):
  people = About.objects.all()
  context={
    'page': 'about',
    'people': people
  }
  return render(request,'about.html',context=context)

@login_required(login_url='login')
def register(request):
  if request.user.is_superuser:
    form = CreateUser()
    if request.method == 'POST':
      form = CreateUser(request.POST)

      if form.is_valid():
        form.save()
        fname,lname = form.cleaned_data.get('first_name'),form.cleaned_data.get('last_name')
        messages.success(request,'Dr. '+fname+' '+lname+' was added to the database.')
      return redirect('register')
  else:
    return redirect('home')
  context={'form':form}
  return render(request,'register.html',context=context)

def loginPage(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    if request.method == 'POST':
      username=request.POST.get('username')
      password=request.POST.get('password')

      user = authenticate(request,username=username,password=password)
      if user is not None:
        login(request,user)
        return redirect('home')
      else:
        messages.info(request,"Incorrect username and password")

  context={}
  return render(request,'login.html',context=context)

def logoutUser(request):
  logout(request)
  return redirect('login')


def docList(request):
  if not request.user.is_superuser:
    return redirect('home')
  users = Profile.objects.all().order_by('name')
  context={
    'users':users
  }
  return render(request,'doctors.html',context=context)

def docProfile(request,pk):
  if not request.user.is_superuser:
    return redirect('home')
  user = Profile.objects.get(id=pk)
  context={
    'user':user
  }
  return render(request,'doctor.html',context=context)

@login_required(login_url='login')
def pendingCases(request):
  cases = queryToDoc.objects.all()
  context={
    'cases':cases
  }
  return render(request,'pendingcases.html',context=context)

@login_required(login_url='login')
def archivedCases(request):
  cases = queryToDoc.objects.all()
  context={
    'cases':cases
  }
  return render(request,'archivedcases.html',context=context)

@login_required(login_url='login')
def archivedCase(request,pk):
  case = queryToDoc.objects.get(id=pk)
  context={
    'case':case
  }
  return render(request,'archivedcase.html',context=context)

def pendingCase(request,pk):
  case = queryToDoc.objects.get(id=pk)
  doc = Profile.objects.get(user=request.user)
  date = str(defaultfilters.date(case.created.astimezone(timezone('Asia/Kolkata')), "DATETIME_FORMAT"))
  mail_id = request.POST.get('tomail')
  content = request.POST.get('content')
  context = {
    'content':content,
    'case':case,
    'doc':doc
  }

  if request.method == 'POST':
    html_content = render_to_string('email_text.html',context=context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
      #subject
      'Regarding Your Prognosis Query on '+date,
      #content
      text_content,
      #from
      settings.EMAIL_HOST_USER,
      #to
      [mail_id]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    case.complete = True
    case.doc = doc.name
    case.docnote = content
    case.probsolve = datetime.now()
    case.save()
    messages.success(request,'Mail Sent')  
    return redirect('cases')
  context={
    'date': date,
    'case':case
  }
  return render(request,'pendingcase.html',context=context)
