from users.models import User
from level.models import LevelUser, LevelIncomeSettings
from home.models import Company

import environ
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def universally_used_data(request):
	if not env('DEBUG'):
		try:
			user = request.user.username
			ref = request.user.referral
			c = Company.objects.all()
			try:
				ref = User.objects.get(username=ref)
			except Exception as e:
				ref = User.objects.get(username="VF111111")
			context = {}
			amount = 0
			try:
				levelp = LevelUser.objects.get(user=request.user.username.lower(), active=True)
			except Exception as e:
				levelp = 'None'
				print(e)

			user = User.objects.get(username=request.user)
			try:
				s = LevelUser.objects.get(user=user.username.lower())
			except Exception as e:
				s = e
			directs = LevelUser.objects.filter(direct=user, active=True).count()
			level1 = LevelUser.objects.filter(direct=user.username).order_by('id')
			level1n = []
			for x in level1:
				level1n.append(x)
			level2n = []
			for y in level1n:
				level2 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level2:
					level2n.append(z)
			level3n = []
			for y in level2n:
				level3 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level3:
					level3n.append(z)
			level4n = []
			for y in level3n:
				level4 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level4:
					level4n.append(z)
			level5n = []
			for y in level4n:
				level5 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level5:
					level5n.append(z)
			level6n = []
			for y in level5n:
				level6 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level6:
					level6n.append(z)
			level7n = []
			for y in level6n:
				level7 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level7:
					level7n.append(z)
			level8n = []
			for y in level7n:
				level8 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level8:
					level8n.append(z)
			level9n = []
			for y in level8n:
				level9 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level9:
					level8n.append(z)
			level10n = []
			for y in level9n:
				level10 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level10:
					level10n.append(z)
			level11n = []
			for y in level10n:
				level11 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level11:
					level11n.append(z)
			level12n = []
			for y in level9n:
				level12 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level12:
					level12n.append(z)
			level13n = []
			for y in level12n:
				level13 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level13:
					level13n.append(z)
			level14n = []
			for y in level13n:
				level14 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level14:
					level14n.append(z)
			level15n = []
			for y in level14n:
				level15 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level15:
					level15n.append(z)
			level16n = []
			for y in level15n:
				level16 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level16:
					level16n.append(z)
			level17n = []
			for y in level16n:
				level17 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level17:
					level17n.append(z)
			level18n = []
			for y in level17n:
				level18 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level18:
					level18n.append(z)
			level19n = []
			for y in level18n:
				level19 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level19:
					level19n.append(z)
			level20n = []
			for y in level19n:
				level20 = LevelUser.objects.filter(direct=y).order_by('id')
				for z in level20:
					level20n.append(z)

			all_levels = [
							level1n, 
							level2n, 
							level3n, 
							level4n, 
							level5n,
							level6n, 
							level7n, 
							level8n, 
							level9n, 
							level10n, 
							level11n, 
							level12n, 
							level13n, 
							level14n, 
							level15n, 
							level16n, 
							level17n, 
							level18n, 
							level19n, 
							level20n
						]
			business = {}
			busi = 0
			level = 0
			all = 0
			for a in all_levels:
				level += 1
				b = 0
				for x in a:
					b += x.level.amount
					busi += x.level.amount
					business['{}'.format(level)] = b
					all += 1
					
			context["amount"] = levelp
			context['business'] = business
			context['ref'] = ref
			context['all'] = all
			context['busi'] = busi
			context['c'] = c
		except Exception as e:
			context = {}
	else:
		c = Company.objects.all()
		context = {
		}
		print(request.user.username.lower())
		try:
			levelp = LevelUser.objects.get(user=request.user.username.lower(), active=True)
		except Exception as e:
			levelp = 'None'
			print(e)
		context['c'] = c
		context["amount"] = levelp
	return context