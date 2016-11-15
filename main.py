import pygame
from Car import Car


class Colors:
    gray = (211, 211, 211)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)


def max(a, b):
    return a if a > b else b


def getMoveDirSecond(car, moveDir):
    print("SECOND", moveDir)
    if moveDir == (0, 0):
        return 0, 0
    else:
        return moveDir[0] + 0.03, 0


def getMoveDirFirst(car, moveDir):
    if car.rect.topleft[0] < 200:
        pass
    elif 200 <= car.rect.topleft[0] <= 400 and car.rect.topleft[1] <= 280:
        moveDir = (max(moveDir[0] - 0.03, 1.5), 0)
    elif car.rect.topleft[0] >= 400 and car.rect.topleft[1] <= 280:
        moveDir = (0, 1)
    elif 280 < car.rect.topleft[1] < 604:
        moveDir = (0, moveDir[1] + 0.1)
    return moveDir


def main():
    pygame.init()
    car = Car((0, 280))
    car2 = Car((330, 280))
    screen = pygame.display.set_mode((996, 604))
    background = pygame.image.load("images/map.png")
    done = False
    message = False
    moveDir = [(4, 0), (0, 0)]
    toRender = [car, car2]
    lightColor = Colors.red
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True
        screen.fill(Colors.gray)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.blit(background, (0, 0))
        pygame.draw.circle(screen, lightColor, (370, 350), 15)
        for c in toRender:
            screen.blit(c.image, c.rect)
        car.update()
        car2.update()
        pygame.time.Clock().tick(30)
        pygame.display.flip()
        moveDir[0] = getMoveDirFirst(car, moveDir[0])
        moveDir[1] = getMoveDirSecond(car2, moveDir[1])
        if moveDir[0] != (4, 0) and moveDir[1] == (0, 0):
            lightColor = Colors.green
            moveDir[1] = (0.8, 0)
    car.move(moveDir[0])
    car2.move(moveDir[1])
