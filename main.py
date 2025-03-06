import random
import pygame

pygame.init()

width, height = 1366, 768
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blackjack")

white = (255, 255, 255)
green = (0, 128, 0)
violet = (204, 153, 255)
black = (0, 0, 0)

font = pygame.font.Font('CreteRound.ttf', 30)
fontValue = pygame.font.Font('CreteRound.ttf', 48)

player_hand = []
dealer_hand = []
outcome = ""

card_images = {}
for suit in ["spades", "hearts", "clubs", "diamonds"]:
    for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            card_images[f"{value}_{suit}"] = pygame.image.load(f"cards/{value}_{suit}.png")
card_back = pygame.image.load("cards/card_back.png")
table_pic = pygame.image.load("table.png")


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def draw_cards(hand, y):
    spacing = 150
    x = 300
    for card in hand:
        value, suit = card.split('_')
        card_image = card_images[f"{value}_{suit}"]
        window.blit(card_image, (x, y))
        x += spacing

def deal_initial_cards(player_hand, dealer_hand):
    player_hand.append(random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]) + "_" + random.choice(["spades", "hearts", "clubs", "diamonds"]))
    dealer_hand.append(random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]) + "_" + random.choice(["spades", "hearts", "clubs", "diamonds"]))

def deal_one_card(hand):
    hand.append(random.choice(["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]) + "_" + random.choice(["spades", "hearts", "clubs", "diamonds"]))

def calculate_hand_value(hand):
    total = 0
    ace_count = 0
    for card in hand:
        value, suit = card.split('_')
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

    player_hand = []
    dealer_hand = []
    game_over = False
    quit_game = False

    deal_initial_cards(player_hand, dealer_hand)
    deal_one_card(player_hand)

    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        player_hand.clear()
                        dealer_hand.clear()
                        game_over = False
                        deal_initial_cards(player_hand, dealer_hand)
                        deal_one_card(player_hand)
                if not game_over:
                    if calculate_hand_value(player_hand) == 21:
                        outcome = "Black Jack!"
                        game_over = True
                    if event.key == pygame.K_h:
                        deal_one_card(player_hand)
                        if calculate_hand_value(player_hand) > 21:
                            outcome = "Player Bust!"
                            game_over = True
                        elif calculate_hand_value(player_hand) == 21:
                            deal_one_card(dealer_hand)
                            if dealer_hand_value == calculate_hand_value(player_hand):
                                outcome = "Push!"
                                game_over = True
                            else:
                                outcome = "You win!"
                                game_over = True
                    elif event.key == pygame.K_s:
                        while calculate_hand_value(dealer_hand) < 17:
                            deal_one_card(dealer_hand)
                        dealer_hand_value = calculate_hand_value(dealer_hand)
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

        draw_cards(player_hand, 410)
        player_hand_value = calculate_hand_value(player_hand)
        draw_text(f"Your Hand Value: {player_hand_value}", font, white, 683, 350)
        draw_text(f"{player_hand_value}", fontValue, white, 200, 500)

        window.blit(card_back, (450, 120))
        draw_cards(dealer_hand, 120)
        dealer_hand_value = calculate_hand_value(dealer_hand)
        draw_text(f"Dealer Hand Value: {dealer_hand_value}", font, white, 683, 60)
        draw_text(f"{dealer_hand_value}", fontValue, white, 200, 200)

        if game_over:
            draw_text(outcome, fontValue, violet, 1150, 350)
            draw_text("Press R to play again!", font, white, 683, 650)
        if not game_over:
            draw_text("Choose an action: [H]it or [S]tand", font, white, 683, 650)


        pygame.display.update()

    pygame.quit()

game_loop()
