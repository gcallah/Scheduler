from cspsolver import CSP, minConflicts

import random
import collections

"""
Takes in the data file and outputs class schedules for each weekday.
"""

MONDAY = 'mon'
TUESDAY = 'tues'
WEDNESDAY = 'wed'
THURSDAY = 'thur'
FRIDAY = 'fri'
WEEKDAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]


def pref_handler(rand_day):
    """Given a random day, return a list of days weighted by preference.

    Arguments:
        rand_day {string} -- A string representing a random day.

    Returns:
        [list] -- [A list of days weighted by preference]
    """
    days = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
    if rand_day not in days:
        raise ValueError("The random day is not in work day.")
    if rand_day == TUESDAY:
        return [MONDAY, WEDNESDAY, THURSDAY, FRIDAY]
    pref = [MONDAY, WEDNESDAY] if rand_day in (
        MONDAY, WEDNESDAY) else [THURSDAY, FRIDAY]
    return [day for day in (pref + days) if day != rand_day]


def assign_days_for_course(course_weekly_days):
    """Assign randomly the meetings days for a
    class given how many time it is held weekly.

    Arguments:
        course_weekly_days {int} -- how many days the class is held per week.

    Returns:
        [list] -- A list of days chosen for the class.
    """
    course_weekly_days = min(course_weekly_days, 5)
    days_chosen = []
    if course_weekly_days == 1:
        workdays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
    elif 2 <= course_weekly_days <= 4:
        # Pairs Mon-Wed and Thurs-Fri preferred if course is held 2 - 4 days
        # per week.
        workdays = [MONDAY, WEDNESDAY, THURSDAY, FRIDAY] * 2 + [TUESDAY]
    else:
        return [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
    for i in range(course_weekly_days):
        rand_day = random.choice(workdays)
        if i == 0:
            workdays = pref_handler(rand_day)
        else:
            workdays = list(set(workdays))
            workdays.remove(rand_day)
        days_chosen.append(rand_day)
    return days_chosen


def maps_day_to_class(course_days_weekly, courses):
    """Maps preferred days to classes (soft constraint).

    Arguments:
        course_days_weekly {dict} --
        A map {class: how many days it's held per week}.
        courses {list} -- A list of classes.

    Returns:
        [dict] -- Returns a map {day: a list of classes on that day}.
    """
    courses_on_days = collections.defaultdict(list)
    for course in courses:
        course_days = assign_days_for_course(course_days_weekly[course])
        for day in course_days:
            courses_on_days[day].append(course)
    return courses_on_days


def hours_for_prof(prof_info, professor_name):
    """Assigns a professor time for their class based on their preferences

    Arguments:
        prof_info {dict} -- A dictionary mapping professor to his class info.
        professor_name {string} -- A professor's name.

    Returns:
        [set] -- A set of (hours, minutes) interval for a professor.
    """
    start = prof_info[professor_name]['start_time']
    end = prof_info[professor_name]['end_time']
    hours_set = {(i, j * 30) for i in range(start, end) for j in range(2)}
    return hours_set


def profs_for_courses(courses, professors, prof_info):
    """Assign professors to given list of courses.

    Arguments:
        courses {list} -- A list of classes.
        professors {list} -- A list of professors.
        prof_info {dict} -- A dictionary mapping professor to
        his class info (courses taught, start_time, end_time).

    Returns:
        [dict] -- Returns a map {course : professor}.
    """
    profs_chosen = {}
    for course in courses:
        intersection = [
            professor for professor in professors if course in prof_info[professor]['courses']]
        if intersection:
            profs_chosen[course] = random.choice(intersection)
    return profs_chosen


def add_nodes(
        courses,
        rooms,
        rooms_chosen,
        full_prof_assignment,
        prof_info,
        csp):
    """Adds nodes (course, professor) and its
    list of domains (rooms, hours) to csp.

    Arguments:
        courses {list} -- A list of classes.
        rooms {list} -- A list of rooms.
        rooms_chosen {dict} -- A dictionary mapping course to rooms.
        full_prof_assignment {dict} --
        A dictionary mapping course to professor.
        prof_info {dict} -- A dictionary mapping professor
        to his class info (courses taught, start_time, end_time).
        csp {cspsolver.CSP} -- A instance of the
        Constraint Satisfaction Problem class.
    """
    for course in courses:
        rooms_for_course = rooms_chosen[course] if course in rooms_chosen else rooms
        professor = full_prof_assignment[course]
        if professor:
            domain = [
                (room,
                 hour) for room in rooms_for_course for hour in hours_for_prof(
                    prof_info,
                    professor)]
            node_name = (course, professor)
            csp.add_node(node_name, domain)


def add_unary_constraint(csp, room_has_capacity):
    """Adds an unary constraint to list of nodes

    Arguments:
        csp {cspsolver.CSP} -- A instance of the
        Constraint Satisfaction Problem class.
        room_has_capacity {<class 'function'>} --
        An unary constraint function.
    """
    for node in csp.nodes:
        csp.add_unary_constraint(node, room_has_capacity)


def compute_course_start_end(
        start_hour,
        start_mins,
        course_mins_map,
        course_name):
    """Given course name, start time, and its duration,
    computes and format end time.

    Arguments:
        start_hour {int} -- Start hour of the course.
        start_mins {[type]} -- Start minute of the course.
        course_mins_map {dict} -- A dictionary mapping course name to duration.
        course_name {str} -- Course name.

    Returns:
        [tuple] -- A tuple of course start and end time in desired format.
    """
    course_start_time = start_hour * 6 + start_mins // 10
    duration = course_mins_map[course_name]
    course_end_time = course_start_time + duration
    return (course_start_time, course_end_time)


def add_binary_constraint(csp, course_mins_map, no_class_overlap, no_time_clash):
    """Adds binary constraints to list of nodes.
    """
    for index, node_n in enumerate(csp.nodes):
        (course_n, prof_n) = node_n
        for j in range(index, len(csp.nodes)):
            node_m = csp.nodes[j]
            (course_m, prof_m) = node_m
            if prof_n == prof_m:
                if course_n == course_m:
                    continue
                csp.add_binary_constraint(node_n, node_m, no_class_overlap)
            csp.add_binary_constraint(node_n, node_m, no_time_clash)


def assigner(user_data):
    """Takes in data provided by the user and creates class schedule.

    Arguments:
        user_data {tuple} -- A tuple of lists containing
        the user's data information.

    Returns:
        [dict] -- Returns a map {day: a list of classes taught
        by professors with room numbers and times}.
    """
    def room_has_capacity(val, course):
        """Unary constraints function: checks to see if given room has
        room for all students in course.

        Arguments:
            val {tuple} -- Contains values for room and time of class.
            Course {string} -- Name of course.

        Returns:
            [bool] -- Whether or not the room has
            capacity for all students in course.
        """
        room, hour_and_min = val
        no_students = course_no_students[course]
        return room_capacities[room] >= no_students

    def no_class_overlap(node1, node2, course1, course2):
        """Binary constraint function: checks to see if
        there is overlap in times between two courses.

        Arguments:
            node1 {tuple} -- (location, (hour, minute)) of the first class.
            node2 {tuple} -- (location, (hour, minute)) of the second class.
            course1 {string} -- Name of first course to check for overlap.
            course2 {string} -- Name of second course to check for overlap.

        Returns:
            [int] -- 1 if no overlap exists between two classes,
            0 if there is overlap.
        """
        _, (hours1, mins1) = node1
        _, (hours2, mins2) = node2
        course_start1, course_end1 = compute_course_start_end(
            hours1, mins1, course_mins_map, course1)
        course_start2, course_end2 = compute_course_start_end(
            hours2, mins2, course_mins_map, course2)
        if course_start1 > course_end2 or course_start2 > course_end1:
            return 0
        elif course_start1 == course_end2 or course_start2 == course_end1:
            return 2
        else:
            return 1

    def no_time_clash(val1, val2, course1, dummy):
        """Binary constraint function: checks to see if there
        is a time clash for a course given two rooms and times.

        Arguments:
            val1 {tuple} -- Contains first set of room and time.
            val2 {tuple} -- Contains second set of room and time.
            course1 {string} -- Name of course to check for time clash.
            dummy {string} -- Dummy parameter. Added to help with refactor.

        Returns:
            [int] -- 1 if no time clash between rooms and times for course,
            0 if there is time clash.
        """
        (room1, time1) = val1
        (room2, time2) = val2
        if room1 != room2:
            return 1
        hours1, mins1 = time1
        hours2, mins2 = time2
        start_time1, end_time1 = compute_course_start_end(
            hours1, mins1, course_mins_map, course1)
        start_time2, _ = compute_course_start_end(
            hours2, mins2, course_mins_map, dummy)
        if start_time1 <= start_time2 < end_time1:
            return 0
        return 1

    professors, prof_info, rooms, room_capacities, courses, \
        course_no_students, course_mins_map, course_days_weekly = user_data

    full_prof_assignment = profs_for_courses(courses, professors, prof_info)
    rooms_chosen = {}
    solution = collections.defaultdict(lambda: None)
    retry = 0
    solved = True
    while retry < 3:
        daily_courses = maps_day_to_class(course_days_weekly, courses)
        max_iters = 100 * (retry + 1)
        for day in WEEKDAYS:
            csp = CSP()
            courses = daily_courses[day]
            add_nodes(
                courses,
                rooms,
                rooms_chosen,
                full_prof_assignment,
                prof_info,
                csp)
            add_unary_constraint(csp, room_has_capacity)
            add_binary_constraint(csp, course_mins_map, no_class_overlap, no_time_clash)
            min_conflict = minConflicts(csp)
            day_solution = min_conflict.solve(max_iters)
            if not day_solution:
                retry += 1
                solved = False
            else:
                solution[day] = day_solution
        if solved:
            break
        solved = True
    return solution
