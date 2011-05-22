from django.core.management.base import NoArgsCommand

from optparse import make_option

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list 
    help = "########### Imports the list of food items corresponding to one and only one particular restaurant, from a csv file ##############"
    requires_model_validation = True

    def handle_noargs(self, **options):
        from crons.jobrunner import run_immediate_jobs
        run_immediate_jobs()
        return None