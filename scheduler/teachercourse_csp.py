from cspsolver import CSP, minConflicts

import random

"""
Takes in the data file and outputs class schedules for each weekday.
"""


def assigner(user_data):
    def add_nodes():
        # nodes have format (c,p)
        for course in courses:
            # enforce room consistency
            if rooms_chosen.get(course) is None:
                # rooms_course = rooms for course
                rooms_course = rooms
            else:
                rooms_course = rooms_chosen[course]
            professor = full_prof_assignment[course]
            if professor is None:
                continue
            domain = [(room, hour) for room in rooms_course for hour in hours_for_prof(professor)]
            node_name = (course, professor)
            csp.add_node(node_name, domain)

    def profs_for_courses(courses):
        profs_chosen = {course: None for course in courses}
        for course in courses:
            hits = []
            for professor in professors:
                their_courses = prof_info[professor]['courses']
                if course in their_courses:
                    hits.append(professor)
            if hits:
                profs_chosen[course] = random.choice(hits)
        return profs_chosen

    # Soft constraint. Assigns courses randomly weighted to preferred days
    def courses_per_day():
        course_days_choice = dict([(course, days_for_course(course)) for course in courses])
        weekdays = ['mon', 'tues', 'wed', 'thur', 'fri']
        courses_on_days = dict([(day, []) for day in weekdays])
        for course, days in course_days_choice.items():
            for day in days:
                courses_on_days[day].append(course)
        return courses_on_days

    def days_for_course(course):
        n = min(course_days_weekly[course], 5)
        days_chosen = []
        # Pairs Mon-Wed and Thurs-Fri preferred if course runs 2 - 4 days
        if 2 <= n <= 4:
            workdays = ['mon', 'wed', 'thur', 'fri'] * 2 + ['tues']
        elif n == 1:
            workdays = ['mon', 'tues', 'wed', 'thur', 'fri']
        else:
            return ['mon', 'tues', 'wed', 'thur', 'fri']
        for i in range(n):
            d = random.choice(workdays)
            if i == 0:
                if d in ['mon', 'wed']:
                    pref = ['mon', 'wed']
                    pref.remove(d)
                    days = ['mon', 'tues', 'wed', 'thur', 'fri']
                    days.remove(d)
                    workdays = days + pref
                elif d in ['thur', 'fri']:
                    pref = ['thur', 'fri']
                    pref.remove(d)
                    days = ['mon', 'tues', 'wed', 'thur', 'fri']
                    days.remove(d)
                    workdays = days + pref
                else:
                    workdays = ['mon', 'wed', 'thur', 'fri']
            else:
                workdays = list(set(workdays))
                workdays.remove(d)
            days_chosen.append(d)
        return days_chosen

    def hours_for_prof(professor):
        # in format (hours,minutes) in 30min intervals
        # start = start_time
        # end = end_time
        start = prof_info[professor]['start_time']
        end = prof_info[professor]['end_time']
        return {(i, j * 30) for i in range(start, end) for j in range(2)}

    def add_unary():
        for node in csp.nodes:
            course, professor = node

            def room_has_capacity(val, course=course, prof=professor):
                room, hour_and_min = val
                no_students = course_no_students[course]
                return bool(room_capacities[room] >= no_students)

            csp.add_unary_constraint((course, professor), room_has_capacity)

    def add_binary():
        nodes = csp.nodes
        for i, n in enumerate(nodes):
            course_n, prof_n = n
            for m in nodes[i:]:
                course_m, prof_m = m
                if prof_n == prof_m:
                    if course_n == course_m:
                        continue
                    '''first binary constraint'''

                    # c1 = course_1, c2 = course_2
                    def no_class_overlap(val1, val2, c1=course_n, c2=course_m):
                        # makes the math easy: calculate course times in
                        # 10min intervals e.g. 120min is 12 intervals
                        hours1, mins1 = val1[1]
                        hours2, mins2 = val2[1]
                        course_start1 = hours1 * 6 + mins1 // 10
                        course_end1 = course_start1 + \
                            course_mins[c1] // 10
                        course_start2 = hours2 * 6 + mins2 // 10
                        course_end2 = course_start2 + \
                            course_mins[c2] // 10
                        # conditions to check if one class starts during other
                        if course_start1 <= course_start2 < course_end1:
                            return bool(False)
                        if course_start2 <= course_start1 < course_end2:
                            return bool(False)
                        # soft constraint: non-sequential classes
                        # get higher weight
                        if course_start1 == course_end2 \
                                or course_start2 == course_end1:
                            return 2
                        return bool(True)

                    csp.add_binary_constraint(n, m, no_class_overlap)
                '''second binary constraint'''

                def no_time_clash(val1, val2, course1=course_n):
                    room1, time1 = val1
                    room2, time2 = val2
                    if room1 != room2:
                        return bool(True)
                    hours1, mins1 = time1
                    hours2, mins2 = time2
                    start_time1 = hours1 * 6 + mins1 // 10
                    end_time1 = start_time1 + course_mins[course1] // 10
                    start_time2 = hours2 * 6 + mins2 // 10
                    if start_time1 <= start_time2 < end_time1:
                        return bool(False)
                    return bool(True)

                csp.add_binary_constraint(n, m, no_time_clash)

    # get the professor-course-room data from the function argument
    professors, prof_info, rooms, room_capacities, courses, \
        course_no_students, course_mins, course_days_weekly = user_data

    # enforce professor-course consistency among different days
    full_prof_assignment = profs_for_courses(courses)
    rooms_chosen = {}  # rooms are consistent
    weekdays = ['mon', 'tues', 'wed', 'thur', 'fri']
    solution = {d: None for d in weekdays}
    retries = 0
    # will retry max 3 times to get a solution
    while retries < 3:
        daily_courses = courses_per_day()
        # upon retry increase maximum iterations
        max_iters = 100 * (retries + 1)
        for d in weekdays:
            csp = CSP()
            courses = daily_courses[d]
            add_nodes()
            add_unary()
            add_binary()
            minconf = minConflicts(csp)
            solved = minconf.solve(max_iters)
            if solved is None:
                retries += 1
                if retries < 3:
                    break
            solution[d] = solved
        break
    return solution