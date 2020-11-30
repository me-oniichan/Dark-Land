import pygame as pg
import random as rn
import sys

pg.init()
pg.mixer.init()

SCREENWIDTH = 400 #WIDTH
SCREENHEIGHT = 600 #HEIGHT
SCREEN = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  #create window

FPS = 32 # FRAMES PER SECOND
CLOCK = pg.time.Clock() # pygame clock

LEFT_MOST = 76  #leftmost postion for player
RIGHT_MOST = 264  #rightmost position for player

LOWEST_ROCK = SCREENHEIGHT - 70

FONT = pg.font.Font("font/chargen.ttf", 30)  #Font to be used
score_font = pg.font.Font("font/chargen.ttf", 20)
over_font = pg.font.Font("font/chargen.ttf", 50)

ret = pg.font.Font("font/chargen.ttf", 20)
message_font = pg.font.SysFont(None, 20)

IMAGES = {
    "entry" : pg.image.load("imgs/entry.png").convert_alpha(),
    "bg" : pg.image.load("imgs/bg.png").convert_alpha(),  #bg image

    "player" : [pg.transform.scale(pg.image.load("imgs/player1.png").convert_alpha(), [32, 40]), #player image
    pg.transform.scale(pg.image.load("imgs/player2.png").convert_alpha(), [33,40])],

    "rock": [pg.transform.scale(pg.image.load("imgs/rock.png").convert_alpha(), (50,50)),
    pg.transform.scale(pg.image.load("imgs/rock2.png").convert_alpha(), (50,50)),
    pg.transform.scale(pg.image.load("imgs/rock3.png").convert_alpha(), (50,50))],

    "bomb" : pg.transform.scale(pg.image.load("imgs/bom.png").convert_alpha(), (13,13)),
    "explosion" : pg.transform.scale(pg.image.load("imgs/explosion.png").convert_alpha(), (70,70)),
    "heart" : pg.transform.scale(pg.image.load("imgs/heart.png").convert_alpha(), (30,30)),
    "tree" : pg.transform.scale(pg.image.load("imgs/tree.png").convert_alpha(), (240, 30)),
    "tree top" : pg.transform.scale(pg.image.load("imgs/tree_top.png").convert_alpha(), (50, 100)),
    "crouch" : pg.transform.scale(pg.image.load("imgs/crouch.png").convert_alpha(), (27, 35)),
    "boat" : pg.transform.scale(pg.image.load("imgs/boat.png").convert_alpha(), [80,80]),
    "paper" : pg.transform.scale(pg.image.load("imgs/paper roll.png").convert_alpha(), [30,30]),
    "message bg" : pg.image.load("imgs/message bg.png").convert_alpha(),
    "message" : pg.transform.scale(pg.image.load("imgs/message.png").convert_alpha(), [360, 450])
}

SOUNDS = {"explosion": pg.mixer.Sound("sound/explosion.wav"),
"fire" : pg.mixer.Sound("sound/fire.wav"),
"damage" : pg.mixer.Sound("sound/damage.wav")
}
chn0 =pg.mixer.Channel(0)
chn1 =pg.mixer.Channel(1)
chn2 = pg.mixer.Channel(2)
SOUNDS["fire"].set_volume(0.2)




#------animation------
text = ["Those bastrads kicked me out",
" even when i was not imposter!!!",
"They will pay for it someday",
"Now what should I do?",
"Ah there's a paper let's see whats in it "]

def animation():
    playerx = SCREENWIDTH + 15
    playery = 570
    boatx = SCREENWIDTH
    boaty = 545
    for i in range(80):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        boatx -= 1
        playerx-=1
        boaty-=3
        playery-=3

        SCREEN.blit(IMAGES["bg"], [0,0])
        SCREEN.blit(IMAGES["paper"], [300, 400])
        SCREEN.blit(IMAGES["boat"], [boatx, boaty])
        SCREEN.blit(IMAGES["player"][0], [playerx, playery])
        pg.display.update()
        CLOCK.tick(FPS)

    msg = 0
    for i in range(100*5-1):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if (i+1)%100 == 0:
            msg+=1
        message  =message_font.render(text[msg], True, (13, 13, 13))
        SCREEN.blit(IMAGES["message bg"], [0,SCREENHEIGHT-50])
        SCREEN.blit(message, [10, SCREENHEIGHT-40])
        pg.display.update()
        CLOCK.tick(FPS)

    SCREEN.blit(IMAGES["bg"], [0,0])
    SCREEN.blit(IMAGES["boat"], [boatx, boaty])
    SCREEN.blit(IMAGES["player"][0], [playerx, playery])

    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_RETURN:
                    return
        
        SCREEN.blit(IMAGES["message"], [25, 80])        
        pg.display.update()
        CLOCK.tick(FPS)
    
#---entry-----
def entry():
    SCREEN.blit(IMAGES["entry"], [0,0])
    pg.display.update()
    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_RETURN:
                    return




#=---rects for different sprites----- 

bomb_rect = IMAGES["bomb"].get_rect()
rock_rect = IMAGES["rock"][0].get_rect()
player_rect = IMAGES["player"][0].get_rect()
explode_rect = IMAGES["explosion"].get_rect()
tree_rect = IMAGES["tree"].get_rect()
bullet_limit = 6

demo_rect = pg.Rect(0,0,65,55)
rock_demo = pg.Rect(0,0,50, 40) 
tree_demo = pg.Rect(0,0,240, 20)


def get_rock():
    ''' This function returns positojn of new rocks'''
    rock_type = rn.randint(0, 2)
    rock_x = rn.randint(76, 214)
    rock_initial = -60
    return [rock_x, -60, rock_type, True]    

def get_bomb(player_x):
    '''adds one more bomb on firing''' 
    Bomby = SCREENHEIGHT -110
    Bombx = player_x + 15
    return [Bombx, Bomby]


def replace(list_, element, new_val):
    for item in list_:
        if item == element:
            index = list_.index(item)
            list_[index] = new_val
            return list_
    return list_

def game_loop():
    '''This Function runs main game continusly and resets after player get out '''
    VEL_Y = 5  # velocity in y direction
    VEL_X = 5  # velocity in x direction
    bg = [[0,0], [0, -SCREENHEIGHT]]  #list to move bg later

    PLAYERX = int(SCREENWIDTH/2)
    PLAYERY = SCREENHEIGHT-100

    CROUCH = False
    HEALTH = 3
    rock_miss = 3
    SCORE = 0
    MOVE = False #true when left or right key is pressed

    varx = 1  #game specific variable
    step = 0  #tracks steps of player
    rocks = []
    rocks.append(get_rock())

    bombs = []
    explosion = []
    trees = []

    while True:  #runs game constantly
        for ev in pg.event.get():
            if ev.type == pg.QUIT:  #if user close game
                return 1

            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_LEFT:
                    if PLAYERX >= LEFT_MOST: #keep player inside play area
                        MOV_X = -VEL_X   #Movement in left direction
                        MOVE = True

                elif ev.key == pg.K_RIGHT:
                    if PLAYERX <= RIGHT_MOST: #keeps player in play area
                        MOV_X = VEL_X  # moverment in right direction
                        MOVE = True  #makes side movement true

                elif ev.key == pg.K_LSHIFT:
                    if CROUCH:
                        CROUCH = False
                    else:
                        CROUCH = True

                elif ev.key == pg.K_SPACE:  #adds bomb on hitting space
                    if not CROUCH:
                        chn0.play(SOUNDS["fire"])
                        if len(bombs) < bullet_limit+1:    #allows only 10 bullets at a time
                            bombs.append(get_bomb(PLAYERX))

            elif ev.type == pg.KEYUP:
                if ev.key == pg.K_LEFT or ev.key == pg.K_RIGHT:
                    MOVE = False #stops side movement

        #----player--------
        if MOVE: #if user key is pressed to move
            PLAYERX+=MOV_X  #changes players x postion
            if LEFT_MOST > PLAYERX or RIGHT_MOST < PLAYERX:
                MOVE = False

        #-------generate rocks---------
        rock_time = rn.randint(30, 50) #trandomize rock apearence
        if varx%rock_time == 0:  #generate new rock
            rocks.append(get_rock())

        #----generate tree---------
        # tree_time = 100
        if varx% 150  == 0:
            trees.append([75, -60, True])

        player_rect.topleft = (PLAYERX, PLAYERY) #player rectangle box


        #----rocks-----------------
        if rocks:    #removes rock if got out of screen 
            if rocks[0][1] > SCREENHEIGHT:
                rock_miss-=1
                rocks.pop(0)

        for i in range(len(rocks)): #moves rock downward
            rocks[i][1]+=VEL_Y

        #--------trees------
        if trees:
            if trees[0][1] > SCREENHEIGHT:
                trees.pop(0)

        for i in range(len(trees)):  #move tree down
            trees[i][1]+=VEL_Y



        #--------Bomb------
        for i in range(len(bombs)):
            bombs[i][1]-=9  #moves bomb

        for i in range(len(bombs)):
            if bombs[i][1] < -10:
                bombs.pop(i)  #removes bomb which left screen
                break



        #-----background---------
        if bg[0][1] == SCREENHEIGHT:  # Checks if 1st background is out of screen
            bg.pop(0)                 #if yes then remove it
            bg.append([0,-SCREENHEIGHT])

        for i in range(len(bg)):  #moves background
            bg[i][1]+=VEL_Y


        if varx%5 == 0:  #changes step of player
            if step == 1:
                step = 0
            else:
                step = 1

        #---------explosion check---------
        for bomb in bombs:
            bomb_rect.topleft = (bomb[0], bomb[1])
            for rock in rocks:
                rock_rect.topleft = (rock[0], rock[1])
                if bomb_rect.colliderect(rock_rect):
                    chn1.play(SOUNDS["explosion"])
                    explosion.append([rock[0], rock[1], 20, True])
                    bombs.remove(bomb)
                    rocks.remove(rock)
                    SCORE += 1
                    

        for i in range(len(explosion)):  #moves explosion
            explosion[i][1]+=VEL_Y

        #-----game over condtion------
        player_rect.topleft  = (PLAYERX, PLAYERY)

        for explode in explosion:  #check if explosion hit player
            explode_rect.topleft = (explode[0], explode[1]) #if player comes in contact of explosion
            cords = explode_rect.midtop
            demo_rect.midtop = cords
            if player_rect.colliderect(demo_rect):
                if explode[3]:
                    chn2.play(SOUNDS["damage"])
                    HEALTH-=1
                    explosion = replace(explosion, explode, [explode[0], explode[1], explode[2], False])
                break

        for rock in rocks:
            rock_rect.topleft = (rock[0], rock[1])
            cords = rock_rect.midtop
            rock_demo.midtop = cords
            if rock_demo.colliderect(player_rect):
                if rock[3]:
                    chn2.play(SOUNDS["damage"])
                    HEALTH-=1
                    rocks = replace(rocks, rock, [rock[0], rock[1], rock[2], False])
                break

        if not CROUCH:
            for tree in trees:
                if tree[2]:
                    tree_rect.topleft = (tree[0], tree[1])
                    cords = tree_rect.midtop
                    tree_demo.midtop = cords
                    if tree_demo.colliderect(player_rect):
                        chn2.play(SOUNDS["damage"])
                        HEALTH-=1
                        trees = replace(trees, tree, [tree[0], tree[1], False])


        varx+=1
        ammo = bullet_limit - len(bombs)  #ammo display
        ammo_text = FONT.render(str(ammo), True, (255,255,0))

        heart = FONT.render(str(HEALTH), True, (255, 0, 0))

        rock_text = FONT.render(f"{str(3 - rock_miss)}/3", True, (170,170,170))

        score = score_font.render(f"Score: {str(SCORE)}", True, (255, 100, 100))

        #--------Biliting------------
        for x,y in bg:      #blits bg
            SCREEN.blit(IMAGES["bg"], [x,y])
        
        if CROUCH:
            SCREEN.blit(IMAGES["crouch"], [PLAYERX, PLAYERY])
        else:
            SCREEN.blit(IMAGES["player"][step], [PLAYERX, PLAYERY])

        for rock in rocks:
            SCREEN.blit(IMAGES["rock"][rock[2]], [rock[0], rock[1]])

        for tree in trees:
            SCREEN.blit(IMAGES["tree"], [tree[0], tree[1]])
            SCREEN.blit(IMAGES["tree top"], [tree[0] - 30, tree[1]-25])
        
        for bomb in bombs:
            SCREEN.blit(IMAGES["bomb"], bomb)
        
        for explode in explosion:
            if explode[2] == 0:
                explosion.remove(explode) #removes explosion when their time ends
            explosion = replace(explosion, explode, [explode[0], explode[1], explode[2]-1, explode[3]])
            SCREEN.blit(IMAGES["explosion"], [explode[0], explode[1]])



        SCREEN.blit(pg.transform.scale(IMAGES["bomb"], [30,30]), [10,10])
        SCREEN.blit(ammo_text, [60, 10])

        SCREEN.blit(IMAGES["heart"], [10, 45])
        SCREEN.blit(heart, [60, 45])

        SCREEN.blit(pg.transform.scale(IMAGES["rock"][0], [30,30]), [10,80])
        SCREEN.blit(rock_text, [60, 80])

        SCREEN.blit(score, [SCREENWIDTH-160, 10])


        if HEALTH <=0 or rock_miss <= 0: #if health gets 0 or missed 3 rocks
            game_over = over_font.render("Game Over", True, (20, 180, 10))
            SCREEN.blit(game_over, [85,250])
            SCREEN.blit(score, [150, 310])
            pg.display.update()    #update disaply    
            return
            

        pg.display.update()    #update disaply    
        CLOCK.tick(FPS)        #fps for game

def end_game():
    over = ret.render("Press Return to play again", True, (180, 50, 50))
    SCREEN.blit(over, [50, 350])
    pg.display.update()
    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_RETURN:
                    return
        CLOCK.tick(FPS)

with open("times.dat", "r+") as f:
    time = int(f.read())
    f.seek(0)
    f.truncate()
    count = time+1
    f.write(str(count))

if time == 0:
    animation()
entry()
while True:
    game_loop()    
    end_game()
              
pg.quit()
sys.exit()