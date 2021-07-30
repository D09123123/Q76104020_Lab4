import pygame
import os
import math
from settings import BLACK, WIN_WIDTH, WIN_HEIGHT


TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        
        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        x1, y1 = enemy.get_pos()     # get the position from the enemy
        x2, y2 = self.center         # tower's position
        if math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= self.radius: # calculate the distance between the enemy and the tower
            return True                                               # if the distance is not larger than the radius, the enemy
        return False                                                  # is in the range of tower shot, return True. Conversely, return F.
        

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # create semi-transparent surface
        transparent_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        transparency = 60  # define transparency: 0~255, 0 is fully transparent
        pygame.draw.circle(transparent_surface,(0, 0, 0, transparency),self.center,self.radius,0) #fill in circle's center point and radius
        win.blit(transparent_surface, (0, 0)) #put the transparent surface in window               and draw the circle on the surface
        


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        if self.cd_count < self.cd_max_count:    #count every frame, if the frame < 60 ,
            self.cd_count += 1
            return False                         #return False to tell cooldown isn't ready
        else:                                    #the frame = 60
            self.cd_count = 0                    #after the tower shoots, the tower shall cooldown again. Count again
            return True                          #return True to tell cooldown is ready
            
        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        

    def attack(self, enemy_group):
        if self.is_cool_down() == True :                     # First to check the tower's cooldown is ready
            for enemy in enemy_group.get():                  # get the enemies' information
                if self.range_circle.collide(enemy) == True: # if enemies' are in range of tower
                    enemy.get_hurt(self.damage)              # enemy will get shooted
                    break                                    # break to make sure the tower will only shoot once wwhen cooldown is ready 
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """

        
       
        

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        tower_x ,tower_y = self.rect.center  # get the tower's position
        if math.sqrt((x - tower_x) ** 2 + (y - tower_y) ** 2) <= self.range * 0.3: # if the mouse position is in range of tower' image
            return True                                                            # (where I make the range smaller(*0.3)) return True
        return False                                                               # else return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        
        self.is_selected = is_selected
        

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

