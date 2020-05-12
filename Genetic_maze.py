import pygame
import time
import numpy as np

WIDTH = 900
HEIGHT = 600
FPS = 30

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genetic Maze")
clock = pygame.time.Clock()

running = True

pop_size = 200
chromosome_len = 1000
jump = 10
iterations = 10000
match_num = 3
penatly = 150505

def gen_maze():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 0)

    pygame.draw.rect(screen, WHITE, (100, 0, 10, 300), 0)
    pygame.draw.rect(screen, WHITE, (100, 0, 10, 300), 0)
    pygame.draw.rect(screen, WHITE, (200, 200, 10, 300), 0)
    pygame.draw.rect(screen, WHITE, (0, 500, 210, 10), 0)
    pygame.draw.rect(screen, WHITE, (200, 200, 100, 10), 0)
    pygame.draw.rect(screen, WHITE, (0, 400, 210, 10), 0)
    pygame.draw.rect(screen, WHITE, (500, 200, 10, 400), 0)
    pygame.draw.rect(screen, WHITE, (400, 100, 10, 400), 0)
    pygame.draw.rect(screen, WHITE, (300, 500, 200, 10), 0)
    pygame.draw.rect(screen, WHITE, (300, 200, 10, 200), 0)
    pygame.draw.rect(screen, WHITE, (100, 100, 210, 10), 0)
    pygame.draw.rect(screen, WHITE, (400, 100, 200, 10), 0)
    pygame.draw.rect(screen, WHITE, (400, 100, 200, 10), 0)
    pygame.draw.rect(screen, WHITE, (700, 0, 10, 200), 0)
    pygame.draw.rect(screen, WHITE, (800, 0, 10, 200), 0)
    pygame.draw.rect(screen, WHITE, (600, 300, 300, 10), 0)
    pygame.draw.rect(screen, WHITE, (600, 400, 200, 10), 0)
    pygame.draw.rect(screen, WHITE, (600, 400, 10, 100), 0)
    pygame.draw.rect(screen, WHITE, (800, 300, 10, 110), 0)

    pygame.draw.rect(screen, RED, (800, 500, 100, 100), 0)

    pygame.display.update()

def circle_draw(x, y, r):
    pygame.draw.circle(screen, RED, (x, y), r, 0)
    pygame.display.update()
    time.sleep(0.001)
    gen_maze()

def choose(dir):

    if dir == 0:
        return (-jump,-jump)
    elif dir == 1:
        return (0,-jump)
    elif dir == 2:
        return (jump,-jump)
    elif dir == 3:
        return (jump,0)
    elif dir == 4:
        return (jump,jump)
    elif dir == 5:
        return (0, jump)
    elif dir == 6:
        return (-jump, jump)
    elif dir == 7:
        return (-jump, 0)

def gen_population(pop_size, chromosome_len):

    pop = np.empty((2, chromosome_len, 1), int)
    for i in range(pop_size):
        chromosome = np.zeros(shape=(2,1))
        last = 5
        for j in range(1,chromosome_len):

            pool = [0,1,2,3,4,5,6,7]

            if last > 3:
                pool.remove(last-4)
            else:
                pool.remove(last+4)

            curr = np.random.choice(pool)
            last = curr

            single = choose(curr)
            single = np.reshape(single, (2,1))

            chromosome = np.hstack((chromosome,single))

        if i == 0:
            pop[:][:] = np.atleast_3d(chromosome[:][:])
        else:
            pop = np.append(pop, np.atleast_3d(chromosome), axis=2)

    return(pop)

def check_collision(x, y):

    if x < 0 or x > WIDTH-1 or y < 0 or y > HEIGHT-1:
        return -1

    col = screen.get_at((int(x), int(y)))

    if (col[0] == 255 and col[1] == 255 and col[2] == 255):
        return -1
    if col[0] == 255 and col[1] == 0 and col[2] == 0:
        return 1
    return 0

def mate(daddy, mommy):
    # split = np.random.randint(0, chromosome_len)
    split = 100

    child_1 = daddy[:, :split]

    child_2 = mommy[:, :split]
    for i in range(1, int(chromosome_len/split)):
        if i%2:
            child_1 = np.append(child_1, daddy[:, (split*i):(split*(i+1))], axis=1)
            child_2 = np.append(child_2, daddy[:, (split * i):(split * (i + 1))], axis=1)
        else:
            child_1 = np.append(child_1, mommy[:, (split*i):(split*(i+1))], axis=1)
            child_2 = np.append(child_2, daddy[:, (split * i):(split * (i + 1))], axis=1)

    # child_1 = daddy[:, :split]
    # child_1 = np.append(child_1, mommy[:, split:], axis=1)
    #
    # child_2 = mommy[:, :split]
    # child_2 = np.append(child_2, daddy[:, split:], axis=1)

    return child_1, child_2

def mutate(chromosome, mut_rate):

    if np.random.randint(0, mut_rate*2) == 0:
        return chromosome

    if np.random.randint(0, 2) == 1:

        last = 5
        for i in range(len(chromosome)):
            pool = [0, 1, 2, 3, 4, 5, 6, 7]

            if last > 3:
                pool.remove(last - 4)
            else:
                pool.remove(last + 4)

            curr = np.random.choice(pool)
            last = curr

            chromosome[:, i] = choose(curr)

        return chromosome

    else:
        for i in range(len(chromosome)):
            if np.random.randint(0, 50) == 1:
                if len(chromosome) - i > 100:
                    last = 5
                    for j in range(i, i+100):

                        pool = [0, 1, 2, 3, 4, 5, 6, 7]

                        if last > 3:
                            pool.remove(last - 4)
                        else:
                            pool.remove(last + 4)

                        curr = np.random.choice(pool)
                        last = curr

                        chromosome[:, j] = choose(curr)
        return chromosome

def fitness(x, y):
    return (WIDTH - x)**2 + (HEIGHT - y)**2

def match(pop, vel):
    contestants = np.empty((2, chromosome_len, 1), int)

    for i in range(vel):
        rand = np.random.randint(0, pop.shape[2])

        if i == 0:
            contestants[:][:] = np.atleast_3d(pop[:,:, rand])
        else:
            contestants = np.append(contestants, np.atleast_3d(pop[:,:, rand]), axis=2)

    best = None
    best_fit = None
    curr_fit = None

    for i in range(vel):
        x = y = 50
        for j in range(chromosome_len):

            check = check_collision(x, y)

            if check == -1:
                curr_fit = fitness(x,y) + penatly
                break
            elif check == 1:
                curr_fit = 0
                break

            x += contestants[0, j, i]
            y += contestants[1, j, i]

        if curr_fit is None:
            curr_fit = fitness(x,y)

        if best is None or bestFit > curr_fit:
            best = contestants[:, :, i]
            bestFit = curr_fit
    return best

def genetic(pop_size, chromosome_len):

    pop = gen_population(pop_size, chromosome_len)

    mut_rate = 2

    gen_maze()

    for i in range(iterations):

        new_pop = pop[:]

        for j in range(pop_size):

            mommy = match(pop, match_num)
            daddy = match(pop, match_num)

            child_1, child_2 = mate(mommy, daddy)

            child_1 = mutate(child_1, mut_rate)
            child_2 = mutate(child_2, mut_rate)

            new_pop = np.append(new_pop, np.atleast_3d(child_1), axis=2)
            new_pop = np.append(new_pop, np.atleast_3d(child_2), axis=2)

        fit_arr = np.empty(0)
        for k in range(new_pop.shape[2]):
            x = y = 50
            for p in range(chromosome_len):
                check = check_collision(x, y)
                if check == -1:
                    fit_arr = np.append(fit_arr, fitness(x, y)+penatly)
                    break
                elif check == 1:
                    fit_arr = np.append(fit_arr,0)
                    break
                x += new_pop[0, p, k]
                y += new_pop[1, p, k]

        index = 0

        sorted_pop = np.empty((2, chromosome_len, 1), int)
        for k in range(len(fit_arr)):
            min = fit_arr[k]
            for p in range(k+1, len(fit_arr)):

                if(min > fit_arr[p]):
                    min = fit_arr[p]
                    index = p

            fit_arr[index] = 9999999
            if k == 0:
                sorted_pop[:][:] = np.atleast_3d(new_pop[:,:,index])
            else:
                sorted_pop = np.append(sorted_pop, np.atleast_3d(new_pop[:,:, index]), axis=2)

        x = y = 50
        for k in range(chromosome_len):

            if check_collision(x, y) != 0:
                break
            circle_draw(int(x),int(y),10)
            pygame.event.get()

            x += sorted_pop[0, k, 0]
            y += sorted_pop[1, k, 0]

        pop = sorted_pop[:,:,:pop_size]

        fit_arr = sorted(fit_arr)
        avr = sum(fit_arr[:pop_size])/pop_size

        if avr - fit_arr[0] < 3000:
            mut_rate+=5
        else:
            mut_rate = 2
        if mut_rate > 3:
            mut_rate = 10

            cut = int(pop_size/5)
            pop = sorted_pop[:, :, :cut]

            pop = np.append(pop, gen_population(pop_size - cut, chromosome_len), axis=2)


        print("Iter = ", i, "Best fit = ", fit_arr[0], "Average fit = ", avr, "x,y = ",(x,y))

    pygame.quit()
    quit()



genetic(pop_size, chromosome_len)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()