from django.core.management.base import BaseCommand, CommandError
import json
from nl2ocl.management.commands._migrationLib import wikisql_json_path, wikisql_json_tables_path
from nl2ocl.models import NLQuestion, QModel, QClass, QAttribute


class Command(BaseCommand):
    help = 'Use to migrate WikiSQL files sotored in /data to Django default Data Base. Unique action: migrate'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str)

    def handle(self, *args, **options):
        action = options["action"]
        if action == "migrate":
            self.migrateAction()
        
    def migrateAction(self):
        tables = 0
        with open( wikisql_json_tables_path() ) as f:
            for line in f:
                table = json.loads(line.strip())
                table_id = table['id']
                table_header = table['header']
                types = table['types']
                # rows = table['rows']
                qmodel = QModel(name=table_id)
                qmodel.save()
                qclass = QClass(qmodel = qmodel, name=table_id)
                qclass.save()
                for i in range(0, len(table_header)):
                    qattribute = QAttribute(name=table_header[i], type=types[i], qclass=qclass)
                    qattribute.save()
                tables += 1
        
        questions = 0
        with open( wikisql_json_path() ) as f:
            for line in f:
                data = json.loads(line.strip())
                model = data['table_id']
                question_text = data['question']
                qmodel = QModel.objects.get(name=model, source=QModel.WIKI)
                question = NLQuestion(qmodel = qmodel, question = question_text)
                question.save()
                questions += 1
        
        self.stdout.write("migrateFromWikiSQL> %s questions and %s tables... " % (questions, tables) + self.style.SUCCESS("OK"))

        