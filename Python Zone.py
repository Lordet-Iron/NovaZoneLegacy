import pygame
import math
import sys
import random
pygame.init()
pygame.font.init()
windowX = 1920
windowY = 1080
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Nova Zone")

# Assets
bg = pygame.image.load("Space.png")
HEALTH = pygame.image.load("Health.png")
HEALTH = pygame.transform.scale(HEALTH, (25, 25))
fighter = pygame.image.load('Space fighter.png')
fighter = pygame.transform.scale(fighter, (84, 50))
INTERCEPTOR1 = pygame.image.load("Kamo 1.png")
INTERCEPTOR1 = pygame.transform.scale(INTERCEPTOR1, (50, 50))
INTERCEPTOR2 = pygame.image.load("Kamo 2.png")
INTERCEPTOR2 = pygame.transform.scale(INTERCEPTOR2, (70, 70))
CARRIER = pygame.image.load("Kamo 4.png")
CARRIER = pygame.transform.scale(CARRIER, (200, 150))
TURRET = pygame.image.load("Kamo Turret.png")
TURRET = pygame.transform.scale(TURRET, (100, 50))
UBER = pygame.image.load("Carrier 1.png")
UBER = pygame.transform.scale(UBER, (70, 70))

KLUX3 = pygame.image.load("Space fighter 3.png")
KLUX3= pygame.transform.scale(KLUX3, (200, 150))
KLUX4 = pygame.image.load("Space fighter 4.png")
KLUX4= pygame.transform.scale(KLUX4, (50, 50))
KLUX5 = pygame.image.load("Space Turret.png")
KLUX5 = pygame.transform.scale(KLUX5, (100, 50))
phaser = pygame.image.load("Phaser.png")
phaser = pygame.transform.scale(phaser, (25, 25))


Title = pygame.font.SysFont('Comic Sans MS', 100)
Text = pygame.font.SysFont('Comic Sans MS', 30)

# Colours
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
clock = pygame.time.Clock()
phasers = []

# Sounds
FIGHTERTHUD = pygame.mixer.Sound("Thud.wav")
FIGHTERTHUD.set_volume(0.1)
PLAYERPHASER = pygame.mixer.Sound("Phaser.wav")
PLAYERPHASER.set_volume(0.1)
DARKMATTER = pygame.mixer.Sound("Matter Drive.wav")
DARKMATTER.set_volume(0.1)
POWER1 = pygame.mixer.Sound("Power 1.wav")
DARKMATTER.set_volume(0.2)

# PLAYER
class player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.fire = 0
        self.clip = 5
        self.radius = 22
        self.health = 100
        self.maxhealth = 100
        self.accuracy = 10
        self.ammo = 20
        self.maxammo = 20
        self.team = 1

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.fire = 0
        self.clip = 5
        self.radius = 22  # 22
        if difficulty == 0:
            self.health = 200
        if difficulty == 1:
            self.health = 100
        if difficulty == 2:
            self.health = 50
        self.accuracy = 10
        self.ammo = 20
        self.maxammo = 20


    def draw(self):
        # Calculating how we move the image using velocity and angle
        x = self.x + math.cos(math.radians(self.angle)) * self.velocity
        y = self.y - math.sin(math.radians(self.angle)) * self.velocity
        if x < 1900 and x > 20:
            self.x = x
        if y < 1060 and y > 20:
            self.y = y


        #pygame.draw.rect(window, Red, (self.x,self.y,50,50))
        fighter = pygame.image.load('Space fighter.png')
        fighter = pygame.transform.scale(fighter, (60, 50))  # 60 50
        fighter = pygame.transform.rotate(fighter, self.angle)
        # New hitbox
        #pygame.draw.circle(window, Red, (int(self.x), int(self.y)),self.radius)  # Create a circle to act as hitbox
        window.blit(fighter, (self.x - int(fighter.get_width() / 2), self.y - int(fighter.get_height() / 2)))  # Set the center of the image


        # Ammo System
        if self.ammo < self.maxammo:
            self.ammo += 0.1

        # Stat Bars
        pygame.draw.rect(window, (0, 255, 0), (20, 1060, (1000 * player.health / 100), 3))
        pygame.draw.rect(window, (0, 0, 235), (20, 1070, (1000 * player.ammo / player.maxammo), 3))

        if self.health > self.maxhealth:
            self.health = self.maxhealth

    def hit(self, damage):
        self.health -= damage




# Phaser 1
class phaser(object):
    def __init__(self, x, y, angle, team, damage, name, radius):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = 13
        self.radius = radius  # 8
        self.damage = damage
        self.team = team
        self.name = name


    def draw(self):
        self.x += math.cos(math.radians(self.angle)) * self.velocity
        self.y -= math.sin(math.radians(self.angle)) * self.velocity
        if self.name == "Phaser":
            phaser = pygame.image.load('Phaser.png')
            phaser = pygame.transform.rotate(phaser, self.angle)
        elif self.name == "Health":
            phaser = pygame.image.load('Health.png')
            phaser = pygame.transform.scale(HEALTH, (25, 25))
            phaser = pygame.transform.rotate(phaser, self.angle)
            self.velocity = 0
        #pygame.draw.circle(window, Green, (int(self.x), int(self.y)), self.radius)  # Hitbox
        window.blit(phaser, (self.x - int(phaser.get_width() / 2), self.y - int(phaser.get_height() / 2)))

class thud(object):
    def __init__(self, x, y, angle, team):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = 13
        self.radius = 8
        self.damage = 5
        self.team = team


    def draw(self):
        self.x += math.cos(math.radians(self.angle)) * self.velocity
        self.y -= math.sin(math.radians(self.angle)) * self.velocity
        phaser = pygame.image.load('Thud.png')
        phaser = pygame.transform.rotate(phaser, self.angle)
        #pygame.draw.circle(window, Green, (int(self.x), int(self.y)), self.radius)  # Hitbox
        window.blit(phaser, (self.x - int(phaser.get_width() / 2), self.y - int(phaser.get_height() / 2)))

class dark_matter(object):
    def __init__(self, x, y, angle, team, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.velocity = 13
        self.radius = 8
        self.damage = damage
        self.team = team


    def draw(self):
        self.x += math.cos(math.radians(self.angle)) * self.velocity
        self.y -= math.sin(math.radians(self.angle)) * self.velocity
        phaser = pygame.image.load('Matter.png')
        phaser = pygame.transform.rotate(phaser, self.angle)
        #pygame.draw.circle(window, Green, (int(self.x), int(self.y)), self.radius)  # Hitbox
        window.blit(phaser, (self.x - int(phaser.get_width() / 2), self.y - int(phaser.get_height() / 2)))

class NPC(object):
    def __init__(self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
        self.x = x
        self.y = y
        self.angle = 0
        self.velocity = 0
        self.fire = 0
        self.clip = clip  # 5
        self.radius = radius  # 26
        self.health = health  # 20
        self.maxhealth = health
        self.target = self.angle
        self.accuracy = accuracy
        self.ammo = ammo
        self.maxammo = ammo
        self.angleB = self.angle
        self.skin = skin
        self.name = str(name)
        self.speed = speed
        self.hitlist = "none"
        self.team = team
        self.spawn = 25564
        self.master = master
        self.energy = 0

        if self.team == 2:
            self.angle = 180

        # The elements in the hitbox are (top left x, top left y, width, height)

    def draw(self):
        # Calculating how we move the image using velocity and angle
        x = self.x + math.cos(math.radians(self.angle)) * self.velocity
        y = self.y - math.sin(math.radians(self.angle)) * self.velocity
        if self.x > x and x > 20:  # Locks fighters inside the window (Requires a change in the self.x calc)
            self.x = x
        elif self.x < x and x < 1900:  # Locks fighters inside the window (Requires a change in the self.x calc)
            self.x = x
        if self.y > y and y > 20:
            self.y = y
        elif self.y < y and y < 1060:
            self.y = y

        # pygame.draw.rect(window, Red, (self.x,self.y,50,50))
        skin = pygame.transform.rotate(self.skin, self.angle)

        #if self.name == "KTURRET" or self.name == "TURRET":
        #    window.blit(skin, (self.x - int(self.master.skin.get_width() / 2), self.y - int(self.master.skin.get_height() / 2)))  # Set the center of the master to me
        #else:
        window.blit(skin, (self.x - int(skin.get_width() / 2), self.y - int(skin.get_height() / 2)))  # Set the center of the image
        # The elements in the hitbox are (top left x, top left y, width, height)
        #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)  # To draw the hit box around the player # REDACTED
        # New hitbox
        #pygame.draw.circle(window, Red, (int(self.x), int(self.y)), self.radius) # Create a circle to act as hitbox

        # Health bar
        if self.name != "TURRET" and self.name != "KTURRET":
            pygame.draw.rect(window, (0, 255, 0), (int(self.x - 25), int(self.y - 40), (50 * self.health / self.maxhealth), 3))

        # Ammo System
        if self.ammo != self.maxammo:
            self.ammo += 0.1

    def hit(self, damage):
        self.health -= damage

    def ai(self):
        global team1
        global team2

        if self.target - self.accuracy < self.angle < self.target + self.accuracy and team1 != [] and team2 != []:
            if self.fire == self.clip and self.ammo >= 1:
                self.fire = 0
                self.ammo -= 1
                if self.team == 1:
                    Phasers.append(phaser(self.x + 5, self.y, random.randrange((int(self.angle) - int(self.accuracy)), (int(self.angle) + int(self.accuracy))), self.team, 5, "Phaser", 8))
                    PLAYERPHASER.play()
                elif self.name == "UBER":
                    Phasers.append(dark_matter(self.x + 5, self.y, random.randrange((int(self.angle) - int(self.accuracy)), (int(self.angle) + int(self.accuracy))), self.team, 15))
                    DARKMATTER.play()
                elif self.team == 2:
                    Phasers.append(thud(self.x + 5, self.y, random.randrange((int(self.angle) - int(self.accuracy)), (int(self.angle) + int(self.accuracy))), self.team))
                    FIGHTERTHUD.play()

        if self.fire != self.clip:
            self.fire += 1

        if self.velocity < self.speed and team1 != [] and team2 != [] and self.name != "KTURRET" and self.name != "TURRET":
            self.velocity += 0.2

        if self.name == "KTURRET" or self.name == "TURRET":
            self.x = self.master.x-20
            self.y = self.master.y

        if self.name == "KCARRIER" or self.name == "CARRIER":
            self.spawn += 1

            if self.spawn == 600:
                if self.team == 2:
                    fighters.append(NPC(self.x, self.y, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                if self.team == 1:
                    fighters.append(NPC(self.x, self.y, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))

                team1 = []
                team2 = []
                team1.append(player)

                for i in fighters:
                    if i.team == 1:
                        team1.append(i)
                    elif i.team == 2:
                        team2.append(i)

                self.spawn = 0
            elif self.spawn == 25565:
                if self.team == 1:
                    fighters.append(NPC(self.x + 100, self.y, 5, 1, 20, 10, 10, 4, KLUX5, "KTURRET", self.team, self))
                if self.team == 2:
                    fighters.append(NPC(self.x + 100, self.y, 5, 1, 20, 10, 10, 4, TURRET, "TURRET", self.team, self))

                team1 = []
                team2 = []
                team1.append(player)

                for i in fighters:
                    if i.team == 1:
                        team1.append(i)
                    elif i.team == 2:
                        team2.append(i)
                self.spawn = 0
        if self.name == "UBER":
            self.energy += 1
            if self.health < 400:
                self.energy += 1
            if self.health < 300:
                self.energy += 1
            if self.health < 200:
                self.energy += 1
            if self.health < 100:
                self.energy += 1

            if self.energy >= 1000:
                self.energy -= 1000
                self.velocity += 20 # def __init__(self, x, y, angle, team, damage, name, radius):
                Phasers.append(dark_matter(self.x + 5, self.y, self.target -3 , self.team, 15))
                Phasers.append(dark_matter(self.x + 5, self.y, self.target - 2, self.team, 15))
                Phasers.append(dark_matter(self.x + 5, self.y, self.target, self.team, 15))
                Phasers.append(dark_matter(self.x + 5, self.y, self.target + 2, self.team, 15))
                Phasers.append(dark_matter(self.x + 5, self.y, self.target + 3, self.team, 15))
                POWER1.play()
                self.hitlist = "none"

        if team1 == [] or team2 == []:
            if self.velocity > 0:
                self.velocity -= 0.2
            if self.velocity < 0:
                self.velocity = 0

        if self.velocity > self.speed:
            self.velocity -= 1


        # TURRET PATCH
        if self.name == "KTURRET" or self.name == "TURRET":
            if self.master.health < 1:
                self.health = 0







def redraw():
    window.fill(Black)
    window.blit(bg, (0, 0))
    player.draw()
    for i in fighters:
        i.draw()
        i.ai()

    for i in Phasers: # Phaser Handler
        i.draw()
        # Collision
        for n in fighters:
            bullet = i
            target = n
            if bullet.y - bullet.radius >= target.y - target.radius and bullet.y + bullet.radius <= target.y + target.radius and bullet.team != target.team:  # Checks x coords
                if bullet.x - bullet.radius >= target.x - target.radius and bullet.x + bullet.radius <= target.x + target.radius:  # Checks y coords
                    target.hit(i.damage)  # calls enemy hit method with the damage amount
                    if target.health <= 0:
                        if target.name == "INTERCEPTOR2":  # (self, x, y, angle, team, damage, name):
                            Phasers.append(phaser(target.x, target.y, 0, 2, -50, "Health", 16))
                        elif target.name == "INTERCEPTOR1":  # (self, x, y, angle, team, damage, name):
                            Phasers.append(phaser(target.x, target.y, 0, 2, -10, "Health", 16))
                        elif target.name == "KCARRIER" or "CARRIER":
                            for y in fighters:
                                if y.master != False:
                                    if y.master.health == 0:
                                        try:
                                            if target.team == 1:
                                                team1.pop(team1.index(y))
                                            if target.team == 2:
                                                team2.pop(team2.index(y))
                                            fighters.pop(fighters.index(y))
                                        except ValueError:
                                            print("Things keep happening twice")

                        try:
                            if target.team == 1:
                                team1.pop(team1.index(n))
                            if target.team == 2:
                                team2.pop(team2.index(n))
                            fighters.pop(fighters.index(n))
                        except ValueError:
                            print("Things keep happening twice")


                    try:
                        Phasers.pop(Phasers.index(i))
                        # removes bullet from bullet list
                    except ValueError:
                        print("Something wrong has happened")

        # Player Bullet collision
        bullet = i
        target = player
        if bullet.y - bullet.radius >= target.y - target.radius and bullet.y + bullet.radius <= target.y + target.radius and bullet.team == 2:  # Checks x coords
            if bullet.x - bullet.radius >= target.x - target.radius and bullet.x + bullet.radius <= target.x + target.radius:  # Checks y coords
                target.hit(i.damage)  # calls enemy hit method with the damage amount
                if target.health <= 0:
                    print("LOSE")
                    LOSE = 1
                try:
                    Phasers.pop(Phasers.index(i))  # removes bullet from bullet list
                    # removes bullet from bullet list
                except ValueError:
                    print("Something wrong has happened")

        if i.x > 2000 or i.x < -50:
            try:
                remove = Phasers.index(i)
                Phasers.pop(remove)
            except ValueError:
                print("Something wrong has happened")
        elif i.y > 1300 or i.y < -50:
            try:
                remove = Phasers.index(i)
                Phasers.pop(remove)
            except ValueError:
                print("Something wrong has happened")
    for i in fighters:  # Fighter AI

        if team1 != [] and team2 != [] and i.hitlist == "none":
            if i.team == 2:
                random.shuffle(team1)
                i.hitlist = team1[0]
            if i.team == 1:
                random.shuffle(team2)
                i.hitlist = team2[0]

        if i.hitlist != "none":
            if i.hitlist.health <= 0:
                i.hitlist = "none"
                for z in team1:
                    if z.health <= 0:
                        team1.pop(team1.index(z))
                for x in team2:
                    if x.health <= 0:
                        team2.pop(team2.index(x))

        if i.hitlist != "none":

            # pygame.draw.line(window, Green, (i.x, i.y), (i.x, i.hitlist.y))
            # pygame.draw.line(window, Red, (i.x, i.y), (i.hitlist.x, i.hitlist.y))
            # pygame.draw.line(window, Blue, (i.x, i.hitlist.y), (i.hitlist.x, i.hitlist.y))

            if i.x - i.hitlist.x < 50 or i.x - i.hitlist.x > -50:
                if i.y - i.hitlist.y < 50 or i.y - i.hitlist.y > - 50:
                    if i.hitlist.y > i.y:
                        #pygame.draw.line(window, Green, (i.x, i.y), (i.x, player.y))
                        #pygame.draw.line(window, Red, (i.x, i.y), (player.x, player.y))
                        #pygame.draw.line(window, Blue, (i.x, player.y), (player.x, player.y))
                        if i.hitlist.x >= i.x:
                            a = i.x - i.hitlist.x
                            c = i.hitlist.y - i.y
                            b = a*a + c*c
                            b = math.sqrt(b)  # Found all side lengths
                            A = b*b + c*c - a*a
                            A = A / (2*b*c)
                            A = math.acos(A)
                            A = math.degrees(A)
                            i.target = A + 270

                        if i.hitlist.x <= i.x:
                            a = i.x - i.hitlist.x
                            c = i.hitlist.y - i.y
                            b = a*a + c*c
                            b = math.sqrt(b)
                            A = b*b + c*c - a*a
                            A = A / (2*b*c)
                            A = math.acos(A)
                            A = math.degrees(A)
                            i.target = 270 - A



                    if i.hitlist.y < i.y:
                        #pygame.draw.line(window, Green, (i.x, i.y), (i.x, player.y))
                        #pygame.draw.line(window, Red, (i.x, i.y), (player.x, player.y))
                        #pygame.draw.line(window, Blue, (i.x, player.y), (player.x, player.y))
                        if i.hitlist.x >= i.x:
                            a = i.x - i.hitlist.x
                            c = i.hitlist.y - i.y
                            b = a*a + c*c
                            b = math.sqrt(b)
                            A = b*b + c*c - a*a
                            A = A / (2*b*c)
                            A = math.acos(A)
                            A = math.degrees(A)
                            i.target = A - 90

                        if i.hitlist.x <= i.x:
                            a = i.x - i.hitlist.x
                            c = i.hitlist.y - i.y
                            b = a*a + c*c
                            b = math.sqrt(b)
                            A = b*b + c*c - a*a
                            A = A / (2*b*c)
                            A = math.acos(A)
                            A = math.degrees(A)
                            i.target = 270 - A

                # Fighter Rotation

                if int(i.angle) != int(i.target):
                    #print(int(i.angle), int(i.target))

                    if int(i.angle) >= 360 and int(i.angleB) >= 359:
                        i.angle = 0
                    if i.angle == 0 and i.angleB == 1:
                        i.angle = 360
                    i.angleB = i.angle

                    if 90 > i.angle > 0 and 270 < i.target < 360:
                        i.angle -= i.velocity/4

                        if i.angle <= 0:
                            i.angle = 360
                    elif 90 > i.target > 0 and 270 < i.angle < 360:
                        i.angle += i.velocity/4

                        if i.angle == 360:
                            i.angle = 0

                    elif i.target >= i.angle:
                        i.angle += i.velocity/4

                    elif i.angle > i.target and i.angle - 90 <= int(i.target):
                        i.angle -= i.velocity/4

                    elif i.angle < i.target and i.angle + 50 >= int(i.target):
                        i.angle += i.velocity/4

                    elif 180 > i.target >= 90:
                        i.angle += i.velocity/4

                    elif 360 >= i.target >= 0 and int(i.target) != int(i.angle):
                        i.angle += i.velocity/4

                    elif 270 > i.target >= 180:
                        i.angle += i.velocity/4

                    else:
                        i.angle -= i.velocity/4
                # elif i.target < i.angle:
                #     i.angle -= 1
                #     i.turn = "neg"

                    # print(4)


    pygame.display.update()

Click = False
page = 0
difficulty = 1


def menu():
    global Playing
    global page
    global difficulty
    clock.tick(60)
    window.fill(Black)

    # Controls
    Click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            Click = True

    keys = pygame.key.get_pressed()
    if keys[pygame.MOUSEBUTTONDOWN]:
        Click = True

    if keys[pygame.K_ESCAPE]:
        Playing = False

    mx, my = pygame.mouse.get_pos()

    if page == 0:

        button1 = pygame.Rect(810, 400, 200, 45)
        buttonC1 = (20, 20, 20)
        button2 = pygame.Rect(810, 500, 200, 45)
        buttonC2 = (20, 20, 20)



        if button1.collidepoint((mx, my)):
            buttonC1 = (200, 200, 200)
            if Click:
                Playing = True

        if button2.collidepoint((mx, my)):
            buttonC2 = (200, 200, 200)
            if Click:
                page = 1


        pygame.draw.ellipse(window, buttonC1, button1)
        textsurface = Text.render('PLAY', False, (0, 100, 50))
        window.blit(textsurface, (870, 398))

        pygame.draw.ellipse(window, buttonC2, button2)
        textsurface = Text.render('Options', False, (0, 100, 50))
        window.blit(textsurface, (855, 498))

    elif page == 1:

        button1 = pygame.Rect(810, 400, 200, 45)
        buttonC1 = (20, 20, 20)
        button2 = pygame.Rect(810, 500, 200, 45)
        buttonC2 = (20, 20, 20)
        button3 = pygame.Rect(810, 600, 200, 45)
        buttonC3 = (20, 20, 20)
        button4 = pygame.Rect(810, 700, 200, 45)
        buttonC4 = (20, 20, 20)

        if difficulty == 0:
            buttonC2 = (20, 200, 20)

        elif difficulty == 1:
            buttonC3 = (20, 200, 20)

        elif difficulty == 2:
            buttonC4 = (20, 200, 20)



        if button1.collidepoint((mx, my)):
            buttonC1 = (200, 200, 200)
            if Click:
                page = 0

        elif button2.collidepoint((mx, my)):
            buttonC2 = (200, 200, 200)
            if Click:
                difficulty = 0

        elif button3.collidepoint((mx, my)):
            buttonC3 = (200, 200, 200)
            if Click:
                difficulty = 1

        elif button4.collidepoint((mx, my)):
            buttonC4 = (200, 200, 200)
            if Click:
                difficulty = 2




        pygame.draw.ellipse(window, buttonC1, button1)
        textsurface = Text.render('Back', False, (0, 100, 50))
        window.blit(textsurface, (875, 398))

        pygame.draw.ellipse(window, buttonC2, button2)
        textsurface = Text.render('Easy', False, (0, 100, 50))
        window.blit(textsurface, (875, 498))

        pygame.draw.ellipse(window, buttonC3, button3)
        textsurface = Text.render('Normal', False, (0, 100, 50))
        window.blit(textsurface, (865, 598))

        pygame.draw.ellipse(window, buttonC4, button4)
        textsurface = Text.render('Hard', False, (0, 100, 50))
        window.blit(textsurface, (875, 698))

    elif page == 10:

        button1 = pygame.Rect(810, 400, 200, 45)
        buttonC1 = (20, 20, 20)
        button2 = pygame.Rect(810, 500, 200, 45)
        buttonC2 = (20, 20, 20)

        if button1.collidepoint((mx, my)):
            buttonC1 = (200, 200, 200)
            if Click:
                Playing = True

        if button2.collidepoint((mx, my)):
            buttonC2 = (200, 200, 200)
            if Click:
                page = 0

        pygame.draw.ellipse(window, buttonC1, button1)
        textsurface = Text.render('Resume', False, (0, 100, 50))
        window.blit(textsurface, (860, 398))

        pygame.draw.ellipse(window, buttonC2, button2)
        textsurface = Text.render('Main menu', False, (0, 100, 50))
        window.blit(textsurface, (838, 498))

    elif page == 12:

        button1 = pygame.Rect(810, 400, 200, 45)
        buttonC1 = (20, 20, 20)

        if button1.collidepoint((mx, my)):
            buttonC1 = (200, 200, 200)
            if Click:
                page = 1

        pygame.draw.ellipse(window, buttonC1, button1)
        textsurface = Text.render('VICTORY', False, (0, 100, 50))
        window.blit(textsurface, (860, 398))


    pygame.display.update()


Playing = False
LOSE = 0
phase = 2
player = player(100, 100)
team1 = []
team1.append(player)
team2 = []
fighters = []
Phasers = []

while True:

    while not Playing:
        menu()

        if page == 0:
            phase = 0
            LOSE = 0
            fighters = []
            Phasers = []
            player.reset(100, 100)
            team1 = []
            team2 = []
            team1.append(player)

    while Playing:  # Lose condition
        clock.tick(60)
        page = 10
        if player.health <= 0:
            Playing = False
            page = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



        # Controls
        keys = pygame.key.get_pressed()
        if LOSE == 0:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.angle += 2
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.angle -= 2
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if player.velocity != 4:
                    player.velocity += 1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if player.velocity != -4:
                    player.velocity -= 1
            if keys[pygame.K_SPACE]:
                if player.fire == player.clip and player.ammo >= 1:
                    player.fire = 0
                    player.ammo -= 1
                    Phasers.append(phaser(player.x + 5, player.y, random.randrange((player.angle - player.accuracy), (player.angle + player.accuracy)), 1, 5, "Phaser", 8))
                    PLAYERPHASER.play()
                if player.fire != player.clip:
                    player.fire += 1
        if keys[pygame.K_ESCAPE]:
             Playing = False

        # Game phases

        if team2 == []:  # Wave handler
            team1 = []
            team1.append(player)
            team2 = []

            if phase == 0:
                fighters.append(NPC(2100, 400, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2000, 500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 600, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))

                if difficulty == 0:
                    fighters.append(NPC(-200, 900, 10, 70, 200, 10, 10, 2, KLUX3, "KCARRIER", 1, False))

            if phase == 1:
                fighters.append(NPC(2500, 1000, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2500, 1100, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 600, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 700, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 1200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))

            if phase == 2:
                fighters.append(NPC(2700, 1000, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2500, 900, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2200, 200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 300, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))


            if phase == 3:
                fighters.append(NPC(2700, 600, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                # fighters.append(fighter(2200, 600, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, INTERCEPTOR2, 2, False))
                fighters.append(NPC(2200, 100, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2000, 70, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))

                fighters.append(NPC(-100, 600, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-100, 700, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 800, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 900, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-200, 900, 10, 70, 200, 10, 10, 2, KLUX3, "KCARRIER", 1, False))

            if phase == 4:
                fighters.append(NPC(2700, 1000, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2700, 900, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                if difficulty == 2:
                    fighters.append(NPC(2700, 800, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2500, 900, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2200, 200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 300, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2600, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2700, 1200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                if difficulty == 0:
                    fighters.append(NPC(-100, 600, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                    fighters.append(NPC(-100, 700, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))

            if phase == 5:
                fighters.append(NPC(2700, 1000, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2700, 900, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2700, 800, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2500, 900, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2200, 200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 300, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2600, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2700, 1200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))

            if phase == 6:
                fighters.append(NPC(2700, 1000, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2700, 900, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2700, 800, 2, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2500, 900, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2200, 200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2100, 300, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2600, 1500, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2700, 1200, 5, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))

                fighters.append(NPC(-200, 900, 10, 70, 600, 10, 10, 2, KLUX3, "KCARRIER", 1, False))
                fighters.append(NPC(-1200, 900, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 600, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 700, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 800, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))

            if phase == 7:
                fighters.append(NPC(2700, 1000, 4, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))  # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):
                fighters.append(NPC(2700, 900, 4, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2700, 800, 4, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2500, 900, 10, 70, 600, 10, 10, 2, CARRIER, "CARRIER", 2, False))
                fighters.append(NPC(2500, 950, 10, 70, 600, 10, 10, 2, CARRIER, "CARRIER", 2, False))

                fighters.append(NPC(-200, 900, 10, 70, 600, 10, 10, 2, KLUX3, "KCARRIER", 1, False))
                fighters.append(NPC(-1200, 900, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 600, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 700, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 800, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))

            if phase == 8:
                fighters.append(NPC(2300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300+50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400+50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500+50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200+50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300 + 50 + 50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400 + 50 + 50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500 + 50 + 50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200 + 50 + 50, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300 + 50 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400 + 50 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500 + 50 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200 + 50 + 50 + 300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3000 + 500, 950, 10, 70, 600, 10, 10, 2, CARRIER, "CARRIER", 2, False))

                fighters.append(NPC(-200, 500, 10, 70, 600, 10, 10, 2, KLUX3, "KCARRIER", 1, False))
                fighters.append(NPC(-200, 100, 10, 70, 600, 10, 10, 2, KLUX3, "KCARRIER", 1, False))

            if phase == 9:
                fighters.append(NPC(-200, 900, 10, 70, 600, 10, 10, 2, KLUX3, "KCARRIER", 1, False))
                fighters.append(NPC(-200, 600, 10, 70, 600, 10, 10, 2, KLUX3, "KCARRIER", 1, False))
                fighters.append(NPC(-100, 600, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-100, 700, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 800, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))
                fighters.append(NPC(-1200, 900, 10, 19, 20, 10, 10, 4, KLUX4, "KLUX4", 1, False))

                fighters.append(NPC(2700, 600, 4, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2700, 700, 4, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2700, 500, 4, 27, 100, 15, 15, 6, INTERCEPTOR2, "INTERCEPTOR2", 2, False))
                fighters.append(NPC(2200, 100, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2000, 70, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2300, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(2400, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3500, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False))
                fighters.append(NPC(3200, 1500, 10, 19, 20, 10, 10, 4, INTERCEPTOR1, "INTERCEPTOR1", 2, False)) # (self, x, y, clip, radius, health, accuracy, ammo, speed, skin, name, team, master):

            if phase == 10:
                fighters.append(NPC(2700, 600, 6, 27, 500, 10, 20, 7, UBER, "UBER", 2, False))

            if phase == 11:
                page = 12
                Playing = False

            phase += 1

            for fighter in fighters:
                if fighter.team == 1:
                    team1.append(fighter)
                elif fighter.team ==2:
                    team2.append(fighter)

        if player.velocity > 0:
            player.velocity -= 0.5
        if player.velocity < 0:
            player.velocity += 0.5

        redraw()


# Created by Harrison Lockwood (Lord Siron)
# Sub 1000 lines YES!