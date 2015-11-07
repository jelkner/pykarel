#/usr/bin/env python3
"""
pykarel is a learning tool for teaching programming based on Karel the Robot.
It uses tkinter for graphical display.

__author__ = "Shane Torbert"
__copyright__ = "Copyright 2015, Shane Torbert"
__credits__ = ["Paul Bui", "Matt Gallagher", "Jeff Elkner"]
__license__ = "Creative Commons Attribution Sharealike 4.0 International"
__version__ = "0.5"
__maintainer__ = "Jeffrey Elkner"
__email__ = "jeff@elkner.net"
__status__ = "Development"
"""
from tkinter import Tk, Canvas
from math import sin, cos, radians
from time import sleep

EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270
INFINITY = -1


class World(Tk):
    def __init__(self, filename=None, block=50, debug=True, delay=0.25,
                 image=False, width=10, height=10):
        Tk.__init__(self)
        self.title("")
        arg = block
        self.width = width
        self.height = height
        self.beepers = {}
        self.ovals = {}
        self.numbers = {}
        self.robots = {}
        self.walls = {}
        self.m = arg * (width + 3)
        self.n = arg * (height + 3)
        self.t = arg
        self.delay = delay
        self.debug = debug
        self.use_image = image
        a = self.t + self.t / 2
        b = self.m - self.t / 2
        c = self.n - self.t / 2
        self.canvas = Canvas(self, bg="white", width=self.m, height=self.n)
        self.canvas.pack()
        count = 1
        for k in range(2*self.t, max(self.m, self.n)-self.t, self.t):
            if k < b:
                self.canvas.create_line(k, c, k, a, fill="red")
                self.canvas.create_text(k, c+self.t/2, text=str(count),
                                        font=("Times",
                                              max(-self.t*2/3, -15), ""))
            if k < c:
                self.canvas.create_line(b, k, a, k, fill="red")
                self.canvas.create_text(a-self.t/2, self.n-k, text=str(count),
                                        font=("Times",
                                              max(-self.t*2/3, -15), ""))
            count += 1
        self.canvas.create_line(a, c, b, c, fill="black", width=3)
        self.canvas.create_line(a, a, a, c, fill="black", width=3)
        if filename is not None:
            self.read_world(filename)
        self.refresh()

    def read_world(self, filename):
        try:
            infile = open("worlds\\{0}.wld".format(filename), "r")
        except IOError:
            try:
                infile = open("worlds/{0}.wld".format(filename), "r")
            except IOError:
                infile = open(filename, "r")
        text = infile.read().split("\n")
        infile.close()
        for t in text:
            if t.startswith("eastwestwalls"):
                s = t.split(" ")
                y, x = int(s[1]), int(s[2])
                self.add_wall(x, y, -1, y)
            if t.startswith("northsouthwalls"):
                s = t.split(" ")
                x, y = int(s[1]), int(s[2])
                self.add_wall(x, y, x, -1)
            if t.startswith("beepers"):
                s = t.split(" ")
                y, x, n = int(s[1]), int(s[2]), int(s[3])
                if n is INFINITY:
                    self.add_infinite_beepers(x, y)
                else:
                    for k in range(n):
                        self.add_beeper(x, y)

    def pause(self):
        sleep(self.delay)

    def is_beeper(self, x, y):
        return (x, y) in list(self.beepers.keys()) and not \
            self.beepers[(x, y)] == 0

    def count_robots(self, x, y):
        if (x, y) not in list(self.robots.keys()):
            return 0
        return len(self.robots[(x, y)])

    def crash(self, x1, y1, x2, y2):
        if 0 in (x1, y1, x2, y2):
            return True
        if (x2, y2) in list(self.walls.keys()) and \
                (x1, y1) in self.walls[(x2, y2)]:
            return True
        if (x1, y1) in list(self.walls.keys()) and \
                (x2, y2) in self.walls[(x1, y1)]:
            return True
        return False

    def add_infinite_beepers(self, x, y):
        flag = (x, y) not in list(self.beepers.keys()) or \
            self.beepers[(x, y)] is 0
        self.beepers[(x, y)] = INFINITY
        text = "oo"
        a = self.t + x * self.t
        b = self.n - (self.t + y * self.t)
        t = self.t / 3
        if flag:
            self.ovals[(x, y)] = self.canvas.create_oval(a-t, b-t, a+t,
                                                         b+t, fill="black")
            self.numbers[(x, y)] = self.canvas.create_text(a, b, text=text,
                                                           fill="white",
                                                           font=("Times",
                                                                 max(-self.t/2,
                                                                     -20),
                                                                 ""))
        else:
            self.canvas.itemconfig(self.numbers[(x, y)], text=text)
        if (x, y) in list(self.robots.keys()):
            for robot in self.robots[(x, y)]:
                robot.lift()

    def add_beeper(self, x, y):
        if (x, y) in list(self.beepers.keys()) and \
                self.beepers[(x, y)] is INFINITY:
            return
        flag = (x, y) not in list(self.beepers.keys()) or \
            self.beepers[(x, y)] is 0
        if flag:
            self.beepers[(x, y)] = 1
        else:
            self.beepers[(x, y)] += 1
        text = str(self.beepers[(x, y)])
        a = self.t + x * self.t
        b = self.n - (self.t + y * self.t)
        t = self.t / 3
        if flag:
            self.ovals[(x, y)] = self.canvas.create_oval(a-t, b-t, a+t, b+t,
                                                         fill="black")
            self.numbers[(x, y)] = self.canvas.create_text(a, b, text=text,
                                                           fill="white",
                                                           font=("Times",
                                                                 max(-self.t/2,
                                                                     -20),
                                                                 ""))
        else:
            self.canvas.itemconfig(self.numbers[(x, y)], text=text)
        if (x, y) in list(self.robots.keys()):
            for robot in self.robots[(x, y)]:
                robot.lift()

    def remove_beeper(self, x, y):
        if self.beepers[(x, y)] is INFINITY:
            return
        self.beepers[(x, y)] -= 1
        flag = self.beepers[(x, y)] is 0
        text = str(self.beepers[(x, y)])
        if flag:
            self.canvas.delete(self.ovals[(x, y)])
            self.canvas.delete(self.numbers[(x, y)])
        else:
            self.canvas.itemconfig(self.numbers[(x, y)], text=text)
        if (x, y) in list(self.robots.keys()):
            for robot in self.robots[(x, y)]:
                robot.lift()

    def add_wall(self, x1, y1, x2, y2):
        if not x1 == x2 and not y1 == y2:
            return
        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1, y2)
            if y1 == -1:
                y1 = y2
            for k in range(y1, y2+1):
                self.walls.setdefault((x1, k), []).append((x1+1, k))
                a = self.t + x1 * self.t+self.t / 2
                b = self.n - (self.t + k * self.t) + self.t / 2
                c = self.t + x1 * self.t + self.t / 2
                d = self.n - (self.t + k * self.t) - self.t / 2
                self.canvas.create_line(a, b+1, c, d-1, fill="black", width=3)
        else:
            x1, x2 = min(x1, x2), max(x1, x2)
            if x1 == -1:
                x1 = x2
            for k in range(x1, x2+1):
                self.walls.setdefault((k, y1), []).append((k, y1+1))
                a = self.t + k * self.t - self.t / 2
                b = self.n - (self.t + y1 * self.t) - self.t / 2
                c = self.t + k * self.t + self.t / 2
                d = self.n - (self.t + y1 * self.t) - self.t / 2
                self.canvas.create_line(a-1, b, c+1, d, fill="black", width=3)

    def draw(self, x, y, d, img):
        t = self.t / 2
        angle = 120
        x = self.t + x * self.t
        y = self.n - (self.t + y * self.t)
        x1 = x + 3 ** 0.5 * t / 2 * cos(radians(d))
        y1 = y - 3 ** 0.5 * t / 2 * sin(radians(d))
        x2 = x + t * cos(radians(d + angle))
        y2 = y - t * sin(radians(d + angle))
        x3 = x + t / 4 * cos(radians(d + 180))
        y3 = y - t / 4 * sin(radians(d + 180))
        x4 = x + t * cos(radians(d - angle))
        y4 = y - t * sin(radians(d - angle))
        if img is not None:
            self.canvas.delete(img)
        return self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4,
                                          fill="blue")

    def erase(self, img):
        self.canvas.delete(img)

    def record_move(self, count, x1, y1, x2, y2):
        for robot in self.robots[(x1, y1)]:
            if robot.count == count:
                self.robots[(x1, y1)].remove(robot)
                self.robots.setdefault((x2, y2), []).append(robot)
                break

    def lift(self, img):
        self.canvas.lift(img)

    def refresh(self):
        self.canvas.update()
        self.pause()

    def register(self, x, y, robot):
        self.robots.setdefault((x, y), []).append(robot)

    def remove(self, x, y, robot):
        self.robots[(x, y)].remove(robot)


class Robot:
    COUNT = 1

    def __init__(self, world, x=1, y=1, direction=EAST, beepers=0):
        self.world = world
        self.image = None
        self.x = x
        self.y = y
        self.d = direction % 360
        self.beepers = beepers
        self.alive = True
        self.world.register(x, y, self)
        self.draw()
        self.world.refresh()
        self.count = Robot.COUNT
        Robot.COUNT += 1
        self.debug()

    def destroy(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        if self.world.debug is True:
            print("DESTROYING...", end=' ')
            self.debug()
        self.world.erase(self.image)
        self.world.refresh()
        self.world.remove(self.x, self.y, self)
        self.alive = False

    def __str__(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        if self.beepers == INFINITY:
            s = "infinite"
        else:
            s = str(self.beepers)
        return "Robot %d at (%d,%d) facing %s carrying %s beeper(s)." % \
               (self.count, self.x, self.y,
                   ["east", "north", "west", "south"][self.d//90], s)

    def lift(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        self.world.lift(self.image)

    def draw(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        self.image = self.world.draw(self.x, self.y, self.d, self.image)

    def debug(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        if self.world.debug is True:
            print(self)

    def move(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        d = self.d/90
        dx = (d + 1) % 2 * (d - 1) * -1
        dy = d % 2 * (d - 2) * -1
        x, y = self.x, self.y
        self.x += dx
        self.y += dy
        if self.world.crash(x, y, self.x, self.y):
            raise Exception("Walked through wall.")
        self.world.record_move(self.count, x, y, self.x, self.y)
        self.draw()
        self.world.refresh()
        self.debug()

    def turn_left(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        self.d += 90
        if self.d == 360:
            self.d = 0
        self.draw()
        self.world.refresh()
        self.debug()

    def put_beeper(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        if self.beepers == 0:
            raise Exception("No beepers to put.")
        if self.beepers is not INFINITY:
            self.beepers -= 1
        self.world.add_beeper(self.x, self.y)
        self.world.refresh()
        self.debug()

    def pick_beeper(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        if not self.world.is_beeper(self.x, self.y):
            raise Exception("No beepers to pick.")
        if self.beepers is not INFINITY:
            self.beepers += 1
        self.world.remove_beeper(self.x, self.y)
        self.world.refresh()
        self.debug()

    def any_beepers_in_beeper_bag(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return not self.beepers == 0

    def front_is_clear(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        d = self.d / 90
        dx = (d + 1) % 2 * (d - 1) * -1
        dy = d % 2 * (d - 2) * -1
        x1, y1 = self.x, self.y
        x2, y2 = x1 + dx, y1 + dy
        return not self.world.crash(x1, y1, x2, y2)

    def left_is_clear(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        d = self.d / 90
        d = (d + 1) % 4
        dx = (d + 1) % 2 * (d - 1) * -1
        dy = d % 2 * (d - 2) * -1
        x1, y1 = self.x, self.y
        x2, y2 = x1 + dx, y1 + dy
        return not self.world.crash(x1, y1, x2, y2)

    def right_is_clear(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        d = self.d / 90
        d = (d + 3) % 4
        dx = (d + 1) % 2 * (d - 1) * -1
        dy = d % 2 * (d - 2) * -1
        x1, y1 = self.x, self.y
        x2, y2 = x1 + dx, y1 + dy
        return not self.world.crash(x1, y1, x2, y2)

    def back_is_clear(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        d = self.d / 90
        d = (d + 2) % 4
        dx = (d + 1) % 2 * (d - 1) * -1
        dy = d % 2 * (d - 2) * -1
        x1, y1 = self.x, self.y
        x2, y2 = x1 + dx, y1 + dy
        return not self.world.crash(x1, y1, x2, y2)

    def facing_north(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return self.d == 90

    def facing_south(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return self.d == 270

    def facing_east(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return self.d == 0

    def facing_west(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return self.d == 180

    def next_to_a_beeper(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return self.world.is_beeper(self.x, self.y)

    def next_to_a_robot(self):
        if not self.alive:
            raise Exception("Robot has been destroyed.")
        return self.world.count_robots(self.x, self.y) > 1
