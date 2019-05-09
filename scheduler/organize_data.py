from .models import Course
from .models import Room
import re
from random import shuffle, random


def organize(form_data):
    courses_from_form, strategy = create_list_of_all_courses(form_data.items())
    all_courses = Course.objects.filter(cname__in=list(courses_from_form)).order_by('capacity')
    all_rooms = Room.objects.all().order_by('capacity')
    data = {
        'consumers': organize_courses(courses_from_form, all_courses, strategy),
        'resources': {
            'rooms': organize_rooms(all_rooms)
        }
    }
    return data


def create_list_of_all_courses(form_data):
    all_courses = []
    for key, value in form_data:
        if key == 'schedule':
            strategy = value
        elif key != 'csrfmiddlewaretoken' \
                and int(value) != 0:
            all_courses.extend([key] * int(value))
    return all_courses, strategy


def organize_courses(courses_from_form, all_courses, strategy="Sort"):
    course_info = {}

    for course in all_courses:
        course_info[course.cname] = {
            'capacity': course.capacity,
            'cnt': 0,
            'times': course.times.all(),
            'days': course.days.all(),
            'duration': course.duration
        }

    ret_courses = {}
    for course in courses_from_form:
        if course in course_info:
            curr_course = {
                'type': ['rooms'],
                'capacity': {
                    'value': course_info[course]['capacity']
                },
                'time': {
                    'value': organize_course_time(course_info[course]['times'],
                                                  course_info[course]['days'],
                                                  course_info[course]['duration'])
                }
            }
            course_info[course]['cnt'] += 1
            course_name = course + "_" + str(course_info[course]['cnt'])
            ret_courses[course_name] = curr_course

    if strategy == 'Sort':
        return dict(sorted(ret_courses.items(), key=lambda k: k[1]['capacity']['value'], reverse=True))
    else:
        return dict(sorted(ret_courses.items(), key=lambda k: random()))


def organize_rooms(all_rooms):
    ret_rooms = {}
    for room in all_rooms:
        curr_room = {
            'capacity': {
                'value': room.capacity,
                'op_type': "GE"
            },
            'time': {
                'value': organize_room_time(room.times.all(),
                                            room.days.all()),
                'op_type': 'IN'
            }
        }
        ret_rooms[room.rname] = curr_room
    return dict(sorted(ret_rooms.items(), key=lambda k: k[1]['capacity']['value']))


def organize_course_time(times_list, days_list, duration):
    expand_times_list = []
    expand_day_times_list = []
    for time_object in times_list:
        time_int = int(time_object.times)
        expand_times = []
        for time_slots in range(time_int, time_int + duration):
            expand_times.append(str(time_slots))
        expand_times_list.append(expand_times)

    for expand_times in expand_times_list:
        for day_object in days_list:
            expand_day_time = []
            for time_slots in expand_times:
                day_str = day_object.days
                if day_str not in ['MW', 'TuTh']:
                    expand_day_time.append(day_str + time_slots)
                else:
                    len_str = len(day_str)
                    expand_day_time.append(day_str[:len_str // 2] + time_slots)
                    expand_day_time.append(day_str[len_str // 2:] + time_slots)
            expand_day_times_list.append(expand_day_time)

    return expand_day_times_list


def organize_room_time(times_list, days_list):
    day_times_dict = {}
    for time_object in times_list:
        for day_object in days_list:
            time = str(day_object.days) + str(time_object.times)
            day_times_dict[time] = 1
    return day_times_dict


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [atoi(c) for c in re.split(r'(\d+)', text)]


def organize_timeslots(times):
    timeslots = []

    times.sort(key=natural_keys)

    prev_date = None
    prev_time = None
    for item in times:
        arr = re.split('(\d+)', item)
        date = arr[0]
        time = int(arr[1])

        if not prev_date:
            timeslots.append(date + str(time))
            prev_date = date
            prev_time = time
        else:
            if date == prev_date:
                if time == prev_time + 1:
                    prev_time += 1
                else:
                    timeslots[-1] = timeslots[-1] + " - {}{}".format(prev_date, str(prev_time + 1))
                    prev_time = time
                    timeslots.append(date + str(time))
            else:
                timeslots[-1] = timeslots[-1] + " - {}{}".format(prev_date, str(prev_time + 1))
                prev_date = date
                prev_time = time
                timeslots.append(date + str(time))

    if prev_date:
        timeslots[-1] = timeslots[-1] + " - {}{}".format(prev_date, str(prev_time + 1))

    return timeslots


def organize_output(scheduled):
    ret_scheduled = []

    for item in scheduled:
        timeslots = organize_timeslots(item['rattributes']['time'])
        new_item = {
            'rname': item['rname'],
            'cname': item['cname'],
            'course_capacity': item['cattributes']['capacity'],
            'room_capacity': item['rattributes']['capacity'],
            'times': timeslots
        }
        ret_scheduled.append(new_item)

    return ret_scheduled


def organize_request(request):
    data_in = dict()
    if 'reschedule' in request.POST:
        for key in request.POST:
            if key == "csrfmiddlewaretoken":
                data_in[key] = request.POST[key]
            elif key == "reschedule":
                data_in["schedule"] = request.POST[key]
            else:
                pos = key.find("_")
                if pos != -1:
                    course_name = key[:pos]
                    if course_name in data_in:
                        data_in[course_name] += 1
                    else:
                        data_in[course_name] = 1
    else:
        for key in request.POST:
            data_in[key] = request.POST[key][0]
        data_in["schedule"] = "Sort"
    return data_in
