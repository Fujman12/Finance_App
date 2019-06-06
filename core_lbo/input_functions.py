acq_close_input = '2018-06-30'
last_fy_input = '2018-06-30'

no_years_input = 5
start_year_input = 2019

revenue_input = [100.00,120.00,150.00,170.00,200.00]
rev_trans_input = 1.00

cogs_input = [20.00,22.00,25.00,30.00,32.00]
cogs_trans_input = 1.00

opex_input = [50.00,50.00,60.00,65.00,70.00]
opex_trans_input = 1.00

capex_input = [20.00,20.00,20.00,20.00,20.00]
capex_trans_input = 1.00

amort_sched_input = [0.2,0.2,0.2,0.2,0.2]

entry_mult_input = 9.0
entry_mult_add = 0.0

exit_mult_input = 9.0
exit_mult_add = 0.0

entry_ebitda = 15.00

leverage_ebitda = 4.0

interest_rate_input = 0.045

tax_assump_input = 0.29
tax_assump_trans = 0.00

deprec_perc_rev_input = 0.04
deprec_perc_rev_trans = 0.00

changenwc_perc_rev_input = 0.04
changenwc_perc_rev_trans = 0.00

start_revolver_input = 75
start_cash_input = 50

purchase_ebitda_input = entry_ebitda

#Transformations

def apply_trans(target_list,transformer):
    if isinstance(transformer,float):
        new_output = [x * transformer for x in target_list]
        return new_output
    else:
        new_output = target_list


revenue_trans = apply_trans(revenue_input,rev_trans_input)
cogs_trans = apply_trans(cogs_input,cogs_trans_input)
opex_trans = apply_trans(opex_input,opex_trans_input)

capex_trans = apply_trans(capex_input,capex_trans_input)


#Input validation

#check input lengths

check_year_no_inputs = [revenue_input]

for x in check_year_no_inputs:
    if len(x) == no_years_input:
        pass
    else:
        print('Please check inputs')



#Transfer inputs
acquisition_close_output = acq_close_input
last_fy_output = last_fy_input

no_years_output = no_years_input
start_year_output = start_year_input

revenue_output = revenue_trans
cogs_output = cogs_trans
opex_output = opex_trans

capex_output = capex_trans

start_debt_output = entry_ebitda * leverage_ebitda
amort_sched_output = [start_debt_output * y for y in amort_sched_input]
interest_rate_output = interest_rate_input

deprec_perc_rev_output = deprec_perc_rev_input + deprec_perc_rev_trans
changenwc_perc_rev_output = changenwc_perc_rev_input + changenwc_perc_rev_trans

tax_assump_output = tax_assump_input + tax_assump_trans

start_revolver_output = start_revolver_input
start_cash_output = start_cash_input

entry_mult_output = entry_mult_input + entry_mult_add
exit_mult_output = exit_mult_input + exit_mult_add

purchase_ebitda_output = purchase_ebitda_input

#define options




class transfered_input_data(object):
    def __init__(self, data_obj):
        self.acquisition_close_output = data_obj.acq_close_input
        self.last_fy_output = data_obj.last_fy_input

        self.no_years_output = data_obj.no_years_input
        self.start_year_output = data_obj.start_year_input

        self.revenue_output = apply_trans(data_obj.revenue_input, data_obj.rev_trans_input)
        self.cogs_output = apply_trans(data_obj.cogs_input, data_obj.cogs_trans_input)
        self.opex_output = apply_trans(data_obj.opex_input, data_obj.opex_trans_input)

        self.capex_output = apply_trans(data_obj.capex_input, data_obj.capex_trans_input)

        self.start_debt_output = data_obj.entry_ebitda * data_obj.leverage_ebitda
        self.amort_sched_output = [self.start_debt_output * y for y in data_obj.amort_sched_input]
        self.interest_rate_output = data_obj.interest_rate_input

        self.deprec_perc_rev_output = data_obj.deprec_perc_rev_input + data_obj.deprec_perc_rev_trans
        self.changenwc_perc_rev_output = data_obj.changenwc_perc_rev_input + data_obj.changenwc_perc_rev_trans

        self.tax_assump_output = data_obj.tax_assump_input + data_obj.tax_assump_trans

        self.start_revolver_output = data_obj.start_revolver_input
        self.start_cash_output = data_obj.start_cash_input

        self.entry_mult_output = data_obj.entry_mult_input + data_obj.entry_mult_add
        self.exit_mult_output = data_obj.exit_mult_input + data_obj.exit_mult_add

        self.purchase_ebitda_output = data_obj.purchase_ebitda_input



class input_data(object):
    def __init__(self, data):
        self.acq_close_input = data.get('acq_close_input')
        self.last_fy_input = data.get('last_fy_input')

        self.no_years_input = data.get('no_years_input')
        self.start_year_input = 2019

        self.revenue_input = data.get('revenue_input')
        self.rev_trans_input = 1.00

        self.cogs_input = data.get('cogs_input')
        self.cogs_trans_input = 1.00

        self.opex_input = data.get('opex_input')
        self.opex_trans_input = 1.00

        self.capex_input = data.get('capex_input')
        self.capex_trans_input = 1.00

        self.amort_sched_input = data.get('amort_sched_input')

        self.entry_mult_input = data.get('entry_mult_input')
        self.entry_mult_add = 0.0

        self.exit_mult_input = data.get('exit_mult_input')
        self.exit_mult_add = 0.0

        self.entry_ebitda = data.get('entry_ebitda')

        self.leverage_ebitda = data.get('leverage_ebitda')

        self.interest_rate_input = data.get('interest_rate_input')

        self.tax_assump_input = 0.29
        self.tax_assump_trans = 0.00

        self.deprec_perc_rev_input = data.get('deprec_perc_rev_input')
        self.deprec_perc_rev_trans = 0.00

        self.changenwc_perc_rev_input = data.get('changenwc_perc_rev_input')
        self.changenwc_perc_rev_trans = 0.00

        self.start_revolver_input = data.get('start_revolver_input')
        self.start_cash_input = data.get('start_cash_input')

        self.purchase_ebitda_input = self.entry_ebitda

def transfer_inputs(dict_from_site):
    prepare_input = input_data(dict_from_site)
    result = transfered_input_data(prepare_input)
    return result



test_dict = {
        'acq_close_input': '2018-06-30',
        'last_fy_input': '2018-06-30',

        'no_years_input': 5,
        'start_year_input': 2019,

        'revenue_input': [100.00,120.00,150.00,170.00,200.00],
        'rev_trans_input': 1.00,

        'cogs_input': [20.00,22.00,25.00,30.00,32.00],
        'cogs_trans_input': 1.00,

        'opex_input': [50.00,50.00,60.00,65.00,70.00],
        'opex_trans_input': 1.00,

        'capex_input': [20.00,20.00,20.00,20.00,20.00],
        'capex_trans_input': 1.00,

        'amort_sched_input': [0.2,0.2,0.2,0.2,0.2],

        'entry_mult_input': 9.0,
        'entry_mult_add': 0.0,

        'exit_mult_input': 9.0,
        'exit_mult_add': 0.0,

        'entry_ebitda': 15.00,

        'leverage_ebitda': 4.0,

        'interest_rate_input': 0.045,

        'tax_assump_input': 0.29,
        'tax_assump_trans': 0.00,

        'deprec_perc_rev_input': 0.04,
        'deprec_perc_rev_trans': 0.00,

        'changenwc_perc_rev_input': 0.04,
        'changenwc_perc_rev_trans': 0.00,

        'start_revolver_input': 75,
        'start_cash_input': 50,
}