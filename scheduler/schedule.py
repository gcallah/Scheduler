from .models import Course
from .models import Room
import json
from collections import Counter


def schedule_algo(request):
    form_data = request.POST
    courses_from_form = create_list_of_all_courses(form_data.items())
    all_courses = Course.objects.filter(
        cname__in=list(courses_from_form)).order_by('capacity')
    all_rooms = Room.objects.all().order_by('capacity')

    scheduled_courses = make_schedule(all_courses, all_rooms,
                                      courses_from_form)
    unscheduled_courses = get_unscheduled_course(
        all_courses, scheduled_courses, courses_from_form)

    return scheduled_courses, unscheduled_courses


def create_list_of_all_courses(form_data):
    all_courses = []
    for key, value in form_data:
        if key != 'csrfmiddlewaretoken' and int(value) != 0:
            for i in range(int(value)):
                all_courses.append(key)
    return all_courses


def make_schedule(all_courses, all_rooms, all_courses_total):
    scheduled_courses = []
    for course in all_courses:
        for room in all_rooms:
            scheduled_rnames = list(map(
                lambda course: course['rname'], scheduled_courses))
            scheduled_cnames = list(map(
                lambda course: course['cname'], scheduled_courses))
            cur_course_cnt = all_courses_total.count(course.cname)
            sched_course_cnt = scheduled_cnames.count(course.cname)
            if (room.rname not in scheduled_rnames
                    and course.cname not in scheduled_cnames
                    and (cur_course_cnt != sched_course_cnt
                         or (cur_course_cnt == sched_course_cnt
                             and cur_course_cnt == 0))):
                if course.capacity <= room.capacity:
                    # and course.days == room.days
                    # and course.start_time >= room.start_time
                    # and course.start_time < room.end_time
                    # and course.end_time <= room.end_time):

                    scheduled_course = {
                        "rname": room.rname,
                        "cname": course.cname,
                        "course_capacity": course.capacity,
                        "room_capacity": room.capacity,
                        "start_time": course.start_time,
                        "end_time": course.end_time,
                        "day_of_week": course.days
                    }

                    scheduled_courses.append(scheduled_course)
    return scheduled_courses


def get_unscheduled_course(all_courses, scheduled_courses, all_courses_total):
    unscheduled_courses = []
    course_names = [d['cname'] for d in scheduled_courses]

    for course in all_courses_total:
        num_scheduled = course_names.count(course)
        num_unscheduled = unscheduled_courses.count(course)
        total_num = all_courses_total.count(course)
        if num_scheduled + num_unscheduled != total_num:
            unscheduled_courses.append(course)

    return unscheduled_courses


# BELOW IS THE METHOD WITH THE APPLIED MIGRATED LOGIC FOR JSON COMMUNICATION
def sched(data):
    data_dict = json.loads(data)
    consumers = data_dict['consumers']
    resourses = data_dict['resources']

    sched = make_sched(consumers, resourses)
    unsched = get_unsched(consumers, sched)

    ret_val = {}
    ret_val['scheduled'] = sched
    ret_val['unscheduled'] = unsched
    return json.dumps(ret_val)


def make_sched(all_courses, resources):
    scheduled_courses = []
    for course in all_courses:
        for type_resource in course['type']:
            resource = resources[type_resource]
            for room in resource:
                scheduled_rnames = list(map(
                    lambda item: item['rname'], scheduled_courses))
                scheduled_cnames = list(map(
                    lambda item: item['cname'], scheduled_courses))
                cur_course_cnt = all_courses.count(course['name'])
                sched_course_cnt = scheduled_cnames.count(course['name'])

                if (room['name'] not in scheduled_rnames
                        and course['name'] not in scheduled_cnames
                        and (cur_course_cnt != sched_course_cnt
                             or (cur_course_cnt == sched_course_cnt
                                 and cur_course_cnt == 0))):
                    ccap = course['attributes'][0]['value']
                    rcap = room['attributes'][0]['value']
                    if ccap <= rcap:
                        scheduled_course = {
                            'rname': room['name'],
                            'cname': course['name'],
                            'course_capacity': ccap,
                            'room_capacity': rcap,
                        }

                        scheduled_courses.append(scheduled_course)
    return scheduled_courses


def get_unsched(all_courses, scheduled_courses):
    unscheduled_courses = []
    sched_course_names = [d['cname'] for d in scheduled_courses]
    all_course_names = [d['name'] for d in all_courses]

    for course in sched_course_names:
        try:
            all_course_names.remove(course)
        except ValueError:
            pass

    return all_course_names
