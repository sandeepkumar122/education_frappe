# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from numpy import empty

class reservationforprogram(Document):
	
	def validate(self):
		# total_seat=frappe.db.sql(""" select reserve_seats from `tabSeat Matrix` where  program=%s and academic_year=%s """,(self.program,self.academic_year),as_dict=1)
		# print(total_seat)
		# total_seat=total_seat[0]['reserve_seats']
		filled_seats=frappe.db.sql(""" select sum(number_of_seats_for_this_reservation) as num,reservation from `tabreservation for program` where	academic_year=%s""",(self.academic_year),as_dict=1 )
		print(filled_seats)
		filled_seats=filled_seats[0]['num']
		if(filled_seats==None):
			filled_seats=0
		# if(filled_seats==100):
		# 	frappe.throw("100 percent completed for this program")
		filled_seats=filled_seats + self.number_of_seats_for_this_reservation
		print(filled_seats)
		if(filled_seats>100):
			frappe.throw("after adding this program seats greater")
		#filled_seats=filled_seats[0]['number_of_seats_for_this_reservation']es
		# empty_seats=total_seat-filled_seats
		# if(empty_seats<=0):
		# 	frappe.throw("reserve seats are completed")
	