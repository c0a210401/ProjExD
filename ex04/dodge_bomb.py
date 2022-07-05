import pygame as pg
import sys
from random import randint

def main():
    clock = pg.time.Clock()       # 時間計測用のオブジェクトを生成
    
    pg.display.set_caption("逃げろ!こうかとん")     # ウィンドウを作成
    screen_img = pg.display.set_mode((1600, 900))  # 幅:1600, 高さ:900 の画面のSurfaceクラスを作成
    screen_rect = screen_img.get_rect()            # 画面のRectクラスのオブジェクトを生成

    bg_img = pg.image.load("fig/pg_bg.jpg")        # 背景の画像のSurfaceクラスを作成
    bg_rect = bg_img.get_rect()                    # 背景の画像のRectクラスのオブジェクトを生成

    tori_img = pg.image.load("fig/3.png")                   # こうかとんの画像のSurfaceクラスを作成
    tori_img = pg.transform.rotozoom(tori_img, 0, 2.0)      # こうかとんの画像の大きさを2倍に設定
    tori_rect = tori_img.get_rect()                         # こうかとんの画像のRectクラスのオブジェクトを生成
    tori_rect.center = 900, 400                             # こうかとんの画像の初期位置を指定　横:900 縦:400

    bom = pg.Surface((20,20))        # 爆弾のSurfaceクラスを作成

    pg.draw.circle(bom, (255, 0, 0), (10,10), 10)       # 半径10の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, (191, 0, 0), (10,10), 8)        # 半径8の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, (127, 0, 0), (10,10), 6)        # 半径6の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, ( 63, 0, 0), (10,10), 4)        # 半径4の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, ( 0, 0, 0), (10,10), 2)         # 半径2の円をbomの位置(10,10)に描画

    bom.set_colorkey("black")        # 描画した爆弾の黒色の部分を透明化
    bom_rect = bom.get_rect()        # 爆弾のRectクラスのオブジェクトを生成

    bom_rect.center = randint(0, screen_rect.width), randint(0, screen_rect.height)     # 爆弾の初期位置を画面内でランダムに指定

    vx, vy = 1, 1        # 爆弾の初期移動速度を指定 vx:横方向 vy:縦方向

    while True:          # 無限ループ
        screen_img.blit(bg_img, bg_rect)        # 背景のSurfaceクラスを貼り付け
        screen_img.blit(tori_img, tori_rect)    # こうかとんのSurfaceクラスを貼り付け
        screen_img.blit(bom, bom_rect)          # 爆弾のSurfaceクラスを貼り付け

        for event in pg.event.get():            # イベントを繰り返して処理
            if event.type == pg.QUIT:           # ウィンドウの[×]ボタンが押されたら
                return                          # main関数から抜ける

        key_states = pg.key.get_pressed()               # どのキーが押されているかを取得
        if key_states[pg.K_UP] == True:                 # [↑]キーが押されているなら
            pg.Rect.move_ip(tori_rect, (0, -1))         # こうかとんが上に1動く
            if tori_rect[1] <= 0:                       # 移動先が画面外の場合
                pg.Rect.move_ip(tori_rect, (0, 1))      # 移動前の位置に戻す
        if key_states[pg.K_DOWN] == True:               # [↓]キーが押されているなら
            pg.Rect.move_ip(tori_rect, (0, 1))          # こうかとんが下に1動く
            if tori_rect[1] >= 800:                     # 移動先が画面外の場合
                pg.Rect.move_ip(tori_rect, (0, -1))     # 移動前の位置に戻す
        if key_states[pg.K_LEFT] == True:               # [←]キーが押されているなら
            pg.Rect.move_ip(tori_rect, (-1, 0))         # こうかとんが左に1動く
            if tori_rect[0] <= 0:                       # 移動先が画面外の場合
                pg.Rect.move_ip(tori_rect, (1, 0))      # 移動前の位置に戻す
        if key_states[pg.K_RIGHT] == True:              # [→]キーが押されているなら
            pg.Rect.move_ip(tori_rect, (1, 0))          # こうかとんが右に1動く
            if tori_rect[0] >= 1500:                    # 移動先が画面外の場合
                pg.Rect.move_ip(tori_rect, (-1, 0))     # 移動前の位置に戻す

        pg.Rect.move_ip(bom_rect, (vx, vy))             # 爆弾を vx, vy にしたがって移動させる
        if bom_rect[0] <= 0 or bom_rect[0] >= 1600:     # 爆弾の移動先が横方向から画面外に行く場合
            vx = -vx                                    # 横方向の移動速度の符号を反転させる
        if bom_rect[1] <= 0 or bom_rect[1] >= 900:      # 爆弾の移動先が縦方向から画面外に行く場合
            vy = -vy                                    # 縦方向の移動速度の符号を反転させる

        ban = pg.Rect.colliderect(tori_rect, bom_rect)     # こうかとんが爆弾にぶつかったかを判定
        if ban == True:                                    # こうかとんが爆弾にぶつかった場合
            return                    # main関数から抜ける

        pg.display.update()           # 画面を更新

        clock.tick(1000)              # 1000fps(1秒)の時を刻む


if __name__ == "__main__":
    pg.init()            # pygameモジュールを初期化
    main()               # main関数を呼び出す
    pg.quit()            # pygameモジュールの初期化を解除
    sys.exit()           # プログラムを終了