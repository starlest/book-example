from django.conf.urls import url, include

from lists import views
from lists import urls as list_urls
from accounts import urls as account_urls

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(account_urls)),
    # url(r'^admin/', admin.site.urls)
]
