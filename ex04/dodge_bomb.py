import pygame as pg
import sys

def main():
    pg.display.set_caption("逃げろ!こうかとん")
    screen_img = pg.display.set_mode((1600, 900))
    screen_rect = screen_img.get_rect()

    bg_img = pg.image.load("fig/pg_bg.jpg")
    bg_rect = bg_img.get_rect()

    screen_img.blit(bg_img, bg_rect)

    pg.display.update()
    clock = pg.time.Clock()
    clock.tick(0.5)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()