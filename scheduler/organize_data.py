from .models import Course
from .models import Room

def organize(form_data):
	courses_from_form = create_list_of_all_courses(form_data.items())
	all_courses = Course.objects.filter(cname__in=list(courses_from_form)).order_by('capacity')
	all_rooms = Room.objects.all().order_by('capacity')
	data = {}
	data["courses"] = organize_courses(courses_from_form, all_courses)
	data["rooms"] = organize_rooms(all_rooms)
	return data


def create_list_of_all_courses(form_data):
    all_courses = []
    for key, value in form_data:
        if (key != 'csrfmiddlewaretoken' and int(value) != 0):
            for i in range(int(value)):
                all_courses.append(key)
    return all_courses


def organize_courses(courses_from_form, all_courses):
	ret_courses = []

	for course in courses_from_form:
		curr_course = {}
		for c in all_courses:
			if c.cname == course:
				curr_course["cname"] = c.cname
				curr_course["ccapacity"] = c.capacity
				ret_courses.append(curr_course)
	return ret_courses

def organize_rooms(all_rooms):
	ret_rooms = []
	for room in all_rooms:
		curr_room = {}
		curr_room["rname"] = room.rname
		curr_room["rcapacity"] = room.capacity
		ret_rooms.append(curr_room)
	return ret_rooms