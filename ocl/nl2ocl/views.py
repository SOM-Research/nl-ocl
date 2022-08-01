from curses import nl
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View, ListView, UpdateView, TemplateView, FormView
import json
import os
from django.conf import settings
from pathlib import Path
from random import randrange
from .models import NLQuestion, QAssociate, QAssociation, QAttribute, QClass, QModel, OCLTranslation, ReportedQuestion
import subprocess
from django.http import JsonResponse
from .serializers import OCLTranslationSerializer
from .forms import NewQuestionForm, ReportQuestionForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class DDView(View):
    message = None

    def __init__(self, *args, **kwargs):
        pass
        
    def get_custom_context(self):
        return {}

    def append_custom_context(self, context):
        custom_context = self.get_custom_context()        
        for key in custom_context:
            context[key]=custom_context[key]
        return context

    def get_context_data(self, **kwargs):
        context = {}
        context = self.append_custom_context(context)
        return context
class DD_message():
    text = "hola"
    icon = ""
    visible = False
    def set_text(self, text):
        self.visible = True
        self.text=text
    def is_visible(self):
        return self.visible

class home(DDView):
    template_name = 'home.html'
    def get(self, request, rel=None):
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home"]
        context['title'] = "NL2OCL"

        context = {"home": "1"}
        return render(request, self.template_name, context)

class random(DDView):
    template_name = 'base.html'
    def get(self, request, rel=None):
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home"]
        context['title'] = "NL2OCL"
    
        question_list = NLQuestion.objects.all()
        rand = randrange(0, len(question_list)-1)

        return redirect("nl2ocl:question", question_list[rand].pk)


class easy(DDView):
    template_name = 'base.html'
    def get(self, request, rel=None):
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home", "easy"]
        context['title'] = "NL2OCL"
        
        question_list = NLQuestion.objects.filter(qmodel__source=QModel.WIKI).all()
        rand = randrange(0, len(question_list)-1)
        question = question_list[rand]

        return redirect("nl2ocl:question", question_list[rand].pk)

class harder(DDView):
    template_name = 'base.html'
    def get(self, request, rel=None):
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home", "easy"]
        context['title'] = "NL2OCL"
        
        question_list = NLQuestion.objects.filter(qmodel__source=QModel.SPIDER).all()
        rand = randrange(0, len(question_list)-1)

        return redirect("nl2ocl:question", question_list[rand].pk)

class sameModel(DDView):
    template_name = 'base.html'
    def get(self, request, rel=None):
        qmodel = None
        if rel:
            qmodel = get_object_or_404(QModel, pk=rel)
        else:
            redirect("home")
               
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home", "same model"]
        context['title'] = "NL2OCL"
        
        question_list = NLQuestion.objects.filter(qmodel=qmodel).all()
        rand = randrange(0, len(question_list)-1)

        return redirect("nl2ocl:question", question_list[rand].pk)

class question(DDView):
    template_name = 'base.html'
    def get(self, request, rel=None):
        nlquestion = None
        if rel:
            nlquestion = get_object_or_404(NLQuestion, pk=rel)
        else:
            redirect("home")
       
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home"]
        context['title'] = "NL2OCL - " + nlquestion.question

        translations = OCLTranslation.objects.filter(nlquestion=nlquestion)
        reports = ReportedQuestion.objects.filter(nlquestion=nlquestion)
        model = nlquestion.qmodel
        
        context = {"question": nlquestion, "translations": translations, "reports": reports, "model": model, "reportQuestionForm": ReportQuestionForm()}
        return render(request, self.template_name, context)
    
    def post(self, request, rel=None, *args, **kwargs):
        nlquestion = None
        if rel:
            nlquestion = get_object_or_404(NLQuestion, pk=rel)
        else:
            redirect("home")

        data = None
        form = ReportQuestionForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            redirect("home")
   
        report = ReportedQuestion(nlquestion=nlquestion, reason=data["reason"])
        report.save()

        return redirect("nl2ocl:question", nlquestion.pk)        

class saveTranslation(APIView):
    def post(self, request, rel=None):
        if rel:
            question = get_object_or_404(NLQuestion, pk=rel)
        else:
            return JsonResponse({'status': 'error'})
                
        user_translation = None
        formjson=OCLTranslationSerializer(data=request.data)
        if formjson.is_valid():
            user_translation = formjson.validated_data
        else:
            return JsonResponse({'status': 'error', 'errors': "NOT VALID FORM!"}) #  formjson.errors
        
        t = OCLTranslation(translation=user_translation["translation"], nlquestion=question)
        t.save()

        return JsonResponse({'status': 'ok'})

class newQuestion(DDView):
    template_name = 'new.html'
    def get(self, request, rel=None):
        context = self.get_context_data()
        context['breadcrump'] = ["/", "home"]
        context['title'] = "NL2OCL"

        qmodel = None
        if rel:
            qmodel = get_object_or_404(QModel, pk=rel)
        else:
            redirect("home")

        context = {"model": qmodel, "form": NewQuestionForm()}
        return render(request, self.template_name, context)

    def post(self, request, rel=None, *args, **kwargs):
        data = None

        qmodel = None
        if rel:
            qmodel = get_object_or_404(QModel, pk=rel)
        else:
            redirect("home")

        form = NewQuestionForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
        else:
            context = {"model": qmodel}
            return render(request, self.template_name, context)        

        question = NLQuestion(qmodel=qmodel, question=data["question"], user=True, approved=False)
        question.save()
        translation = OCLTranslation(nlquestion=question, translation=data["translation"], user=True, approved=False)
        translation.save()

        return redirect("nl2ocl:question", question.pk)


class getUMLImage(DDView):
    template_name = 'model_image.html'
    def get(self, request, rel=None):
        qmodel = None
        if rel is None:
            pass
        else:
            qmodel = get_object_or_404(QModel, pk=rel)
        
        context = {"model": qmodel}
        path_to_png = os.path.join(BASE_DIR,'static', 'plantuml', qmodel.pascalCaseName+".png")
        path_to_wsd = os.path.join(BASE_DIR,'static', 'plantuml', qmodel.pascalCaseName+".wsd")
        
        if Path(path_to_wsd).is_file() and not Path(path_to_png).is_file():
            subprocess.call(['java', '-jar', os.path.join(BASE_DIR, 'plantuml', 'plantuml.jar'), path_to_wsd])

        elif not Path(path_to_png).is_file():
            qassociations = QAssociation.objects.filter(qmodel=qmodel).all()
            associations = []
            fks = []
            for association in qassociations:
                associates = QAssociate.objects.filter(association=association).select_related("attribute__qclass").all()
                associates_processed = []
                for item in associates:
                    associates_processed.append( {"item": item.attribute, "qclass": item.attribute.qclass, "multiplicity": item.multiplicity} )
            
                fks.append(associates_processed[1]["item"].pk)
                associations.append({"left": associates_processed[0], "right": associates_processed[1]})            
            
            qclassess = QClass.objects.filter(qmodel=qmodel)
            classes = []
            for qclass in qclassess:
                attributes = []
                attributes_raw = QAttribute.objects.filter(qclass=qclass).all()
                for attribute in attributes_raw:
                    if not attribute.pk in fks:
                        attributes.append({"name": attribute.camelCaseName, "type": attribute.pascalCaseType})
                if qmodel.source == QModel.SPIDER:
                    classes.append({"name": qclass.pascalCaseName, "attributes": attributes})            
                else:
                    classes.append({"name": "MyClass", "attributes": attributes})            
            context = {"model": qmodel, "classes": classes, "associations": associations }

            model = qmodel.pascalCaseName
            uml = render_to_string("model.html", context)
            file = os.path.join(BASE_DIR, 'static', 'plantuml', model+'.wsd')
            with open(file, 'w') as f:
                f.write(uml)
            
            subprocess.call(['java', '-jar', os.path.join(BASE_DIR, 'plantuml', 'plantuml.jar'), file])


        return render(request, self.template_name, context)