import CSP_Solver
import json 
import random

'''
Teacher-Course-Class problem solver
*********************************

Nodes & Domains
-----------------
Nodes of form (c,p)
c : str. class name
p: str. professor's name
Domain values assigned as (r,h)
r: str. room assigned
h: set. (h,m) hours and minutes (in 30min intervals)

Unary Constraints
--------------
Suppose (c,p) assigned (r,h).
* capacity of room r should allow class c.

Binary Constraints
--------------
With (c,p) assigned (r,h) and (c',p') assigned (r',h')
* If p=p', i.e teachers are the same, then classes c and c' must not overlap
        +Soft Constraint: In this case one class shouldn't finish just as the other ends.
* To all other vars, if rooms are equal times must not overlap
'''
def TeacherCourseClassCSP():
        
        def add_nodes():
                #nodes have format (c,p)
                for c in courses:
                    p = full_prof_assignment[c]
                    if p==None: continue
                    domain = [(r,h) for r in rooms for h in hours_for_prof(p)]
                    node_name = (c,p)
                    csp.add_node(node_name,domain)
                    
        def profs_for_courses(courses):
                profs_chosen = {c:None for c in courses}
                for c in courses:
                        hits = []
                        for p in professors:
                                their_courses = prof_info[p]['courses']
                                if c in their_courses: hits.append(p)
                        profs_chosen[c] = random.choice(hits)
                return profs_chosen
        
        #Soft constraint. Returns courses assigned to days
        def courses_per_day():
                course_days_choice = dict([(c,days_for_course(c)) for c in courses])
                weekdays = ['mon','tues','wed','thur','fri']
                courses_on_days = dict([(d,[]) for d in weekdays])
                for c,days in course_days_choice.items():
                        for d in days:
                                courses_on_days[d].append(c)
                return courses_on_days
        
        def days_for_course(c):
                m = course_mins[c]
                n = min(course_days_weekly[c],5)
                days_chosen = []
                #Pairs Mon-Wed and Thurs-Fri preferred for 2-4 days per week
                if 2<=n and n<=4:
                        workdays = ['mon','wed','thur','fri']*2 + ['tues']
                elif n==1:
                        workdays = ['mon','tues','wed','thur','fri']
                else:
                        return ['mon','tues','wed','thur','fri']
                for i in range(n):
                        d = random.choice(workdays)
                        if i==0:
                                if d in ['mon','wed']:
                                        pref = ['mon','wed']
                                        pref.remove(d)
                                        days = ['mon','tues','wed','thur','fri']
                                        days.remove(d)
                                        workdays = days + pref
                                elif d in ['thur','fri']:
                                        pref = ['thur','fri']
                                        pref.remove(d)
                                        days = ['mon','tues','wed','thur','fri']
                                        days.remove(d)
                                        workdays = days + pref
                                else:
                                        workdays = ['mon','wed','thur','fri']
                        else:
                                workdays = list(set(workdays))
                                workdays.remove(d)
                        days_chosen.append(d)
                return days_chosen
                                
                
        def hours_for_prof(p):
                start_time = prof_info[p]['start_time']
                end_time = prof_info[p]['end_time']
                return {(i,j*30) for i in range(start_time,end_time) for j in range(2)}

        def add_unary():                                
                for n in csp.nodes:   
                        c,p = n
                        def room_has_capacity(val,course=c,prof=p):
                                room,hour_and_min = val
                                no_students = course_no_students[course]
                                return bool(room_capacities[room]>= no_students)
                        csp.add_unary_constraint((c,p),room_has_capacity)
        def add_binary():
                nodes = csp.nodes
                for i,n in enumerate(nodes):
                        course_n, prof_n = n
                        for m in nodes[i:]:
                                course_m, prof_m = m
                                if prof_n == prof_m:
                                        if course_n==course_m: continue
                                        '''first binary constraint'''
                                        def no_class_overlap(val1,val2,course1=course_n,course2=course_m):
                                                #makes the math easy: calculate course times in 10min intervals e.g. 120min is 12 intervals
                                                hours1, mins1 = val1[1]
                                                hours2, mins2 = val2[1]
                                                course_start1 = hours1*6 + mins1//10
                                                course_end1 = course_start1 + course_mins[course1]//10
                                                course_start2 = hours2*6 + mins2//10
                                                course_end2 = course_start2 + course_mins[course2]//10
                                                #conditions to check if one class starts during other
                                                if course_start1 <= course_start2 and course_start2 < course_end1:
                                                        return bool(False)
                                                if course_start2 <= course_start1 and course_start1 < course_end2:
                                                        return bool(False)
                                                #soft constraint part
                                                if course_start1==course_end2 or course_start2==course_end1:
                                                        return 2
                                                return bool(True)
                                        csp.add_binary_constraint(n,m,no_class_overlap)
                                '''second binary constraint'''
                                def no_time_clash(val1,val2,course1=course_n):
                                        room1, time1 = val1
                                        room2, time2 = val2
                                        if room1!=room2: return bool(True)
                                        hours1,mins1 = time1
                                        hours2,mins2 = time2
                                        start_time1 = hours1*6 + mins1//10
                                        end_time1 = start_time1 + course_mins[course1]//10
                                        start_time2 = hours2*6 + mins2//10
                                        if start_time1 <= start_time2 and start_time2 < end_time1:
                                                return bool(False)
                                        return bool(True)                         
                                csp.add_binary_constraint(n,m,no_time_clash)       
        #function body
        with open('sample_json_data.txt','r') as outfile:
            data = json.load(outfile)
            courses = data['courses']
            professors = data['professors']
            rooms = data['rooms']
            room_capacities = data['room_capacities']
            prof_info = data['prof_info']
            course_no_students = data['course_no_students']
            course_mins = data['course_mins']
            course_days_weekly = data['course_days_weekly']

        full_prof_assignment = profs_for_courses(courses)       #enforce professor-course consistency among different days
        weekdays = ['mon','tues','wed','thur','fri']
        solution = {d:None for d in weekdays}    
        daily_courses = courses_per_day()
        for d in weekdays:
                #add some kind of retry functionality (3 strikes rule?)
                csp = CSP_Solver.CSP()
                courses = daily_courses[d]
                #can define |professors| and other variables
                add_nodes()
                add_unary()
                add_binary()
                minconf = CSP_Solver.minConflicts(csp)
                solution[d] = minconf.solve()
        return solution

#code to test functionality 
teachercourse = TeacherCourseClassCSP()
justdays = ['mon','tues','wed','thur','fri']
for d in justdays:
        solution = teachercourse[d]
        print()
        print(d,':')
        for k,a in solution.items():
                course,prof = k
                r,hour = a
                h,m=hour
                if m<10: m='0'+str(m)
                print(prof,' //',course, '// room ',r,('// %i:%s' %(h,m)))
        
