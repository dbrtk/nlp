

from django.urls import path

from . import views


urlpatterns = [

    path('compute-matrices', views.compute_matrices, name='generate_matrices'),

    path('generate-features-weights', views.generate_features_weights,
         name='generate_features_weights'),

    path('features-to-json', views.features_to_json, name='features_to_json'),

    path('features-docs', views.get_features_and_docs, name='features_docs'),

    # path('features-count', views.features_count, name='features_count'),

    # path('remove-feature', views.remove_feature, name='remove_feature'),
    # path('dendogram', views.dendogram, name='dendogram'),


    path('test-celery', views.test_celery, name='testcelery'),
]
