import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY, YEARLY
from collections import OrderedDict
from .input_functions import test_dict, transfer_inputs

#Inputs

class LBO_Model:
    def __init__(self,name, input_data=test_dict):
        self.name = name

        # acquisition_close_date = acquisition_close_output
        # last_fy_date = last_fy_output
        # Years = no_years_output
        # Start_Year = start_year_output
        # Revenue = revenue_output
        # COGS = cogs_output
        # Opex = opex_output
        # Capex = capex_output
        # Start_Debt = start_debt_output
        # Amort_Sched = amort_sched_output
        # Interest_Rate = interest_rate_output
        # Depreciation_Perc_Rev = deprec_perc_rev_output
        # Change_NWC_Perc_Rev = changenwc_perc_rev_output
        # Tax_Assump = tax_assump_output
        #
        # Start_Revolver = start_revolver_output
        # Start_Cash = start_cash_output
        # Entry_Multiple = entry_mult_output
        # Exit_Multiple = exit_mult_output
        # Purchase_EBITDA = purchase_ebitda_output

        data = transfer_inputs(input_data)

        acq_close_input = data.acquisition_close_output
        last_fy_input = data.last_fy_output
        no_years_input = data.no_years_output
        start_year_input = data.start_year_output
        revenue_input = data.revenue_output
        cogs_input = data.cogs_output
        opex_input = data.opex_output
        capex_input = data.capex_output
        Start_Debt = data.start_debt_output
        amort_sched_input = data.amort_sched_output
        interest_rate_input = data.interest_rate_output
        deprec_perc_rev_input = data.deprec_perc_rev_output
        changenwc_perc_rev_input = data.changenwc_perc_rev_output
        tax_assump_input = data.tax_assump_output
        leverage_mult_input = data.leverage_ebitda_output

        start_revolver_input = data.start_revolver_output
        start_cash_input = data.start_cash_output
        entry_mult_input = data.entry_mult_output
        exit_mult_input = data.exit_mult_output
        entry_ebitda = data.purchase_ebitda_output

        # declare starting variables

        start_debt = entry_ebitda * leverage_mult_input
        start_revolver = start_revolver_input
        revolver_balance = start_revolver_input
        start_cash = start_cash_input
        cash_balance = start_cash_input

        no_years = no_years_input
        start_year = start_year_input

        # required functions

        def calendarisation(acq_close,last_fy):
            acq_close_obj = datetime.datetime.strptime(acq_close,'%Y-%m-%d').date()
            last_fy_obj = datetime.datetime.strptime(last_fy,'%Y-%m-%d').date()
            next_fy_obj = last_fy_obj + relativedelta(years=1)
            stub_period = next_fy_obj - acq_close_obj
            stub_period_mult = stub_period.days / 365
            return stub_period_mult

        def model_irr(entry_price,exit_price,year):
            cash_flows = []
            for y in range(0,year+1):
                cash_flows.append(0)
            cash_flows[0] = np.negative(entry_price)
            cash_flows[year] = exit_price
            irr_output = np.irr(cash_flows)
            return irr_output

        # build time dictionary


        strt_dt = datetime.date(2019,6,1)
        end_dt = datetime.date(2024,6,30)

        dt_interval = 3

        no_per = 12 / dt_interval

        dates = [f"{dt:%d-%b-%Y}" for dt in rrule(MONTHLY,
                                    interval=dt_interval,
                                    bymonthday=-1,
                                    dtstart=strt_dt,
                                    until=end_dt)]



        calendarisation_perc = calendarisation(acq_close_input,last_fy_input)

        # declare the dictionaries

        time_dict = OrderedDict()
        revenue_dict = {}
        cogs_dict = {}
        grossmargin_dict = {}
        opex_dict = {}
        ebitda_dict = {}
        deprec_dict = {}
        changenwc_dict = {}
        capex_dict = {}
        debt_amort_dict = {}
        debt_sched_dict = {}
        interest_pay_dict = {}
        ebit_dict = {}
        ebt_dict = {}
        tax_pay_dict = {}
        netincome_dict = {}
        cfads_dict = {}
        fcf_dict = {}
        revolver_draw_dict = {}
        revolver_drawn_dict = {}
        revolver_avail_dict = {}
        cash_to_bs_dict = {}
        cash_dict = {}

        # build the model - income statement

        counter = 0

        for x in range(0,len(dates)):
            key = 'Period'+str(x)
            y = x - 1
            key1 = 'Period'+str(y)
            value = dates[x]
            time_dict[key] = value

            # set a day zero value for the initial period
            # usually these will be zero for the flow inputs
            # while they will be the input number for balance sheet items

            if x == 0:
                value = 0.0
                revenue_dict[key] = value
                cogs_dict[key] = value
                grossmargin_dict[key] = value
                opex_dict[key] = value
                ebitda_dict[key] = value
                deprec_dict[key] = value
                ebit_dict[key] = value

                capex_dict[key] = value
                changenwc_dict[key] = value
                debt_amort_dict[key] = value
                debt_sched_dict[key] = start_debt
                interest_pay_dict[key] = value
                revolver_draw_dict[key] = value

                ebt_dict[key] = value
                tax_pay_dict[key] = value
                netincome_dict[key] = value

                cfads_dict[key] = value
                fcf_dict[key] = value
                cash_to_bs_dict[key] = value

                revolver_drawn_dict[key] = start_revolver - revolver_balance

                cash_dict[key] = start_cash

            # build the remainder of the flows from year 1 to end

            else:
                revenue_dict[key] = revenue_input[counter] / (12/dt_interval)
                cogs_dict[key] = cogs_input[counter] / (12/dt_interval)
                grossmargin_dict[key] = revenue_dict[key] - cogs_dict[key]
                opex_dict[key] = opex_input[counter] / (12/dt_interval)
                ebitda_dict[key] = grossmargin_dict[key] - opex_dict[key]
                deprec_dict[key] = deprec_perc_rev_input * revenue_dict[key]
                ebit_dict[key] = ebitda_dict[key] - deprec_dict[key]

                capex_dict[key] = capex_input[counter] / (12/dt_interval)
                changenwc_dict[key] = changenwc_perc_rev_input * revenue_dict[key]
                debt_amort_dict[key] = ( amort_sched_input[counter] ) / (12/dt_interval)
                debt_sched_dict[key] = debt_sched_dict[key1] - debt_amort_dict[key]
                # note here on interest, as this is a periodic model
                # debt gets drawn in the period it is needed (key1 - previous period)
                # and paid back in the period it matures (key - current period)
                interest_pay_dict[key] = (dt_interval / 12) * (debt_sched_dict[key1] + revolver_drawn_dict[key1]) * interest_rate_input
                ebit_dict[key] = ebitda_dict[key] - deprec_dict[key]
                ebt_dict[key] = ebit_dict[key] - interest_pay_dict[key]
                tax_pay_dict[key] = ebt_dict[key] * tax_assump_input
                netincome_dict[key] = ebt_dict[key] - tax_pay_dict[key]

                cfads_dict[key] = ebitda_dict[key] - capex_dict[key] - changenwc_dict[key] - tax_pay_dict[key]
                fcf_dict[key] = cfads_dict[key] - interest_pay_dict[key] - debt_amort_dict[key]

                #build the revolver

                if fcf_dict[key] >= 0:
                    if fcf_dict[key] + revolver_balance >= start_revolver:
                        cash_to_bs_dict[key] = fcf_dict[key] - (start_revolver - revolver_balance)
                        revolver_draw_dict[key] = revolver_balance - start_revolver
                        revolver_avail_dict[key] = start_revolver
                        revolver_balance = start_revolver
                        revolver_drawn_dict[key] = (start_revolver - revolver_balance)
                    else:
                        revolver_draw_dict[key] = np.negative(fcf_dict[key])
                        revolver_avail_dict[key] = revolver_balance + fcf_dict[key]
                        revolver_balance = revolver_balance + fcf_dict[key]
                        cash_to_bs_dict[key] = 0
                        revolver_drawn_dict[key] = (start_revolver - revolver_balance)
                else:
                    if fcf_dict[key] + revolver_balance >= 0:
                        revolver_avail_dict[key] = revolver_balance + fcf_dict[key]
                        revolver_draw_dict[key] = np.negative(fcf_dict[key])
                        revolver_balance = revolver_balance + fcf_dict[key]
                        cash_to_bs_dict[key] = 0
                        revolver_drawn_dict[key] = (start_revolver - revolver_balance)
                    else:
                        revolver_avail_dict[key] = 0
                        revolver_draw_dict[key] = revolver_balance
                        revolver_balance = 0
                        cash_to_bs_dict[key] = revolver_balance + fcf_dict[key]
                        revolver_drawn_dict[key] = (start_revolver - revolver_balance)

                # finally, cash

                cash_dict[key] = cash_balance + cash_to_bs_dict[key]
                cash_balance = cash_dict[key]

                if x % (12/dt_interval) == 0:
                    counter = counter + 1
                else:
                    counter = counter


        # aggregate periodic models into annual models

        dates_ann = [f"{dt:%d-%b-%Y}" for dt in rrule(YEARLY,
                                                     interval=1,
                                                     bymonth=6,
                                                     bymonthday=-1,
                                                     dtstart=strt_dt,
                                                     until=end_dt)]

        years_dict = OrderedDict()
        for x in range(0,len(dates_ann)):
            key = 'Year'+str(x)
            value = dates_ann[x]
            years_dict[key] = value


        def annualise(periodic):
            annual = {}
            counting_bal = 0
            for x in range(0,len(dates)):
                key = 'Period'+str(x)
        #        key1 = 'Period'+str(x - 1)
                key_ann = 'Year'+str(int(x/(12/dt_interval)))
                if x == 0:
                    value = periodic['Period'+str(x)]
                    annual[key_ann] = value
                else:
                    if x % (12/dt_interval) != 0:
                        counting_bal = counting_bal + periodic[key]
                    else:
                        counting_bal = counting_bal + periodic[key]
                        value = counting_bal
                        annual[key_ann] = value
                        counting_bal = 0
            return annual


        def annualise_bs(periodic):
            annual = {}
            for x in range(0,len(dates_ann)):
                key = 'Year'+str(x)
                if x == 0:
                    value = periodic['Period'+str(x)]
                    annual[key] = value
                else:
                    z = x * (12/dt_interval)
                    value = periodic['Period'+str(int(z))]
                    annual[key] = value
            return annual


        revenue_ann_dict = annualise(revenue_dict)
        cogs_ann_dict = annualise(cogs_dict)
        grossmargin_ann_dict = annualise(grossmargin_dict)
        opex_ann_dict = annualise(opex_dict)
        ebitda_ann_dict = annualise(ebitda_dict)
        deprec_ann_dict = annualise(deprec_dict)
        ebit_ann_dict = annualise(ebit_dict)
        interest_pay_ann_dict = annualise(interest_pay_dict)
        ebt_ann_dict = annualise(ebt_dict)
        tax_ann_dict = annualise(tax_pay_dict)
        netincome_ann_dict = annualise(netincome_dict)

        capex_ann_dict = annualise(capex_dict)
        changenwc_ann_dict = annualise(changenwc_dict)

        cfads_ann_dict = annualise(cfads_dict)
        debt_amort_ann_dict = annualise(debt_amort_dict)
        fcf_ann_dict = annualise(fcf_dict)
        revolver_draw_ann_dict = annualise(revolver_draw_dict)
        cashtobs_ann_dict = annualise(cash_to_bs_dict)


        cash_ann_dict = annualise_bs(cash_dict)
        debt_sched_ann_dict = annualise_bs(debt_sched_dict)
        revolver_drawn_ann_dict = annualise_bs(revolver_drawn_dict)

        # build valuation models


        purchase_price = entry_mult_input * entry_ebitda
        entry_equity = purchase_price - start_debt + start_cash

        purchase_price_dict = {}
        for x in range(0,len(dates_ann)):
            key = years_dict['Year'+str(x)]
            value = 0
            purchase_price_dict[key] = value

        update_pp = {years_dict.get('Year0',''): purchase_price}
        purchase_price_dict.update(update_pp)


        entry_debt_dict = {}
        for x in range(0,len(dates_ann)):
            key = years_dict['Year'+str(x)]
            value = 0
            entry_debt_dict[key] = value

        update_ed = {years_dict.get('Year0',''): start_debt}
        entry_debt_dict.update(update_ed)

        entry_net_debt_dict = {}
        for x in range(0,len(dates_ann)):
            key = years_dict['Year'+str(x)]
            value = 0
            entry_net_debt_dict[key] = value

        update_nd = {years_dict.get('Year0',''): start_debt - start_cash}
        entry_net_debt_dict.update(update_nd)


        entry_equity_dict = {}
        for x in range(0,len(dates_ann)):
            key = years_dict['Year'+str(x)]
            value = 0
            entry_equity_dict[key] = value

        entry_equity_dict[years_dict['Year0']] = entry_equity

        valuation_dict = {}
        for x in range(0,len(dates_ann)):
            key = 'Year'+str(x)
            value = ebitda_ann_dict[key] * exit_mult_input
            if x == 0:
#                if calendarisation_perc == 0:
                 valuation_dict[key] = purchase_price
#                else:
#                    valuation_dict[key] = value / calendarisation_perc
            else:
                valuation_dict[key] = value


        equity_value_dict = {}
        for x in range(0,len(dates_ann)):
            key = 'Year'+str(x)
            equity_value_dict[key] = valuation_dict[key] - debt_sched_ann_dict[key] - revolver_drawn_ann_dict[key] + cash_ann_dict[key]

        net_debt_dict = {}
        for x in range(0,len(dates_ann)):
            key = 'Year'+str(x)
            net_debt_dict[key] = debt_sched_ann_dict[key] + revolver_drawn_ann_dict[key] - cash_ann_dict[key]


        irr_dict = {}
        for x in range(0,len(dates_ann)):
            key = 'Year'+str(x)
            value = model_irr(entry_equity,equity_value_dict[key],x+1)
            irr_dict[key] = "{0:.0%}".format(round(value,2))

        # build output models


        pd.options.display.float_format = '{:,.1f}'.format


        index_names = ['Period Ending',
                       'Revenue',
                       '(-)COGS',
                       '(=)Gross Margin',
                       '(-)Operating Expenses',
                       '(=)EBITDA',
                       '(-)Capex',
                       '(-/+)Increase/Decrease in NWC',
                       '(-)Cash Tax Payment',
                       '(=)Cash Flow Available for Debt Service',
                       '(-)Interest Payment',
                       '(-)Scheduled Debt Amortisation',
                       '(=)Free Cash Flow',
                       '(+/-)Revolver Drawdown/Repayment',
                       '(=)Cash to Balance Sheet']

        output_data = [time_dict,
                       revenue_dict,
                       cogs_dict,
                       grossmargin_dict,
                       opex_dict,
                       ebitda_dict,
                       capex_dict,
                       changenwc_dict,
                       tax_pay_dict,
                       cfads_dict,
                       interest_pay_dict,
                       debt_amort_dict,
                       fcf_dict,
                       revolver_draw_dict,
                       cash_to_bs_dict]

        output_ann_data = [years_dict,
                           revenue_ann_dict,
                           cogs_ann_dict,
                           grossmargin_ann_dict,
                           opex_ann_dict,
                           ebitda_ann_dict,
                           capex_ann_dict,
                           changenwc_ann_dict,
                           tax_ann_dict,
                           cfads_ann_dict,
                           interest_pay_ann_dict,
                           debt_amort_ann_dict,
                           fcf_ann_dict,
                           revolver_draw_ann_dict,
                           cashtobs_ann_dict]

        self.cashflow_model = pd.DataFrame(index=index_names,
                                    data=output_data)

        self.cashflow_ann_model = pd.DataFrame(index=index_names,
                                          data=output_ann_data)

        index_names = ['Period Ending',
                       'Revenue',
                       '(-)COGS',
                       '(=)Gross Margin',
                       '(-)Operating Expenses',
                       '(=)EBITDA',
                       '(-)Deprecitation',
                       '(=)EBIT',
                       '(+)Net Interest',
                       '(=)PBT',
                       '(-)Tax',
                       '(=)Net Income']

        output_data = [time_dict,
                       revenue_dict,
                       cogs_dict,
                       grossmargin_dict,
                       opex_dict,
                       ebitda_dict,
                       deprec_dict,
                       ebit_dict,
                       interest_pay_dict,
                       ebt_dict,
                       tax_pay_dict,
                       netincome_dict]

        output_ann_data =[years_dict,
                          revenue_ann_dict,
                          cogs_ann_dict,
                          grossmargin_ann_dict,
                          opex_ann_dict,
                          ebitda_ann_dict,
                          deprec_ann_dict,
                          ebit_ann_dict,
                          interest_pay_ann_dict,
                          ebt_ann_dict,
                          tax_ann_dict,
                          netincome_ann_dict]


        self.fin_model = pd.DataFrame(index=index_names,
                                 data=output_data)

        self.fin_ann_model = pd.DataFrame(index=index_names,
                                     data=output_ann_data)


        index_names = ['Debt Outstanding',
                       'Revolver Drawn',
                       'Cash']

        bs_data = [debt_sched_dict,
                   revolver_drawn_dict,
                   cash_dict]


        self.balance_sheet_model = pd.DataFrame(index=index_names,
                                 data=bs_data)


        self.index_names = ['Debt Outstanding',
                       'Revolver Drawn',
                       'Cash']

        bs_ann_data = [debt_sched_ann_dict,
                   revolver_drawn_ann_dict,
                   cash_ann_dict]

        self.balance_sheet_ann_model = pd.DataFrame(index=index_names,
                                 data=bs_ann_data)



        entry_names = ['Purchase Price                         ',
                      'Starting Net Debt',
                      'Purchase Equity']

        entry_data = [purchase_price_dict,
                              entry_net_debt_dict,
                              entry_equity_dict]

        self.entry_output = pd.DataFrame(index=entry_names,
                                            data=entry_data)


        val_names = ['Enterprise Value                       ',
                             'Net Debt',
                             'Equity Value']

        val_data = [valuation_dict,
                            net_debt_dict,
                            equity_value_dict]

        self.val_output = pd.DataFrame(index=val_names,
                                            data=val_data)

        irr_names = ['IRR                                    '
                             ]

        irr_data = [irr_dict]

        self.irr_output = pd.DataFrame(index=irr_names,
                                            data=irr_data)
    def show_output(self):
        print(self.cashflow_ann_model)

    def show_irr(self):
        irr_out = self.irr_output.style
        return irr_out

    def show_model(self):
        model_out = self.cashflow_ann_model

        return_mod = model_out.style
        return return_mod

    def show_bs_output(self):
        bs_out = self.balance_sheet_ann_model.style
        return bs_out

    def show_entry(self):
        entry_out = self.entry_output.style
        return entry_out

    def show_val_output(self):
        val_out = self.val_output.style
        return val_out

#print(amort_sched_dict)
#Styling

#irr_styled = irr_output.style.set_properties(subset=[Years_Dict['Year0']], **{'width': '300px'})
#irr_styled.render()
