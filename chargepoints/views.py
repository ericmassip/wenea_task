from django.views.generic import TemplateView


class LobbyView(TemplateView):
    template_name = "chargepoints/lobby.html"
