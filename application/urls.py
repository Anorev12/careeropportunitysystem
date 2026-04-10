from django.urls import path
from . import views

urlpatterns = [
    # Application CRUD
    path('',                                     views.application_list,           name='application_list'),
    path('apply/<int:job_id>/',                  views.apply_job,                  name='apply_job'),
    path('<int:pk>/',                            views.application_detail,         name='application_detail'),
    path('<int:pk>/withdraw/',                   views.withdraw_application,       name='withdraw_application'),
    path('<int:pk>/update-status/',              views.update_application_status,  name='update_application_status'),

    # Interview CRUD
    path('<int:application_pk>/interview/add/',  views.schedule_interview,         name='schedule_interview'),
    path('interview/<int:pk>/edit/',             views.edit_interview,             name='edit_interview'),
    path('interview/<int:pk>/delete/',           views.delete_interview,           name='delete_interview'),
]