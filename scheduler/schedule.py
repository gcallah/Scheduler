from django.shortcuts import render
from .models import Course
from .models import Room

site_hdr = "Course Scheduler"


def schedule_algo(request):
    form_data = request.POST
    # Returns a dictionary of courses and the number of sections
    # to schedule for each course. If number of sections is 0,
    # then course name does not get added to dictionary
    courses_from_form = create_list_of_all_courses(form_data.items())
    all_courses = Course.objects.filter(cname__in=list(
        courses_from_form)).order_by('capacity')
    all_rooms = Room.objects.all().order_by('capacity')
    scheduled_courses = make_schedule(all_courses,
                                      all_rooms,
                                      courses_from_form)
    unscheduled_courses = get_unscheduled_course(
        all_courses, scheduled_courses, courses_from_form)
    print(unscheduled_courses)
    print(request)
    return render(request, 'schedule.html', {
        'scheduled': scheduled_courses,
        'unscheduled': unscheduled_courses,
        'header': site_hdr
    })


def create_list_of_all_courses(form_data):
    all_courses = []
    for key, value in form_data:
        if (key != 'csrfmiddlewaretoken' and int(value) != 0):
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
            if (room.rname not in scheduled_rnames and
                    all_courses_total.count(course.cname)
                    != scheduled_cnames.count(course.cname)):
                if course.capacity < room.capacity:
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
