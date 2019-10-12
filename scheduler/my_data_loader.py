'''Handling to make class scheduler notebook more user friendly'''

# pip3 install pandas
# pip3 install xlrd

import pandas as pd
from IPython.display import HTML, display
import tabulate
from teachercourse_csp import assigner

'Part I: Load and manage the spreadsheet data'
df = pd.read_excel('my_data.xlsx')

prof_df = df.iloc[:, 0:4]
prof_df['prof_courses'] = prof_df['prof_courses'].str.replace(', ', ',')
prof_df.dropna(inplace=True)
rooms_df = df.iloc[:, 4:6]
rooms_df.dropna(inplace=True)
rooms_df['room_capacity'] = rooms_df['room_capacity'].astype(u'int8')
rooms_df['rooms'] = rooms_df['rooms'].astype('str')
courses_df = df.iloc[:, 6:]
courses_df.dropna(inplace=True)

profs = []
prof_info = {}
for index, row in prof_df.iterrows():
    data = {}
    prof = row['professor']
    profs.append(prof)
    courses = row['prof_courses'].split(',')
    data['courses'] = courses
    data['start_time'] = row['prof_start_time']
    data['end_time'] = row['prof_end_time']
    prof_info[prof] = data

rooms = []
room_capacities = {}
for _, row in rooms_df.iterrows():
    room = row['rooms']
    room_capacities[room] = row['room_capacity']
    rooms.append(room)

courses = []
course_no_students = {}
course_mins = {}
course_days = {}
for _, row in courses_df.iterrows():
    course = row['course']
    courses.append(course)
    course_no_students[course] = int(row['course_no_students'])
    course_mins[course] = int(row['course_mins'])
    course_days[course] = int(row['course_days_weekly'])

# User feedback
print("Your excel data is now ready to use")

'Part II: Print out the data for the user to check'


def user_data_printer():
    table = {'PROFS': profs,
             'ROOMS': rooms,
             'COURSES': courses}
    headers = ['profs', 'rooms', 'courses']
    tablefmt = 'html'
    colalign = ("center", "center", "center")
    my_data = tabulate.tabulate(table, headers, tablefmt, colalign)
    return HTML(my_data)


check_your_data = user_data_printer()


'Part III: Run the scheduler and display output'


def time_formatter(course, start_time):
    hs, ms = start_time
    end = hs*6 + ms//10 + course_mins[course]//10
    end_time = (end//6, (end - (end//6)*6)*10)
    he, me = end_time
    output = '{:0>2}'.format(hs) + ':' + '{:0>2}'.format(ms)
    output = output + ' to ' + '{:0>2}'.format(he) + ':' + '{:0>2}'.format(me)
    return output


user_data = (profs, prof_info, rooms, room_capacities, courses,
             course_no_students, course_mins, course_days)
full_schedule = assigner(user_data)
weekdays = ['mon', 'tues', 'wed', 'thur', 'fri']

columns = ['Day', 'Course', 'Professor', 'Room', 'Period']
df_out = pd.DataFrame(None, columns=columns)
for day in weekdays:
    schedule = full_schedule[day]
    for var, val in schedule.items():
        course, professor = var
        room, start_time = val
        df_inc = {'Day': day.upper(),
                  'Course': [course],
                  'Professor': [professor],
                  'Room': [room],
                  'Period': [time_formatter(course, start_time)]}
        df_inc = pd.DataFrame.from_dict(df_inc)
        df_out = pd.concat([df_out, df_inc], ignore_index=True)

# show_me_the_schedule = lambda : display(df_out)


def show_me_the_schedule():
    return display(df_out)
