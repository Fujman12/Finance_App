import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

        acquisition_close_date = data.acquisition_close_output
        last_fy_date = data.last_fy_output
        Years = data.no_years_output
        Start_Year = data.start_year_output
        Revenue = data.revenue_output
        COGS = data.cogs_output
        Opex = data.opex_output
        Capex = data.capex_output
        Start_Debt = data.start_debt_output
        Amort_Sched = data.amort_sched_output
        Interest_Rate = data.interest_rate_output
        Depreciation_Perc_Rev = data.deprec_perc_rev_output
        Change_NWC_Perc_Rev = data.changenwc_perc_rev_output
        Tax_Assump = data.tax_assump_output

        Start_Revolver = data.start_revolver_output
        Start_Cash = data.start_cash_output
        Entry_Multiple = data.entry_mult_output
        Exit_Multiple = data.exit_mult_output
        Purchase_EBITDA = data.purchase_ebitda_output

        #Define functions
        Years_Dict = {}
        for x in range(0,Years):
            key = 'Year'+str(x)
            value = Start_Year + x
            Years_Dict[key] = value

        #Calendarisation function
        def calendarisation(acq_close,last_fy):
            acq_close_obj = datetime.strptime(acq_close,'%Y-%m-%d').date()
            last_fy_obj = datetime.strptime(last_fy,'%Y-%m-%d').date()
            next_fy_obj = last_fy_obj + relativedelta(years=1)
            stub_period = next_fy_obj - acq_close_obj
            stub_period_mult = stub_period.days / 365
            return stub_period_mult

        #Calc IRR
        def model_irr(entry_price,exit_price,year):
            cash_flows = []
            for y in range(0,year+1):
                cash_flows.append(0)
            cash_flows[0] = np.negative(entry_price)
            cash_flows[year] = exit_price
            irr_output = np.irr(cash_flows)
            return irr_output

        #Valuation model
        Purchase_Price = Entry_Multiple * Purchase_EBITDA
        Entry_Equity = Purchase_Price - Start_Debt + Start_Cash

        Purchase_Price_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = 0
            Purchase_Price_Dict[key] = value

        Update_PP = {Years_Dict.get('Year0',''): Purchase_Price}
        Purchase_Price_Dict.update(Update_PP)


        Entry_Debt_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = 0
            Entry_Debt_Dict[key] = value

        Update_ED = {Years_Dict.get('Year0',''): Start_Debt}
        Entry_Debt_Dict.update(Update_ED)

        Entry_Net_Debt_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = 0
            Entry_Net_Debt_Dict[key] = value

        Update_ND = {Years_Dict.get('Year0',''): Start_Debt - Start_Cash}
        Entry_Net_Debt_Dict.update(Update_ND)


        Entry_Equity_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = 0
            Entry_Equity_Dict[key] = value

        Entry_Equity_Dict[Start_Year] = Entry_Equity


        #Balance Sheet items

        Revolver_Balance = Start_Revolver
        Cash_Balance = Start_Cash

        #Set Up Calculations

        calendarisation_perc = calendarisation(acquisition_close_date,last_fy_date)

        #Income Statement Calculations

        stub_period = calendarisation(acquisition_close_date,last_fy_date)
        print(stub_period)

        Revenue_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Revenue[x]
            if x == 0:
                Revenue_Dict[key] = value * calendarisation_perc
            else:
                Revenue_Dict[key] = value


        COGS_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = COGS[x]
            if x == 0:
                COGS_Dict[key] = value * calendarisation_perc
            else:
                COGS_Dict[key] = value



        Gross_Margin_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            Gross_Margin_Dict[key] = Revenue_Dict[key] - COGS_Dict[key]


        gross_margin_perc_dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Gross_Margin_Dict[key] / Revenue_Dict[key]
            gross_margin_perc_dict[key] = "{0:.1%}".format(round(value,3))


        Opex_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Opex[x]
            if x == 0:
                Opex_Dict[key] = value * calendarisation_perc
            else:
                Opex_Dict[key] = value



        EBITDA_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            EBITDA_Dict[key] = Gross_Margin_Dict[key] - Opex_Dict[key]



        Depreciation_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            if x == 0:
                Depreciation_Dict[key] = Revenue_Dict[key] * Depreciation_Perc_Rev * calendarisation_perc
            else:
                Depreciation_Dict[key] = Revenue_Dict[key] * Depreciation_Perc_Rev



        Change_NWC_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            if x == 0:
                Change_NWC_Dict[key] = Revenue_Dict[key] * Change_NWC_Perc_Rev * calendarisation_perc
            else:
                Change_NWC_Dict[key] = Revenue_Dict[key] * Change_NWC_Perc_Rev


        #Cash Flow Calculations

        Capex_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Capex[x]
            if x == 0:
                Capex_Dict[key] = value * calendarisation_perc
            else:
                Capex_Dict[key] = value



        #Debt Calculations

        Debt_Amort_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Amort_Sched[x]
            if x == 0:
                Debt_Amort_Dict[key] = value * calendarisation_perc
            else:
                Debt_Amort_Dict[key] = value



        Debt_Sched_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Start_Debt - sum([Debt_Amort_Dict[y] for y in range(Start_Year,Start_Year+x)])
            Debt_Sched_Dict[key] = value



        Interest_Payment_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = Debt_Sched_Dict[key] * Interest_Rate
            if x == 0:
                Interest_Payment_Dict[key] = value * calendarisation_perc
            else:
                Interest_Payment_Dict[key] = value



        #Post EBITDA

        EBT_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = EBITDA_Dict[key] - Depreciation_Dict[key] - Interest_Payment_Dict[key]
            EBT_Dict[key] = value



        Tax_Pay_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = EBT_Dict[key] * Tax_Assump
            Tax_Pay_Dict[key] = value



        #Put together the cash outflow

        CFADS_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = EBITDA_Dict[key] - Capex_Dict[key] - Change_NWC_Dict[key] - Tax_Pay_Dict[key]
            CFADS_Dict[key] = value



        FCF_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = CFADS_Dict[key] - Interest_Payment_Dict[key] - Debt_Amort_Dict[key]
            FCF_Dict[key] = value



        #Draw down the revolver

        Revolver_Draw_Dict = {}
        Revolver_Dict = {}
        Cash_To_BS_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            if FCF_Dict[key] >= 0:
                if FCF_Dict[key] + Revolver_Balance >= Start_Revolver:
                    Cash_To_BS_Dict[key] = FCF_Dict[key] - (Start_Revolver - Revolver_Balance)
                    Revolver_Draw_Dict[key] = Revolver_Balance - Start_Revolver
                    Revolver_Dict[key] = Start_Revolver
                    Revolver_Balance = Start_Revolver
                else:
                    Revolver_Draw_Dict[key] = np.negative(FCF_Dict[key])
                    Revolver_Dict[key] = Revolver_Balance + FCF_Dict[key]
                    Revolver_Balance = Revolver_Balance + FCF_Dict[key]
                    Cash_To_BS_Dict[key] = 0
            else:
                if FCF_Dict[key] + Revolver_Balance >= 0:
                    Revolver_Dict[key] = Revolver_Balance + FCF_Dict[key]
                    Revolver_Draw_Dict[key] = np.negative(FCF_Dict[key])
                    Revolver_Balance = Revolver_Balance + FCF_Dict[key]
                    Cash_To_BS_Dict[key] = 0
                else:
                    Revolver_Dict[key] = 0
                    Revolver_Draw_Dict[key] = Revolver_Balance
                    Revolver_Balance = 0
                    Cash_To_BS_Dict[key] = Revolver_Balance + FCF_Dict[key]


        Cash_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            Cash_Dict[key] = Cash_Balance + Cash_To_BS_Dict[key]
            Cash_Balance = Cash_Balance + Cash_To_BS_Dict[key]


        #End Valuation Summary


        Valuation_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = EBITDA_Dict[key] * Exit_Multiple
            if x == 0:
                if calendarisation_perc == 0:
                    Valuation_Dict[key] = value
                else:
                    Valuation_Dict[key] = value / calendarisation_perc
            else:
                Valuation_Dict[key] = value


        Equity_Value_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            Equity_Value_Dict[key] = Valuation_Dict[key] - Debt_Sched_Dict[key] + Cash_Dict[key]

        Net_Debt_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            Net_Debt_Dict[key] = Debt_Sched_Dict[key] - Cash_Dict[key]


        IRR_Dict = {}
        for x in range(0,Years):
            key = Years_Dict['Year'+str(x)]
            value = model_irr(Entry_Equity,Equity_Value_Dict[key],x+1)
            IRR_Dict[key] = "{0:.0%}".format(round(value,2))


        #Display

        pd.options.display.float_format = '{:,.1f}'.format


        index_names = ['Revenue',
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

        output_data = [Revenue_Dict,
                       COGS_Dict,
                       Gross_Margin_Dict,
                       Opex_Dict,
                       EBITDA_Dict,
                       Capex_Dict,
                       Change_NWC_Dict,
                       Tax_Pay_Dict,
                       CFADS_Dict,
                       Interest_Payment_Dict,
                       Debt_Amort_Dict,
                       FCF_Dict,
                       Revolver_Draw_Dict,
                       Cash_To_BS_Dict]

        self.output_model = pd.DataFrame(index=index_names,
                                    data=output_data)




        bs_names = ['Debt Outstanding',
                    'Revolver Capacity Remaining            ',
                    'Cash on Balance Sheet']

        bs_data = [Debt_Sched_Dict,
                   Revolver_Dict,
                   Cash_Dict]

        self.bs_output = pd.DataFrame(index=bs_names,
                                 data=bs_data)



        entry_names = ['Purchase Price                         ',
                       'Starting Net Debt',
                       'Purchase Equity']

        entry_data = [Purchase_Price_Dict,
                      Entry_Net_Debt_Dict,
                      Entry_Equity_Dict]

        self.entry_output = pd.DataFrame(index=entry_names,
                                    data=entry_data)


        val_names = ['Enterprise Value                       ',
                     'Net Debt',
                     'Equity Value']

        val_data = [Valuation_Dict,
                    Net_Debt_Dict,
                    Equity_Value_Dict
                    ]

        self.val_output = pd.DataFrame(index=val_names,
                                    data=val_data)

        irr_names = ['IRR                                    '
                     ]

        irr_data = [IRR_Dict]

        self.irr_output = pd.DataFrame(index=irr_names,
                                    data=irr_data)


    def show_output(self):
        print(self.output_model)
        print('')
        print(self.bs_output)
        print('')
        print(self.entry_output)
        print('')
        print(self.val_output)
        print('')
        print(self.irr_output)

    def show_irr(self):
        irr_out = self.irr_output.style
        return irr_out

    def show_model(self):
        model_out = self.output_model

        return_mod = model_out.style.apply({'font-weight': 'bold'},
                                            subset=pd.IndexSlice[model_out.index[model_out.index=='(=)EBITDA'],:])
        return return_mod

    def show_bs_output(self):
        bs_out = self.bs_output.style
        return bs_out

    def show_entry(self):
        entry_out = self.entry_output.style
        return entry_out

    def show_val_output(self):
        val_out = self.val_output.style
        return val_out

#Styling

#irr_styled = irr_output.style.set_properties(subset=[Years_Dict['Year0']], **{'width': '300px'})
#irr_styled.render()
