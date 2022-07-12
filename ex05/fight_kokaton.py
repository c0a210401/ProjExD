import pygame as pg
import sys
from random import randint
import tkinter.messagebox as tkm
import datetime

class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)                 # ウィンドウを作成
        self.scr = pg.display.set_mode(wh)            # 幅, 高さが wh の画面のSurfaceクラスを作成
        self.bgimg = pg.image.load(image)             # 背景の画像のSurfaceクラスを作成
        self.bgr = self.bgimg.get_rect()              # 背景の画像のRectクラスのオブジェクトを生成

    def blit(self):
        self.scr.blit(self.bgimg, self.bgr)           # 背景のSurfaceクラスを貼り付け


class Bird:
    def __init__(self, image: str, size: float, xy):
        self.toi = pg.image.load(image)                          # こうかとんの画像のSurfaceクラスを作成
        self.toi = pg.transform.rotozoom(self.toi, 0, size)      # こうかとんの画像の大きさをsize倍に設定
        self.tor = self.toi.get_rect()                           # こうかとんの画像のRectクラスのオブジェクトを生成
        self.tor.center = xy                                     # こうかとんの画像の初期位置を指定　横:900 縦:400

    def blit(self, sr: Screen):
        sr.scr.blit(self.toi, self.tor)                       # こうかとんのSurfaceクラスを貼り付け

    def Update(self, xy, sr: Screen):
        self.tor = xy
        key_states = pg.key.get_pressed()              # どのキーが押されているかを取得
        if key_states[pg.K_UP]:                        # [↑]キーが押されているなら
            pg.Rect.move_ip(self.tor, (0, -1))         # こうかとんが上に1動く
            if self.tor[1] <= 0:                       # 移動先が画面外の場合
                pg.Rect.move_ip(self.tor, (0, 1))      # 移動前の位置に戻す
        if key_states[pg.K_DOWN]:                      # [↓]キーが押されているなら
            pg.Rect.move_ip(self.tor, (0, 1))          # こうかとんが下に1動く
            if self.tor[1] >= 800:                     # 移動先が画面外の場合
                pg.Rect.move_ip(self.tor, (0, -1))     # 移動前の位置に戻す
        if key_states[pg.K_LEFT]:                      # [←]キーが押されているなら
            pg.Rect.move_ip(self.tor, (-1, 0))         # こうかとんが左に1動く
            if self.tor[0] <= 0:                       # 移動先が画面外の場合
                pg.Rect.move_ip(self.tor, (1, 0))      # 移動前の位置に戻す
        if key_states[pg.K_RIGHT]:                     # [→]キーが押されているなら
            pg.Rect.move_ip(self.tor, (1, 0))          # こうかとんが右に1動く
            if self.tor[0] >= 1500:                    # 移動先が画面外の場合
                pg.Rect.move_ip(self.tor, (-1, 0))     # 移動前の位置に戻す

        self.blit(sr)


class Bomb:
    def __init__(self, color, size, vxy):
        self.bom = pg.Surface((2*size,2*size))         # 爆弾のSurfaceクラスを作成
        self.r = color[0]               # r値を取り出す
        self.g = color[1]               # g値を取り出す
        self.b = color[2]               # b値を取り出す
        pg.draw.circle(self.bom, (self.r, self.g, self.b), (size, size), size)                          # 半径10の円をbomの位置(10,10)に描画
        pg.draw.circle(self.bom, (self.r*0.75, self.g*0.75, self.b*0.75), (size, size), size*0.8)       # 半径8の円をbomの位置(10,10)に描画
        pg.draw.circle(self.bom, (self.r*0.5,  self.g*0.5,  self.b*0.5),  (size, size), size*0.6)       # 半径6の円をbomの位置(10,10)に描画
        pg.draw.circle(self.bom, (self.r*0.25, self.g*0.25, self.b*0.25), (size, size), size*0.4)       # 半径4の円をbomの位置(10,10)に描画
        pg.draw.circle(self.bom, (0, 0, 0), (size, size), size*0.2)                                     # 半径2の円をbomの位置(10,10)に描画

        self.bom.set_colorkey("black")                         # 描画した爆弾の黒色の部分を透明化

        self.bomr = self.bom.get_rect()                        # 爆弾のRectクラスのオブジェクトを生成
        self.bomr.center = randint(0, 1600), randint(0, 900)   # 爆弾を描画する位置をランダムに指定(0~1600の間)
        self.vx, self.vy = vxy                                 # 爆弾の初期移動速度を指定 vx〇:横方向速度 vy〇:縦方向速度

    def blit(self, sr: Screen):
        sr.scr.blit(self.bom, self.bomr)                       # 爆弾のSurfaceクラスを貼り付け

    def Update(self, crash, sr: Screen):
        pg.Rect.move_ip(self.bomr, (self.vx, self.vy))         # 爆弾をvx, vy にしたがって移動させる
        if self.bomr[0] <= 0 or self.bomr[0] >= 1600:          # 爆弾の移動先が横方向から画面外に行く場合
            self.vx = -self.vx                                 # 横方向の移動速度の符号を反転させる
        if self.bomr[1] <= 0 or self.bomr[1] >= 900:           # 爆弾の移動先が縦方向から画面外に行く場合
            self.vy = -self.vy                                 # 縦方向の移動速度の符号を反転させる
        if crash != 0:                                         # Avoモードのこうかとんとぶつかっている場合
            pass                                               # 更新しない
        
        self.blit(sr)


class Avo:
    def __init__(self, image, size, br: Bird):
        self.Rscr = pg.image.load(image)                          # こうかとんの画像のSurfaceクラスを作成
        self.Rscr = pg.transform.rotozoom(self.Rscr, 0, size)     # こうかとんの画像の大きさをsize倍に設定
        self.Rrct = self.Rscr.get_rect()                          # こうかとんの画像のRectクラスのオブジェクトを生成
        self.Rrct.center = br.tor[0], br.tor[1]                   # こうかとんの画像の初期位置を指定　横:900 縦:400

    def blit(self, sr: Screen):
        sr.scr.blit(self.Rscr, self.Rrct)                       # 爆弾のSurfaceクラスを貼り付け

    def Update(self, xy, sr: Screen):
        self.Rrct = xy
        key_states = pg.key.get_pressed()               # どのキーが押されているかを取得
        if key_states[pg.K_UP]:                         # [↑]キーが押されているなら
            pg.Rect.move_ip(self.Rrct, (0, -1))         # こうかとんが上に1動く
            if self.Rrct[1] <= 0:                       # 移動先が画面外の場合
                pg.Rect.move_ip(self.Rrct, (0, 1))      # 移動前の位置に戻す
        if key_states[pg.K_DOWN]:                       # [↓]キーが押されているなら
            pg.Rect.move_ip(self.Rrct, (0, 1))          # こうかとんが下に1動く
            if self.Rrct[1] >= 800:                     # 移動先が画面外の場合
                pg.Rect.move_ip(self.Rrct, (0, -1))     # 移動前の位置に戻す
        if key_states[pg.K_LEFT]:                       # [←]キーが押されているなら
            pg.Rect.move_ip(self.Rrct, (-1, 0))         # こうかとんが左に1動く
            if self.Rrct[0] <= 0:                       # 移動先が画面外の場合
                pg.Rect.move_ip(self.Rrct, (1, 0))      # 移動前の位置に戻す
        if key_states[pg.K_RIGHT]:                      # [→]キーが押されているなら
            pg.Rect.move_ip(self.Rrct, (1, 0))          # こうかとんが右に1動く
            if self.Rrct[0] >= 1500:                    # 移動先が画面外の場合
                pg.Rect.move_ip(self.Rrct, (-1, 0))     # 移動前の位置に戻す

        self.blit(sr)


class Slash:
    def __init__(self, image, xy):
        self.zscr = pg.image.load(image)
        self.zscr = pg.transform.rotozoom(self.zscr, 0, 1)
        self.zrct = self.zscr.get_rect()
        self.zrct.center = xy[0], xy[1]+100

    def blit(self, sr: Screen):
        sr.scr.blit(self.zscr, self.zrct)  

def main():
    st = datetime.datetime.now()  # 現在時間を取得
    clock = pg.time.Clock()       # 時間計測用のオブジェクトを生成

    scre = Screen("負けるな!こうかとん", (1600, 900), "fig/pg_bg.jpg")

    kouka = Bird("fig/3.png", 2.0, (900, 400))

    kouka_R = Avo("fig/7.png", 2.0, kouka)

    bomr = Bomb((255, 0, 0), 20, (1, 1))    # 爆弾を生成
    bomg = Bomb((0, 255, 0), 20, (2, 2))
    bomb = Bomb((0, 0, 255), 20, (3, 3))

    sr, sg, sb = 0, 0, 0

    while True:              # 無限ループ
        scre.blit()          # 背景のSurfaceクラスを貼り付け

        for event in pg.event.get():            # イベントを繰り返して処理
            if event.type == pg.QUIT:           # ウィンドウの[×]ボタンが押されたら
                return                          # main関数から抜ける

        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE]:
            kouka_R.blit(scre)
            kouka_R.Update(kouka.tor, scre)
            banR = pg.Rect.colliderect(kouka_R.Rrct, bomr.bomr)     # こうかとんが爆弾にぶつかったかを判定
            banG = pg.Rect.colliderect(kouka_R.Rrct, bomg.bomr)
            banB = pg.Rect.colliderect(kouka_R.Rrct, bomb.bomr)
            
            slash = Slash("fig/slash.png",kouka_R.Rrct)
            slash.blit(scre)

            if banR == True:            # こうかとんが爆弾にぶつかった場合
                bomr.Update(1, scre)
            if banG == True:
                bomg.Update(1, scre)
            if banB == True:
                bomb.Update(1, scre)

        else:
            kouka.Update(kouka_R.Rrct,scre)    # こうかとんを表示するための画面の更新
            banr = pg.Rect.colliderect(kouka.tor, bomr.bomr)     # こうかとんが爆弾にぶつかったかを判定
            bang = pg.Rect.colliderect(kouka.tor, bomg.bomr)     # こうかとんが爆弾にぶつかったかを判定
            banb = pg.Rect.colliderect(kouka.tor, bomb.bomr)     # こうかとんが爆弾にぶつかったかを判定

            if banr == True or bang == True or banb == True:            # こうかとんが爆弾にぶつかった場合
                ed = datetime.datetime.now()                            # 終了した時間を取得
                time = (ed-st).seconds                                  # 何秒間逃げ続けたかを計算
                tkm.showinfo("爆発", f"こうかとんは{time}秒耐えました")    # 結果を表示する
                return                                                  # main関数から抜ける

        bomr.Update(0, scre)     # 爆弾を表示するための画面の更新
        bomg.Update(0, scre)
        bomb.Update(0, scre)

        pg.display.update()           # 画面を更新
        clock.tick(1000)              # 1000fps(1秒)の時を刻む


if __name__ == "__main__":
    pg.init()            # pygameモジュールを初期化
    main()               # main関数を呼び出す
    pg.quit()            # pygameモジュールの初期化を解除
    sys.exit()           # プログラムを終了