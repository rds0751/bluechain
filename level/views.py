from django.shortcuts import render
from django.contrib.auth import get_user_model 
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, FormView, CreateView
from django.shortcuts import render, redirect
from users.models import User
from .models import Activation, LevelIncomeSettings, UserTotal
from django.contrib.auth.decorators import login_required
from wallets.models import WalletHistory
from django.core.paginator import Paginator

class OtherListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "level/search_results_other.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["hide_search"] = True
        context["users_list"] = (
            get_user_model()
            .objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
            .distinct()
        )     
        return context

@login_required
def leveltree(request):
    user = request.user
    page = request.GET.get('page', 1)
    level1 = BinaryTree.objects.filter(direct_user_id=request.user.username, active=True).only('user')
    level1n = []
    for x in level1:
        level1n.append(x)
    level2n = []
    for y in level1n:
        level2 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level2:
            level2n.append(z)
    level3n = []
    for y in level2n:
        level3 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level3:
            level3n.append(z)
    level4n = []
    for y in level3n:
        level4 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level4:
            level4n.append(z)
    level5n = []
    for y in level4n:
        level5 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level5:
            level5n.append(z)
    level6n = []
    for y in level5n:
        level6 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level6:
            level6n.append(z)
    level7n = []
    for y in level6n:
        level7 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level7:
            level7n.append(z)
    level8n = []
    for y in level7n:
        level8 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level8:
            level8n.append(z)
    level9n = []
    for y in level8n:
        level9 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level9:
            level9n.append(z)
    level10n = []
    for y in level9n:
        level10 = BinaryTree.objects.filter(direct_user_id=y, active=True).only('user')
        for z in level10:
            level10n.append(z)
    
    all_levels = [level1n, level2n, level3n, level4n, level5n, level6n, level7n, level8n, level9n, level10n]
    all_users = level1n
    counting = {}
    level = 0
    for a in all_levels:
        level += 1
        counting['{}'.format(level)] = len(a)

    user_list = []
    for u in all_users:
        try:
            user = User.objects.get(username=u)
            user_list.append(user)
        except Exception as e:
            pass
    paginator = Paginator(user_list, 45)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        users = paginator.page(page)
    except(EmptyPage, InvalidPage):
        users = paginator.page(1)

    # Get the index of the current page
    index = users.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index - 4 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]
    return render(request, 'binary/network.html', {'counting': counting, 'user_':request.user, 'user_list':users, 'page_range': page_range,})

@login_required
def leveljoin(request):
    packages = LevelIncomeSettings.objects.all()
    message = "Please Proceed with upgrade"

    def directupgraded(user):
        user = (Activation.objects.filter(Q(user__iexact=str(user))).distinct())
        if user:
            return True
        else:
            return False

    def userjoined(user):
        user = (Activation.objects.filter(Q(user__iexact=str(user))).distinct())
        if user:
            return False
        else:
            return True


    global packamount
    if request.method == 'POST':
        level = 0
        user=request.user
        upline_user = user.referral
        user_id = User.objects.get(username=str(user))
        userjoined = userjoined(user)
        packamount = float(request.POST["amount"])
        if userbal >= packamount:
            if userjoined:
                if user_id.income <= packamount:
                    packamount = packamount - user_id.income
                    user_id.income = 0
                    print("if1")
                    if user_id.binary_income <= packamount:
                        packamount = packamount - user_id.binary_income
                        user_id.binary_income = 0
                        print("if2")
                        if user_id.added_amount <= packamount:
                            packamount = packamount - user_id.added_amount
                            user_id.added_amount = 0
                            print("if3")
                            if packamount != 0:
                                user_id.received_amount = user_id.received_amount - packamount
                                packamount = 0
                                print("if4")
                        else:
                            user_id.added_amount = user_id.added_amount - packamount
                            packamount = 0
                            print("if5")
                    else:
                        user_id.binary_income = user_id.binary_income - packamount
                        packamount = 0
                        print("if6")
                else:
                    user_id.income = user_id.income - packamount
                    packamount = 0
                    print("if7")
                userwallet = WalletHistories()
                userwallet.user_id = user_id
                userwallet.amount = float(request.POST["amount"])
                userwallet.type = "debit"
                userwallet.comment = "spent level id"
                


                user_id.cash_back += 1000
                
                usercashback = WalletHistories()
                usercashback.user_id = user_id
                usercashback.amount = 1000
                usercashback.type = "reward"
                usercashback.comment = "reward points"

                def finduplines(user):
                	try:
                		user = User.objects.get(username__iexact=str(user))
                		upline = user.referal
                	except User.DoesNotExist:
                		upline = 'blank'
                	return upline

                level = 0
                uplines = [upline_user,]
                while level < 10 and upline_user != 'blank':
                	upline_user = finduplines(str(upline_user))
                	uplines.append(upline_user)
                	level += 1

                level = 1
                for upline in uplines:
                	try:
                		upline_user = User.objects.get(username__iexact=upline)
                	except Exception as e:
                		upline_user = 'blank'
                	if upline_user != 'blank':
                		bo = directupgraded(upline_user)
                		if bo:
		                	upline_amount = LevelIncomeSettings.objects.get(level=level).amount
		                	upline_user.income += upline_amount*0.9
		                	upline_wallet = WalletHistories()
		                	upline_wallet.user_id = upline
		                	upline_wallet.amount = upline_amount
		                	upline_wallet.type = "credit"
		                	upline_wallet.comment = "new id upgraded in level{}".format(level)
		                	upline_user.save()
		                	upline_wallet.save()
		                else:
		                	message = 'already upgraded'
	                level = level + 1
                

                
                model = Activation()
                model.user_id = user_id
                model.amount = 999
                model.status = 'success'
                model.binary_level = level
                model.upline_user_id = upline_user
                model.save()
                usercashback.save()
                userwallet.save()
                user_id.save()
                return redirect('/binary/tree/{}'.format(user_id))
            else:
                message = "user already joined new packages coming soon"
        else:
            message = "not enough available balance in wallet"
    else:
        message = ""
    return render(request, 'level/level_join.html', {'packages': packages, "message": message})
