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
    course_cap = {}
    course_cnt = {}
    for course in all_courses:
        course_cap[course.cname] = course.capacity
        course_cnt[course.cname] = 0

    ret_courses = {}
    for course in courses_from_form:
        if course in course_cap:
            curr_course = {
                'type': ['rooms'],
                'capacity': {
                    'value': course_cap[course]
                }
            }
            course_name = course + "_" + str(course_cnt[course])
            course_cnt[course] += 1
            ret_courses[course_name] = curr_course

    return dict(sorted(ret_courses.items(), key=lambda k: k[1]['capacity']['value'], reverse=True))


def organize_rooms(all_rooms):
    ret_rooms = {}
    for room in all_rooms:
        curr_room = {
            'capacity': {
                'value': room.capacity,
                'op_type': "GE"
            }
        }
        ret_rooms[room.rname] = curr_room
    return dict(sorted(ret_rooms.items(), key=lambda k: k[1]['capacity']['value']))


def organize_output(scheduled):
    ret_scheduled = []

    for item in scheduled:
        new_item = {
            'rname': item['rname'],
            'cname': item['cname'],
            'course_capacity': item['cattributes']['capacity']['value'],
            'room_capacity': item['rattributes']['capacity']['value'],
        }
        ret_scheduled.append(new_item)

    return ret_scheduled