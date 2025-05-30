import pygame as pg, sys
import random
from pygame import mixer

pg.init()
mixer.init()
screen = pg.display.set_mode((800, 600))
##BGM
mixer.music.load("assets/sounds/black-box-cozy-forest-122347.mp3")
mixer.music.play(-1)

## 自機データ
myship_speed = 5
myimg = pg.image.load("assets/images/myship2.png")
myimg = pg.transform.scale(myimg, (50, 50))
myrect = pg.Rect(400, 500, 50, 50)
## 自機の弾
bulletimg = pg.image.load("assets/images/laser.png")
bulletimg = pg.transform.scale(bulletimg, (16, 16))
bulletrect = pg.Rect(400, -100, 16, 16)
# replay = pg.image.load("")
## 敵
ufoimg = pg.image.load("assets/images/enemy1_1.png")
ufoimg = pg.transform.scale(ufoimg, (50, 50))
ufos = []
ufo_speeds = [] # 各UFOの横方向の速度
ufo_direction = 1 # 1:右へ, -1:左へ (全体で共有)
ufo_drop_speed = 10 # UFOが一段落ちる時の速度
# 敵の弾
enemy_bullet_img = pg.image.load("assets/images/enemy_bullet.png")
enemy_bullet_img = pg.transform.scale(enemy_bullet_img, (16, 16))
enemy_bullets = [] # 敵の弾リスト(Rectのリスト)

heart_img = pg.image.load("assets/images/heart.png")
heart_img = pg.transform.scale(heart_img, (30, 30)) # サイズ調整
for yy in range(4):
    for xx in range(7):
        ufos.append(pg.Rect(50+xx*100, 40+yy*50, 50, 50)) # UFOのサイズを50,50に修正
        ufo_speeds.append(2) # 初期速度

pushFlag = False
page = 1 # 1: ゲーム, 2: ゲームオーバー, 3: ヘルプ
player_life = 3
# score = 0

replay_img = pg.image.load("assets/images/enemy1_1.png")
## btnを押したら、newpageにジャンプ
def button_to_jamp(btn, newpage):
    global page, pushFlag
    # ユーザーからの入力を調べる
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]: # マウスボタンが押されている
        # pg.mixer.Sound("").play()
        if btn.collidepoint(mx, my) and not pushFlag:
            page = newpage
            pushFlag = True # ボタン押下済みとマーク
        else:
            pushFlag = False # ボタンを離したことを検出
            
## ゲームステージ
def gamestage():
    # 画面初期化
    global vx, vy, can_shoot
    global page
    # global score
    global ufo_direction
    global player_life
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
    ## 自機の弾の処理
    if keys[pg.K_SPACE] and bulletrect.y < 0 and can_shoot:
        bulletrect.x = myrect.x + 25 - 8
        bulletrect.y = myrect.y
        pg.mixer.Sound("assets/sounds/ビーム砲1.mp3").play()
        can_shoot = False # 自機の弾が発射されたら連射を禁止
    if mdown[0] and bulletrect.y < 0:
        bulletrect.x = myrect.x + 25 - 8
        bulletrect.y = myrect.y
        pg.mixer.Sound("assets/sounds/ビーム砲1.mp3").play()
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
        ## 自機の弾とufoの衝突処理
        if ufo.colliderect(bulletrect) and ufo.width > 0:
            # score += 1000
            ufo.width = 0   # UFOの幅を0にする
            ufo.height = 0  # UFOの高さを0にする
            # ufo.y = -1000
            # ufo.x = random.randint(0, 750)
            bulletrect.y = -100
            # pg.mixer.Sound("").play()
        if ufo.width > 0:
            screen.blit(ufoimg, ufo)
        # screen.blit(ufoimg, ufo)
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
    ## UFOの弾を発射(ランダムに発射)
    if random.randint(0, 60) == 0 and len(ufos) > 0: # 約1秒に1回
        shooter = random.choice(ufos)
        enemy_bullets.append(pg.Rect(shooter.centerx - 8, shooter.bottom, 16, 16))
    # 敵の弾の処理
    for bullet in enemy_bullets[:]:
        bullet.y += 10
        screen.blit(enemy_bullet_img, bullet)
        # 自機に当たったらライフを減らす
        if bullet.colliderect(myrect):
            player_life -= 1
            enemy_bullets.remove(bullet)
            if player_life <= 0:
                page = 2 # ゲームオーバー画面へ
        # 画面外に出た弾を削除
        if bullet.top > 600:
            enemy_bullets.remove(bullet)
    # ライフ表示
    font = pg.font.Font(None, 40)
    text = font.render("LIFE : "+str(player_life), True, pg.Color("WHITE"))
    screen.blit(text, (20, 560))
    # ハートアイコンで残機表示(左下)
    for i in range(player_life):
        screen.blit(heart_img, (130 + i * 35, 560)) # 画面左下に並べて表示
    text_help = font.render("H:HELP", True, pg.Color("WHITE"))
    screen.blit(text_help, (700, 560))
## データのリセット
def gamereset():
    # global score
    # score = 0
    global can_shoot, pushFlag
    global enemy_bullets
    global player_life
    global ufo_direction
    # score = 0
    player_life = 3
    enemy_bullets = []
    myrect.x = 400
    myrect.y = 500
    bulletrect.y = -100
    can_shoot = True
    pushFlag = False
    ufo_direction = 1
    ufos.clear()
    ufo_speeds.clear()
    for yy in range(4):
        for xx in range(7):
            ufos.append(pg.Rect(50+xx*100, 40+yy*50, 50, 50)) # UFOのサイズを50,50に修正
            ufo_speeds.append(2) # 初期速度
## ゲームオーバー
def gameover():
    screen.fill(pg.Color("BLACK"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("RED"))
    screen.blit(text, (20, 20))
    btn1 = screen.blit(replay_img,(320, 480))
    font = pg.font.Font(None, 40)
    font = pg.font.Font(None, 40)
    text = font.render("LIFE : 0", True, pg.Color("WHITE"))
    screen.blit(text, (20, 180))
    # text = font.render("SCORE : "+str(score), True, pg.Color("WHITE"))
    # 絵をかいたり、判定したりする
    button_to_jamp(btn1, 1)
    ## ボタンを押してリプレイしたら、ゲームをリセット
    if page == 1:
        gamereset()
def help_page():
    global page, pushFlag
    screen.fill(pg.Color("BLACK"))
    # (ここから下に通常の描画やボタンの処理を書く)
    jp_font = pg.font.Font("assets/fonts/NotoSansJP-Regular.ttf", 30)
    font_title = pg.font.Font(None, 80)
    font_text = pg.font.Font(None, 40)
    title = font_title.render("HELP", True, pg.Color("WHITE"))
    screen.blit(title, (330, 40))
    help_text = [
        "== 操作方法 ==",
        "← → : 自機の移動",
        "スペースキー or マウス左クリック : 弾を発射",
        "Hキー : ヘルプ表示",
        "戻るには Bキー を押してください"
        "",
        "== ゲームルール ==",
        "・敵のUFOをすべて倒そう",
        "・敵の弾に当たるとライフが減る",
        "・ライフが0になるとゲームオーバー",
        ""
    ]
    for i, line in enumerate(help_text):
        text = jp_font.render(line, True, pg.Color("WHITE"))
        screen.blit(text, (100, 150 + i * 40))
    keys = pg.key.get_pressed()
    if keys[pg.K_b]: # Bキーで戻る
        global page
        page = 1
            
# この下をずっとループ
while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()
    elif page == 3:
        help_page()
    # 画面を表示
    pg.display.update()
    pg.time.Clock().tick(60)
    # 閉じるボタンを押したら終了
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_h and page == 1:
                page = 3 # ヘルプ画面に遷移