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
    if rand_day == TUESDAY: 
        return [MONDAY, WEDNESDAY, THURSDAY, FRIDAY] 
    pref = [MONDAY, WEDNESDAY] if rand_day in (MONDAY, WEDNESDAY) else [THURSDAY, FRIDAY]
    return [day for day in (pref+days) if day != rand_day]

def assign_days_for_course(course_weekly_days):
    """Assign randomly the meetings days for a class given how many time it is held weekly.

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
        # Pairs Mon-Wed and Thurs-Fri preferred if course is held 2 - 4 days per week.
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
        course_days_weekly {dict} -- A map {class: how many days it's held per week}.
        courses {list} -- A list of classes.

    Returns:
        [dict] -- Returns a map {day: a list of classes on that day}.
    """
    weekdays = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]
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
        prof_info {dict} -- A dictionary mapping professor to his class info (courses taught, start_time, end_time).

    Returns:
        [dict] -- Returns a map {course : professor}.
    """
    profs_chosen = {}
    for course in courses:
        intersection = [professor for professor in professors if course in prof_info[professor]['courses']]
        if intersection:
            profs_chosen[course] = random.choice(intersection)
    return profs_chosen

def add_nodes(courses, rooms, rooms_chosen, full_prof_assignment, prof_info, csp):
    """Adds nodes (course, professor) and its list of domains (rooms, hours) to csp.

    Arguments:
        courses {list} -- A list of classes.
        rooms {list} -- A list of rooms.
        rooms_chosen {dict} -- A dictionary mapping course to rooms.
        full_prof_assignment {dict} -- A dictionary mapping course to professor.
        prof_info {dict} -- A dictionary mapping professor to his class info (courses taught, start_time, end_time).
        csp {cspsolver.CSP} -- A instance of the Constraint Satisfaction Problem class.
    """
    for course in courses:
        rooms_for_course = rooms_chosen[course] if course in rooms_chosen else rooms
        professor = full_prof_assignment[course]
        if professor:
            domain = [(room, hour) for room in rooms_for_course for hour in hours_for_prof(prof_info, professor)]
            node_name = (course, professor)
            csp.add_node(node_name, domain)

def assigner(user_data):
    """Takes in data provided by the user and creates class schedule.

    Arguments:
        user_data {tuple} -- A tuple of lists containing the user's data information.

    Returns:
        [dict] -- Returns a map {day: a list of classes taught by professors with room numbers and times}.
    """
    def add_unary():
        """Adds an unary constraint to list of nodes
        """
        for node in csp.nodes:
            course, professor = node

            def room_has_capacity(val, course=course, prof=professor):
                """Checks to see if given room has room for all students in course.

                Arguments:
                    val {tuple} -- Contains values for room and time of class.
                    Course {string} -- Name of course.
                    Professor {string} -- Name of professor.

                Returns:
                    [bool] -- Whether or not the room has capacity for all students in course.
                """
                room, hour_and_min = val
                no_students = course_no_students[course]
                return bool(room_capacities[room] >= no_students)

            csp.add_unary_constraint((course, professor), room_has_capacity)

    def add_binary():
        """Adds binary constraints to list of nodes.
        """
        nodes = csp.nodes
        for i, n in enumerate(nodes):
            course_n, prof_n = n
            for m in nodes[i:]:
                course_m, prof_m = m
                if prof_n == prof_m:
                    if course_n == course_m:
                        continue

                    # c1 = course_1, c2 = course_2
                    def no_class_overlap(val1, val2, c1=course_n, c2=course_m):
                        """Checks to see if there is overlap in times between two courses.

                        Arguments:
                            val1 {tuple} -- Contains time of first course.
                            val2 {tuple} -- Contains time of second course.
                            c1 {string} -- Name of first course to check for overlap.
                            c2 {string} -- Name of second course to check for overlap.

                        Returns:
                           [bool] -- True if no overlap exists between two classes, false if there is overlap.
                        """
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
                    """Checks to see if there is a time clash for a course given two rooms and times.

                    Arguments:
                        val1 {tuple} -- Contains first set of room and time.
                        val2 {tuple} -- Contains second set of room and time.
                        course1 {string} -- Name of course to check for time clash.

                    Returns:
                        [bool] -- True if no time clash between rooms and times for course, false if there is time clash.
                    """
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
    full_prof_assignment = profs_for_courses(courses, professors, prof_info)
    rooms_chosen = {}  # rooms are consistent
    solution = {d: None for d in WEEKDAYS}
    retries = 0
    # will retry max 3 times to get a solution
    while retries < 3:
        daily_courses = maps_day_to_class(course_days_weekly, courses)
        # upon retry increase maximum iterations
        max_iters = 100 * (retries + 1)
        for d in WEEKDAYS:
            csp = CSP()
            courses = daily_courses[d]
            add_nodes(courses, rooms, rooms_chosen, full_prof_assignment, prof_info, csp)
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