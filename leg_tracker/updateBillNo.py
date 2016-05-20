'''
Utility function to fix rollcall votes
by adding corresponding bill numbers

usage:
export DJANGO_SETTINGS_MODULE=leg_tracker.settings
python updateBillNo.py
'''

import json, os, urllib, re

import django
django.setup()

from billcatcher.models import Bill, Rollcall

#bill_url = 'http://52.22.90.29/bills/?format=json'

rollcall_url = 'http://52.22.90.29/rollcalls/?format=json'

#load bill data
#bill_response = urllib.urlopen(bill_url)
#bill_data = json.loads(bill_response.read())
#print "...bills loaded"

#load all rollcall votes
rollcall_response = urllib.urlopen(rollcall_url)
rollcall_data = json.loads(rollcall_response.read())

#for each vote:
for vote in rollcall_data:
	#get the bill identifier
	bill_url = vote['bill_identifier']
	bill_response = urllib.urlopen(bill_url + '?format=json')
	bill_data = json.loads(bill_response.read())

	print 'Bill number:' + bill_data['bill_number']

	#r = Rollcall.objects.get(rollcall_id=vote['rollcall_id'])
	#r.bill_number = bill_data['bill_number']
	#r.save()

	try:
		Rollcall.objects.filter(rollcall_id=vote['rollcall_id']).update(bill_number=bill_data['bill_number'])
	except:
		print 'Error writing rollcall data on',vote['rollcall_id']
