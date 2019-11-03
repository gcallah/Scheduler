"""Driver code for running cspsolver.py
"""
import json
import datamaker
import pandas as pd
from teachercourse_csp import assigner
from IPython.display import display


def main(): 
    def time_formatter(course, start_time):
        hs,ms = start_time
        end = hs*6 + ms//10 + course_mins[course]//10
        end_time = (end//6, (end - (end // 6) * 6) * 10)
        he,me = end_time
        output = '{:0>2}'.format(hs)+':'+'{:0>2}'.format(ms)+' to ' + '{:0>2}'.format(he)+':'+ '{:0>2}'.format(me) 
        return output

    df = pd.read_excel('my_data.xlsx')

    prof_df = df.iloc[:,0:4]
    prof_df['prof_courses'] = prof_df['prof_courses'].str.replace(', ',',')
    rooms_df = df.iloc[:,4:6]
    rooms_df.dropna(inplace=True)
    rooms_df['room_capacity'] = rooms_df['room_capacity'].astype(u'int8')
    rooms_df['rooms'] = rooms_df['rooms'].astype('str')
    courses_df = df.iloc[:,6:]
    courses_df.dropna(inplace=True)

    professors = []
    prof_info = {}
    for index, row in prof_df.iterrows():
            data = {}
            prof = row['professor']
            professors.append(prof)
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
    course_days_weekly = {}
    for _, row in courses_df.iterrows():
        course = row['course']
        courses.append(course)
        course_no_students[course] = int(row['course_no_students'])
        course_mins[course] = int(row['course_mins'])
        course_days_weekly[course] = int(row['course_days_weekly'])
    print("Data loaded successfully!")

    datamaker.make_data()

    input_file = "sample_data.txt"
    with open(input_file,'r') as f:
        data = json.load(f)
        
    professors = data['professors']
    prof_info = data['prof_info']
    rooms = data['rooms']
    room_capacities = data['room_capacities']
    courses = data['courses']
    course_no_students = data['course_no_students']
    course_mins = data['course_mins']
    course_days_weekly = data['course_days_weekly']

    # print(professors)
    # print(rooms)

    user_data = (professors,prof_info,rooms,room_capacities,courses,course_no_students,course_mins,course_days_weekly)
    full_schedule = assigner(user_data)
    weekdays = ['mon','tues','wed','thur','fri']

    columns = ['Day','Course','Professor', 'Room','Period']
    df_out = pd.DataFrame(None, columns=columns)
    for day in weekdays:
        schedule = full_schedule[day]
        # print(day.upper())
        # print('-----')
        for var,val in schedule.items():
            course,professor = var
            room,start_time = val
            df_inc = {'Day':day,'Course':[course],'Professor':[professor], 'Room':[room],'Period':[time_formatter(course,start_time)]}
            df_inc = pd.DataFrame.from_dict(df_inc)
            df_out = pd.concat([df_out,df_inc],ignore_index=True)
        # print('')

    display(df_out)
main()