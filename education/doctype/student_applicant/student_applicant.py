# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_years, date_diff, getdate, nowdate


class StudentApplicant(Document):
	def autoname(self):
		from frappe.model.naming import set_name_by_naming_series
		if self.student_admission:
			naming_series = None
			if self.program:
				# set the naming series from the student admission if provided.
				student_admission = get_student_admission_data(self.student_admission, self.program)
				if student_admission:
					naming_series = student_admission.get("applicant_naming_series")
				else:
					naming_series = None
			else:
				frappe.throw(_("Select the program first"))

			if naming_series:
				self.naming_series = naming_series

		set_name_by_naming_series(self)

	def validate(self):
		self.validate_dates()
		self.title = " ".join(filter(None, [self.first_name, self.middle_name, self.last_name]))

		if self.student_admission and self.program and self.date_of_birth:
			self.validation_from_student_admission()

	def validate_dates(self):
		if self.date_of_birth and getdate(self.date_of_birth) >= getdate():
			frappe.throw(_("Date of Birth cannot be greater than today."))


	def on_update_after_submit(self):
		student = frappe.get_list("Student",  filters= {"student_applicant": self.name})
		if student:
			frappe.throw(_("Cannot change status as student {0} is linked with student application {1}").format(student[0].name, self.name))

	def on_submit(self):
		if self.paid and not self.student_admission:
			frappe.throw(_("Please select Student Admission which is mandatory for the paid student applicant"))

	def validation_from_student_admission(self):

		student_admission = get_student_admission_data(self.student_admission, self.program)

		if student_admission and student_admission.min_age and \
			date_diff(nowdate(), add_years(getdate(self.date_of_birth), student_admission.min_age)) < 0:
				frappe.throw(_("Not eligible for the admission in this program as per Date Of Birth"))

		if student_admission and student_admission.max_age and \
			date_diff(nowdate(), add_years(getdate(self.date_of_birth), student_admission.max_age)) > 0:
				frappe.throw(_("Not eligible for the admission in this program as per Date Of Birth"))


	def on_payment_authorized(self, *args, **kwargs):
		self.db_set('paid', 1)

	# def before_submit(self):
	# 	doc=frappe.get_doc('Student Applicant',self.name)
	# 	entrance=doc.entrance
		
	# 	check_entrance=frappe.db.sql(""" select entrance from `tabCut Off` where select_program=%s""",(doc.program))
	# 	if(entrance!=check_entrance):
	# 		frappe.throw(_("user has choosen wrong entrance"))

	def before_submit(self):
		doc=frappe.get_doc('Student Applicant',self.name)
		print("\n\n\n\n\n")
		program=doc.program
		reservation=doc.reservation
		year=doc.academic_year
		#fetching total seats 
		total_seat=frappe.db.sql("""select total_seat,reserve_seats from `tabSeat Matrix` where  program=%s and academic_year=%s """,(program,year),as_dict=1)
		print(total_seat)
		total=total_seat[0]['total_seat']
		reserve=total_seat[0]['reserve_seats'] 
		general_cat=total-reserve
		#seats which are full
		count= frappe.db.sql("""select count(*) as num from `tabStudent Applicant` where reservation=%s and program=%s and academic_year=%s and application_status='Admitted'""",(reservation,program,year),as_dict=1)
		count=count[0]['num']
		print(reservation)
		print(program)
		#for every reservation how many number of seats alloted
		reservation_program=frappe.db.sql("""select number_of_seats_for_this_reservation from `tabreservation for program` where reservation=%s and academic_year=%s""",(reservation,year),as_dict=1)
		print(reservation_program)
		print("\n\n\n\n\n")
		reserve_percent=reservation_program[0]['number_of_seats_for_this_reservation']
		reserve_seats=(reserve_percent/100)*reserve
		print("open seats")
		print(reserve_seats)
		#checking open seats count 
		if reservation=='':
			print("checking general category")
			if count>=general_cat:
				frappe.throw(_("general category seats are fulled"))
		
		print("checking reserve category")
		if count>=reserve:
			frappe.throw(_("reserve category has been full"))
		# 	print("from inside")
		self.validate_program_seats(reservation,count)
		print("\n\n\n\n\n")
		# frappe.throw("all are working ")

	def validate_program_seats(self,reservation,count):
		print("checking program wise seats for ncc,nss")
		reserve_seats=frappe.db.sql("""select number_of_seats_for_this_reservation from `tabreservation for program` where reservation=%s """,(reservation),as_dict=1)

		reserve_seats=reserve_seats[0]['number_of_seats_for_this_reservation']
		print(reserve_seats)
		if count>=reserve_seats:
			frappe.throw(_("Seats is fulled"))
		
		
		
def get_student_admission_data(student_admission, program):

	student_admission = frappe.db.sql("""select sa.admission_start_date, sa.admission_end_date,
		sap.program, sap.min_age, sap.max_age, sap.applicant_naming_series
		from `tabStudent Admission` sa, `tabStudent Admission Program` sap
		where sa.name = sap.parent and sa.name = %s and sap.program = %s""", (student_admission, program), as_dict=1)

	if student_admission:
		return student_admission[0]
	else:
		return None

