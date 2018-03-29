
class Ship:

    def __init__(self):
        self.player_pos =  [200, 150,25,25]
        self.health = [5,5]
        self.shield = [3,3]   
        self.char = 1
        self.arrow_pos1 = [250,320]
        self.is_invins = False
        self.timer = 90
        self.cooldown = [25,25]
        self.vel = [0, 0]
        self.direction = 1
        self.bullets = []

    def change_vel(self,leftstick_x,leftstick_y):
        sensitivity = 0.4
        
        if leftstick_x < -sensitivity :
            self.vel[0] = -player_speed
            self.dir = 2
        elif leftstick_x > sensitivity :
            self.vel[0] = player_speed
            self.dir = 4
        else:
            self.vel[0] = 0

        if leftstick_y < -sensitivity :
            self.vel[1] = -player_speed
            self.dir = 1
        elif leftstick_y > sensitivity :
            self.vel[1] = player_speed
            self.dir = 3
        else:
            self.vel[1] = 0

    def heal(self):
        self.health[0] += 1
        if self.health[0] > self.health[1]:
            self.health[0] = self.health[1]

    
