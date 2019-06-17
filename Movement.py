import RPi.GPIO as gpio
import time
import Sensor as s
# import LSM303D as lsm

gpio.cleanup()
gpio.setwarnings(False)

forward_left_pin = 16
reverse_left_pin = 11
forward_right_pin = 15
reverse_right_pin = 13

move_delay = 0.01

# right_heading = lsm.getHeading()
# print(right_heading)
# down_heading = right_heading
# left_heading = right_heading
# up_heading = right_heading

# speed for s>7.7V ###
#f_speed = 85
#f_tf = 0.80
#p_speed =88
#p_r_tf=0.08
#p_l_tf=0.08
#f_p_r_tf =0.47
#f_p_l_tf = 0.52
#left_aid = 5
#
#feed_r = 0.08
#feed_l = 0.08
#too_close_speed = 0.15
#too_far_speed = 0.5

# --- speed for s<7.7V --- #
#f_speed = 90
#f_tf = 0.820
#left_aid = 7
#
#p_speed = 88
#p_r_tf = 0.080
#p_l_tf = 0.082
#f_p_r_tf = 0.49
#f_p_l_tf = 0.52
#
#feed_r = 0.10
#feed_l = 0.10
#
#too_close_speed = 0.15
#too_far_speed = 0.5

# --- speed for s<7.4V --- #
f_speed = 92
f_tf = 0.880

p_speed = 88
p_r_tf = 0.12
p_l_tf = 0.10

f_p_r_tf = 0.49
f_p_l_tf = 0.55
left_aid = 7
feed_r = 0.1
feed_l = 0.105

too_close_speed = 0.15
too_far_speed = 0.5

# --- speed for s<7 --- #
# f_speed = 94
# f_tf = 0.850
# p_speed =94
# p_r_tf=0.10
# p_l_tf=0.10
# f_p_r_tf =0.50
# f_p_l_tf = 0.53
# left_aid = 5

# --- speed for s<6.6 --- #
# f_speed = 94
# f_tf = 0.90
# p_speed =94
# p_r_tf=0.12
# p_l_tf=0.12
# f_p_r_tf =0.52
# f_p_l_tf = 0.55
# left_aid = 7


def cleanup():
    gpio.cleanup()


# ----- Delay ----- #
def delay(tf=move_delay):
    time.sleep(tf)


# ----- Forward ----- #
def forward(col=0, direction='a', g22=False, tf=f_tf):
    #    print(" In Forward")
    try:
        gpio.cleanup()
        if g22:
            print("gww")
            tf+=0.650
        dist_form_wall = s.m_sensor()
        if dist_form_wall < 30 and tf > 0.3:
            tf = tf - 0.3
        gpio.setmode(gpio.BOARD)
        gpio.setup(forward_left_pin, gpio.OUT)
        gpio.setup(reverse_left_pin, gpio.OUT)
        gpio.setup(forward_right_pin, gpio.OUT)
        gpio.setup(reverse_right_pin, gpio.OUT)

        forward_left = gpio.PWM(forward_left_pin, 207)
        reverse_left = gpio.PWM(reverse_left_pin, 207)
        forward_right = gpio.PWM(forward_right_pin, 207)
        reverse_right = gpio.PWM(reverse_right_pin, 207)

        forward_right.start(f_speed)
        forward_left.start(f_speed + left_aid)
        reverse_left.stop()
        reverse_right.stop()

        delay(tf)
        gpio.cleanup()
        delay(0.15)

        if direction == 'r' or direction == 'd':
            return col + 1
        elif direction == 'l' or direction == 'u' or direction == 'up':
            return col - 1
        else:
            return col
    except Exception as e:
        print('error in forward')
        print(e)
        cleanup()


# ----- FeedBack ----- #
def is_too_close_to_left(dist1):
    try:
        if dist1 <= 5:
            pivot_right(feed_r)
    except Exception as e:
        print('error in is_too_close_to_left')
        print(e)
        cleanup()


def wt_check_on_left(dist1, dist2, diff):
    try:
        if diff >= 1:
            if dist2 < dist1:
                if dist2 < 10:
                    if diff < 3:
                        pivot_right(feed_r)
                    else:
                        pivot_right(feed_r + 0.02)
                else:
                    if diff < 3:
                        pivot_right(feed_r + 0.02)
                    else:
                        pivot_right(feed_r)

            elif dist2 > dist1:
                if dist2 <= 5:
                    pivot_left(feed_l - 0.05)
                else:
                    if diff < 3:
                        pivot_left(feed_l)
                    else:
                        pivot_left(feed_l + 0.05)
    except Exception as e:
        print('wt_error in check_on_left')
        print(e)
        cleanup()


def wt_check_on_right(dist2, dist3, dist4, diff2):
    try:
#        print("in check_on_right")
        if diff2 >= 1:
            if dist4 < dist3:
                if dist2 > 5:
                    if diff2 <= 3:
                        pivot_left(feed_l+0.02)
                    else:
                        pivot_left(feed_l + 0.04)
                else:
                    if diff2 < 3:
                        pivot_left(feed_l - 0.02)
                    else:
                        pivot_left(feed_l)

            elif dist4 > dist3:
                if dist2 <= 5:
                    pivot_right(feed_r)
                else:
                    if diff2 < 5:
                        pivot_right(feed_r - 0.02)
                    else:
                        pivot_right(feed_r)
    except Exception as e:
        print('error in wt_check_on_right')
        print(e)
        cleanup()


def check_on_left(dist1, dist2, diff):
    try:
        if not s.f_sensor():
            print("check on left, dif: ",diff)
            if diff >= 1:
                if dist2 > dist1:
                    if diff <= 3:
                        pivot_left(feed_l)
                    else:
                        pivot_left(feed_l + 0.02)
                        
                elif dist2 < dist1:
                    if diff <= 3:
                        pivot_right(feed_r)
                    else:
                        pivot_right(feed_r + 0.02)
    except Exception as e:
        print('error in check_on_left')
        print(e)
        cleanup()


def check_on_right(dist3, dist4, diff2):
    try:
        if not s.f_sensor():
            print("check on right, diff2: ",diff2)
            if diff2 >= 1:
                if dist4 > dist3:
                    if diff2 <= 3:
                        pivot_right(feed_r)
                    else:
                        pivot_right(feed_r + 0.02)
                    
                elif dist4 < dist3:
                    if diff2 <= 3:
                        pivot_left(feed_l)
                    else:
                        pivot_left(feed_l + 0.02)
    except Exception as e:
        print('error in check_on_right')
        print(e)
        cleanup()
        

def feedback(dist1, dist3, flag, row, col, length, width):
    #    print(" in feedback")
    #    print("flag: ",flag," row: ",row)
    try:
#        if not s.f_sensor():
        if flag == 'r':
            if row < length/2:
                dist2 = s.l_sensor()
                diff = abs(dist2 - dist1)
                if diff < 15:
                    check_on_left(dist1, dist2, diff)
                elif diff >= 15:
                    dist4 = s.r_sensor()
                    diff2 = abs(dist4 - dist3)
                    check_on_right(dist3, dist4, diff2)
            else:
                dist4 = s.r_sensor()
                diff2 = abs(dist4 - dist3)
                if diff2 < 15:
                    check_on_right(dist3, dist4, diff2)
                elif diff2 >= 15:
                    dist2 = s.l_sensor()
                    diff = abs(dist2 - dist1)
                    check_on_left(dist1, dist2, diff)

        elif flag == 'l':
            if row > length/2:
                dist2 = s.l_sensor()
                diff = abs(dist2 - dist1)
                if diff < 15:
                    check_on_left(dist1, dist2, diff)
                elif diff >= 15:
                    dist4 = s.r_sensor()
                    diff2 = abs(dist4 - dist3)
                    check_on_right(dist3, dist4, diff2)
            else:
                dist4 = s.r_sensor()
                diff2 = abs(dist4 - dist3)
                if diff2 < 15:
                    check_on_right(dist3, dist4, diff2)
                elif diff2 >= 15:
                    dist2 = s.l_sensor()
                    diff = abs(dist2 - dist1)
                    check_on_left(dist1, dist2, diff)

        elif flag == 'u' or flag == 'up':
            if col < width/2:
                dist2 = s.l_sensor()
                diff = abs(dist2 - dist1)
                if diff < 15:
                    check_on_left(dist1, dist2, diff)
                elif diff >= 15:
                    dist4 = s.r_sensor()
                    diff2 = abs(dist4 - dist3)
                    check_on_right(dist3, dist4, diff2)
            else:
                dist4 = s.r_sensor()
                diff2 = abs(dist4 - dist3)
                if diff2 < 15:
                    check_on_right(dist3, dist4, diff2)
                elif diff2 >= 15:
                    dist2 = s.l_sensor()
                    diff = abs(dist2 - dist1)
                    check_on_left(dist1, dist2, diff)

        elif flag == 'd':
            if row > width/2:
                dist2 = s.l_sensor()
                diff = abs(dist2 - dist1)
                if diff < 15:
                    check_on_left(dist1, dist2, diff)
                elif diff >= 15:
                    dist4 = s.r_sensor()
                    diff2 = abs(dist4 - dist3)
                    check_on_right(dist3, dist4, diff2)
            else:
                dist4 = s.r_sensor()
                diff2 = abs(dist4 - dist3)
                if diff2 < 15:
                    check_on_right(dist3, dist4, diff2)
                elif diff2 >= 15:
                    dist2 = s.l_sensor()
                    diff = abs(dist2 - dist1)
                    check_on_left(dist1, dist2, diff)

    except Exception as e:
        gpio.cleanup()
        print("error in feedback")
        print(e)
                        
                        
def wt_feedback(dist1, dist3):
    try:
#        print("wt fb")
        if not s.f_sensor():
            dist2 = s.l_sensor()
            dist4 = s.r_sensor()
            diff = abs(dist2 - dist1)
            diff2 = abs(dist4 - dist3)
            if diff < 15:
                wt_check_on_left(dist1, dist2, diff)
            elif diff >= 15:
                wt_check_on_right(dist2, dist3, dist4, diff2)

    except Exception as e:
        gpio.cleanup()
        print("error in wtfeedback")
        print(e)


# ----- Forward + FeedBack ----- #

def is_too_close_to_wall_fb():
    try:
        dist_form_wall = s.m_sensor()
        while dist_form_wall < 8:
            reverse(too_close_speed)
            dist_form_wall = s.m_sensor()
    except Exception as e:
        print('error in is_too_close_to_wall_fb')
        print(e)
        cleanup()


def is_too_far_from_wall_fb():
    try:
        dist_form_wall = s.m_sensor()
        while 10 < dist_form_wall < 25:
            forward(1, 'r', False, too_far_speed)
            dist_form_wall = s.m_sensor()
    except Exception as e:
        print('error in is_too_far_from_wall_fb')
        print(e)
        cleanup()


def can_move_forward():
    try:
        if s.m_sensor() > 25:
            if 9 < s.m_l_sensor() < 25:
                print("issue: ", s.m_l_sensor())
                pivot_right(p_r_tf+0.03)
            elif s.m_l_sensor() <= 9:
                print("issue: ", s.m_l_sensor())
                pivot_right(p_r_tf+0.08)
            elif 9 < s.m_r_sensor() < 25:
                print("issue: ", s.m_r_sensor())
                pivot_left(p_l_tf+0.03)
            elif s.m_r_sensor() <= 9:
                print("issue: ", s.m_r_sensor())
                pivot_left(p_l_tf+0.08)
    except Exception as e:
        print('error in can_move_forward')
        print(e)
        cleanup()


def is_too_far_from_left(dist_form_wall):
    try:
        if dist_form_wall > 15:
            pivot_left(0.09)
        elif dist_form_wall > 10:
            pivot_left(0.07)
    except Exception as e:
        print('error in is_too_far_from_left')
        print(e)
        cleanup()


def forwardFeed(flag, row, col, length=0, width=0, wt=False, g22=False):
    try:
        can_move_forward()
        dist1 = s.l_sensor()
        dist3 = s.r_sensor()
        if wt:
            is_too_close_to_left(dist1)
            is_too_far_from_left(dist1)
                
        if flag == 'r' or flag == 'l':
            col = forward(col, flag, g22)
            if wt:
                wt_feedback(dist1, dist3)
                if row == 1:
                    if flag != 'u' and flag != 'up':
                        is_too_close_to_wall_fb()
                else:
                    is_too_close_to_wall_fb()                            
                is_too_far_from_wall_fb()
            else:
                feedback(dist1, dist3, flag, row, col, length, width)
            return col
        elif flag == 'u' or flag == 'd' or flag == 'up':
            row = forward(row, flag)
            if wt:
                wt_feedback(dist1, dist3)
                is_too_close_to_wall_fb()
                is_too_far_from_wall_fb()
            else:
                feedback(dist1, dist3, flag, row, col, length, width)
            return row
    except Exception as e:
        gpio.cleanup()
        print("error in forwardFeed")
        print(e)


# ----- Reverse ----- #
def reverse(tf=0.05):
    #    print(" In Reverse")
    try:
        if not s.m_sensor() < 5:
            tfr = tf
        else:
            tfr = 0.07
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(forward_left_pin, gpio.OUT)
        gpio.setup(reverse_left_pin, gpio.OUT)
        gpio.setup(forward_right_pin, gpio.OUT)
        gpio.setup(reverse_right_pin, gpio.OUT)

        forward_left = gpio.PWM(forward_left_pin, 207)
        reverse_left = gpio.PWM(reverse_left_pin, 207)
        forward_right = gpio.PWM(forward_right_pin, 207)
        reverse_right = gpio.PWM(reverse_right_pin, 207)

        reverse_right.start(f_speed)
        reverse_left.start(f_speed)
        forward_left.stop()
        forward_right.stop()

        delay(tfr)

        gpio.cleanup()

        delay(0.1)
    except Exception as e:
        print('error in reverse')
        print(e)
        cleanup()


# ----- Pivot Left ----- #
def pivot_left(tf=p_l_tf):
    #    print(" In Pivot Left")
        
    try:
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(forward_left_pin, gpio.OUT)
        gpio.setup(reverse_left_pin, gpio.OUT)
        gpio.setup(forward_right_pin, gpio.OUT)
        gpio.setup(reverse_right_pin, gpio.OUT)

        forward_left = gpio.PWM(forward_left_pin, 207)
        reverse_left = gpio.PWM(reverse_left_pin, 207)
        forward_right = gpio.PWM(forward_right_pin, 207)
        reverse_right = gpio.PWM(reverse_right_pin, 207)

        forward_right.start(p_speed)
        reverse_left.start(p_speed)
        forward_left.stop()
        reverse_right.stop()

        if tf < 0:
            tf = p_l_tf

        time.sleep(tf)
        gpio.cleanup()
        delay(0.12)
    except Exception as e:
        print("error in pivot left")
        print(e)
        cleanup()


# ----- Pivot Right ----- #
def pivot_right(tf=p_r_tf):
    #    print(" In Pivot Right")
    try:
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(forward_left_pin, gpio.OUT)
        gpio.setup(reverse_left_pin, gpio.OUT)
        gpio.setup(forward_right_pin, gpio.OUT)
        gpio.setup(reverse_right_pin, gpio.OUT)

        forward_left = gpio.PWM(forward_left_pin, 207)
        reverse_left = gpio.PWM(reverse_left_pin, 207)
        forward_right = gpio.PWM(forward_right_pin, 207)
        reverse_right = gpio.PWM(reverse_right_pin, 207)

        forward_left.start(p_speed)
        reverse_right.start(p_speed)
        reverse_left.stop()
        forward_right.stop()

        delay(tf)
        gpio.cleanup()
        delay(0.12)
    except Exception as e:
        print('error in pivot right')
        print(e)
        cleanup()


# ----- Deadlock----- #
def deadlock(flag, row, col, length, width):
    #    print(" In Deadlock")
    try:
        if s.m_sensor() < 10:
            reverse(0.2)
        ninty_deg_right()
        if s.m_sensor() < 10:
            reverse(0.2)
        ninty_deg_right()
        col = forwardFeed(flag, row, col, length, width)
        return col
    except Exception as e:
        print('error in deadlock')
        print(e)
        cleanup()


# ----- ninty Deg to the Right ----- #

def first_func_for_90dr(f2):
#    print("in first_func_for_90dr")
    if len(f2) == 1:
        pivot_right(p_r_tf)
        f2.append(s.m_r_sensor())
    elif len(f2) < 3 and not f2[len(f2) - 1] < f2[len(f2) - 2]:
        pivot_right()
        f2.append(s.m_r_sensor())
    else:
        if f2[len(f2) - 1] < f2[len(f2) - 2]:
            pivot_right()
            f2.append(s.m_r_sensor())
            if f2[len(f2) - 1] > f2[len(f2) - 2]:
                r2 = s.m_r_sensor()
                r3 = s.m_l_sensor()
                pivot_left(p_l_tf - 0.01)
                l2 = s.m_r_sensor()
                l3 = s.m_l_sensor()
                if abs(r2 - r3) < abs(l2 - l3):
                    pivot_right(p_l_tf - 0.01)
                    return False
                else:
                    return False
        else:
            r2 = s.m_r_sensor()
            r3 = s.m_l_sensor()
            pivot_left(p_l_tf - 0.01)
            l2 = s.m_r_sensor()
            l3 = s.m_l_sensor()
            if abs(r2 - r3) < abs(l2 - l3):
                pivot_right(p_l_tf - 0.01)
                return False
            else:
                return False


def second_funck_for_90dr(dist_from_f_mid):
#    print("2nd feed back")
    dist_from_left = []
    dist_from_left.append(s.l_sensor())
    sum_dist = []
    sum_dist.append(abs(dist_from_left[len(dist_from_left) - 1] - dist_from_f_mid))

    if sum_dist[len(sum_dist) - 1] <= 1:
        pass
    elif sum_dist[len(sum_dist) - 1] > 1:
        pivot_right(p_r_tf)
        dist_from_left.append(s.l_sensor())
        sum_dist.append(abs(dist_from_left[len(dist_from_left) - 1] - dist_from_f_mid))
        if sum_dist[len(sum_dist) - 1] <= 1:
            pass
        elif 1 < sum_dist[len(sum_dist) - 1] <= sum_dist[len(sum_dist) - 2]:
            pivot_right(p_r_tf)
            dist_from_left.append(s.l_sensor())
            sum_dist.append(abs(dist_from_left[len(dist_from_left) - 1] - dist_from_f_mid))
            if sum_dist[len(sum_dist) - 1] <= 1 or sum_dist[len(sum_dist) - 1] < sum_dist[len(sum_dist) - 2]:
                pass
#            elif sum_dist[len(sum_dist) - 1] > sum_dist[len(sum_dist) - 2]:
#                pivot_left(p_l_tf)
        elif sum_dist[len(sum_dist) - 1] > sum_dist[len(sum_dist) - 2]:
#            pivot_left(p_l_tf)
            dist_from_left.append(s.l_sensor())
            sum_dist.append(abs(dist_from_left[len(dist_from_left) - 1] - dist_from_f_mid))
            if sum_dist[len(sum_dist) - 1] <= 1:
                pass
            elif sum_dist[len(sum_dist) - 1] > 1:
#                pivot_left(p_l_tf)
                dist_from_left.append(s.l_sensor())
                sum_dist.append(abs(dist_from_left[len(dist_from_left) - 1] - dist_from_f_mid))


def ninty_deg_right():
    try:
        #    print(" In 90 Deg to the Right")
        dist_from_f_mid = round(s.m_sensor())
        f2 = []
        pivot_right(f_p_r_tf)
        f2.append(s.m_r_sensor())
        while not s.f_sensor():
            if not first_func_for_90dr(f2):
                break
        if not s.f_sensor():
            second_funck_for_90dr(dist_from_f_mid)

    except Exception as e:
        print('error in pivot 90 deg right')
        print(e)
        cleanup()


# ----- 90 Deg to the Left  -----#
def first_func_for_90dl(f3):
    if len(f3) < 3:
        pivot_left()
        f3.append(s.m_l_sensor())
    else:
        if f3[len(f3) - 1] < f3[len(f3) - 2]:
            pivot_left()
            f3.append(s.m_l_sensor())
            if f3[len(f3) - 1] > f3[len(f3) - 2]:
                l2 = s.m_r_sensor()
                l3 = s.m_l_sensor()
                pivot_right(p_r_tf - 0.01)
                r2 = s.m_r_sensor()
                r3 = s.m_l_sensor()
                if abs(r2 - r3) > abs(l2 - l3):
                    pivot_left(p_l_tf - 0.01)
                    return False
                else:
                    return False
        else:
            l2 = s.m_r_sensor()
            l3 = s.m_l_sensor()
            pivot_right(p_r_tf - 0.01)
            r2 = s.m_r_sensor()
            r3 = s.m_l_sensor()
            if abs(r2 - r3) > abs(l2 - l3):
                pivot_left(p_l_tf - 0.01)
                return False
            else:
                return False


def second_funck_for_90dl(dist_from_f_mid):
    try:
        print(dist_from_f_mid)
        dist_from_right = []
        dist_from_right.append(s.r_sensor())
        print(dist_from_right)
        sum_dist = []
        sum_dist.append(abs(dist_from_right[len(dist_from_right) - 1] - dist_from_f_mid))
        print(sum_dist)

        if sum_dist[len(sum_dist) - 1] <= 1:
            print("<1")
            pass
        elif sum_dist[len(sum_dist) - 1] > 1:
            print(">1")
            pivot_left(p_l_tf)
            dist_from_right.append(s.r_sensor())
            sum_dist.append(abs(dist_from_right[len(dist_from_right) - 1] - dist_from_f_mid))
            if sum_dist[len(sum_dist) - 1] <= 1:
                print(sum_dist)          
                print(dist_from_right)      
                pass
            elif 1 < sum_dist[len(sum_dist) - 1] <= sum_dist[len(sum_dist) - 2]:
                pivot_left(p_l_tf)
                dist_from_right.append(s.r_sensor())
                sum_dist.append(abs(dist_from_right[len(dist_from_right) - 1] - dist_from_f_mid))
                if sum_dist[len(sum_dist) - 1] <= 1 or sum_dist[len(sum_dist) - 1] < sum_dist[len(sum_dist) - 2]:
                    print(sum_dist)
                    print(dist_from_right)   
                    pass
                elif sum_dist[len(sum_dist) - 1] > sum_dist[len(sum_dist) - 2]:
                    pivot_right(p_r_tf)
            elif sum_dist[len(sum_dist) - 1] > sum_dist[len(sum_dist) - 2]:
                pivot_right(p_r_tf)
                dist_from_right.append(s.r_sensor())
                sum_dist.append(abs(dist_from_right[len(dist_from_right) - 1] - dist_from_f_mid))
                if sum_dist[len(sum_dist) - 1] <= 1:
                    pass
                elif sum_dist[len(sum_dist) - 1] > 1:
                    pivot_right(p_r_tf)
                    dist_from_right.append(s.r_sensor())
                    sum_dist.append(abs(dist_from_right[len(dist_from_right) - 1] - dist_from_f_mid))

    except Exception as e:
        print('error in 90 deg left')
        print(e)
        cleanup()


def ninty_deg_left():
    try:
        print(" In 90 Deg to the Left")
        dist_from_f_mid = round(s.m_sensor())
        f3 = []
        pivot_left(f_p_l_tf)
        f3.append(s.m_l_sensor())
        while not s.f_sensor():
            if not first_func_for_90dl(f3):
                break
        if not s.f_sensor():
            second_funck_for_90dl(dist_from_f_mid)
    except Exception as e:
        print('error in 90 deg left')
        print(e)
        cleanup()


# ----- Down Navigation ----- #
def dn(flag, row, col, length, width, dl=False):
    #    print(" In down Navigation")
    try:
        if s.m_sensor() < 15:
            reverse()
            delay(move_delay)
        if not dl:
            if flag == 'r':
                ninty_deg_right()
                forwardFeed(flag, row, col, length, width)
                if s.m_sensor() < 10:
                    reverse(0.2)
                ninty_deg_right()
            elif flag == 'l':
                ninty_deg_left()
                forwardFeed(flag, row, col, length, width)
                if s.m_sensor() < 10:
                    reverse(0.2)
                ninty_deg_left()
            return row + 1
        else:
            if flag == 'r':
                ninty_deg_right()
                forwardFeed(flag, row, col, length, width)
                if s.m_sensor() < 10:
                    reverse(0.2)
                ninty_deg_left()
            elif flag == 'l':
                ninty_deg_left()
                forwardFeed(flag, row, col, length, width)
                if s.m_sensor() < 10:
                    reverse(0.2)
                ninty_deg_right()
            return row + 1
    except Exception as e:
        print("error in down nav")
        print(e)
        gpio.cleanup()


# ----- Up Navigation ----- #
def un(flag, row, col, length, width):
    try:
        if flag == 'r':
            ninty_deg_left()
            forwardFeed(flag, row, col, length, width)
            delay(move_delay)
        elif flag == 'l':
            ninty_deg_right()
            forwardFeed(flag, row, col, length, width)
            delay(move_delay)
        return row - 1
    except Exception as e:
        print('error in up nav')
        print(e)
        cleanup()



#while s.m_sensor() > 15:
#    forwardFeed('r', 0, 0)
#ninty_deg_right()
#ninty_deg_left()
# reverse()



