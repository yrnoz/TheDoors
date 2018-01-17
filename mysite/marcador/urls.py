from django.conf.urls import url


urlpatterns = [
    url(r'^user/(?P<username>[-\w]+)/$', 'marcador.views.doors_user',
        name='marcador_doors_user'),
    url(r'^$', 'marcador.views.friends_list', name='marcador_friends_list'),
]