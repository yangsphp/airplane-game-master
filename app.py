import pygame
from pygame.locals import *
import time
import random


# 我机
class HeroPlane(object):
    def __init__(self, screen):
        # 设置飞机默认的位置
        self.x = 230
        self.y = 550
        # 设置要显示内容的窗口
        self.screen = screen
        # 用来保存英雄飞机需要的图片名字
        self.imageName = "./feiji/hero.gif"
        # 根据名字生成飞机图片
        self.image = pygame.image.load(self.imageName)
        # 用来保存英雄飞机发射出的所有子弹
        self.bullet = []

        # 爆炸效果用的如下属性
        self.hit = False  # 表示是否要爆炸
        self.bomb_list = []  # 用来存储爆炸时需要的图片
        self.__crate_images()  # 调用这个方法向bomb_list中添加图片
        self.image_num = 0  # 用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0  # 用来记录当前要显示的爆炸效果的图片的序号

    def __crate_images(self):
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n1.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n2.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n3.png"))
        self.bomb_list.append(pygame.image.load("./feiji/hero_blowup_n4.png"))

    def bomb(self):
        self.hit = True

    def display(self):
        if self.hit:
            self.screen.blit(self.bomb_list[self.image_index], (self.x, self.y))
            self.image_num += 1
            if self.image_num == 7:
                self.image_num = 0
                self.image_index += 1
            if self.image_index > 3:
                time.sleep(1)
                exit()  # 调用exit让游戏退出
        else:
            self.screen.blit(self.image, (self.x, self.y))
        # 用来存放需要删除的对象信息
        needDelItemList = []
        for b in self.bullet:
            b.display()
            b.move()
            if b.judge():
                needDelItemList.append(b)
        # 删除self.bulletL中需要删除的对象
        for i in needDelItemList:
            self.bullet.remove(i)

    def moveLeft(self):
        self.x -= 10

    def moveRight(self):
        self.x += 10

    def sheBullet(self):
        newBullet = Bullet(self.x, self.y, self.screen)
        self.bullet.append(newBullet)


# 子弹
class Bullet(object):
    def __init__(self, x, y, screen):
        self.x = x + 40
        self.y = y - 20
        self.screen = screen
        self.image = pygame.image.load("./feiji/bullet-3.gif")

    def move(self):
        self.y -= 20

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    # 判断子弹是否越界
    def judge(self):
        if self.y < 0:
            return True
        return False


# 敌机
class EnemyPlane(object):

    def __init__(self, screen):
        # 设置飞机默认的位置
        self.x = 0
        self.y = 0
        # 设置要显示内容的窗口
        self.screen = screen
        self.imageName = "./feiji/enemy-1.gif"
        self.image = pygame.image.load(self.imageName)
        # 用来存储敌人飞机发射的所有子弹
        self.bulletList = []
        self.direction = "right"

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        # 存储待删除的子弹
        needDelItemList = []
        for b in self.bulletList:
            b.display()
            b.move()
            if b.judge():
                needDelItemList.append(b)
        # 删除self.bulletL中需要删除的对象
        for i in needDelItemList:
            self.bulletList.remove(i)

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        if self.x > 480 - 50:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    # 敌机发射子弹
    def shot(self):
        random_num = random.randint(1, 100)
        if random_num == 10 or random_num == 20:
            EnemyNewBullet = EnemyBullet(self.x, self.y, self.screen)
            self.bulletList.append(EnemyNewBullet)


# 敌机子弹
class EnemyBullet(object):
    def __init__(self, x, y, screen):
        self.x = x + 22
        self.y = y + 40
        self.screen = screen
        self.image = pygame.image.load("./feiji/bullet1.png")

    # 移动子弹
    def move(self):
        self.y += 20

    # 显示子弹
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

    # 判断子弹是否越界
    def judge(self):
        if self.y > 650:
            return True
        return False


# 键盘监听
def key_control(plane):
    # 获取事件，比如按键等
    for event in pygame.event.get():
        # 判断是否是点击了退出按钮
        if event.type == QUIT:
            exit()
        # 判断是否是按下了键
        elif event.type == KEYDOWN:
            # 检测按键是否是a或者left
            if event.key == K_a or event.key == K_LEFT:
                plane.moveLeft()
            # 检测按键是否是d或者right
            elif event.key == K_d or event.key == K_RIGHT:
                plane.moveRight()

            # 检测按键是否是空格键
            elif event.key == K_SPACE:
                plane.sheBullet()
            elif event.key == K_b:
                plane.bomb()


def main():
    # 创建一个游戏窗口
    screen = pygame.display.set_mode((480, 650), 0, 32)
    # 创建背景图片
    background = pygame.image.load("./feiji/background.png")
    # 创建一个飞机对象
    plane = HeroPlane(screen)
    # 创建一个敌人飞机
    enemyPlane = EnemyPlane(screen)
    while True:
        # 将图片放到屏幕上
        screen.blit(background, (0, 0))
        # 显示我的飞机到屏幕
        plane.display()
        # 显示敌机到屏幕
        enemyPlane.display()
        # 移动敌机
        enemyPlane.move()
        # 敌机发射子弹
        enemyPlane.shot()
        # 更新显示
        pygame.display.update()
        # 监听键盘，控制我机
        key_control(plane)
        time.sleep(0.08)
    pass


if __name__ == '__main__':
    main()
