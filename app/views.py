from django.shortcuts import render, redirect
from django.views.generic import View
from core_lbo.core_lbo import LBO_Model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from app.models import inputDB, generate_title


class InputDataView(View):

    def get(self, request, *args, **kwargs):
        inputDBList = []
        if request.user.is_authenticated:
            inputDBList = inputDB.objects.filter(user=request.user)
        return render(request, 'input.html', {'inputDBList': inputDBList or []})

    def post(self, request, *args, **kwargs):
        data = parse_data(request.POST)
        client = LBO_Model('abc', data)
        client.show_output()
        inputDBList = []
        if request.user.is_authenticated:
            inputDBList = inputDB.objects.filter(user=request.user)
        context = {'is_output': True,
                   'show_entry': client.show_entry().set_table_attributes('class="table table-bordered"'),
                   'show_val_output': client.show_val_output().set_table_attributes('class="table table-bordered"'),
                   'show_irr': client.show_irr().set_table_attributes('class="table table-bordered"'),
                   'show_model': client.show_model().set_table_attributes('class="table table-bordered"'),
                   'show_bs_output': client.show_bs_output().set_table_attributes('class="table table-bordered"'),
                   'inputDBList': inputDBList or []
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


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('input')
        else:
            for error, error_list in form.errors.items():
                for error_messege in error_list:
                    messages.error(request, error_messege)
            return redirect('signup')
    else:
        if request.user.is_authenticated:
            return redirect('input')
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('input')
        else:
            messages.error(request,'username or password not correct')
            return redirect('signin')
    else:
        if request.user.is_authenticated:
            return redirect('input')
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_request(request):
    logout(request)
    return redirect('input')


def save_inputDB(request):
    if request.user.is_authenticated:
        data = request.GET.get('data')
        title = request.GET.get('title')

        item = inputDB()
        item.title = generate_title() if not title else title
        item.data = data
        item.user = request.user

        try:
            item.save()
        except:
            return JsonResponse({'status': 'error', 'error': 'Error occurred while saving the item'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Error 403: Forbidden request.'})
    return JsonResponse({'status': 'ok', 'title': item.title, 'id': item.pk })


def update_inputDB(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')
        data = request.GET.get('data')

        item = inputDB.objects.get(pk=id)
        if item:
            item.data = data
        else:
            return JsonResponse({'status': 'error', 'error': 'Error 403: Item with id' + str(id) + ' not found'})
        try:
            item.save()
        except:
            return JsonResponse({'status': 'error', 'error': 'Error occurred while saving the item'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Error 403: Forbidden request.'})
    return JsonResponse({'status': 'ok', 'title': item.title, 'id': item.pk })


def load_inputDB(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')

        item = inputDB.objects.get(pk=id)
        if item:
            return JsonResponse({'status': 'ok', 'title': item.title, 'id': item.pk, 'data': item.data })
        else:
            return JsonResponse({'status': 'error', 'error': 'Error 403: Item with id' + str(id) + ' not found'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Error 403: Forbidden request.'})


def load_inputDB_list(request):
    if request.user.is_authenticated:
        item_list = inputDB.objects.filter(user=request.user).order_by('-date_modified')
        result = [{
            'title': item.title,
            'id': item.id,
            'created': item.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            'updated': item.date_modified.strftime("%Y-%m-%d %H:%M:%S")
        } for item in item_list]
        return JsonResponse({'status': 'ok', 'item_list': result})
    else:
        return JsonResponse({'status': 'error', 'error': 'Error 403: Forbidden request.'})


def delete_inputDB(request):
    if request.user.is_authenticated:
        id = request.GET.get('id')

        item = inputDB.objects.get(pk=id)
        if item:
            try:
                item.delete()
            except:
                return JsonResponse({'status': 'error', 'error': 'Error occurred while deleting the item'})
        else:
            return JsonResponse({'status': 'error', 'error': 'Error 403: Item with id' + str(id) + ' not found'})
    else:
        return JsonResponse({'status': 'error', 'error': 'Error 403: Forbidden request.'})
    return JsonResponse({'status': 'ok'})