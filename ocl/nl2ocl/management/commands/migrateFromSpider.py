from unicodedata import name
from django.core.management.base import BaseCommand, CommandError
import json
from nl2ocl.management.commands._migrationLib import spider_json_path, spider_json_tables_path
from nl2ocl.models import NLQuestion, QModel, QClass, QAttribute, QAssociation, QAssociate


class Command(BaseCommand):
    help = 'Use to migrate Spider files sotored in /data to Django default Data Base. Unique action: migrate'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)

    def handle(self, *args, **options):
        action = options["action"]
        if action == "migrateTables":
            self.migrateTables()
        elif action == "migrateQuestions":
            self.migrateQuestions()       
        elif action == "migrateAssociations":
            self.migrateAssociations()  

    def migrateTables(self):
        models = 0
        classes = 0
        with open( spider_json_tables_path() ) as f:
            file = ""
            for line in f:
                file = file + line
            db = json.loads(file)
            for data in db:
                database = data['db_id']
                tables = data['table_names']
                columns = data['column_names']
                types = data['column_types']

                qmodel = QModel(name = database, source=QModel.SPIDER)
                qmodel.save()
                models += 1
                    
                for i in range(0, len(tables)):
                    table = tables[i]
                    qclass = QClass(qmodel=qmodel, name=table)
                    qclass.save()
                    classes += 1

                    for w in range(0, len(columns)):
                        column = columns[w]
                        if column[0] == i:
                            qattribute = QAttribute(qclass=qclass, name=column[1], type = types[i])
                            qattribute.save()
        
        self.stdout.write("migrateFromSpider> %s models, %s classes... " % (models, classes) + self.style.SUCCESS("OK"))


    def migrateQuestions(self):
        questions = 0
        with open( spider_json_path() ) as f:
            file = ""
            for line in f:
                file = file + line
            db = json.loads(file)
            for data in db:
                database = data['db_id']
                question_text = data['question']
                query = data['query']

                qmodel = QModel.objects.get(name=database)
                question = NLQuestion(qmodel=qmodel, question=question_text, query=query)
                question.save()

                questions += 1
            
        self.stdout.write("migrateFromSpider> %s questions... " % (questions) + self.style.SUCCESS("OK"))        


    def migrateAssociations(self):
        models = 0
        associations = 0        
        with open( spider_json_tables_path() ) as f:
            file = ""
            for line in f:
                file = file + line
            db = json.loads(file)
            for data in db:
                database = data['db_id']
                columns = data['column_names']
                tables = data['table_names']
                fks = data['foreign_keys']

                qmodel = QModel.objects.filter(name = database, source=QModel.SPIDER).first()
                models = models + 1

                qclassess = []
                for i in range(0, len(tables)):
                    table = tables[i]
                    qclassess.append( QClass.objects.filter(qmodel=qmodel, name=table).first() )

                for i in range(0, len(fks)):
                    fk = fks[i]
                    left = columns[ fk[0] ]
                    right = columns[ fk[1] ]

                    association = QAssociation(qmodel=qmodel)
                    association.save()
                    associations = associations + 1

                    left_attribute = QAttribute.objects.filter(qclass=qclassess[ left[0] ], name=left[1]).first()
                    left_associate = QAssociate(association=association, attribute=left_attribute, role=QAssociate.FOREIGN_KEY)
                    left_associate.save()

                    right_attribute = QAttribute.objects.filter(qclass=qclassess[ right[0] ], name=right[1]).first()
                    right_associate = QAssociate(association=association, attribute=right_attribute, role=QAssociate.REVERSE)
                    right_associate.save()

        self.stdout.write("migrateFromSpider> %s models, %s associations... " % (models, associations) + self.style.SUCCESS("OK"))