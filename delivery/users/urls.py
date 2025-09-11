from django.urls import path
from users.views import VerifyUserView, RegisterControllerView, RegisterCourierView, FetchUserView
from users.views import UpdateControllerView, UpdateCourierView

from users import views

urlpatterns = [
    path('register/courier/', view=RegisterCourierView.as_view()),
    path('register/controller/', view=RegisterControllerView.as_view()),
    path('verify/', view=VerifyUserView.as_view()),
    path('fetch/user/', view=FetchUserView.as_view()), 
    path('update/courier', view=UpdateCourierView.as_view()),
    path('update/controller/', view=UpdateControllerView.as_view()),
    path('controller/couriers/', view=views.FetchCouriersByController.as_view()), 
    path('controller/add/courier/', view=views.AddCourier.as_view()), 
    path('courier/fetch/phone/', view=views.FetchCourierByPhone.as_view())
]
