import pygame as pg
import sys
from random import randint
import tkinter.messagebox as tkm
import datetime

def boom_cre(r, g, b):                                               # 爆弾を生成する関数　r,g,b : 爆弾の色指定
    bom = pg.Surface((20,20))                                        # 爆弾のSurfaceクラスを作成
    pg.draw.circle(bom, (r, g, b), (10,10), 10)                      # 半径10の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, (r*0.75, g*0.75, b*0.75), (10,10), 8)        # 半径8の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, (r*0.5, g*0.5, b*0.5), (10,10), 6)           # 半径6の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, (r*0.25, g*0.25, b*0.25), (10,10), 4)        # 半径4の円をbomの位置(10,10)に描画
    pg.draw.circle(bom, (0, 0, 0), (10,10), 2)                       # 半径2の円をbomの位置(10,10)に描画

    bom.set_colorkey("black")        # 描画した爆弾の黒色の部分を透明化

    bom_rect = bom.get_rect()                               # 爆弾のRectクラスのオブジェクトを生成
    bom_rect.center = randint(0, 1600), randint(0, 900)     # 爆弾を描画する位置をランダムに指定(0~1600の間)
    return bom, bom_rect                                    # 爆弾のSurfaceとRectを返す

def main():
    st = datetime.datetime.now()  # 現在時間を取得
    clock = pg.time.Clock()       # 時間計測用のオブジェクトを生成
    
    pg.display.set_caption("逃げろ!こうかとん")     # ウィンドウを作成
    screen_img = pg.display.set_mode((1600, 900))  # 幅:1600, 高さ:900 の画面のSurfaceクラスを作成

    bg_img = pg.image.load("fig/pg_bg.jpg")        # 背景の画像のSurfaceクラスを作成
    bg_rect = bg_img.get_rect()                    # 背景の画像のRectクラスのオブジェクトを生成

    tori_img = pg.image.load("fig/3.png")                   # こうかとんの画像のSurfaceクラスを作成
    tori_img = pg.transform.rotozoom(tori_img, 0, 2.0)      # こうかとんの画像の大きさを2倍に設定
    tori_rect = tori_img.get_rect()                         # こうかとんの画像のRectクラスのオブジェクトを生成
    tori_rect.center = 900, 400                             # こうかとんの画像の初期位置を指定　横:900 縦:400

    bomr = boom_cre(255, 0, 0)   # 爆弾を生成
    vxr, vyr = 1, 1              # 爆弾の初期移動速度を指定 vx〇:横方向速度 vy〇:縦方向速度
    bomg = boom_cre(0, 255, 0)
    vxg, vyg = 2, 2
    bomb = boom_cre(0, 0, 255)
    vxb, vyb = 1, 1

    while True:          # 無限ループ
        screen_img.blit(bg_img, bg_rect)        # 背景のSurfaceクラスを貼り付け
        screen_img.blit(tori_img, tori_rect)    # こうかとんのSurfaceクラスを貼り付け
        screen_img.blit(bomr[0], bomr[1])       # 爆弾のSurfaceクラスを貼り付け
        screen_img.blit(bomg[0], bomg[1])       # 爆弾のSurfaceクラスを貼り付け
        screen_img.blit(bomb[0], bomb[1])       # 爆弾のSurfaceクラスを貼り付け

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

        pg.Rect.move_ip(bomr[1], (vxr, vyr))               # 爆弾をvx, vy にしたがって移動させる
        if bomr[1][0] <= 0 or bomr[1][0] >= 1600:          # 爆弾の移動先が横方向から画面外に行く場合
            vxr = -vxr                                     # 横方向の移動速度の符号を反転させる
        if bomr[1][1] <= 0 or bomr[1][1] >= 900:           # 爆弾の移動先が縦方向から画面外に行く場合
            vyr = -vyr                                     # 縦方向の移動速度の符号を反転させる

        pg.Rect.move_ip(bomg[1], (vxg, vyg))               # 爆弾をvx, vy にしたがって移動させる
        if bomg[1][0] <= 0 or bomg[1][0] >= 1600:          # 爆弾の移動先が横方向から画面外に行く場合
            vxg = -vxg                                     # 横方向の移動速度の符号を反転させる
        if bomg[1][1] <= 0 or bomg[1][1] >= 900:           # 爆弾の移動先が縦方向から画面外に行く場合
            vyg = -vyg                                     # 縦方向の移動速度の符号を反転させる

        pg.Rect.move_ip(bomb[1], (vxb, vyb))               # 爆弾をvx, vy にしたがって移動させる
        if bomb[1][0] <= 0 or bomb[1][0] >= 1600:          # 爆弾の移動先が横方向から画面外に行く場合
            if vxb >= 0:                                   # 横方向の速度の符号が＋の場合
                vxb = -(vxb+1)                             # 1足して横方向の移動速度の符号を反転させる
            else:                                          # 横方向の速度の符号が-の場合
                vxb = -(vxb-1)                             # 1引いて横方向の移動速度の符号を反転させる
        if bomb[1][1] <= 0 or bomb[1][1] >= 900:           # 爆弾の移動先が縦方向から画面外に行く場合
            if vyb >= 0:                                   # 縦方向の速度の符号が＋の場合
                vyb = -(vyb+1)                             # 1足して縦方向の移動速度の符号を反転させる
            else:                                          # 縦方向の速度の符号が＋の場合
                vyb = -(vyb-1)                             # 1引いて縦方向の移動速度の符号を反転させる

        banr = pg.Rect.colliderect(tori_rect, bomr[1])     # こうかとんが爆弾にぶつかったかを判定
        bang = pg.Rect.colliderect(tori_rect, bomg[1])     # こうかとんが爆弾にぶつかったかを判定
        banb = pg.Rect.colliderect(tori_rect, bomb[1])     # こうかとんが爆弾にぶつかったかを判定

        if banr == True or bang == True or banb == True:            # こうかとんが爆弾にぶつかった場合
            fall_img = pg.image.load("fig/8.png")                   # こうかとんの8の画像のSurfaceクラスを作成
            fall_img = pg.transform.rotozoom(fall_img, 180, 2.0)    # こうかとんの画像の角度を反転、大きさを2倍に設定
            fall_rect = fall_img.get_rect()                         # こうかとんの画像のRectクラスのオブジェクトを生成
            fall_rect.center = tori_rect[0]+40, tori_rect[1]+50     # こうかとんがぶつかった場所の座標を微調整し画像の位置に設定
            screen_img.blit(fall_img, fall_rect)                    # こうかとんのSurfaceクラスを貼り付け
            ed = datetime.datetime.now()                            # 終了した時間を取得
            time = (ed-st).seconds                                  # 何秒間逃げ続けたかを計算
            tkm.showinfo("爆発", f"こうかとんは{time}秒耐えました")    # 結果を表示する
            return                                                  # main関数から抜ける

        pg.display.update()           # 画面を更新
        clock.tick(1000)              # 1000fps(1秒)の時を刻む


if __name__ == "__main__":
    pg.init()            # pygameモジュールを初期化
    main()               # main関数を呼び出す
    pg.quit()            # pygameモジュールの初期化を解除
    sys.exit()           # プログラムを終了