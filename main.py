import pygame
import random
import os

#  high DPI mode
os.environ['SDL_VIDEO_HIGHDPI_FULLSCREEN_SPACES'] = '1'
os.environ['SDL_VIDEO_ALLOW_HIGHDPI'] = '1'

# Pygameの初期設定
pygame.init()

screen_info = pygame.display.Info()  # スクリーンサイズの取得
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h  # 画面解像度を取得
print(f"Screen resolution: {WIDTH} x {HEIGHT}")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # フルスクリーンモード
pygame.display.set_caption("Blackjack Game")
font = pygame.font.SysFont("arial", 24)

def display_text(text, x, y, color=(255, 255, 255), size=24):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# 背景画像の読み込み
current_dir = os.path.dirname(__file__)  # スクリプトのあるディレクトリ
background_path = os.path.join(current_dir,"Game", "assets", "background.jpg")
background_image = pygame.image.load(background_path)
#background_image = pygame.image.load("background.jpg")  # 背景画像ファイル名
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # 画面サイズに合わせて拡大/縮小
#DEFAULT_MENU_BACKGROUND = "Game","assets","main menu","Main_menu.jpg"  # デフォルトの背景画像
DEFAULT_MENU_BACKGROUND = os.path.join(current_dir,"Game", "assets", "main menu", "Main_menu.jpg")
menu_background_path = DEFAULT_MENU_BACKGROUND  # 動的に変更可能

def load_menu_background(path):
    """メニュー背景画像を読み込む"""
    try:
        return pygame.image.load(path).convert()
    except FileNotFoundError:
        print(f"Error: Background image '{path}' not found. Using default background.")
        return pygame.image.load(DEFAULT_MENU_BACKGROUND).convert()
    

def handle_mouse_hover(options, mouse_pos, start_y, option_height, font_size):
    """
    Determine which menu option is hovered over by the mouse.
    """
    for i, option in enumerate(options):
        option_rect = pygame.Rect(WIDTH // 2 - 100, start_y + i * option_height, 200, font_size)
        if option_rect.collidepoint(mouse_pos):
            return i
    return -1

#メインメニュークラス
def show_main_menu():
    menu_running = True
    selected_option = 0  # 選択肢のインデックス
    options = ["Start Game", "Exit"]

def draw_controls(screen):
    """
    Display the controls for Hit and Stand in the game screen.
    """
    font = pygame.font.Font(None, 24)  # フォント設定
    text_color = (255, 255, 255)  # 白色
    background_color = (0, 0, 0)  # 黒色
    padding = 10

    # ヒットとスタンドのテキスト
    hit_text = font.render("Hit: Press H", True, text_color, background_color)
    stand_text = font.render("Stand: Press S", True, text_color, background_color)

    # 表示位置の計算（右下）
    screen_width, screen_height = screen.get_size()
    hit_text_rect = hit_text.get_rect(bottomright=(screen_width - padding, screen_height - 50))
    stand_text_rect = stand_text.get_rect(bottomright=(screen_width - padding, screen_height - 20))

    # 表示（画面に描画）
    screen.blit(hit_text, hit_text_rect)
    screen.blit(stand_text, stand_text_rect)

def draw(screen, background, player_hand, dealer_hand, game_message):
    """
    Draw the game screen with all components, including hands, messages, and controls.
    """
    # 背景描画
    screen.blit(background, (0, 0))

    # プレイヤーとディーラーの手札を描画
    draw_hand(screen, player_hand, (50, 300), "Player")
    draw_hand(screen, dealer_hand, (50, 50), "Dealer")

    # メッセージ描画
    font = pygame.font.Font(None, 36)
    text = font.render(game_message, True, (255, 255, 255))
    screen.blit(text, (50, 500))

    # 操作方法の表示
    draw_controls(screen)

    # 描画内容を更新
    pygame.display.flip()

# カードとプレイヤーのクラス
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()
    
    def get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

class Player:
    def __init__(self):
        self.hand = []
    
    def add_card(self, card):
        self.hand.append(card)

    def calculate_hand(self):
        value = sum(card.value for card in self.hand)
        aces = sum(1 for card in self.hand if card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

# デッキ生成関数
def generate_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

# ブラックジャックのメインゲームループ
    pygame.quit()


# ブラックジャックのメインゲームループ
def game_loop():
    show_main_menu()
    deck = generate_deck()
    player = Player()
    dealer = Player()

    # プレイヤーとディーラーに最初の2枚を配る
    player.add_card(deck.pop())
    player.add_card(deck.pop())
    dealer.add_card(deck.pop())
    dealer.add_card(deck.pop())
    
    player_turn = True
    running = True
    clock = pygame.time.Clock()
    result = None  # 結果を表示するための変数

    while running:
        screen.blit(background_image, (0, 0))  # 背景画像を描画

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and player_turn:
                if event.key == pygame.K_h:  # 'h'キーでヒット
                    player.add_card(deck.pop())
                    if player.calculate_hand() > 21:
                        player_turn = False  # プレイヤーがバストしたらターン終了
                elif event.key == pygame.K_s:  # 's'キーでスタンド
                    player_turn = False
                elif event.key == pygame.K_ESCAPE:  # ESCキーでウィンドウを閉じる
                    running = False

        # プレイヤーの手札を表示
        display_text("Player's Hand:", 50, HEIGHT - 200)
        for idx, card in enumerate(player.hand):
            display_text(f"{card.rank} of {card.suit}", 50, HEIGHT - 170 + idx * 30)
        player_score = player.calculate_hand()
        display_text(f"Player Score: {player_score}", 50, HEIGHT - 70)

        # ディーラーの手札を表示（1枚伏せる）
        display_text("Dealer's Hand:", WIDTH - 350, 100)
        if player_turn:
            display_text(f"{dealer.hand[0].rank} of {dealer.hand[0].suit}", WIDTH - 350, 130)
            display_text("Hidden Card", WIDTH - 350, 160)
        else:
            for idx, card in enumerate(dealer.hand):
                display_text(f"{card.rank} of {card.suit}", WIDTH - 350, 130 + idx * 30)
            dealer_score = dealer.calculate_hand()
            display_text(f"Dealer Score: {dealer_score}", WIDTH - 350, 230)

        # ゲーム終了条件のチェック
        if not player_turn and result is None:
            # ディーラーのターン
            dealer_score = dealer.calculate_hand()
            while dealer_score < 17:
                dealer.add_card(deck.pop())
                dealer_score = dealer.calculate_hand()

            # 勝敗の判定
            if player_score > 21:
                result = "Player Busts! Dealer Wins!"
            elif dealer_score > 21:
                result = "Dealer Busts! Player Wins!"
            elif player_score > dealer_score:
                result = "Player Wins!"
            elif player_score < dealer_score:
                result = "Dealer Wins!"
            else:
                result = "It's a Tie!"
        
        # 結果を表示
        if result:
            display_text(result, WIDTH // 2 - 100, HEIGHT // 2)

        pygame.display.flip()
        clock.tick(30)

def how_to_play_screen():
    """How to Playの説明画面"""
    running = True
    background = load_menu_background(menu_background_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # 背景画像を調整

    # フォントを指定
    font_path = os.path.join(current_dir, "Game", "assets", "fonts", "NotoSans-Italic-VariableFont_wdth,wght.ttf")
    title_font = pygame.font.Font(font_path, 50)  # タイトル用の大きいフォント
    text_font = pygame.font.Font(font_path, 30)  # 説明文用のフォント

    # How to Playの内容
    instructions = [
        "Welcome to Blackjack!",
        "Objective: Get as close to 21 as possible without exceeding it.",
        "Card Values:",
        "- Number cards: Face value",
        "- Face cards (J, Q, K): 10 points each",
        "- Ace: 1 or 11 points",
        "",
        "Controls:",
        "- 'H' to Hit (draw a card)",
        "- 'S' to Stand (end your turn)",
        "- 'Esc' to Exit",
    ]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESCキーでメインメニューに戻る
                    running = False

        # 背景を描画
        screen.blit(background, (0, 0))

        # タイトルを描画
        title_surface = title_font.render("How to Play", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)

        # 説明文を描画
        for i, line in enumerate(instructions):
            text_surface = text_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topleft=(50, 200 + i * 40))
            screen.blit(text_surface, text_rect)

        # メッセージを表示（メインメニューに戻る方法）
        back_text = text_font.render("Press ESC to return to Main Menu", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(back_text, back_rect)

        # 画面更新
        pygame.display.flip()

    # メインメニューに戻る
    main_menu()


def main_menu():
    """メインメニューを表示する"""
    running = True
    background = load_menu_background(menu_background_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # 画面サイズに調整

    options = ["Start Game", "How to play", "Exit"]

    # フォントを指定
    font_path = os.path.join(current_dir, "Game", "assets", "fonts", "NotoSans-Italic-VariableFont_wdth,wght.ttf")
    font_size = 40  # フォントサイズ
    menu_font = pygame.font.Font(font_path, font_size)

    while running:
        mouse_pos = pygame.mouse.get_pos()  # マウスカーソルの位置を取得

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左クリック
                    for i, option in enumerate(options):
                        # オプションの矩形を計算
                        text_surface = menu_font.render(option, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + i * 70))
                        if text_rect.collidepoint(mouse_pos):  # マウスが矩形内にある場合
                            if options[i] == "Start Game":
                                running = False  # メインメニューを終了
                                game_loop()  # ゲームループを開始
                            elif options[i] == "How to play":
                                running = False
                                how_to_play_screen()
                            elif options[i] == "Exit":
                                pygame.quit()
                                exit()

        # 背景を描画
        screen.blit(background, (0, 0))

        # メニューオプションを描画
        for i, option in enumerate(options):
            # マウスがオプションの上にあるかをチェック
            text_surface = menu_font.render(option, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + i * 70))
            if text_rect.collidepoint(mouse_pos):  # マウスが文字に重なっている場合
                color = (255, 255, 0)  # 選択された色
            else:
                color = (255, 255, 255)  # 通常の色

            # テキストを描画
            text_surface = menu_font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + i * 70))
            screen.blit(text_surface, text_rect)

        # 画面更新
        pygame.display.flip()

    pygame.quit()

# ゲームの実行（エントリーポイント）
if __name__ == "__main__":
    main_menu()

# ゲームの実行
game_loop()

