from hrms.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
import frappe
from frappe import _
import json
from math import radians, cos, sin, asin, sqrt
class CustomEmployeeCheckin(EmployeeCheckin):
	

	def validate(self):
		if not self.device_id:
			return
		try:
			locs=self.device_id.split(",")
			lat=float(locs[0])
			lng=float(locs[1])
		except:
			return
		user=frappe.session.user
		emp=frappe.db.get_all("Employee",filters={"user_id":user})
		if len(emp)==0:
			return
		emp=emp[0]["name"]
		shifts=frappe.db.get_list("Shift Assignment",filters={"employee":emp},fields=["shift_type"])
		if len(shifts)==0:
			return
		shift=shifts[0]["shift_type"]
		loc=frappe.db.get_value("Shift Type",shift,"allowed_locations")
		loc=json.loads(loc)
		locations=[]
		closest=999999999999
		for f in loc["features"]:
			geo=f["properties"]
			locations.append({"lat":f["geometry"]["coordinates"][1],"long":f["geometry"]["coordinates"][0],"radius":round(float(geo["radius"]),2)})
			latt=f["geometry"]["coordinates"][1]
			lngg=f["geometry"]["coordinates"][0]
			radius=float(geo["radius"])*0.001
			a = haversine(lngg,latt,lng,lat)
			#frappe.throw(str([a,radius]))
			if a <= radius:
				return
			if radius<closest:
				closest=radius
		frappe.throw(_("Location is not in any valid area for shift {},closest checkin point is {} km away").format(shift,round(radius,3)))


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
