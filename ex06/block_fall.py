import pygame as pg
import sys
from random import randint
import copy
# C0A21040 北村 耕大

BAR_POS = 30    # 棒の画面最下部からの距離


class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)                   # ウィンドウを作成
        self.scr = pg.display.set_mode(wh)              # 幅, 高さが wh の画面のSurfaceクラスを作成
        self.images = pg.image.load(image)              # 背景の画像のSurfaceクラスを作成
        self.rect = self.images.get_rect()              # 背景の画像のRectクラスのオブジェクトを生成

    def blit(self):
        self.scr.blit(self.images, self.rect)           # 背景のSurfaceクラスを貼り付け


class Bar(pg.sprite.Sprite):
    def __init__(self, name, size, sr: Screen):
        pg.sprite.Sprite.__init__(self)                        # 初期化処理
        self.image = pg.image.load(name).convert()             # 棒の画像をピクセル変換処したSurfaceクラスを作成
        self.image = pg.transform.scale(self.image, size)      # 棒の画像の大きさをsize倍に設定

        self.image.set_colorkey("black")                       # 描画した棒の黒色の部分を透明化
        self.rect = self.image.get_rect()                      # 棒のRectクラスのオブジェクトを生成
        self.rect.center = 200, sr.rect.bottom - BAR_POS       # 棒の画像の初期位置を指定　横:200 縦:470

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
            if self.rect.right >= sr.rect.right:              # 移動先が画面外の場合
                pg.Rect.move_ip(self.rect, (-1, 0))           # 移動前の位置に戻す

        self.blit(sr)


class Ball(pg.sprite.Sprite):
    def __init__(self, name, vxy, size, blocks, score):
        pg.sprite.Sprite.__init__(self)                       # 初期化処理
        self.image = pg.image.load(name).convert_alpha()      # ボールの画像をピクセル変換処したSurfaceクラスを作成
        self.image = pg.transform.scale(self.image, size)     # ボールの画像の大きさをsize倍に設定

        self.image.set_colorkey("black")            # 描画したボールの黒色の部分を透明化
        self.rect = self.image.get_rect()           # ボールのRectクラスのオブジェクトを生成
        self.rect.center = randint(0, 400), randint(200, 500 - BAR_POS) # ボールを描画する位置を一定の範囲内でランダムに指定(x:0~400, y:200~470)

        self.blocks = blocks                        # ブロックを参照
        self.vx, self.vy = vxy                      # ボールの初期移動速度を指定 vx〇:横方向速度 vy〇:縦方向速度

        self.score = score                                     #スコア表示を参照
        self.hit = 0                                           #ブロックを破壊した回数


    def blit(self, sr: Screen):
        sr.scr.blit(self.image, self.rect)                     # ボールのSurfaceクラスを貼り付け

    def Update(self, sr: Screen):
        pg.Rect.move_ip(self.rect, (self.vx, self.vy))               # ボールをvx, vy にしたがって移動させる
        if self.rect.left <= 0 or self.rect.right >= sr.rect.right:   # ボールうの移動先が横方向から画面外に行く場合
            self.vx = -self.vx                                       # 横方向の移動速度の符号を反転させる
        if self.rect.top <= 0 or self.rect.bottom >= 500:            # ボールの移動先が縦方向から画面外に行く場合
            self.vy = -self.vy                                 # 縦方向の移動速度の符号を反転させる

        blocks_list = pg.sprite.spritecollide(self, self.blocks, True)   # ボールとぶつかったブロックを削除
        if len(blocks_list) > 0:                        # ブロックとボールの接触があった場合
            self.hit += 10                              
            self.score.add_score(self.hit)
            self.hit = 0
            ball_rect = copy.copy(self.rect)            # ボールオブジェクトの位置を保存
            for block in blocks_list:                   # 接触したブロックを取り出す
                if block.rect.top > ball_rect.top and block.rect.bottom > ball_rect.bottom and self.vy > 0:
                    self.rect.bottom = block.rect.top   # ボールがブロックの上部に接触した場合
                    self.vy = -self.vy                  # 縦方向の速度を反転
                if block.rect.top < ball_rect.top and block.rect.bottom < ball_rect.bottom and self.vy < 0:
                    self.rect.top = block.rect.bottom   # ボールがブロックの下部に接触した場合
                    self.vy = -self.vy                  # 縦方向の速度を反転
                if block.rect.left > ball_rect.left and block.rect.right > ball_rect.right and self.vx > 0:
                    self.rect.right = block.rect.left   # ボールがブロックの左部に接触した場合
                    self.vx = -self.vx                  # 横方向の速度を反転
                if block.rect.left < ball_rect.left and block.rect.right < ball_rect.right and self.vx < 0:
                    self.rect.left = block.rect.right   # ボールがブロックの右部に接触した場合
                    self.vx = -self.vx                  # 横方向の速度を反転

        self.blit(sr)

    def reflect(self, sr: Screen):
        ran = randint(0, 1)          # ボールの反射方向を
        self.vy = -self.vy           # 縦方向の速度を反転
        if ran == 1:                 # 50%の確率で
            self.vx = -self.vx       # 横方向の速度を反転

        self.blit(sr)


class Block(pg.sprite.Sprite):
    def __init__(self, name, x, y, size):
        pg.sprite.Sprite.__init__(self)                        # 初期化処理
        self.image = pg.image.load(name).convert()             # ブロックの画像をピクセル変換処理したSurfaceクラスを作成
        self.image = pg.transform.scale(self.image, size)      # ブロックの画像の大きさをsize倍に設定

        self.rect = self.image.get_rect()             # ブロックのRectクラスのオブジェクトを生成
        self.rect.left = x * self.rect.width          # ブロックのx軸の位置を設定
        self.rect.top  = y * self.rect.height         # ブロックのy軸の位置を設定

    def draw(self, sr: Screen):
        sr.scr.blit(self.image, self.rect)            # ブロックのSurfaceクラスを貼り付け

# C0B21183 杉本 英吾 #s
class Score():
    def __init__(self, x, y):                         # 文字のフォント設定
        self.sysfont = pg.font.SysFont(None,30)       # スコアの数値を初期化
        self.score = 0                                # スコアの初期位置を設定
        self.x, self.y = x, y

    def draw(self, sr: Screen):
        img = self.sysfont.render("SCORE:"+str(self.score), True, (255,0,0))     # スコアのSurfaceクラスを作成
        sr.scr.blit(img, (self.x, self.y))                                       # スコアのSurfaceクラスを貼り付け

    def add_score(self,x):
        self.score += x                          # scoreに点数を追加
#s 
 
def main():
    clock = pg.time.Clock()                                            # 時間計測用のオブジェクトを生成
    scre = Screen("ブロック崩し", (400, 500), "fig/ダウンロード.png")   # 400x500のスクリーンを生成
    scre.blit()                                                        # 背景のSurfaceクラスを貼り付け

    blocks = pg.sprite.Group()                                    # ブロックのグループを作成
    for x in range(10):
        for y in range(10):
            blocks.add(Block("fig/block.PNG", x, y, (40, 20)))    # ブロックを生成
    score = Score(0, 0)
    bar = Bar("fig/bar.png", (150, 20), scre)                     # 棒を生成
    bal = Ball("fig/ball.png", (1, 1), (20, 20), blocks,score)          # ボールを生成

    while True:                 # 無限ループ
        scre.blit()             # 背景のSurfaceクラスを貼り付け
        bal.blit(scre)          # ボールのSurfaceクラスを貼り付け
        bar.blit(scre)          # 棒のSurfaceクラスを貼り付け
        blocks.draw(scre.scr)   # ブロックのSurfaceクラスを貼り付け
        score.draw(scre)  

        tf = pg.Rect.colliderect(bar.rect, bal.rect)   # ボールが棒にぶつかったかを判定
        if tf == True:                                 # ぶつかっていた場合
            bal.reflect(scre)                          # ボールを反射させる

        bar.Update(scre)                        # 棒を表示するための画面の更新
        bal.Update(scre)                        # 玉を表示するための画面の更新

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