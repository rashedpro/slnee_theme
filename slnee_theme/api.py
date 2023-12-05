import frappe
from hrms.hr.doctype.leave_application.leave_application import get_leave_details
from frappe.utils import getdate
from frappe import _

@frappe.whitelist()
def get_check(date=None):
	date=getdate(date)
	user=frappe.session.user
	emp=frappe.db.get_all("Employee",filters={"user_id":user})
	if len(emp)==0:
		return ({"check_in":None,"check_out":None,"employee":False})
	if not date:
		date=getdate()
	check_in=frappe.get_list("Employee Checkin",filters=[['time', 'between', [date, date]],["log_type","in",["IN"]]],fields=["name","time"],order_by="time asc")
	check_out=frappe.get_list("Employee Checkin",filters=[['time', 'between', [date, date]],["log_type","in",["OUT"]]],fields=["name","time"],order_by="time desc")
	cin=""
	cout=""
	if len(check_in)>0:
		cin=check_in[0]["time"]
	if len(check_out)>0:
		cout=check_out[0]["time"]
	if not cin:
		cin=None
	if not cout:
		cout=None
	return ({"check_in":cin,"check_out":cout,"employee":True})

@frappe.whitelist()
def get_leaves():
	user=frappe.session.user
	emp=frappe.db.get_all("Employee",filters={"user_id":user})
	if len(emp)==0:
		return []
	emp=emp[0]["name"]
	date=getdate()
	balance=get_leave_details(emp,date)
	leaves=frappe.db.get_all("Leave Type")
	l=balance["leave_allocation"]
	new_leaves=[]
	for i in leaves:
		if i["name"] in l.keys():
			new=l[i["name"]]
			new["id"]=i["name"]
			new["name"]=_(i["name"])
			new_leaves.append(new)
		else:
			new={"id":i["name"],"name":_(i["name"]),"total_leaves":0,"expired_leaves":0,"leaves_taken":0,"leaves_pending_approval":0,"remaining_leaves":0}
			new_leaves.append(new)
	data={"leave_balance":new_leaves,"leave_approver":balance["leave_approver"]}
	return data

@frappe.whitelist()
def get_applications(status=None):
	user=frappe.session.user
	emp=frappe.db.get_all("Employee",filters={"user_id":user})
	if len(emp)==0:
		return({"leaves":[],"loans":[]})
	emp=emp[0]["name"]
	leaves_filters={"employee":emp}
	loan_filters={"applicant":emp}
	expenses_filters={"employee":emp}
	benefits_filters={"employee":emp}
	if status:
		leaves_filters["status"]=status
		loan_filters["status"]=status
		expenses_filters["status"]=status
		if status=="Open":
			expenses_filters["status"]="Draft"
			benefits_filters["status"]="Draft"
		elif status =="Opened":
			benefits_filters["status"]="Submitted"
		else:
			benefits_filters["status"]="Cancelled"
	leaves=frappe.db.get_all("Leave Application",filters=leaves_filters,fields=["*"])
	loans=frappe.db.get_all("Loan Application",filters=loan_filters,fields=["*"])
	expenses=frappe.db.get_all("Expense Claim",filters=expenses_filters,fields=["*"])
	shifts=frappe.db.get_all("Shift Request",filters=expenses_filters,fields=["*"])
	benefits=frappe.db.get_all("Employee Benefit Application",filters=benefits_filters,fields=["*"])
	for e in expenses:
		doc=frappe.get_doc("Expense Claim",e["name"])
		e["doctype"]="Expense Claim"
		e["expenses"]=doc.expenses
	for l in loans:
		l["doctype"]="Loan Application"
	for l in leaves:
		l["doctype"]="Leave Application"
	for s in shifts:
		s["doctype"]="Shift Request"
	for b in benefits:
		b["doctype"]="Employee Benefit Application"
	hr=shifts
	payroll=loans+expenses+benefits
	
	data={"leaves":leaves,"hr":hr,"payroll":payroll}
	return data
