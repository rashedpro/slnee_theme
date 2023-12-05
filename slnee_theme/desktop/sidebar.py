
import frappe
from frappe import _

@frappe.whitelist()
def get_language():
	return ( frappe.get_doc("User",frappe.session.user).language or "en" )


@frappe.whitelist()
def change_language(user,language):
	doc=frappe.get_doc("User",user)
	if doc.language!=language:
		doc.language=language
		doc.save()
		frappe.db.commit()
		return("changed")
	return("same")

@frappe.whitelist()
def get_sidebar(module):
	if not module or module =="Home":
		return
	workspace=frappe.get_doc("Workspace",module)
	hide_no_childs=workspace.hide_no_childs
	module_items=workspace.sidebar_items
	items=[]
	count=0
	total=len(module_items)
	for i in module_items:
		if i.is_menu:
			item=i.__dict__
			item["label"]=_(item["label"])
			if count +1 < total and not  module_items[count+1].is_menu:
				item["childs"]=get_childs(count+1,total,module_items)
				items.append(item)
			else:
				if not hide_no_childs:
					item["childs"]=[]
					items.append(item)
		count+=1
	if workspace.force_default:
		color1= workspace.default_color_1
		color2=  workspace.default_color_2
	else:
		color1=workspace.color or workspace.default_color_1  or "#03fcca"
		color2=workspace.color_2 or workspace.default_color_2 or "#03fc88"
	font=workspace.font or ""
	font_css=workspace.font_css1 or ""
	module={"items":items,"color1":color1,"color2":color2,"direction":workspace.direction,"font":font,"font_css":font_css}
	return (module)


def get_childs(c,total,module_items):
	childs=[]
	while(True):
		if c>=total :
			return childs
		i=module_items[c]
		if i.is_menu:
			return childs
		if i.type=="Doctype":
			url="/app/"+i.doctype_url.replace(" ","-").lower()
		else:
			url="/app/query-report/"+i.report_url
		item=i.__dict__
		item["childs"]=[]
		item["url"]=url
		item["label"]=_(item["label"])
		childs.append(item)
		c+=1



@frappe.whitelist()
def update_sidebar(module,new_name="",childs=[]):
	doc=frappe.get_doc("Workspace",module)
	if new_name:
		doc.rename(new_name)
		doc.title=new_name
	doc.save()
	frappe.db.commit()
