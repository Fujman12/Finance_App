from django.shortcuts import render
from django.views.generic import View
from core_lbo.core_lbo import LBO_Model

class InputDataView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'input.html', {})

    def post(self, request, *args, **kwargs):
        data = parse_data(request.POST)
        client = LBO_Model('abc', data)
        client.show_output()
        context = {'is_output': True,
                   'show_entry': client.show_entry().set_table_attributes('class="table table-bordered"'),
                   'show_val_output': client.show_val_output().set_table_attributes('class="table table-bordered"'),
                   'show_irr': client.show_irr().set_table_attributes('class="table table-bordered"'),
                   'show_model': client.show_model().set_table_attributes('class="table table-bordered"'),
                   'show_bs_output': client.show_bs_output().set_table_attributes('class="table table-bordered"'),
                   }
        return render(request, 'input.html', context)

def parse_data(post):
    result = {}

    date_fields = [
        'acq_close_input',
        'last_fy_input',]

    integer_fields = ['no_years_input']

    float_fields = [
        'entry_mult_input',
        'entry_ebitda',
        'exit_mult_input',
        'changenwc_perc_rev_input',
        'leverage_ebitda',
        'interest_rate_input',
        'start_revolver_input',
        'start_cash_input',
        'deprec_perc_rev_input',]

    list_fields = [
        'revenue_input',
        'cogs_input',
        'opex_input',
        'capex_input',
        'amort_sched_input',]

    for field in date_fields:
        result[field] = post.get(field, '')

    for field in integer_fields:
        result[field] = int(post.get(field, 0))

    for field in float_fields:
        result[field] = float(post.get(field, 0))

    for field in list_fields:
        list = []
        no_years = int(result.get('no_years_input'))
        for year in range(no_years):
            key = field + '_year_' + str(year+1)
            value = float(post.get(key, 0))
            list.append(value)
        result[field] = list
    return result