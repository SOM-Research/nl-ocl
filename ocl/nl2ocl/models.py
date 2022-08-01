from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.db.models.fields.related import ForeignKey, RelatedField
import re


class QModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    WIKI = 'W'
    SPIDER = 'S'
    ModelSources = [
        (WIKI, 'WikiSQL'),
        (SPIDER, 'Spider'),
    ]
    source = models.CharField(
        max_length=1,
        choices=ModelSources,
        default=WIKI,
    )
    @property
    def pascalCaseName(self):
        self.name = re.sub('[^0-9a-zA-Z]+', ' ', self.name)
        name_list = self.name.split(' ')
        for i in range( 0, len(name_list)):
            name_list[i] = str(name_list[i]).capitalize()
        return "".join(name_list)    

    def __str__(self):
        return '%s' % (self.name)

class NLQuestion(models.Model):
    qmodel = models.ForeignKey(QModel, on_delete=models.CASCADE, related_name="questions")    
    question = models.TextField()
    user = models.BooleanField(default=False)
    approved = models.BooleanField(default=True)
    query = models.TextField(default=None, null=True)
    
    def __str__(self):
        return '%s' % (self.question)

class OCLTranslation(models.Model):
    nlquestion = models.ForeignKey(NLQuestion, on_delete=models.CASCADE, related_name="translation")    
    translation = models.TextField(default=None)
    date=models.DateTimeField(auto_now_add=True)
    user = models.BooleanField(default=True)    
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return '%s' % (self.translation)

class ReportedQuestion(models.Model):
    nlquestion = models.ForeignKey(NLQuestion, on_delete=models.CASCADE, related_name="reportedQuestion")    
    reason = models.TextField(default=None)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return '%s' % (self.reason)

class QClass(models.Model):
    qmodel = models.ForeignKey(QModel, on_delete=models.CASCADE, related_name="tables")
    name = models.CharField(max_length=200)
    @property
    def pascalCaseName(self):
        self.name = re.sub('[^0-9a-zA-Z]+', ' ', self.name)
        name_list = self.name.split(' ')
        for i in range( 0, len(name_list)):
            name_list[i] = str(name_list[i]).capitalize()
        return "".join(name_list)
    
    def __str__(self):
        return '%s' % (self.name)


class QAttribute(models.Model):
    qclass = models.ForeignKey(QClass, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)

    @property
    def pascalCaseType(self):
        if str(self.type).lower() == "text":
            self.type = "String"
        elif str(self.type).lower() == "number":
            self.type = "Int"
        elif str(self.type).lower() == "time":
            self.type = "Date"            
 
        name_list = self.type.split(' ')
        for i in range( 0, len(name_list)):
            name_list[i] = str(name_list[i]).capitalize()
        return "".join(name_list)

    @property
    def camelCaseName(self):
        self.name = re.sub('[^0-9a-zA-Z]+', ' ', self.name)
        name_list = self.name.split(' ')
        for i in range( 0, len(name_list)):
            name_list[i] = str(name_list[i]).capitalize()
        res = "".join(name_list)
        return res[0].lower() + res[1:]
    
    def __str__(self):
        return '%s' % (self.name)

class QAssociation(models.Model):
    qmodel = models.ForeignKey(QModel, on_delete=models.CASCADE)

class QAssociate(models.Model):
    association = models.ForeignKey(QAssociation, on_delete=models.CASCADE)
    attribute = models.ForeignKey(QAttribute, on_delete=models.CASCADE)

    FOREIGN_KEY = 'FK'
    REVERSE = 'RV'
    Roles = [
        (FOREIGN_KEY, 'FK'),
        (REVERSE, 'RV'),
    ]
    role = models.CharField(
        max_length=2,
        choices=Roles,
        default=FOREIGN_KEY,
    )    

    @property
    def multiplicity(self):
        if self.role == self.FOREIGN_KEY:
            return "*"
        else:
            return "1"

