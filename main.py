import random
import pygame

pygame.init()

width, height = 1366, 768
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blackjack")

white = (255, 255, 255)
green = (0, 128, 0)
violet = (204, 153, 255)

font = pygame.font.Font('CreteRound.ttf', 30)
fontValue = pygame.font.Font('CreteRound.ttf', 48)

suits = ["spades", "hearts", "clubs", "diamonds"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

card_images = {}
for suit in suits:
    for value in values:
            card_images[f"{value}_{suit}"] = pygame.image.load(f"cards/{value}_{suit}.png")

# card_back = pygame.image.load("cards/card_back.png") # for historic purposes
table_pic = pygame.image.load("table.png")

player_y = 410
dealer_y = 120

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x,y))
    window.blit(text_surface, text_rect)

def draw_cards(hand, y, count = None):
    spacing = 150
    x = 300
    if count is None:
        count = len(hand)
    for i in range(count):
        card = hand[i]
        value, suit = card.split('_')
        card_image = card_images[f"{value}_{suit}"]
        window.blit(card_image, (x, y))
        x += spacing

def create_deck():
    deck = [f"{value}_{suit}" for suit in suits for value in values]
    random.shuffle(deck)
    return deck

def animate_card_deal(card_image, start_pos, end_pos, animating_hand):
    steps = 20
    dx = (end_pos[0] - start_pos[0]) / steps
    dy = (end_pos[1] - start_pos[1]) / steps
    x, y = start_pos

    for _ in range(steps):
        window.blit(table_pic, (0, 0))
        if animating_hand == "player":
            draw_cards(player_hand, player_y, len(player_hand) - 1)
            draw_cards(dealer_hand, dealer_y)
        elif animating_hand == "dealer":
            draw_cards(player_hand, player_y)
            draw_cards(dealer_hand, dealer_y, len(dealer_hand) - 1)
        window.blit(card_image, (x,y))
        pygame.display.update()
        x += dx
        y += dy

def deal_initial_cards(deck, player_hand, dealer_hand):
    deal_card(deck, player_hand, player_y, "player")
    deal_card(deck, dealer_hand, dealer_y, "dealer")
    deal_card(deck, player_hand, player_y, "player")
    # deal_card(deck, dealer_hand, dealer_y, "dealer", card_override=card_back, add_to_hand=False)
    # for historic purposes

def deal_card(deck, hand, y, animating_hand):
    card = deck.pop()
    hand.append(card)
    value, suit = card.split('_')
    card_image = card_images[f"{value}_{suit}"]
    x_offset = 300 + 150 * (len(hand) - 1)
    animate_card_deal(card_image, (width // 2, 0), (x_offset, y), animating_hand)

def calculate_hand_value(hand):
    total = 0
    ace_count = 0
    for card in hand:
        value = card.split('_')[0]
        if value in ["J", "Q", "K"]:
            total += 10
        elif value == "A":
            total += 11
            ace_count += 1
        else:
            total += int(value)
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total


def game_loop():
    global player_hand, dealer_hand
    game_over = False
    quit_game = False
    outcome = ""

    deck = create_deck()
    player_hand = []
    dealer_hand = []

    deal_initial_cards(deck, player_hand, dealer_hand)

    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    deck = create_deck()
                    player_hand.clear()
                    dealer_hand.clear()
                    game_over = False
                    outcome = ""
                    deal_initial_cards(deck, player_hand, dealer_hand)

                if not game_over:
                    player_hand_value = calculate_hand_value(player_hand)

                    if player_hand_value == 21:
                        outcome = "Black Jack!"
                        game_over = True

                    if event.key == pygame.K_h:
                        deal_card(deck, player_hand, player_y, "player")
                        player_hand_value = calculate_hand_value(player_hand)
                        if player_hand_value > 21:
                            outcome = "Player Bust!"
                            game_over = True
                        elif player_hand_value == 21:
                            deal_card(deck, dealer_hand, dealer_y, "dealer")
                            dealer_hand_value = calculate_hand_value(dealer_hand)
                            if dealer_hand_value == player_hand_value:
                                outcome = "Push!"
                            else:
                                outcome = "You win!"
                            game_over = True

                    elif event.key == pygame.K_s:
                        while calculate_hand_value(dealer_hand) < 17:
                            deal_card(deck, dealer_hand, dealer_y, "dealer")
                        dealer_hand_value = calculate_hand_value(dealer_hand)
                        player_hand_value = calculate_hand_value(player_hand)

                        if dealer_hand_value > 21:
                            outcome = "Dealer Bust!"
                        elif dealer_hand_value > player_hand_value:
                            outcome = "Dealer wins!"
                        elif dealer_hand_value < player_hand_value:
                            outcome = "You win!"
                        else:
                            outcome = "Push!"
                        game_over = True

        window.blit(table_pic, (0, 0))

        # window.blit(card_back, (450, 120)) # for historic purposes
        draw_cards(dealer_hand, dealer_y)
        dealer_hand_value = calculate_hand_value(dealer_hand)
        draw_text(f"Dealer Hand Value: {dealer_hand_value}", font, white, 683, 60)
        draw_text(f"{dealer_hand_value}", fontValue, white, 200, 200)

        draw_cards(player_hand, player_y)
        player_hand_value = calculate_hand_value(player_hand)
        draw_text(f"Your Hand Value: {player_hand_value}", font, white, 683, 350)
        draw_text(f"{player_hand_value}", fontValue, white, 200, 500)

        if game_over:
            draw_text(outcome, fontValue, violet, 1150, 350)
            draw_text("Press R to play again!", font, white, 683, 650)
        else:
            draw_text("Choose an action: [H]it or [S]tand", font, white, 683, 650)

        pygame.display.update()

    pygame.quit()

game_loop()