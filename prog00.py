from pykarel import *

wld = World("first")
karel = Robot(wld)
karel.move()
karel.pick_beeper()
karel.move()
karel.turn_left()
karel.move()
karel.put_beeper()
karel.move()
karel.turn_left()
karel.turn_left()
wld.mainloop()
