import json

from django.views.generic import TemplateView, View
from django.http import JsonResponse

from .models import History
from .algo import algorithm
from .algo import prediction
from .algo import diagram_data
from .algo import diagram_options


class MainPage(TemplateView):
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        result_text = algorithm(data['original_text'], data['offset'], data['encryption'])
        data['result_text'] = result_text
        history = History.objects.create(**data)
        return_json = history.to_dict()
        return_json['prediction'] = prediction(data['original_text']);
        return JsonResponse(return_json)


class HistoryView(View):
    def get(self, request, *args, **kwargs):
        histories = History.objects.all().order_by('-created_at')[:15]
        histories = list(map(lambda x: x.to_dict(), histories))
        return JsonResponse({'histories': histories})


class DiagramView(View):
    def post(self,request, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        return_data = diagram_data(data['text'])
        return_options = diagram_options()
        return JsonResponse({'return_data':  return_data, 'return_options': return_options})
