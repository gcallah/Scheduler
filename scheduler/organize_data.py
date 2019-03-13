from .models import Course
from .models import Room


def organize(form_data):
    courses_from_form = create_list_of_all_courses(form_data.items())
    all_courses = Course.objects.filter(cname__in=list(courses_from_form)).order_by('capacity')
    all_rooms = Room.objects.all().order_by('capacity')
    data = {
        'consumers': organize_courses(courses_from_form, all_courses),
        'resources': {
            'rooms': organize_rooms(all_rooms)
        }
    }
    return data


def create_list_of_all_courses(form_data):
    all_courses = []
    for key, value in form_data:
        if key != 'csrfmiddlewaretoken' and int(value) != 0:
            all_courses.extend([key] * int(value))
    return all_courses


def organize_courses(courses_from_form, all_courses):
    all_courses_dict = {}
    for course in all_courses:
        all_courses_dict[course.cname] = course.capacity

    ret_courses = []
    for course in courses_from_form:
        if course in all_courses_dict:
            curr_course = {
                'name': course,
                'type': ['rooms'],
                'attributes': {
                    'capacity': {
                        'value': all_courses_dict[course]
                    }
                }
            }
            ret_courses.append(curr_course)

    return sorted(ret_courses, key=lambda k: k['attributes']['capacity']['value'], reverse=True)


def organize_rooms(all_rooms):
    ret_rooms = []
    for room in all_rooms:
        curr_room = {
            "name": room.rname,
            'attributes': {
                'capacity': {
                    'value': room.capacity
                }
            }
        }
        ret_rooms.append(curr_room)
    return sorted(ret_rooms, key=lambda k: k['attributes']['capacity']['value'])
