import pigo
import time  # import just in case students need
import random

# esetup logs
import logging

LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/PnR-Final/log_robot.log"  # don't forget to make this file!
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


class Piggy(pigo.Pigo):
    """Student project, inherits teacher Pigo class which wraps all RPi specific functions"""

    def __init__(self):
        """The robot's constructor: sets variables and runs menu loop"""
        print("I have been instantiated!")
        # Our servo turns the sensor. What angle of the servo( ) method sets it straight?
        self.MIDPOINT = 103
        # YOU DECIDE: How close can an object get (cm) before we have to stop?
        self.SAFE_STOP_DIST = 32
        self.HARD_STOP_DIST = 15
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.LEFT_SPEED = 155
        # YOU DECIDE: What left motor power helps straighten your fwd()?
        self.RIGHT_SPEED = 150
        # This one isn't capitalized because it changes during runtime, the others don't
        self.turn_track = 0
        # Our scan list! The index will be the degree and it will store distance
        self.scan = [None] * 180
        self.set_speed(self.LEFT_SPEED, self.RIGHT_SPEED)
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        self.left_total=0
        self.right_total=0
        if __name__ == "__main__":
            while True:
                self.stop()
                self.menu()

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like to add an experimental method
        menu = {"n": ("Navigate forward", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Check status", self.status),
                "h": ("Open House", self.open_house),
                "q": ("Quit", quit_now),
                "t": ("Test", self.skill_test)}
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answers
        ans = raw_input("Your selection: ")
        # activate the item selected
        menu.get(ans, [None, error])[1]()

    def open_house(self):
        """reacts to distant measurement in a cute way"""
        while True:
            if self.dist() < 20:
                self.set_speed(60, 60)
                self.encB(18)
                self.set_speed(90, 90)
                self.unsure()
                self.skid_back()
                self.encF(28)
            time.sleep(.1)

    def skid_back(self):
        for x in range(3):
            self.encB(2)

    def unsure(self):
        self.set_speed(90, 90)
        self.encF(14)
        self.encB(20)
        for x in range(2):
            for angle in range(self.MIDPOINT - 20, self.MIDPOINT + 20, 10):
                self.servo(angle)

    # YOU DECIDE: How does your GoPiggy dance?
    def dance(self):
        """executes a series of methods that add up to a compound dance"""
        if not self.safe_to_dance():
            print("\n---- NOT SAFE TO DANCE ----\n")
            return
        print("\n---- LET'S DANCE ----\n")
        ##### WRITE YOUR FIRST PROJECT HERE
        for x in range(2):
            self.shuffle_forward()
            self.bob_head()
            self.spin()
            self.shuffle_backwards()
            self.circle_shake()
            self.skid()
            self.shake_head()
            self.fake()
            self.back_up()
            self.turn()
            self.shake_head()
            self.pivot()
            self.spin()
            self.shimmy()
            self.run()
            self.sprinkler_body()
            self.spin()
            self.skid()
            self.sprinkler_body()
            self.bob_head()
            self.shake()
            self.shimmy()
            self.skid()
            self.circle_shake()
            self.sprinkler()

    def shuffle_forward(self):
        """move left right to right and go forward"""
        for x in range(2):
            self.encF(9)
            self.encL(2)
            self.encR(2)
            self.encF(10)

    def bob_head(self):
        """move head side to side"""
        for x in range(self.MIDPOINT - 20, self.MIDPOINT - 20, 5):
            self.servo(x)

    def spin(self):
        """go in circles"""
        self.encL(20)
        self.encR(20)

    def shuffle_backwards(self):
        """move left and write then go back"""
        for x in range(2):
            self.encB(5)
            self.encF(2)
            self.encB(5)

    def skid(self):
        """move minimal amount back and forth"""
        for x in range(3):
            self.encF(1)
            self.encB(1)

    def fake(self):
        """look like going left then go right"""
        self.encF(10)
        self.encL(1)  # fake small move left
        self.encR(5)
        self.encF(10)

    def sprinkler_body(self):
        """move left and right"""
        for x in range(5):
            self.encL(1)
        self.encR(5)  # move pack
        for x in range(5):
            self.encL(1)
        self.encL(5)  # move back

    def back_up(self):
        """move backwards"""
        for x in range(3):
            self.encB(5)
            self.encF(1)
            self.encB(1)

    def turn(self):
        """turn to the side"""
        self.encL(20)
        self.encF(10)  # make a square
        self.encR(20)
        self.encB(10)

    def shake_head(self):
        """shake head quickly one one side"""
        for x in range(3):
            for x in range(self.MIDPOINT - 60, self.MIDPOINT - 16, 10):
                self.servo(x)

    def pivot(self):
        """go in a half circle one point at a time"""
        for x in range(14):  # is this half cirlce?
            self.encL(1)  # move slowly in a half cicle

    def shimmy(self):
        """move left and right"""
        for x in range(3):
            self.encL(3)
            self.encF(1)
            self.encR(3)
            self.encF(1)

    def run(self):
        """start slow and then go"""
        for x in range(2):
            self.encL(1)
            self.encF(1)  # minimal movement
            self.encR(1)
            self.encF(1)
            self.encF(20)  # forward a lot

    def shake(self):
        """move left and right """
        for x in range(5):
            self.encL(2)
            self.encR(2)

    def circle_shake(self):
        """move 90 deg at a time then go back"""
        for x in range(4):
            self.encR(7)  # is this 90 deg?
            self.encB(4)

    def safe_to_dance(self):
        """circles around the room"""
        # check for problems
        for x in range(4):
            if not self.is_clear():
                return False
            self.encR(8)  # is this 90 deg?
        return True

    def sprinkler(self):
        """moves your head like a sprinkler"""
        # repeat the move 5 times
        for x in range(5):
            for angle in range(self.MIDPOINT - 20, self.MIDPOINT + 20, 5):
                self.servo(angle)

        # If we find no problems
        return True

    def obstacle_count(self):
        """scans and estimates the number of obstacles within sight"""
        self.wide_scan()
        found_something = False
        counter = 0
        term_dist = 150
        for ang, distance in enumerate(self.scan):
            if distance and distance < term_dist and not found_something:
                found_something = True
                counter += 1
                print("Object # %d found, I think" % counter)
            if distance and distance > term_dist and found_something:
                found_something = False
        print("\n----I SEE %d OBJECTS----\n" % counter)

    def skill_test(self):
        """demonstrates nav skills"""
        choice = raw_input("left/right or Turn Until Clear")

        if "l" in choice:
            self.wide_scan(count=4)  # scan the area
            # pick left or right

            # create two variables, left_total and right_total
            left_total = 0
            right_total = 0
            # loop from self.MIDPOINT - 60 to self.MIDPOINT
            for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
                if self.scan[angle]:
                    # add up the numbers to right_total
                    right_total += self.scan[angle]
            # loop from self.MIDPOINT to self.MIDPOINT + 60
            for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
                if self.scan[angle]:
                    # add up the numbers to left_total
                    left_total += self.scan[angle]
            # if right is bigger:
            if right_total > left_total:
                # turn right
                self.encR(3)
            # if left is bigger:
            if right_total < left_total:
                # turn left
                self.encL(3)
        else:
            while not self.is_clear():
                self.encR(1)

    def safety_check(self):
        """subroutine of the dance method"""
        self.servo(self.MIDPOINT)  # look straight ahead
        for loop in range(4):
            if not self.is_clear():
                print("NOT GOING TO DANCE")
                return False
            print("Check #%d" % (loop + 1))
            self.encR(8)  # figure out 90 deg
        print("Safe to dance!")
        return True

    def nav(self):
        """auto pilots and attempts to maintain original heading"""
        logging.debug("Starting the nav method")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        count = 0
        error_count = 0
        while True:
            if self.is_clear():
                self.encF(10)
                error_count = 0
            else:
                error_count +=1
                if error_count ==10:
                    pass

                self.encB(4)
                self.encL(4)
                if not self.is_clear():
                    self.encB(4)
                    self.encR(8) #turning right



    def is_clear_infront(self):
        """checks the scan array to see if there is a path dead ahead"""
        for ang in range (self.MIDPOINT-10, self.MIDPOINT +10):
            if self.scan[ang] and self.scan[ang] < self.SAFE_STOP_DIST:
                return False

    """def cruise(self):
         pulse drive straight while path is clear 


        self.servo(self.MIDPOINT)  # make head straight
        if self.dist() < self.SAFE_STOP_DIST:
            break  # break each time to avoid being stuck in a loop

        self.servo(self.MIDPOINT + 50)  # if 15 degrees from the midpoint is
        if self.dist() > self.SAFE_STOP_DIST:
            break  # pulse drive

        self.servo(self.MIDPOINT - 50)  # looking left?
        if self.dist() > self.SAFE_STOP_DIST:
            return

        self.encF(5)


        self.stop()


    #-this method did not work - but I left it in to show progress- trying to copy the Skill_test method -"""
    def check(self):
        self.wide_scan(count=4)  # scan the area #i would really like the robot to move faster
        left_total = 0
        right_total = 0
        for angle in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[angle]:
                right_total += self.scan[angle]
        for angle in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[angle]:
                left_total += self.scan[angle]
        if right_total > left_total:
            self.encR(6)
        if right_total < left_total:
            self.encL(6)"""







####################################################
############### STATIC FUNCTIONS

def error():
    records general,less specific error
    logging.error("ERROR")
    print('ERROR')


def quit_now():
    """shuts down app
    raise SystemExit


##################################################################
######## The app starts right here when we instantiate our GoPiggy


try:
    g = Piggy()
except (KeyboardInterrupt, SystemExit):
    pigo.stop_now()
except Exception as ee:
    logging.error(ee.__str__())
