import pygame as pg, sys
import random

pg.init()
screen = pg.display.set_mode((800, 600))
## 自機データ
myship_speed = 5
myimg = pg.image.load("assets/images/myship.png")
myimg = pg.transform.scale(myimg, (50, 50))
myrect = pg.Rect(400, 500, 50, 50)
## 弾
bulletimg = pg.image.load("assets/images/bullet.png")
bulletimg = pg.transform.scale(bulletimg, (16, 16))
bulletrect = pg.Rect(400, -100, 16, 16)
# replay = pg.image.load("")
## 敵
ufoimg = pg.image.load("assets/images/ufo.png")
ufoimg = pg.transform.scale(ufoimg, (50, 50))
ufos = []
ufo_speeds = [] # 各UFOの横方向の速度
ufo_direction = 1 # 1:右へ, -1:左へ (全体で共有)
ufo_drop_speed = 10 # UFOが一段落ちる時の速度

for yy in range(4):
    for xx in range(7):
        ufos.append(pg.Rect(50+xx*100, 40+yy*50, 50, 50)) # UFOのサイズを50,50に修正
        ufo_speeds.append(2) # 初期速度

pushFlag = False
page = 1
# score = 0

replay_img = pg.image.load("assets/images/ufo.png")
## btnを押したら、newpageにジャンプ
def button_to_jamp(btn, newpage):
    global page, pushFlag
    # ユーザーからの入力を調べる
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]:
        # pg.mixer.Sound("").play()
        if btn.collidepoint(mx, my) and pushFlag == False:
            page = newpage
            pushFlag = True
        else:
            pushFlag = False
            
## ゲームステージ
def gamestage():
    # 画面初期化
    global vx, vy, can_shoot
    global page
    # global score
    global ufo_direction
    screen.fill(pg.Color("BLACK"))
    # ユーザーからの入力を調べる
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]: ##左
        myrect.x -= myship_speed
    if keys[pg.K_RIGHT]:
        myrect.x += myship_speed
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    #絵をかいたり、判定したりする
    ## 自機の処理
    # myrect.x = mx - 25
    screen.blit(myimg, myrect)
    ## 弾の処理
    if keys[pg.K_SPACE] and bulletrect.y < 0 and can_shoot:
        bulletrect.x = myrect.x + 25 - 8
        bulletrect.y = myrect.y
        # pg.mixer.Sound("").play()
        can_shoot = False # 弾が発射されたら連射を禁止
    if mdown[0] and bulletrect.y < 0:
        bulletrect.x = myrect.x + 25 - 8
        bulletrect.y = myrect.y
        # pg.mixer.Sound("").play()
    if bulletrect.y >= 0:
        bulletrect.y += -15
        screen.blit(bulletimg, bulletrect)
    else:
        can_shoot = True 
    ## 敵の処理
    # 画面端に到達したUFOがあるかチェック
    hit_edge = False
    for i, ufo in enumerate(ufos):
        # ufoの横移動
        ufo.x += ufo_speeds[i] * ufo_direction
        # 画面端到達したか判定
        if ufo.right > 800 or ufo.left < 0:
            hit_edge = True
        ## 弾とufoの衝突処理
        if ufo.colliderect(bulletrect):
            # score += 1000
            ufo.y = -100
            ufo.x = random.randint(0, 750)
            bulletrect.y = -100
            # pg.mixer.Sound("").play()
        screen.blit(ufoimg, ufo)
    # 画面端に到達していたら方向を反転し、一段下に移動
    if hit_edge:
        ufo_direction *= -1
        for ufo in ufos:
            ufo.y += ufo_drop_speed
    # スコア
    # score = score + 10
    # font = pg.font.Font(None, 40)
    # text = font.render("SCORE : "+str(score), True, pg.Color("WHITE"))
    # screen.blit(text, (20, 20))
## データのリセット
def gamereset():
    # global score
    # score = 0
    global can_shoot, pushFlag
    myrect.x = 400
    myrect.y = 500
    bulletrect.y = -100
    can_shoot = True
    pushFlag = False
    for i in range(10):
        ufos[i] = pg.Rect(random.randint(0, 800), -100 * i, 50, 50)
## ゲームオーバー
def gameover():
    screen.fill(pg.Color("BLACK"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("RED"))
    screen.blit(text, (20, 20))
    btn1 = screen.blit(replay_img,(320, 480))
    font = pg.font.Font(None, 40)
    # text = font.render("SCORE : "+str(score), True, pg.Color("WHITE"))
    # 絵をかいたり、判定したりする
    button_to_jamp(btn1, 1)
    ## ボタンを押してリプレイしたら、ゲームをリセット
    if page == 1:
        gamereset()
        
# この下をずっとループ
while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()
    # 画面を表示
    pg.display.update()
    pg.time.Clock().tick(60)
    # 閉じるボタンを押したら終了
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()