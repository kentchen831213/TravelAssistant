from django.views.generic import TemplateView


class TripPage(TemplateView):
    template_name = 'trip.html'

class ThankPage(TemplateView):
    template_name = 'index.html'

class HomePage(TemplateView):
    template_name = 'index.html'

