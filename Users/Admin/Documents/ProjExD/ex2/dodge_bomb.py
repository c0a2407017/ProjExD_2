import os
import random
import sys
import time
import pygame as pg

#こうかとんの動きの速さ
WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP : (0,-5),
    pg.K_DOWN : (0,5),
    pg.K_LEFT : (-5,0),
    pg.K_RIGHT : (5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_boud(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとん、爆弾rect
    戻り値：判定結果(tuple)
    画面内ならTrue,逆はFalse
    """
    yoko,tate=True,True
    if rct.left < 0 or WIDTH < rct.right:  # 横判定
        yoko=False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦判定
        tate=False
    return yoko,tate



def gameover(screen: pg.Surface) -> None:  # ゲームオーバー関数   
    print("test")
    overlay = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(overlay,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    overlay.set_alpha(128)
    screen.blit(overlay,[0,0])
    font = pg.font.Font(None,80)
    txt = font.render("Game over",True,(255,255,255))
    screen.blit(txt,[430,260])
    img=pg.image.load("fig/8.png")
    img1=img
    screen.blit(img, [370, 260])
    screen.blit(img1, [770, 260])
    pg.display.update()
    time.sleep(5)
    

def bomb():
    bb_dict={}
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_dict[r,bb_img]
    return bb_accs,bb_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_img = pg.Surface((20,20))
    #爆弾をランダムで出現
    

    bb_img.set_colorkey((0,0,0))
    bb_rct= bb_img.get_rect()
    bb_rct.center= random.randint(0,WIDTH),random.randint(0,HEIGHT)

    vx=5
    vy=5
    #背景
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 


        if kk_rct.colliderect(bb_rct):
            gameover(screen) 
            return
            

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key , mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]          
        kk_rct.move_ip(sum_mv)
        if check_boud(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])


        bb_rct.move_ip(vx,vy)
        yoko,tate=check_boud(bb_rct)
        if not yoko:
            vx *=-1
        if not tate:
            vy *=-1


        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
