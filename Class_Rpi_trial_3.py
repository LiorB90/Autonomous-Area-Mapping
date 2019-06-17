from __future__ import print_function
import Movement
import Sensor as s
import time
import Wall_Track_Pi_3 as wt

side_sensor_dist = 15
forward_sensor_dist = 20


def print_f(room, flag='r'):

    if flag == 'r':
        for row in room:
            for cell in row:
                print(cell, end=" ")
            print('\n')
    elif flag == 'l':
        for row in room:
            for cell in row:
                print(cell, end=" ")
            print('\n')
    print('\n')


def is_last_row(robot_room, row, col):
    if row == len(robot_room)-2:
        return True
    elif row == len(robot_room)-3 and robot_room[len(robot_room)-2][col] == 'k':
        for i in range(1, len(robot_room[row]) - 1):
            if robot_room[row][i] == 'u':
                return False

    return False


def is_unknown_region(closest_unknown, robot_room):
    closest_unknown.clear()
    for line in range(len(robot_room) - 2, 0, -1):
        for column in range(1, len(robot_room[line])-1):
            if robot_room[line][column] == 'u':
                for x in range(column-1, 0, -1):
                    if robot_room[line][x] == 'w':
                        # left_wall = True
                        break
                for x in range(column+1, len(robot_room[0])-1):
                    if robot_room[line][x] == 'w':
                        # right_wall = True
                        break
#                if cant_get_there(robot_room, line, column) or (right_wall and left_wall):
                if cant_get_there(robot_room, line, column):
                    robot_room[line][column] = 'w'
                    # left_wall = False
                    # right_wall = False
                else:
                    closest_unknown.append(line)
                    closest_unknown.append(column)
                    return True
    return False


def cant_get_there(robot_room, row, col):
    for i in range(row - 1, -1, -1):
        if robot_room[i][col] == 'k' or robot_room[i][col] == 'z' or robot_room[i][col] == 'u':
            return False
        if robot_room[i][col] == 'w':
            for j in range(col + 1, len(robot_room[i])):
                if robot_room[i][j] == 'k' or robot_room[i][j] == 'z' or robot_room[i][col] == 'u':
                    return False
                if robot_room[i][j] == 'w':
                    for k in range(i + 1, row+2):
                        if robot_room[k][j] == 'k' or robot_room[k][j] == 'z':
                            return False
                        if robot_room[k][j] == 'w':
                            for w in range(j - 1, col - 2, -1):
                                if robot_room[k][w] == 'k' or robot_room[k][w] == 'z' or robot_room[i][col] == 'u':
                                    return False
                                if robot_room[k][w] == 'w':
                                    for z in range(k - 1, i - 1, -1):
                                        if robot_room[z][w] == 'k' or robot_room[z][w] == 'z'\
                                                or robot_room[i][col] == 'u':
                                            return False

                                        if robot_room[z][w] != 'w':
                                            break
                                        if z == i:
                                            for rows in range(i + 1, k):
                                                for cell in range(col, j):
                                                    robot_room[rows][cell] = 'w'
                                            print("Cant Get There")
                                            return True
                                else:
                                    break
                        else:
                            break
                else:
                    break
    return False


def mark_space(space, row, col):
    if space[row][col] == 'u':
        space[row][col] = 'k'
    elif space[row][col] == 'k':
        space[row][col] = 'z'


class SizeSelect(object):

    def __init__(self):
        self.rf_on = False
        self.gf_on = False
        self.obs_row = 0
        self.obs_col = 0
        self.obs_hei = 0
        self.obs_wid = 0
        self.robot_room = []
        self.full_room = []
        self.wt_flag = True
        self.closest_unknown = []
        self.done_gap_filling = False
        self.done_region_filling = False
        self.flag = 'r'
        self.row = 1
        self.col = 1
        self.room_length = 0
        self.room_width = 0
        self.before_obstacle = True
        self.obs_bypass = False
        self.last_filling = False
        self.obs_last_row = False

    def sensor_checking(self):
        direction = self.flag
        row = self.row
        col = self.col
        if direction == 'r':
            if s.r_sensor() < side_sensor_dist\
               and row < len(self.robot_room) - 2:
                self.robot_room[row + 1][col] = 'w'

        elif direction == 'l':
            if s.l_sensor() < side_sensor_dist\
                    and row < len(self.robot_room) - 2:
                self.robot_room[row + 1][col] = 'w'

    def start(self, fwt=True):
        try:
            print_f(self.robot_room)
            print('(', self.row, " ", self.col, ')')
            if fwt and self.wt_flag:
                self.full_room = wt.wall_track()
                print("Done WT")
                print_f(self.full_room, self.flag)
                self.room_length = len(self.full_room)-2
                self.room_width = len(self.full_room[0])-2
                self.set_room()
                for i in range(2, self.room_length):
                    for j in range(2, self.room_width):
                        if i == 2:
                            if self.full_room[i][j] == 'b':
                                self.col = j-1
                                self.full_room[i][j] = 'k'
                            self.robot_room[i-1][j-1] = self.full_room[i][j]
                        else:
                            self.robot_room[i-1][j-1] = self.full_room[i][j]

                self.wt_flag = False
            if s.m_sensor() < 10:
                Movement.reverse(0.2)

    # ---------------- Region Filling ---------------- #
            if not self.done_region_filling:
                print_f(self.robot_room)
                # --------- Beginning --------- #
                if self.rf_on:
                    mark_space(self.robot_room, self.row, self.col)
                self.rf_on = True
                if self.col == 1 and self.row == 1:
                    self.sensor_checking()

                    # --------- Is Region Filling Done? --------- #
                if is_last_row(self.robot_room, self.row, self.col):
                    self.done_region_filling = True
                    print("done region filling")

                    # --------- Right Movement --------- #
                elif (s.m_sensor() > forward_sensor_dist
                      and self.flag == 'r'
                      and self.robot_room[self.row][self.col+1] == 'u'
                      and self.col < len(self.robot_room[self.row]) - 2):
                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                    self.room_length, self.room_width)
                    self.sensor_checking()

                    # --------- Left Movement --------- #
                elif s.m_sensor() > forward_sensor_dist  \
                        and self.flag == 'l' \
                        and self.robot_room[self.row][self.col-1] == 'u'  \
                        and self.col > 1:
                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                    self.room_length, self.room_width)
                    self.sensor_checking()
                    # self.robot_room[self.row][self.col] = 'k'

                    # --------- Obstacle for moving right --------- #
                elif (s.m_sensor() < forward_sensor_dist
                      or self.robot_room[self.row][self.col+1] == 'k'
                      or self.robot_room[self.row][self.col+1] == 'z'
                      or self.robot_room[self.row][self.col+1] == 'w')\
                        and self.flag == 'r':
                    if self.col < (len(self.robot_room[self.row])-2) and s.m_sensor() < forward_sensor_dist:
                        self. robot_room[self.row][self.col+1] = 'w'

                    # --------- 180 Deg to the Right --------- #
                    if self.robot_room[self.row+1][self.col] != 'w' and self.robot_room[self.row+1][self.col] != 'k':
                        self.row = Movement.dn(self.flag, self.row, self.col,
                                               self.room_length, self.room_width)
                        self.flag = 'l'
                        self.sensor_checking()

                        # --------- Dead Lock to the Right - Reverse --------- #
                    else:
                        self.flag = 'l'
                        if not(is_last_row(self.robot_room, self.row, self.col)):
                            self.col = Movement.deadlock(self.flag, self.row, self.col,
                                                         self.room_length, self.room_width)
                            while self.robot_room[self.row+1][self.col] != 'u':
                                self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                self.room_length, self.room_width)
                            self.row = Movement.dn(self.flag, self.row, self.col,
                                                   self.room_length, self.room_width, True)

                    # --------- Obstacle for Moving Left --------- #
                elif (s.m_sensor() < forward_sensor_dist
                      or self.robot_room[self.row][self. col-1] != 'k'
                      or self.robot_room[self.row][self.col-1] == 'z'
                      or self.robot_room[self.row][self.col-1] == 'w'
                      or self.full_room[self.row+1][self.col] == 'k') and self.flag == 'l':
                    if self.col > 1 and s.m_sensor() < forward_sensor_dist:
                        self.robot_room[self.row][self.col-1] = 'w'

                        # --------- 180 Deg to the Left --------- #
                    if self.robot_room[self.row+1][self.col] != 'w' and self.robot_room[self.row+1][self.col] != 'k':
                        self.row = Movement.dn(self.flag, self.row, self.col,
                                               self.room_length, self.room_width)
                        self.flag = 'r'
                        self.sensor_checking()

                        # --------- Dead Lock to the Left - Reverse --------- #
                    else:
                        self.flag = 'r'
                        if not(is_last_row(self.robot_room, self.row, self.col)):
                            self.col = Movement.deadlock(self.flag, self.row, self.col,
                                                         self.room_length, self.room_width)
                            while self.robot_room[self.row+1][self.col] != 'u':
                                self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                self.room_length, self.room_width)
                            self.row = Movement.dn(self.flag, self.row, self.col,
                                                   self.room_length, self.room_width, True)

                if self.robot_room[len(self.robot_room)-2][len(self.robot_room[len(self.robot_room)-2])-2] != 'u' \
                   or self.robot_room[len(self.robot_room) - 2][1] != 'u':
                    self.obs_last_row = False

    # ------------------ Gap Filling ------------------ #
            else:
                if self.gf_on:
                    mark_space(self.robot_room, self.row, self.col)
                self.gf_on = True
                # Room.print_f(self.robot_room)
                print("--------- start GF --------- ")
                # --------- Checking if Done Gap Filling --------- #
                not_done = is_unknown_region(self.closest_unknown, self.robot_room)
                if not not_done:
                    print("done Gap Filling")
                    self.robot_room[self.row][self.col] = 'E'
                    for i in range(2, self.room_length):
                        for j in range(2, self.room_width):
                            self.full_room[i][j] = self.robot_room[i-1][j-1]
                    return True

                # --------- Getting to Line Beneath the unknown area --------- #
                elif self.closest_unknown[0] + 1 < self.row:
                        print(self.closest_unknown)
                        if s.m_sensor() < 10:
                            Movement.reverse(0.2)
                        if self.flag == 'l':
                            Movement.ninty_deg_right()
                            self.flag = 'up'
                        elif self.flag == 'r':
                            Movement.ninty_deg_left()
                            self.flag = 'up'
                        if self.robot_room[self.row - 1][self.col] != 'w' and s.m_sensor() > forward_sensor_dist:
                            self.row = Movement.forwardFeed(self.flag, self.row, self.col,
                                                            self.room_length, self.room_width)

                        else:
                            self.robot_room[self.row - 1][self.col] = 'w'
                            if self.closest_unknown[1] < self.col:
                                Movement.ninty_deg_left()
                                self.flag = 'l'
                                self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                self.room_length, self.room_width)
                                Movement.ninty_deg_right()
                                self.flag = 'up'
                            elif self.closest_unknown[1] < self.col:
                                Movement.ninty_deg_right()
                                self.flag = 'r'
                                self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                self.room_length, self.room_width)
                                Movement.ninty_deg_left()
                                self.flag = 'up'

                    # --------- Getting to Col of the Unknown Area --------- #
                elif self.closest_unknown[0] < self.row:
                    if s.m_sensor() < 10:
                        Movement.reverse(0.2)
                        # --------- Unknown Area to the Right --------- #
                    if self.closest_unknown[1] > self.col:
                        if s.m_sensor() < 10:
                            Movement.reverse(0.2)
                        if self.flag == 'l':
                            Movement.ninty_deg_right()
                            Movement.ninty_deg_right()
                            self.flag = 'r'

                        if self.robot_room[self.row-1][self.col] != 'u':
                            if self.flag == 'up':
                                Movement.ninty_deg_right()
                                self.flag = 'r'
                            self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                            self.room_length, self.room_width)

                            self.sensor_checking()
                            if (self.col == self.room_width-2 or self.robot_room[self.row][self.col+1] == 'w') and\
                                    self.closest_unknown[1] < self.room_width-2:
                                self.flag = 'up'
                        else:
                            self.row = Movement.un(self.flag, self.row, self.col,
                                                   self.room_length, self.room_width)
                            if s.m_sensor() < 10:
                                Movement.reverse(0.2)
                            Movement.ninty_deg_right()
                            self.flag = 'r'

                    # --------- Unknown Area Same Col --------- #
                    elif self.closest_unknown[1] == self.col:
                        print("same col ", self.flag)
                        if s.m_sensor() < 10:
                            Movement.reverse(0.2)
                        if self.flag == 'r':
                            Movement.ninty_deg_left()
                            self.flag = "up"
                        elif self.flag == 'l':
                            Movement.ninty_deg_right()
                            self.flag = "up"
                        self.row = Movement.forwardFeed(self.flag, self.row, self.col,
                                                        self.room_length, self.room_width)
#                        '
                        self.sensor_checking()

                    # --------- Unknown to the Left --------- #
                    elif self.closest_unknown[1] < self.col:
                        if s.m_sensor() < 10:
                            Movement.reverse(0.2)
                        if self.flag == 'r':
                            Movement.ninty_deg_left()
                            Movement.ninty_deg_left()
                            self.flag = 'l'
                        if self.robot_room[self.row - 1][self.col] != 'u':
                            if self.flag == 'up':
                                Movement.ninty_deg_left()
                                self.flag = 'l'
                            self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                            self.room_length, self.room_width)
                            self.sensor_checking()

                        else:
                            self.row = Movement.un(self.flag, self.row, self.col,
                                                   self.room_length, self.room_width)
                            if s.m_sensor() < 10:
                                Movement.reverse(0.2)
                            Movement.ninty_deg_left()
                            self.flag = 'l'

                    # ---------- Unknown on Same Row or Beneath ---------- #
                elif self.closest_unknown[0] >= self.row:
                        # ---------- Unknown On Same Row ---------- #
                    if self.closest_unknown[0] == self.row:
                            # ---------- To the Right ---------- #
                        if self.closest_unknown[1] > self.col \
                                and self.col < self.room_width-2:
                            print(self.flag, " ", self.col)
                            if self.flag == 'l' and self.col == 1:
                                Movement.ninty_deg_right()
                                Movement.ninty_deg_right()
                                self.flag = 'r'
                                if s.m_sensor() > forward_sensor_dist:
                                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                    self.room_length, self.room_width)
                                    self.sensor_checking()
                            elif self.flag == 'r':
                                if s.m_sensor() > forward_sensor_dist:
                                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                    self.room_length, self.room_width)
                                    self.sensor_checking()
                            elif self.flag == 'up':
                                Movement.ninty_deg_right()
                                self.flag = 'r'
                                self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                self.room_length, self.room_width)

                                # ---------- To the Left ---------- #
                        elif self.closest_unknown[1] < self.col\
                                and self.col > 1:
                            if self.flag == 'r' and self.col == self.room_width-2:
                                Movement.ninty_deg_left()
                                Movement.ninty_deg_leftt()
                                self.flag = 'l'
                                if s.m_sensor() > forward_sensor_dist:
                                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                    self.room_length, self.room_width)
                                    self.sensor_checking()
                            elif self.flag == 'l':
                                if s.m_sensor() > forward_sensor_dist:
                                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                    self.room_length, self.room_width)
                                    self.sensor_checking()

                            elif self.flag == 'up':
                                Movement.ninty_deg_left()
                                self.flag = 'l'
                                self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                self.room_length, self.room_width)

                        # ---------- Unknown Beneath Row ---------- #
                    elif self.closest_unknown[0] > self.row:
                        print("beneath")
                        if self.flag == 'r':
                            if self.robot_room[self.row+1][self.col] != 'w':
                                self.row = Movement.dn(self.flag, self.row, self.col,
                                                       self.room_length, self.room_width)
                                self.flag = 'l'
                                self.sensor_checking()
                                if self.closest_unknown[0] > self.row:
                                    Movement.ninty_deg_right()
                                    Movement.ninty_deg_right()
                                    self.flag = 'r'
                                elif is_unknown_region(self.closest_unknown, self.robot_room):
                                    if self.closest_unknown[0] < self.row:
                                        Movement.ninty_deg_right()
                                        Movement.ninty_deg_right()
                                        self.flag = 'r'
                            else:
                                if self.col < self.room_width-2:
                                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                    self.room_length, self.room_width)
                                    self.sensor_checking()
                                else:
                                    Movement.ninty_deg_left()
                                    Movement.ninty_deg_left()
                                    self.flag = 'l'

                        elif self.flag == 'l':
                            if self.robot_room[self.row+1][self.col] != 'w':
                                self.row = Movement.dn(self.flag, self.row, self.col,
                                                       self.room_length, self.room_width)
                                self.flag = 'r'
                                self.sensor_checking()
                                if self.closest_unknown[0] > self.row:
                                    Movement.ninty_deg_left()
                                    Movement.ninty_deg_left()
                                    self.flag = 'l'
                                elif is_unknown_region(self.closest_unknown, self.robot_room):
                                    if self.closest_unknown[0] < self.row:
                                        Movement.ninty_deg_left()
                                        Movement.ninty_deg_left()
                                        self.flag = 'l'
                            else:
                                if self.col > 1:
                                    self.col = Movement.forwardFeed(self.flag, self.row, self.col,
                                                                    self.room_length, self.room_width)
                                    self.sensor_checking()
                                else:
                                    Movement.ninty_deg_right()
                                    Movement.ninty_deg_right()
                                    self.flag = 'r'

        except Exception as e:
            print(e)
            Movement.cleanup()
            return True

    def set_room(self):
        for i in range(self.room_length):
            self.robot_room.append(['w'])
            if i == 0 or i == self.room_length - 1:
                for j in range(1, self.room_width):
                    self.robot_room[i].append('w')
            else:
                for j in range(1, self.room_width - 1):
                    self.robot_room[i].append(' ')
                self.robot_room[i].append('w')
        for rows in range(1, len(self.robot_room) - 1):
            for cell in range(1, len(self.robot_room[rows]) - 1):
                self.robot_room[rows][cell] = 'u'

    def GetRoom(self):
        return self.full_room


def convertRoomToString(robo_room):
    width = len(robo_room[0])
    length = len(robo_room)
    converted_str = ""
    for i in range(length):
        if 0 < i < length:
            converted_str = converted_str + 'q'
        for j in range(width):
            converted_str = converted_str+ robo_room[i][j]
    return converted_str


def start():
    try:
        robo = SizeSelect()
        room_f = []
        not_done = False
        while not not_done:
            not_done = robo.start()
            time.sleep(0.01)
            room_f = robo.GetRoom()
        print_f(room_f)
        string = convertRoomToString(room_f)
        return string
    except Exception as e:
        print("error in start")
        print(e)


# def test():
#     robot_room = [['w', 'w', 'w', 'w', 'w', 'w'],
#                   ['w', 'k', 'k', 'k', 'k', 'w'],
#                   ['w', 'k', 'z', 'k', 'k', 'w'],
#                   ['w', 'k', 'k', 'w', 'k', 'w'],
#                   ['w', 'k', 'k', 'E', 'k', 'w'],
#                   ['w', 'w', 'w', 'w', 'w', 'w']]
#     str = convertRoomToString(robot_room)
#     return str
# print(test())

#str3 = ""
#time.sleep(3)
#str3 = start()
#print(str3)
