# Imports
import pygame
import intersects
import xbox360_controller

# Initialize game engine
pygame.init()


# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Maze"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

#controller object
my_controller = xbox360_controller.Controller(0)
# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,205)

#sounds
coin = pygame.mixer.Sound('sounds/coin.ogg')
track = 'sounds/soundtrack.ogg'
smooth = 'sounds/smooth.ogg'

#pics
space = pygame.image.load('pictures/space.png')
black_space = pygame.image.load('pictures/black_space.jpg')
potion = pygame.image.load('pictures/potion.png')
shield = pygame.image.load('pictures/shield.png')

ship_1 = pygame.image.load('pictures/craft1.png')
ship_2 = pygame.transform.rotate(ship_1, 90)
ship_3 = pygame.transform.rotate(ship_2, 90)
ship_4 = pygame.transform.rotate(ship_3, 90)

frames1 = [ship_1, ship_2, ship_3, ship_4]

craft_1 = pygame.image.load('pictures/ship1.png')
craft_2 = pygame.transform.rotate(craft_1, 90)
craft_3 = pygame.transform.rotate(craft_2, 90)
craft_4 = pygame.transform.rotate(craft_3, 90)

frames2 = [craft_1,craft_2, craft_3, craft_4]

one = pygame.image.load('pictures/one.png')
two = pygame.image.load('pictures/two.png')
three = pygame.image.load('pictures/three.png')
fight = pygame.image.load('pictures/fight.png')

count = [one,two,three]

icon1 = pygame.image.load('pictures/icon1.png')

#player1
player1 =  [200, 150,25,25]
health1 = [5,5]
shield1 = [3,3]
char1 = 1
arrow_pos1 = 250
invins1 = False
timer1 = 90
vel1 = [0, 0]
dir1 = 1
bullets1 = []
ammo1 = 1
p1_fired = False

#player2
player2 = [250, 150, 25, 25]
health2 = [5,5]
shield2 = [3,3]
char2 = 1
arrow_pos2 = 250
invins2 = False
timer2 = 90
vel2 = [0, 0]
dir2 = 1
bullets2 = []
ammo2 = 10
p2_fired = False

player_speed = 5

# make walls
wall1 =  [0, 0, 25, 600]
wall2 =  [0, 0, 800, 25]
wall3 =  [775, 0, 25, 600]
wall4 = [0,575,800,25]
wall5 = [300,250,250,25]
wall6 = [550,250,25,251]
wall7 = [300,500,275,25]
wall8 = [300,100,25,100]
wall9 = [150, 100, 400, 25]
wall10 = [150,100,25,400]

walls = [wall1,wall2, wall3,wall4,wall5,wall6,wall7,wall8,wall9,wall10]

# Make potions
pot1 = [300, 475,25,25]
pot2 = [400, 200,25,25]
pot3 = [100, 150,25,25]

pots = [pot1, pot2, pot3]

#make shields
s1 = [450,400,40,40]
s2 = [650,400,40,40]

shields = [s1,s2]

# Game loop
win = False
done = False

'''functions for the game'''
def title_screen():
    font = pygame.font.Font(None, 45)
    screen.blit(black_space,[0,0])
    s1 = font.render("Welcome to Space Wars",1,GREEN)
    s2 = font.render("Player1: Arrow keys to move, 'ctr' to shoot",1,GREEN)
    s3 = font.render("Player2: 'w','a','s','d' to move, 'e' to shoot",1,GREEN)
    s4 = font.render("Press 'back' when ready!",1,GREEN)
    screen.blit(s1,[(WIDTH//2) - ((s1.get_width())//2),100])
    screen.blit(s2,[(WIDTH//2) - ((s2.get_width())//2),300])
    screen.blit(s3,[(WIDTH//2) - ((s3.get_width())//2),400])
    screen.blit(s4,[(WIDTH//2) - ((s4.get_width())//2),500])

def char_selection_screen():
    screen.blit(black_space, [0,0]) 
    
    font = pygame.font.Font(None, 45)
    s1 = font.render("Choose Your Player!",1,GREEN)
    s2 = font.render("Press 'start' to continue!",1,GREEN)
    screen.blit(s1,[(WIDTH//2) - ((s1.get_width())//2),100])
    screen.blit(s2,[(WIDTH//2) - ((s2.get_width())//2),500])
    
    ship_sprite1  = pygame.transform.scale2x(ship_1)
    ship_sprite2 = pygame.transform.scale2x(craft_1)
     
    screen.blit(ship_sprite1, [200,200])
    screen.blit(ship_sprite2, [500,200])

def char_lockin(arrow_pos):
    if arrow_pos == 250:
        return 1
    if arrow_pos == 550:
        
        return 2

def play_song(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)

def draw_arrow(x,y,player):
    if player == 1:
        pygame.draw.rect(screen, RED, [x,y,5,15])
    else:
        pygame.draw.rect(screen, GREEN, [x,y,5,15])
    
def end_screen(health1):
    font = pygame.font.Font(None, 45)
    
    winner = "Player1"
    if health1[0] <= 0:
        winner = "Player2"
    
    s2 = font.render(winner + " wins!",1,GREEN)
    screen.blit(s2,[(WIDTH//2) - ((s2.get_width())//2),250])
    s1 = font.render("Press 'start' to play again",1,GREEN)
    screen.blit(s1,[(WIDTH//2) - ((s1.get_width())//2),300])
        
def shoot(player,bullets,direc,ammo):
    if len(bullets) < ammo: 
        b_vel = [0,-24]
        shape = [5,15]
        x = player[0]
        y = player[1]
        
        if direc == 2:
            b_vel = [-24,0]
            shape = [15,5]
            y += 17
        elif direc == 3:
            b_vel = [0,24]
            x += 17
        elif direc == 4:
            b_vel = [24,0]
            shape = [15,5]
            y += 17
        else:
            x += 17
               
        bullets.append( [x, y, shape[0], shape[1], b_vel] )

def draw_bullet(x,y,l,w):
    pygame.draw.rect(screen, GREEN, [x,y,l,w])

def get_frame_list(char):
    if char == 1:
        return frames1
    if char == 2:
        return frames2

def get_frame(direc,frames):
    
    if direc == 1:
        frame = frames[0]
    if direc == 2:
        frame = frames[1]
    elif direc == 3:
        frame = frames[2]
    elif direc == 4:
        frame = frames[3]

    return frame

def edge_detect(player):
    left = player[0]
    right = player[0] + player[2]
    top = player[1]
    bottom = player[1] + player[3]
    
    if left > WIDTH:
        player[0] = 0 - player[2]
    elif right < 0:
        player[0] = WIDTH
                
    if bottom < 0:
        player[1] = HEIGHT
    elif top > HEIGHT:
        player[1] = 0 - player[3]

def collect_pot(hit_list,health):
    for hit in hit_list:
        if health[0] != health[1]:
            pots.remove(hit)
            heal(health)
            coin.play()

def collect_shield(shield_list, shield):
    for collect in shield_list:
        if shield[0] != shield[1]:
            shields.remove(collect)
            shield[0] = shield[1]
            
def move_bullets(bullets):
    for bullet in bullets:
        b_vel = bullet[4]
        
        bullet[0] += b_vel[0]
        bullet[1] += b_vel[1]

    for w in walls:
        for b in bullets:
            if intersects.rect_rect(b,w):
                bullets.remove(b)

def draw_bullets(bullets):
    for b in bullets:
        draw_bullet(b[0],b[1],b[2],b[3])
        
        if b[0] < -10 or b[0] > 800 \
           or b[1] < -10 or b[1] > 600:
            bullets.remove(b)

def health_bar(x,health,shield):
    current_health = health[0]
    max_health = health[1]
    
    current_shield = shield[0]
    max_shield = shield[1]
    
    percent_health = current_health/max_health
    percent_shield = current_shield/max_shield
    
    pygame.draw.rect(screen, GREEN, [x,8,percent_health*160,15])
    pygame.draw.rect(screen, BLUE, [x,8,percent_shield*160,15])

    #border
    pygame.draw.rect(screen, BLACK, [x + 160,8,2,15])
    pygame.draw.rect(screen, BLACK, [x,21,160,2])
    pygame.draw.rect(screen, BLACK, [x,8,160,2])
    pygame.draw.rect(screen, BLACK, [x - 1,8,3,15])

    
def heal(health):
    health[0] += 1
    if health[0] > health[1]:
        health[0] = health[1]

def setup(health1,health2):
    global stage,tick
    stage = CHAR_SELECT
    tick = 0
    
    health1[0] = health1[1]
    health2[0] = health2[1]

    shield1[0] = shield1[1]
    shield2[0] = shield2[1]

    player1[0],player1[1] = 50,50
    player2[0],player2[1] = 675,200

    vel1[0],vel1[1] = 0,0
    vel2[0],vel2[1] = 0,0

    
CHAR_SELECT = 0
START = 1
COUNT_DOWN = 2
PLAYING = 3
END = 4

setup(health1,health2)
play_song(smooth)

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        #fires lazer
        elif event.type == pygame.KEYDOWN:
            if stage == PLAYING:
                if event.key == pygame.K_e:
                    p2_fired = True

                
    pressed = pygame.key.get_pressed()
    xbox = my_controller.get_buttons()
    
    if xbox[xbox360_controller.A]:
        p1_fired = True
    lt_x, lt_y = my_controller.get_left_stick()
    start = xbox[xbox360_controller.START]
    select = xbox[xbox360_controller.BACK]

    up2 = pressed[pygame.K_w]
    down2 = pressed[pygame.K_s]
    left2 = pressed[pygame.K_a]
    right2 = pressed[pygame.K_d]
    

    '''controls while game is playing'''        
    if stage == PLAYING:
        #shoots bullet
        if p1_fired:
            shoot(player1,bullets1,dir1,ammo1)
            p1_fired = False

        if p2_fired:
            shoot(player2,bullets2,dir2,ammo2)
            p2_fired = False
        
        #player 1 move
        if lt_x < 0:
            vel1[0] = -player_speed
            dir1 = 2
        elif lt_x > 0:
            vel1[0] = player_speed
            dir1 = 4
        else:
            vel1[0] = 0

        if lt_y < 0:
            vel1[1] = -player_speed
            dir1 = 1
        elif lt_y > 0:
            vel1[1] = player_speed
            dir1 = 3
        else:
            vel1[1] = 0
        
        
        #player2 move
        if left2:
            vel2[0] = -player_speed
            dir2 = 2
        elif right2:
            vel2[0] = player_speed
            dir2 = 4
        else:
            vel2[0] = 0
        
        if up2:
            vel2[1] = -player_speed
            dir2 = 1
        elif down2:
            vel2[1] = player_speed
            dir2 = 3
        else:
            vel2[1] = 0
        
    #move bullets
    move_bullets(bullets1)
    move_bullets(bullets2)

    #setting the frame of the ship
    frame_list1 = get_frame_list(char1)
    frame_list2 = get_frame_list(char2)
    
    frame1 = get_frame(dir1,frame_list1)
    frame2 = get_frame(dir2,frame_list2)
        
    #updates the dimension of hit box based off of frame
    player1[2] = frame1.get_width()
    player1[3] = frame1.get_height()

    player2[2] = frame2.get_width()
    player2[3] = frame2.get_height()
    
    ''' move the player in horizontal direction '''
    player1[0] += vel1[0]
    player2[0] += vel2[0]
    
    ''' resolve collisions horizontally '''
    for w in walls:
        
        if intersects.rect_rect(player1, w):        
            if vel1[0] > 0:
                player1[0] = w[0] - player1[2]
            elif vel1[0] < 0:
                player1[0] = w[0] + w[2]
                
        if intersects.rect_rect(player2, w):        
            if vel2[0] > 0:
                player2[0] = w[0] - player2[2]
            elif vel2[0] < 0:
                player2[0] = w[0] + w[2]
                
    ''' move the player in vertical direction '''
    player1[1] += vel1[1]
    player2[1] += vel2[1]
    
    ''' resolve collisions vertically '''
    for w in walls:
        
        if intersects.rect_rect(player1, w):                    
            if vel1[1] > 0:
                player1[1] = w[1] - player1[3]
            if vel1[1]< 0:
                player1[1] = w[1] + w[3]
                
        if intersects.rect_rect(player2, w):                    
            if vel2[1] > 0:
                player2[1] = w[1] - player2[3]
            if vel2[1]< 0:
                player2[1] = w[1] + w[3]
                

    ''' here is where you should resolve player collisions with screen edges '''
    #edge detection
    edge_detect(player1)
    edge_detect(player2)
                
    #hit list of the players
    pot_list1 = [p for p in pots if intersects.rect_rect(player1, p)]
    pot_list2 = [p for p in pots if intersects.rect_rect(player2, p)]
    
    collect_pot(pot_list1,health1)
    collect_pot(pot_list2,health2)
        
    #strike list, detects players collisions with bullets
    strikes1 = [s for s in bullets2 if intersects.rect_rect(player1,s)]
    strikes2 = [s for s in bullets1 if intersects.rect_rect(player2,s)]

    #hit list of the shields
    shield_list1 = [s for s in shields if intersects.rect_rect(player1, s)]
    shield_list2 = [s for s in shields if intersects.rect_rect(player2, s)]

    collect_shield(shield_list1,shield1)
    collect_shield(shield_list2,shield2)


    #checks if player is invinsible and reduces invinsibility timer
    if invins1:
        timer1 -= 1
        
        if timer1 == 0:
            invins1 = False
            timer1 = 90

    if invins2:
        timer2 -= 1
        
        if timer2 == 0:
            invins2 = False
            timer2 = 90

    #damages player if collides with bullet
    for s in strikes1:
        if not invins1:
            if shield1[0] > 0:
                shield1[0] -= 1
            else:
                health1[0] -= 1
            invins1 = True
    
    for s in strikes2:
        if not invins2:
            if shield2[0] > 0:
                shield2[0] -= 1
            else:
                health2[0] -= 1
            invins2 = True

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    screen.blit(space,[0,0])

    #draw bullets
    draw_bullets(bullets1)
    draw_bullets(bullets2)

    #draw walls
    for w in walls:
        pygame.draw.rect(screen, RED, w)

    #draw coins
    for p in pots:
        screen.blit(potion, [p[0],p[1]])

    #draw shields
    for s in shields:
        screen.blit(shield, [s[0],s[1]])

    #draw players
    screen.blit(frame1, [player1[0],player1[1]])
    screen.blit(frame2, [player2[0],player2[1]])

    #display score
    font = pygame.font.Font(None, 25)
    
    s1 = font.render("Player1: ",1,GREEN)
    screen.blit(s1,[20,8])

    s2 = font.render("Player2: " ,1,GREEN)
    screen.blit(s2,[480,8])

    #dispalys health bars
    health_bar(100,health1,shield1)
    health_bar(560,health2,shield2)

    if health1[0] == 0 or health2[0] == 0:
        stage = END
        
    '''character selection screen'''
    if stage == CHAR_SELECT:
        char_selection_screen()
        draw_arrow(arrow_pos1,320,1)
        draw_arrow(arrow_pos2,345,2)

        if lt_x > 0:
            if arrow_pos1 < 550:
                arrow_pos1 += 300
        if lt_x < 0:
            if arrow_pos1 > 250:
                arrow_pos1 -= 300
        if right2:
            if arrow_pos2 < 550:
                arrow_pos2 += 300
        if left2:
            if arrow_pos2 > 250:
                arrow_pos2 -= 300

        char1 = char_lockin(arrow_pos1)
        char2 = char_lockin(arrow_pos2)
                
        if start:
            stage = START
            
    '''intro stage'''
    if stage == START:
        title_screen()
        if select:
            stage = COUNT_DOWN

    '''count down stage'''
    if stage == COUNT_DOWN:
        sec = tick/60
           
        if sec <= 1:
            screen.blit(three,[WIDTH//2 - 100,200])
        elif sec > 1 and sec <= 2:
            screen.blit(two,[WIDTH//2 - 100,200])
        elif sec > 2 and sec <= 3:
            screen.blit(one,[WIDTH//2 - 100,200])
        elif sec > 3 and sec <= 4:
            screen.blit(fight,[WIDTH//2 - 200,200])
        elif sec > 4:
            stage = PLAYING

        tick += 1
        
    '''ending stage'''
    if stage == END:
        end_screen(health1)
        if start:
            setup(health1,health2)
    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)

# Close window and quit
pygame.quit()
