from ast import arg
import frappe
from frappe import _

@frappe.whitelist()
def generate_list(**args):
    program_name=args.get('program')
    year=args.get('academic_year')
    edu=['10th Pass','12th Pass','graduate','Post Graduate']

    minimum=frappe.db.sql("""select previous_qualification,minimum_percent_for_eligibility from `tabEligibility Criteria` where program=%s""",(program_name),as_dict=1)
    param_course=minimum[0]['previous_qualification']
    param_index=edu.index(param_course)
    percetage=minimum[0]['minimum_percent_for_eligibility']
    
    user_enter=frappe.db.sql("""select name,minimum_qualification from `tabStudent Applicant` where application_status='Applied' and program=%s and academic_year=%s""",(program_name,year),as_dict=1)
    print(user_enter)
    for j in user_enter:
        name1=j['name']
        doc=frappe.get_doc('Student Applicant',name1)
        quali=j['minimum_qualification']
        eligi=edu.index(quali)
        if param_index>eligi:
            doc.application_status='Not Eligible'
            doc.save()
        
        
    # user_quali=user_enter[0]['minimum_qualification']
    # eligi=edu.index(user_quali)
    # if param_index>eligi:
    #     frappe.throw(_("user "))
    cutOff=frappe.db.sql(""" select select_program,entrance,marks from `tabCut Off` where select_program=%s and year=%s """,(program_name,year),as_dict=1)
    print("\n\n\n")
    print(cutOff[0]['marks'])
    marks=cutOff[0]['marks']
    print("\n\n\n")
    students=frappe.db.sql(""" select name from `tabStudent Applicant` where application_status='Applied' and program=%s and marks>=%s""",(program_name,marks),as_dict=1)
    print("\n\n\n")
    print(students)
    for i in students:
        name=i['name']
        doc=frappe.get_doc('Student Applicant',name)
        doc.application_status='In-Merit'
        doc.save()
    print("\n\n\n")
    return students


