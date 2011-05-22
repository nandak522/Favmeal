from django.core.management.base import NoArgsCommand

from optparse import make_option

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list 
    help = "########### Runs all the custom sql queries, by parsing each .sql file from schemachanges directroy in the project path ##############"
    requires_model_validation = True

    def handle_noargs(self, **options):
        import os
        from django.conf import settings
        changes_dir = os.path.join(settings.ROOT_PATH, 'schemachanges/')
        changes_list = [f for f in os.listdir(changes_dir) if f.endswith('.sql')]
        changes_list.sort()
        applied_changes = self.get_applied_change_numbers()
        for change in changes_list:
            if change.split(".sql")[0] not in applied_changes:
                print "Applying change ", change
                if self.execute_script(os.path.join(changes_dir, change)):
                    self.note_change_number(change.split(".sql")[0])
        print " Schema changes applied"
    
    def execute_script(self,script_file):
        import re
        from django.db import connection, transaction
        cursor = connection.cursor()
        try:
            statements = re.compile(r";[ \n\t]*$", re.M)
            fp = open(script_file, 'U')
            for statement in statements.split(fp.read()):
                statement = re.sub(r"--.*[\n\Z]", "", statement)
                if statement.strip():
                    statement+= ";"
                    cursor.execute(statement)
            fp.close
            transaction.commit_unless_managed()
            return True
        except Exception, e:
            transaction.rollback_unless_managed()
            print " error ", e, " while applying ", script_file
            return False

    def note_change_number(self,change_number):        
        import datetime
        from django.db import connection, transaction
        cursor = connection.cursor()
        version_note_query =  "insert into schema_tracking (change, applied_on) values ('%s', '%s');" % (change_number, str(datetime.datetime.now()))
        cursor.execute(version_note_query)
        transaction.commit_unless_managed()
    
    def get_applied_change_numbers(self):    
        import datetime
        from django.db import connection, transaction
        try:
            cursor = connection.cursor()
            get_changes =  "select change from schema_tracking ;"
            cursor.execute(get_changes)
            has_more= True
            changes = []
            while has_more:
                rows = cursor.fetchmany(100)
                if not rows:
                    has_more= False
                else:
                    for row in rows:
                       changes.append(row[0])
            transaction.commit_unless_managed()
            return changes
        except Exception:
            transaction.rollback_unless_managed()
            return []