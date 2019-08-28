import pygame
import random



pygame.mixer.init()

pygame.init()

display_width = 500
display_height = 500
win = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption("потом придумаю...")
pygame.mixer.music.load('background.mp3')



usr_width = 60
usr_height = 100
usr_x = display_width - 450
usr_y = display_height - usr_height + 25
clock = pygame.time.Clock()
isJump = False

jumpCount = 30
animCount = 0
img_counter = 0


pause_img = pygame.image.load('pause.png')
cactus_img = pygame.image.load('cactus_1.png'),pygame.image.load('cactus_0.png'),pygame.image.load('cactus_2.png')
cactus_options = [37,440, 37,400, 20,420]

WalkRight = [pygame.image.load('Dino0.png'),pygame.image.load('Dino1.png'),
pygame.image.load('Dino2.png'),pygame.image.load('Dino3.png'),
pygame.image.load('Dino4.png')]

pause = pygame.image.load('pause.png')

class Cactus:
    def __init__ (self,x,y,width,image,speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.image = image
    def move(self):
        if self.x >= - self.width:
            win.blit(self.image,(self.x,self.y))
            self.x -= self.speed
            return True
        else:
            return False
    def return_self(self,radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        win.blit(self.image,(self.x,self.y))
def run_game():
    global isJump
    bg = pygame.image.load('pygame_bg')
    pygame.mixer.music.play(-1)
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            isJump = True

        if keys[pygame.K_ESCAPE]:
            pause()
        if isJump:
            jump()
        win.blit(bg,(0,0))
        draw_array(cactus_arr)
        draw_user()
        if check_collision(cactus_arr):
            pygame.mixer.music.stop()
            game = False
        pygame.display.update()
        clock.tick(100)
    return game_over()
def jump():
    global usr_y,jumpCount,isJump
    if jumpCount >= -30:
        usr_y -= jumpCount // 2.5
        jumpCount -= 1
    else:
        usr_y = 425
        jumpCount = 30
        isJump = False
def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Cactus(display_width + 100,height ,width,img,4))

    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Cactus(display_width + 400,height,width,img,4))

    choice = random.randrange(0,3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Cactus(display_width + 700,height,width,img,4))

def find_radius(array):
    maximum = max(array[0].x, array[1].x,array[2].x)
    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum
    choice = random.randrange(0,5)
    if choice == 0:
        radius += random.randrange(0,15)
    else:
        radius += random.randrange(200,350)
    return radius

def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)
            choice = random.randrange(0,3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]
            cactus.return_self(radius,height,width, img)
def draw_user():
    global img_counter,usr_y
    if img_counter == 25:
        img_counter = 0
    win.blit(WalkRight[img_counter // 5],(usr_x,usr_y - 10,usr_width,usr_height))
    img_counter+= 1

def print_text(message,x,y,font_color = (0,0,0),font_type = "PINGPONG.TTF",font_size = 30):
    font_type = pygame.font.Font(font_type,font_size)
    text = font_type.render(message,True,font_color)
    win.blit(text,(x,y))
def pause():
    paused = True
    pygame.mixer.music.pause()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text("Stopped.Enter to continue",70,250)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False
        pygame.display.update()
        clock.tick(15)
    pygame.mixer.music.unpause()
def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 440:
            if not isJump:
                if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                    return True
            elif jumpCount >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        return True
        else:
            if not isJump:
                if barrier.x <= usr_x + usr_width -  5 <= barrier.x + barrier.width:
                    return True
            elif jumpCount == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                        return True
            elif jumpCount >= -1:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        return True
                else:
                    if usr_y + usr_height - 10 >= barrier.y:
                        if barrier.x <= usr_x <= barrier.x + barrier.width:
                            return True


    return False
def game_over():
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text("Game Over",170,250)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick(15)
while run_game():
    pass
pygame.quit()
quit()

input()
