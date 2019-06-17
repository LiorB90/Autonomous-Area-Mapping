from __future__ import print_function
import Movement
import Sensor as s
from time import sleep

side_sensor_dist = 25
forward_sensor_dist = 25

move_flag = False

def delay():
    sleep(0.01)


def print_f(froom, flag='r'):
    try:
        if flag == 'r':
            for row in froom:
                for cell in row:
                    print(cell, end=" ")
                print('\n')    
    except Exception as e:
        print('error in printf WT')
        print(e)
        cleanup()


def check_len(test):    
    counter_width = len(test[0])
    for i in range(1, len(test)):
        if len(test[i]) > counter_width:
            counter_width = len(test[i])
    for i in range(len(test)):
        if len(test[i]) < counter_width:
            for j in range(counter_width - len(test[i])):
                test[i].append('w')
    
    return test
    

def obs_in_2_2(robot_room, e_row, e_col, eflag):
    try:
        print("------------- In obs in 2,2 -------------")
        flag = eflag
        test = robot_room
        length = len(test)
        width = len(test[0])
        e_row = Movement.forwardFeed(flag, e_row, e_col, length, width)
        if test[e_row][e_col] == 'k':
            test[e_row][e_col] = 'z' 
        Movement.ninty_deg_left(flag)
        
        print("-------------  looking right ------------")
        flag = 'r'
        if s.m_sensor() > forward_sensor_dist:
            e_col = Movement.forwardFeed(flag, e_row, e_col, length, width)
            if test[e_row][e_col] == 'u':
                test[e_row][e_col] = 'k'
        while s.l_sensor() <= side_sensor_dist:        
            print("-------------  obs on the left ------------")
            print_f(test, 'R')
            test[e_row-1][e_col] = 'w'
            if s.m_sensor() > forward_sensor_dist:
                e_col = Movement.forwardFeed(flag, e_row, e_col, length, width)
                if test[e_row][e_col] == 'u':
                    test[e_row][e_col] = 'k'
            else:
                break
        if s.l_sensor() > side_sensor_dist:        
            print("-------------  no more obs ------------")
            Movement.ninty_deg_left()
            flag = 'u'
            e_row = Movement.forwardFeed(flag, e_row, e_col, length, width)
            print("------------- in place ------------")
            if test[e_row][e_col] == 'u':
                test[e_row][e_col] = 'b'
            Movement.ninty_deg_right()
            print("------------- in direction ------------")
        return test    
    except Exception as e:
        print('error in obs in 2_2')
        print(e)
        

def get_to_2_2(robot_room, e_row, e_col, eflag):
    try:
        if eflag == 'l':
            Movement.ninty_deg_right()
        if eflag == 'r':
            Movement.ninty_deg_left()
        flag = 'u'
        done = False
        test = robot_room
        length = len(robot_room)
        width = len(robot_room[0])
        while not done:
            print_f(test, 'R')
            print("-----------------------")
            if e_col == 2 and e_row == 2:
                if flag != 'r':
                    Movement.ninty_deg_right()
                done = True
                
            elif e_row == 2:
                if e_col < 2:
                    flag = 'r'
                    Movement.ninty_deg_right()
                    if s.m_sensor() > forward_sensor_dist:
                        e_col = Movement.forwardFeed(flag, e_row, e_col, length, width, True)
                        if test[e_row][e_col] == 'u':
                            test[e_row][e_col] = 'k'
                        elif test[e_row][e_col] == 'k':
                            test[e_row][e_col] = 'z'
                    else:
                        test[e_row][e_col+1] = 'w'                  
                        flag = 'd'
                        Movement.ninty_deg_right()
                        test = obs_in_2_2(test, e_row, e_col, flag)
                        done = True
                                               
            elif e_row > 2:
                if e_col < 2:
                    flag = 'r'
                    Movement.ninty_deg_right()
                    if s.m_sensor() > forward_sensor_dist:
                        e_col = Movement.forwardFeed(flag, e_row, e_col, length, width, True)
                        if test[e_row][e_col] == 'u':
                            test[e_row][e_col] = 'k'
                        elif test[e_row][e_col] == 'k':
                            test[e_row][e_col] = 'z'
                elif e_col == 2:
                    flag = 'u'
                    Movement.ninty_deg_left()
                    if s.m_sensor() > forward_sensor_dist:
                        e_row = Movement.forwardFeed(flag, e_row, e_col, length, width)
                        if test[e_row][e_col] == 'u':
                            test[e_row][e_col] = 'k'
                        elif test[e_row][e_col] == 'k':
                            test[e_row][e_col] = 'z'
        return test    
    except Exception as e:
        print('error in get to 2,2')
        print(e)


def mark_space(space, row, col):
    if space[row][col] == 'u':
        space[row][col] = 'k'
    elif space[row][col] == 'k':
        space[row][col] = 'z'


def wall_track():
    try:

        done = 0
        row = 1
        col = 1
        test = [['k']]
        flag = 'r'
        while done == 0:
            if s.m_sensor() < 10:
                Movement.reverse(0.1)
            print("ROOM: ", '(', row, ',', col, ')'," TEST: ", '(', row-1, ',', col-1, ')', " flag: ", flag)
            print_f(test, "r")
            print("-----------------------")
            print("-----------------------")
            # ----------- RIGHT MOVEMENT --------------- #
            if flag == 'r':
                if s.l_sensor() <= side_sensor_dist:
                    if s.m_sensor() > forward_sensor_dist:
                        col = Movement.forwardFeed(flag, row, col, 0, 0, True)
                        if col > len(test[row-1]):
                            test[row-1].append('k')
                            if test[row - 1][col-1] == 'u':
                                test[row - 1][col-1] = 'k'
                        else:
                            mark_space(test, row-1, col-1)
                    else:
                        test[row-1].append('w')
                        if row > 1:
                            if test[row-1] > test[row-2]:
                                test[row - 2].append('w')
                        Movement.ninty_deg_right()
                        flag = 'd'
                        
                elif len(test[row-2]) >= len(test[row-1]):
                    if test[row-2][col-1] == 'k':
                        if s.m_sensor() > forward_sensor_dist:
                            col = Movement.forwardFeed(flag, row, col, 0, 0, True)
                            if col >= len(test[row-1]):
                                test[row-1].append('k')
                            if test[row - 1][col-1] == 'u':
                                test[row - 1][col-1] = 'k'
                        else:
                            test[row-1].append('w')
                            Movement.ninty_deg_right()
                            flag = 'd'
                    else:                
                        Movement.ninty_deg_left()
                        flag = 'u'    
                        
                else:
                    flag = 'u'                    
                    Movement.ninty_deg_left()

            # ---------- DOWN MOVEMENT ---------- #
            elif flag == 'd':
                if s.l_sensor() <= side_sensor_dist:
                    if s.m_sensor() > forward_sensor_dist:
                        row = Movement.forwardFeed(flag, row, col, 0, 0, True)
                        if row > len(test):
                            test.append([])
                            for cell in range(col - 1):
                                test[row - 1].append('u')
                            test[row - 1].append('k')
                        elif len(test[row-1]) < len(test[row-2]):
                            for i in range(len(test[row-2]) - len(test[row-1])-1):
                                test[row-1].append('u')
                        if test[row - 1][col - 1] == 'u':
                            test[row - 1][col - 1] = 'k'
                        if s.l_sensor() > side_sensor_dist:
                            flag = 'r'                    
                            Movement.ninty_deg_left()
                        else:
                            test[row-1].append('w')
                    else:
                        test.append([])
                        if len(test[row-1]) > len(test[row]):
                            for i in range(col-1):
                                test[row].append('u')
                            test[row].append('w')
                        if len(test[row]) < len(test[row-1]):
                            test[row].append('w')
                        Movement.ninty_deg_right()
                        flag = 'l'
                        
                elif test[row-1][col] == 'k':
                    if s.m_sensor() > forward_sensor_dist:
                        row = Movement.forwardFeed(flag, row, col, 0, 0, True)
                        if row > len(test):
                            test.append([])
                            for cell in range(col - 1):
                                test[row - 1].append('u')
                            test[row - 1].append('k')
                        if test[row - 1][col - 1] == 'u':
                            test[row - 1][col - 1] = 'k'

            # ---------- LEFT MOVEMENT ---------- #
            elif flag == 'l':
                if s.l_sensor() <= side_sensor_dist:
                    test[row][col-1] = 'w'
                    if s.m_sensor() > forward_sensor_dist:
                        col = Movement.forwardFeed(flag, row, col, 0, 0, True)
                        if col == 0:
                            col = 1
                            test[row-1][col-1] = 'u'
                            
                        mark_space(test, row - 1, col - 1)
                        print("left marking")
                    else:
                        Movement.ninty_deg_right()
                        flag = 'u'  
                        if col > 1:
                            for i in range(1, col):
                                test[row-1][col - 1 - i] = 'w'
                                if row < len(test):
                                    test[row][col-1-i] = 'w'

                elif test[row][col-1] == 'k':
                    if s.m_sensor() > forward_sensor_dist:
                        col = Movement.forwardFeed(flag, row, col, 0, 0, True)
                    if test[row - 1][col-1] == 'u':
                        test[row - 1][col-1] = 'k'
                    done = 1
                    for i in range(1, len(test)-1):
                        if test[i][0] == 'u':
                            done = 0
                            break

                else:
                    flag = 'd'
                    Movement.ninty_deg_left()

            # ---------- UP MOVEMENT ---------- #
            elif flag == 'u':
                if done == 0:
                    if s.l_sensor() <= side_sensor_dist:                                    
                        if col > 1:
                            for i in range(1, col):
                                test[row-1][col-1-i] = 'w'
                                if row < len(test):
                                    test[row][col-1-i] = 'w'
                        if s.m_sensor() > forward_sensor_dist:
                            row = Movement.forwardFeed(flag, row, col, 0, 0, True)
                            mark_space(test, row-1, col-1)
                            if s.l_sensor() > side_sensor_dist:
                                Movement.ninty_deg_left()
                                flag = 'l'
                        else:
                            if row > 1:
                                test[row - 2][col - 1] = 'w'
                            Movement.ninty_deg_right()
                            flag = 'r'
                            
                    elif len(test) > row and test[row][col-1] != 'w':
                        if test[row][col-1] == 'k':
                            Movement.ninty_deg_left()
                            flag = 'l'

                    elif len(test[row-2]) >= len(test[row-1]):
                        print("right condition")
                        if test[row-2][col-1] == 'k':
                            if s.m_sensor() > forward_sensor_dist:
                                row = Movement.forwardFeed(flag, row, col, 0, 0, True)
                                if len(test[row - 1]) >= len(test[row]):
                                    if test[row-1][col-1] == 'u':
                                        test[row-1][col-1] = 'k'
                                else:
                                    test[row - 1].append('k')
                        elif test[row][col-1] == 'k':
                            Movement.ninty_deg_left()
                            flag = 'l'
                        elif test[row - 1][col-2] == 'k':
                            if s.m_sensor() > forward_sensor_dist:
                                row = Movement.forwardFeed(flag, row, col, 0, 0, True)
                                if test[row-1][col-1] == 'u':
                                    test[row-1][col-1] = 'k'                              
                                
                    elif len(test[row-2]) < len(test[row-1]):
                        if test[row - 1][col-2] == 'k':
                            if s.m_sensor() > forward_sensor_dist:
                                row = Movement.forwardFeed(flag, row, col, 0, 0, True)
                                test[row - 1].append('k')
                            
                    else:
                        Movement.ninty_deg_left()
                        flag = 'l'

                    if row - 1 > 0 and len(test[row - 2]) >= len(test[row - 1]):
                        if test[row - 2][col - 1] == 'k' or test[row - 2][col - 1] == 'w':
                            done = 1
                            for i in range(1, len(test)-1):
                                if test[i][0] == 'u':
                                    done = 0
                                    break
                            if s.m_sensor() < 10:
                                Movement.reverse(0.08)
                            print_f(test, 'r')
                            print("-----------------------")

        print("---------- DONE WT ----------")
        print("ROOM: ", '(', row, ',', col, ')')
        print("TEST: ", '(', row-1, ',', col-1, ')')
        test.insert(0, [])
        for i in range(len(test)):
            if i == 0:
                for j in range(len(test[1])):
                    test[i].append('w')
            for j in range(len(test[i])):
                test[i].insert(0, 'w')
                break
        print('----- AFTER WALL TRACK ------')
        print_f(test, "r")
        print('----- Filling Blanks ------')
        test = check_len(test)
        print_f(test, "r")
        print('----- Getting to Unknown ------')
        test = get_to_2_2(test, row, col, flag)
        print_f(test, "r")
            
        return test        
    except Exception as e:
        print('error in WT')
        print(e)
#        gpio.cleanup()  


#robot_room = []
#try:
#    robot_room = wall_track()
#except Exception as e:
#    print(e)
#    Movement.cleanup()
#print('----- ROBOT ROOM ------')
#print_f(robot_room, 'R')
