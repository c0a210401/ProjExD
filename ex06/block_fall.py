import pygame as pg
import sys
from random import randint
import copy
# C0A21040 北村 耕大

class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)                 # ウィンドウを作成
        self.scr = pg.display.set_mode(wh)            # 幅, 高さが wh の画面のSurfaceクラスを作成
        self.bgimg = pg.image.load(image)             # 背景の画像のSurfaceクラスを作成
        self.bgr = self.bgimg.get_rect()              # 背景の画像のRectクラスのオブジェクトを生成

    def blit(self):
        self.scr.blit(self.bgimg, self.bgr)           # 背景のSurfaceクラスを貼り付け

class Bar(pg.sprite.Sprite):
    def __init__(self, name):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(name).convert()
        self.image = pg.transform.scale(self.image, (150, 20))

        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = 200, 430

    def blit(self, sr: Screen):
        sr.scr.blit(self.image, self.rect)                    # 棒のSurfaceクラスを貼り付け

    def Update(self, sr: Screen):
        key_states = pg.key.get_pressed()                     # どのキーが押されているかを取得
        if key_states[pg.K_LEFT]:                             # [←]キーが押されているなら
            pg.Rect.move_ip(self.rect, (-1, 0))               # 棒が左に1動く
            if self.rect.left <= 0:                           # 移動先が画面外の場合
                pg.Rect.move_ip(self.rect, (1, 0))            # 移動前の位置に戻す
        if key_states[pg.K_RIGHT]:                            # [→]キーが押されているなら
            pg.Rect.move_ip(self.rect, (1, 0))                # 棒が右に1動く
            if self.rect.right >= sr.bgr.right:               # 移動先が画面外の場合
                pg.Rect.move_ip(self.rect, (-1, 0))           # 移動前の位置に戻す

        self.blit(sr)

class Ball(pg.sprite.Sprite):
    def __init__(self, name, vxy, blocks):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(name).convert_alpha()
        self.image = pg.transform.scale(self.image, (20, 20))
        self.image.set_colorkey("black")
 
        self.rect = self.image.get_rect()
        self.rect.center = 50, 400

        self.blocks = blocks
        self.vx, self.vy = vxy                                 # 玉の初期移動速度を指定 vx〇:横方向速度 vy〇:縦方向速度

    def blit(self, sr: Screen):
        sr.scr.blit(self.image, self.rect)                     # 玉のSurfaceクラスを貼り付け

    def Update(self, sr: Screen):
        pg.Rect.move_ip(self.rect, (self.vx, self.vy))         # 玉をvx, vy にしたがって移動させる
        if self.rect.left <= 0 or self.rect.right >= sr.bgr.right:  # 玉の移動先が横方向から画面外に行く場合
            self.vx = -self.vx                                 # 横方向の移動速度の符号を反転させる
        if self.rect.top <= 0 or self.rect.bottom >= 500:           # 玉の移動先が縦方向から画面外に行く場合
            self.vy = -self.vy                                 # 縦方向の移動速度の符号を反転させる

        blocks_list = pg.sprite.spritecollide(self, self.blocks, True)
        if len(blocks_list) > 0:
            ball_rect = copy.copy(self.rect)
            for block in blocks_list:
                if block.rect.top > ball_rect.top and block.rect.bottom > ball_rect.bottom and self.vy > 0:
                    self.rect.bottom = block.rect.top
                    self.vy = -self.vy
                if block.rect.top < ball_rect.top and block.rect.bottom < ball_rect.bottom and self.vy < 0:
                    self.rect.top = block.rect.bottom
                    self.vy = -self.vy
                if block.rect.left > ball_rect.left and block.rect.right > ball_rect.right and self.vx > 0:
                    self.rect.right = block.rect.left
                    self.vx = -self.vx
                if block.rect.left < ball_rect.left and block.rect.right < ball_rect.right and self.vx < 0:
                    self.rect.left = block.rect.right
                    self.vx = -self.vx

        self.blit(sr)

    def reflect(self, sr: Screen):
        a = randint(0, 1)
        self.vy = -self.vy
        if a == 1:
            self.vx = -self.vx
        else:
            pass

        self.blit(sr)

class Block(pg.sprite.Sprite):
    def __init__(self, name, x, y):
        pg.sprite.Sprite.__init__(self)
 
        self.image = pg.image.load(name).convert()
        self.image = pg.transform.scale(self.image, (40, 20))

        self.rect = self.image.get_rect()
        self.rect.left = x * self.rect.width
        self.rect.top  = y * self.rect.height

    def draw(self, sr: Screen):
        sr.scr.blit(self.image, self.rect)   
 
def main():
    clock = pg.time.Clock()       # 時間計測用のオブジェクトを生成
    scre = Screen("ブロック", (400, 500), "fig/ダウンロード.png")
    scre.blit()          # 背景のSurfaceクラスを貼り付け

    blocks = pg.sprite.Group()
    for x in range(10):
        for y in range(10):
            blocks.add(Block("fig/block.PNG", x, y))

    #bal = Ball((255, 0, 0), 10, (1, 1), blocks)
    bal = Ball("fig/ball.png", (1, 1), blocks)
    bar = Bar("fig/bar.png")

    while True:              # 無限ループ
        scre.blit()          # 背景のSurfaceクラスを貼り付け
        bal.blit(scre)
        bar.blit(scre)
        blocks.draw(scre.scr)

        n = pg.Rect.colliderect(bar.rect, bal.rect)
        if n == True:
            bal.reflect(scre)

        bar.Update(scre)
        bal.Update(scre)

        for event in pg.event.get():            # イベントを繰り返して処理
            if event.type == pg.QUIT:           # ウィンドウの[×]ボタンが押されたら
                return                          # main関数から抜ける        
        
        pg.display.update()           # 画面を更新
        clock.tick(1000)              # 1000fps(1秒)の時を刻む


if __name__ == "__main__":
    pg.init()            # pygameモジュールを初期化
    main()               # main関数を呼び出す
    pg.quit()            # pygameモジュールの初期化を解除
    sys.exit()           # プログラムを終了