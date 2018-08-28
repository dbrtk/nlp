

from django.urls import path

from . import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'thesite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    path('features-to-json', views.features_to_json, name='features_to_json'),
    path('features-docs', views.features_docs, name='features_docs'),

    path('features-count', views.features_count, name='features_count'),

    path('remove-feature', views.remove_feature, name='remove_feature'),
    path('dendogram', views.dendogram, name='dendogram'),

]
