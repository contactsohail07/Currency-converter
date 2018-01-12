from django.conf.urls import url
from . import views

urlpatterns=[url(r'^$',views.frontpage,name='frontpage'),
			 url(r'^formpage/$',views.formpage,name='formpage'),
			 url(r'^formpage/output/$',views.formpage,name='formpage1'),
			 url(r'^signup/$',views.signup,name='signup'),
			 url(r'^signin/$',views.signin,name='signin'),
			 url(r'^signout/$',views.signout,name='signout'),]