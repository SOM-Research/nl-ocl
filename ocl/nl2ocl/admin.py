from django.contrib import admin
from .models import NLQuestion, OCLTranslation, ReportedQuestion

admin.site.register(NLQuestion)
admin.site.register(OCLTranslation)
admin.site.register(ReportedQuestion)