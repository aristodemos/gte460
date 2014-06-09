# -*- coding: utf-8 -*-
import datetime, sys
from django.utils import timezone
from django.db import models
# coding=<encoding name>
# Create your models here.

class Ekpaideusi (models.Model):
	AVIONICS = 'AV'
	SKAFOS = 'FS'
	KINITIRAS='KT'
	SKAFOSKINITIRAS='SK'	
	SUBSYSTEM_CHOICES=(
	(AVIONICS, 'Avionics'),
	(SKAFOS, unicode('Σκάφος')),
	(SKAFOSKINITIRAS, unicode('Σκάφος - Κ/Τ')),
	(KINITIRAS, unicode('Κ/Τ'))
	)
	
	title 		= 	models.CharField(max_length=100)
	f_egkrisis	=	models.CharField(max_length=100)
	system		=	models.ForeignKey('SystemTypes')
	'''Avionics ή Σκάφος ή Κ/Τ  '''
	subsystem	=	models.CharField(max_length=2, choices=SUBSYSTEM_CHOICES, null=True, blank=True)
	location	=	models.CharField(max_length=100)
	'''arxiki i sosme sti moira '''
	type_of_training 	= models.ForeignKey('TrainingType')
	expected_date		= models.DateField("Expected Completion Date")
	completed			= models.BooleanField(default=False)
	
	
	def __unicode__(self):  
		return self.title
	def not_expired(self):
		return not (self.expected_date <= datetime.date.today() and self.completed == False)
	not_expired.admin_order_field 	= 'expected_date'
	not_expired.boolean				= True
	not_expired.short_description	= 'Training Expiry Date Reached'
	class Meta:
		verbose_name = 'Εκπαίδευση'
		verbose_name_plural = 'Εκπαιδεύσεις'
	
class Staff (models.Model):
	full_name	=	models.CharField(max_length=100)
	vathmos		=	models.CharField(max_length=10)
	eidikotita	=	models.ForeignKey('Eidikotites')
	kathikon	=	models.ForeignKey('Kathikonta', 	null=True, blank=True)
	email		= 	models.EmailField(max_length=75, 	null=True, blank=True)
	telephone	=	models.CharField(max_length=10, 	null=True, blank=True)
	asma		=	models.CharField(max_length=5)
	arxaiotita	=	models.PositiveSmallIntegerField()
	trainings	=	models.ManyToManyField('Ekpaideusi', through='Membership')
	'''
	def trainings_names(self):
		return ',' .join([a.title for a in self.trainings.all()])
	trainings_names.short_description = "Training Name"
	'''
	def __unicode__(self):
		return self.full_name
	class Meta:
		verbose_name = 'Στέλεχος'
		verbose_name_plural = 'Προσωπικό'


class Membership(models.Model):
	EPIPEDO1 = 'LV1'
	EPIPEDO3 = 'LV3'
	EPIPEDO5 = 'LV5'
	EPIPEDO7 = 'LV7'
	Epipeda_Ejou_Choices=(
	(EPIPEDO1, 'Επιπέδου 1'), 
	(EPIPEDO3, 'Επιπέδου 3'),
	(EPIPEDO5, 'Επιπέδου 5'), 
	(EPIPEDO7, 'Επιπέδου 7')
	)
	EKTELESTIS1 	= 'EK1'
	EKTELESTIS2 	= 'EK2'
	EPITHEORITIS1 	= 'EP1'
	EPITHEORITIS2 	= 'EP2'
	Vathmoi_Ejou_Choices=(
	(EKTELESTIS1 , 	'Εκτελεστής 1ου'), 
	(EKTELESTIS2 , 	'Εκτελεστής 2ου'),
	(EPITHEORITIS1, 'Επιθεωρητής 1ου'), 
	(EPITHEORITIS2, 'Επιθεωρητής 2ου')
	)
	person = models.ForeignKey(Staff)
	training = models.ForeignKey(Ekpaideusi)
	vathmos_ejou		= models.CharField(max_length=3, choices=Vathmoi_Ejou_Choices, null=True, blank=True )
	epipedo_ejou		= models.CharField(max_length=3, choices=Epipeda_Ejou_Choices, null=True, blank=True)
	
	def __unicode__(self):
		return 'Εξουσιοδοτήσεις'
	class Meta:
		verbose_name = 'Εξουσιοδότηση'
		verbose_name_plural = 'Εξουσιοδοτήσεις'
		ordering = ['-vathmos_ejou', '-epipedo_ejou']
		
class Kathikonta (models.Model):
	kathikon	=	models.CharField(max_length=30)
	def __unicode__(self):
		return self.kathikon
	class Meta:
		verbose_name = 'Καθήκον'
		verbose_name_plural = 'Καθήκοντα'
	
class Eidikotites (models.Model):
	eidikotita	=	models.CharField(max_length=30)
	def __unicode__(self):
		return self.eidikotita
	class Meta:
		verbose_name = 'Ειδικότητα'
		verbose_name_plural = 'Ειδικότητες'

class TrainingType (models.Model):
	Training_Choices = ((u'I', u'Πρωτογενής'),(u'S', u'ΣΟΣΜΕ'),(u'O', u'Other'))
	type_of_training	=	models.CharField(max_length=2, choices=Training_Choices)
	def __unicode__(self):
		return self.type_of_training
	class Meta:
		verbose_name = 'Τύπος Εκπαίδευσης'
		verbose_name_plural = 'Τύποι Εκπαιδεύσεων'

class SystemTypes (models.Model):
	System_Types = (('AW', u'AW139'), ('BN', u'ISLANDER'), ('BL','Bell206'), ('PC', 'PC9'), ('TO', 'Other Tools'), ('GE', 'Ground Handling Equipment'))
	system = models.CharField(max_length=5, choices=System_Types)
	def __unicode__(self):
		return self.system
	class Meta:
		verbose_name = 'Σύστημα'
		verbose_name_plural = 'Συστήματα'
