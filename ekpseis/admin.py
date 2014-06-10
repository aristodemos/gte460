# -*- coding: utf-8 -*-
from django.forms import ModelChoiceField
from django.contrib import admin
from ekpseis.models import *

# Register your models here.
class MembershipInline(admin.TabularInline):
	model = Membership
	extra = 2
	list_display_links = ['person']

class StaffAdmin(admin.ModelAdmin):
	fields = ['arxaiotita', 'asma', 'full_name', 'vathmos', 'eidikotita','kathikon', 'date_of_birth','email', 'telephone']
	list_display=('arxaiotita', 'full_name', 'vathmos', 'eidikotita', 'kathikon', 'asma')
	list_display_links = ['full_name']
	#list_editable = ('eidikotita', 'kathikon')
	ordering=['arxaiotita']
	inlines = (MembershipInline,)
		
		
class EkpaideusiAdmin(admin.ModelAdmin):
	list_display=('title','expected_date','f_egkrisis','not_expired', 'completed')
	inlines = (MembershipInline,)

admin.site.register(Ekpaideusi, EkpaideusiAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Kathikonta)
admin.site.register(Eidikotites)
admin.site.register(TrainingType)
admin.site.register(SystemTypes)