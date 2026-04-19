from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    # Auth
    path('login/',                               views.application_login,         name='application_login'),
    path('register/',                            views.application_register,      name='application_register'),
    path('logout/',                              views.application_logout,        name='application_logout'),

    # Jobs
    path('',                                     views.application_list,          name='application_list'),
    path('jobs/',                                views.job_list,                  name='job_list'),
    path('jobs/<int:pk>/',                       views.job_detail,                name='job_detail'),
    path('apply/<int:job_id>/',                  views.apply_job,                 name='apply_job'),

    # Applications
    path('<int:pk>/',                            views.application_detail,        name='application_detail'),
    path('<int:pk>/withdraw/',                   views.withdraw_application,      name='withdraw_application'),
    path('<int:pk>/update-status/',              views.update_application_status, name='update_application_status'),

    # Interviews
    path('<int:application_pk>/interview/add/',  views.schedule_interview,        name='schedule_interview'),
    path('interview/<int:pk>/edit/',             views.edit_interview,            name='edit_interview'),
    path('interview/<int:pk>/delete/',           views.delete_interview,          name='delete_interview'),
]