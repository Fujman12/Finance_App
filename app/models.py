from django.db import models
from datetime import datetime
from django.conf import settings
import string
import random


class inputDB(models.Model):
    title = models.TextField()
    date_created = models.DateTimeField()
    date_modified = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    data = models.TextField()
    # acq_close_input = models.TextField()
    # last_fy_input = models.TextField()
    #
    # no_years_input = models.IntegerField()
    #
    # entry_mult_input = models.FloatField()
    # entry_ebitda = models.FloatField()
    # exit_mult_input = models.FloatField()
    # changenwc_perc_rev_input = models.FloatField()
    # leverage_ebitda = models.FloatField()
    # interest_rate_input = models.FloatField()
    # start_revolver_input = models.FloatField()
    # start_cash_input = models.FloatField()
    # deprec_perc_rev_input = models.FloatField()
    #
    # revenue_input = models.TextField()
    # cogs_input = models.TextField()
    # opex_input = models.TextField()
    # capex_input = models.TextField()
    # amort_sched_input = models.TextField()


    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        self.date_modified = datetime.now()
        super(inputDB, self).save()

def generate_title():
    result = "ItemName_" + randomString()
    return result


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
