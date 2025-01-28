import pygame
import asyncio

# 画面サイズ設定
SCR_W = 800
SCR_H = 600

pygame.init()
screen = pygame.display.set_mode((SCR_W, SCR_H))
clock = pygame.time.Clock()

# 画面状態ID
ST_TITLE = 0
ST_MAIN_GAME = 1
ST_RESULT = 2


# ********************************************


class Card:
    def __init__(self, x, y, width, height, color, image_path, card_word):
        """
        カードの初期設定。位置やサイズ、色、画像、単語を設定する。
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.dragging = False
        # ドラッグ中かどうか
        self.offset_x = 0
        # ドラッグ時のオフセット
        self.offset_y = 0
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.word = card_word

    def draw(self, screen):
        """
        カードを画面に描画する
        """
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.image, self.rect)

    def handle_event(self, event, blank):
        """
        カードのドラッグ操作を処理する
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            # カードの位置を適切な場所に移動
            for target in blank:
                if (target[0] < self.rect.x + 50 < target[0] + 100) and (
                        target[1] < self.rect.y + 50 < target[1] + 100):
                    self.rect.x = target[0]
                    self.rect.y = target[1]
                    pygame.display.update()
                    pygame.display
                    # 枠のIDの値と一致するところに、画像の読みを入れる。
                    # 最終的に、画面に表示されている順番に、画像の読みが並んだリストになる。
                    # つまり、しりとりが成立している並びかチェックできるようになる。
                    return target[2]

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # ドラッグ中はカードをマウスに合わせて動かす
                self.rect.x = event.pos[0] + self.offset_x
                self.rect.y = event.pos[1] + self.offset_y

        return -2

    def get_last_char(self):
        """
        カードの単語の最後の文字を返す（しりとり用）
        """
        return self.word[-1]

    def get_first_char(self):
        """
        カードの単語の最初の文字を返す（しりとり用）
        """
        return self.word[0]


class Bord:
    def __init__(self):
        """
        画像設置位置の座標を設定する
        """
        self.rect = None
        self.blank = []
        # 6つの枠位置を作成（X座標とY座標）
        for W in range(5):
            self.blank.append((W * (100 + 50) + 50, 80, W))  # 横座標、縦座標、枠のID（順番を記録するため）
        for W in range(5):
            self.blank.append((W * (100 + 50) + 50, 200, W + 5))  # 横座標、縦座標、枠のID（順番を記録するため）

    def draw(self, screen):
        """
        画像設置位置の枠線を描画する
        """
        for target in self.blank:
            self.rect = pygame.Rect(target[0] - 1, target[1] - 1, 101, 101)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 5)


class state:
    """
    状態を管理する基底クラス
    """
    name = "NoName"
    font = None

    def __init__(self, font):
        self.font = font

    def handle_event(self, event):
        pass

    def draw(self):
        pass


class title(state):
    """
    タイトル画面の状態を管理
    """
    text_surface = None

    def __init__(self, font):
        super().__init__(font)
        self.text_surface = self.font.render("title", True, (255, 255, 255))
        self.name = "title"
        self.image = pygame.image.load("resource/cake7.jpg")
        self.image = pygame.transform.scale(self.image, (800, 600))
        # img_char = pygame.image.load("resource/cake7.jpg")
        self.rect = (0, 0, 0, 0)

    def handle_event(self, event):
        """
        マウスクリックでメインゲームに遷移
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            return ST_MAIN_GAME
        else:
            return ST_TITLE

    def draw(self, screen):
        """
        タイトル画面を描画
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, (10, 10))


class mainGame(state):
    """
    メインゲームの状態を管理
    """

    def __init__(self, font):
        super().__init__(font)
        self.temp = None
        self.display_words = None
        self.text_surface = font.render("mainGame", True, (0, 0, 255))
        self.name = "mainGame"
        self.image = pygame.image.load("resource/cake7.jpg")

        # ゲームで使用するカードを作成
        self.cards = [
            Card(100, 400, 100, 100, (0, 0, 0), "resource/cake7.jpg", "けーき"),
            Card(200, 400, 100, 100, (0, 0, 0), "resource/fox7.jpg", "きつね"),
            Card(300, 400, 100, 100, (0, 0, 0), "resource/cat7.jpg", "ねこ"),
            Card(400, 400, 100, 100, (0, 0, 0), "resource/compass7.jpg", "こんぱす"),
            Card(500, 400, 100, 100, (0, 0, 0), "resource/watermelon7.jpg", "すいか"),
            Card(100, 500, 100, 100, (0, 0, 0), "resource/card7.jpg", "かーど"),
            Card(200, 500, 100, 100, (0, 0, 0), "resource/doughnut7.jpg", "どーなつ"),
            Card(300, 500, 100, 100, (0, 0, 0), "resource/fishing7.jpg", "つり"),
            Card(400, 500, 100, 100, (0, 0, 0), "resource/apple7.jpg", "りんご"),
            Card(500, 500, 100, 100, (0, 0, 0), "resource/gorilla7.jpg", "ごりら"),

        ]

        # 画像設置位置の枠
        self.bord = Bord()
        self.used_words = []

        # ボタンの当たり判定
        self.button_rect = pygame.Rect(SCR_W - 100, SCR_H - 100, SCR_W - 50, SCR_H - 50)

        # しりとりの使った単語
        self.sequence_words = []
        self.current_word = ""  # 現在のしりとりの単語

        # 　画像の並び順の記録用
        self.bord_chain = [None] * len(self.bord.blank)

        # 答え合わせモードかどうか
        self.check_flag = False
        # しりとりが成立しているかどうか
        self.answer_flag = True

    def handle_event(self, event):
        """
        ゲーム内でのイベント処理
        """
        for card in self.cards:
            self.temp = card.handle_event(event, self.bord.blank)
            if not self.temp == -2:
                print(self.temp)
                self.bord_chain[self.temp] = card

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(self.bord_chain)
            if self.button_rect.collidepoint(event.pos):
                if self.check_flag:
                    self.check_flag = False
                    self.bord_chain = [None] * len(self.bord.blank)
                else:
                    self.current_word = ""
                    self.answer_flag = True
                    self.shiritori()

        return ST_MAIN_GAME

    def shiritori(self):
        print("チェック")
        # 配置されたカードがしりとりのルールに従っているか確認
        for card in self.bord_chain:
            if card is None:
                break
            if self.current_word == "":  # 最初のカードの場合
                self.current_word = card.word
                self.used_words.append(card.word)
            else:
                if card.get_first_char() == self.current_word[-1]:  # しりとりのルールチェック
                    self.current_word = card.word
                    self.used_words.append(card.word)
                else:
                    self.answer_flag = False
                    break
        self.check_flag = True

    def draw(self, screen):
        """
        メインゲーム画面を描画
        """
        screen.blit(self.text_surface, (10, 10))
        self.bord.draw(screen)
        # screen.blit(self.image, self.rect)
        # カードを描画
        for card in self.cards:
            card.draw(screen)

        pygame.draw.rect(screen, (255, 255, 0), self.button_rect)

        # 現在のしりとりの進行状況を表示
        if self.check_flag and self.answer_flag:
            self.display_words = "正解！："
            for cWord in self.bord_chain:
                if cWord:
                    self.display_words = self.display_words + cWord.word + ">"
                else:
                    break
            word_surface = self.font.render(f"{self.display_words}", True, (255, 0, 0))
        elif self.check_flag:
            word_surface = self.font.render("間違いがあります！右下の四角をクリックしてください。", True, (255, 0, 0))
        else:
            word_surface = self.font.render("並べ終えたら右下の黄色の四角をクリックしてください。", True, (255, 0, 0))

        screen.blit(word_surface, (10, 40))

async def main():
    """
    ゲームのメインループ
    """
    going = True
    font = pygame.font.Font("ipaexg.ttf", 19)
    screen.fill((220, 220, 220))

    # ゲーム状態を管理するオブジェクト
    states = [title(font), mainGame(font)]
    # currentState = ST_TITLE
    currentState = ST_MAIN_GAME

    # ゲームのメインループ
    while going:
        # イベントを取得。イベントとは、マウスの操作やキーボードの操作等。
        # イベントの発生が無い場合、このfor文は動かない。
        for event in pygame.event.get():
            screen.fill((220, 220, 220))
            states[currentState].draw(screen)

            # 終了イベント（画面の×ボタン押下など）の場合、ループを抜ける
            if event.type == pygame.QUIT:
                going = False

            # 発生したイベントに応じてゲームの状態を変更する
            currentState = states[currentState].handle_event(event)

        pygame.display.update()
        await asyncio.sleep(0)  # You must include this statement in your main loop. Keep the argument at 0.
        clock.tick(60)

    pygame.quit()


asyncio.run(main())
