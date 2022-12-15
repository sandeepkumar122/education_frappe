// Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Merit list Generation', {
	
	refresh: function(frm) {
		
		frm.add_custom_button(("Generate List"),function(){
			var program=frm.selected_doc.program;
			var year=frm.selected_doc.academic_year;
			console.log(program);
			frappe.call({
				method: "erpnext.education.doctype.merit_list_generation.api.generate_list", 
				args:{
					'program':program,
					'academic_year':year
				},
				callback: function(r) {
					console.log(r)
				}
			})
		})
	}
});
