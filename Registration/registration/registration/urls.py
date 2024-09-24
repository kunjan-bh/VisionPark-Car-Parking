"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appl import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', views.homepage, name = 'home'),
    path('signup/', views.signuppage, name = 'signup'),
    path('login/', views.loginpage, name = 'login'),
    # path('accounts/login/', views.loginpage, name = 'login'),
    
    path('about/', views.aboutpage, name = 'about'),
    path('contact/', views.contactpage, name = 'contact'),
    path('book/', views.bookpage, name = 'book'),
    path('logout/', views.logoutpage, name = 'logout'),
    path('booking-success/', views.bookingsuccess, name = 'bookingsuccess'),
    path('booking-history/', views.bookinghistory, name = 'bookinghistory'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('book-fixed/', views.bookfixed, name='bookfixed'),
    path('book-flexible/', views.bookflexible, name='bookflexible'),
    path('get-slot-availability/', views.show_slot_availability, name='show_slot_availability'),
    path('book-extend/', views.book_extend, name='bookextend'),
    path('extend-booking/<int:booking_id>/', views.extend_booking, name='extend_booking'),
    path('extend-success/', views.extendsuccess, name = 'extendsuccess'),
    path('payment-success/<int:booking_id>/', views.payment_success, name = 'paymentsuccess'),
    path('get_latest_license_plate/', views.get_latest_license_plate, name = 'getlatestlicenseplate'),
    path('process-image/', views.process_image, name = 'processimage'),

    path('confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('confirmation-image/confirmation-image', views.confirmation_image, name = 'confirmationimage'),
    path('book/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('about/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('booking-history/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('booking-success/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('book-fixed/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('book-flexible/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('contact/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),
    path('book-extend/confirmation-image/', views.confirmation_image, name = 'confirmationimage'),

    path('update_booking_status/<str:status>/', views.update_booking_status, name='update_booking_status'),

    path('finish-session/', views.finish_session, name = 'finishsession'),
    path('book/finish-session/', views.finish_session, name = 'finishsession'),
    path('about/finish-session/', views.finish_session, name = 'finishsession'),
    path('booking-history/finish-session/', views.finish_session, name = 'finishsession'),
    path('booking-success/finish-session/', views.finish_session, name = 'finishsession'),
    path('book-fixed/finish-session/', views.finish_session, name = 'finishsession'),
    path('book-flexible/finish-session/', views.finish_session, name = 'finishsession'),
    path('contact/finish-session/', views.finish_session, name = 'finishsession'),
    path('book-extend/finish-session/', views.finish_session, name = 'finishsession'),

    path('chatbot/', views.chat_bot, name = 'chatbot'),
    path('about/chatbot/', views.chat_bot, name = 'chatbot-about'), 
    path('contact/chatbot/', views.chat_bot, name = 'chatbot-contact'),
    path('book/chatbot/', views.chat_bot, name = 'chatbot-book'),
    path('booking-success/chatbot/', views.chat_bot, name = 'chatbot-booking-success'),
    path('booking-history/chatbot/', views.chat_bot, name = 'chatbot-booking-history'),
    path('book-fixed/chatbot/', views.chat_bot, name = 'chatbot-book-fixed'),
    path('book-flexible/chatbot/', views.chat_bot, name = 'chatbot-book-flexible'),
    path('book-extend/chatbot/', views.chat_bot, name = 'chatbot-book-extend'),
    path('extend-success/chatbot/', views.chat_bot, name = 'chatbot-extend-success'),
    path('confirmation-image/chatbot/', views.chat_bot, name = 'chatbot-confirmation-image'),
    path('finish-session/chatbot/', views.chat_bot, name = 'chatbot-finish-session'),
]
