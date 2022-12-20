from django.urls import path,include

from . import views

urlpatterns = [
  path('',views.index,name='home'),
  path('dashboard',views.dashboard,name='dashboard'),
  path('register',views.register,name='register'),
  path('login',views.loginPage,name='login'),
  path('logout',views.logoutUser,name='logout'),
  path('results',views.predDis,name='results'),
  path('doctors',views.docList,name='doctors'),
  path('cases',views.pendingCases,name='cases'),
  path('arcases',views.archivedCases,name='arcases'),
  path('doctor/<str:pk>/',views.docProfile,name='doctor'),
  path('case/<str:pk>/',views.pendingCase,name='case'),
  path('arcase/<str:pk>/',views.archivedCase,name='arcase'),

  path('about',views.about,name='about'),

]