import json
from collections import Counter


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
    all_courses = sorted(all_courses, key=lambda k: k['attributes'][0]['value'], reverse=True)

    scheduled_courses = []
    counter_cnt = Counter([c['name'] for c in all_courses])
    for course in all_courses:
        for type_resource in course['type']:
            resource = resources[type_resource]
            resource = sorted(resource, key=lambda k: k['attributes'][0]['value'], reverse=True)
            for room in resource:
                scheduled_rnames = list(map(
                    lambda item: item['rname'], scheduled_courses))
                scheduled_cnames = list(map(
                    lambda item: item['cname'], scheduled_courses))

                tot_course_cnt = counter_cnt[course['name']]
                sched_course_cnt = scheduled_cnames.count(course["name"])

                if (room['name'] not in scheduled_rnames
                        and tot_course_cnt != sched_course_cnt):

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
