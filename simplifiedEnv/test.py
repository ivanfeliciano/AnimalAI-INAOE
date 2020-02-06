import random
def generate_basic_good(number_of_conf):
    max_gold_goals = max_good_goals = 10
    
    for c in range(number_of_conf):
        grid = [[" " for i in range(40)] for j in range(40)]
        num_green_balls = random.randint(1, max_good_goals)
        num_gold_balls = random.randint(1, max_gold_goals)
        list_of_idx = random.sample(range(40*40), num_gold_balls + num_green_balls + 1)
        list_of_idx.sort()
        print(list_of_idx)
        k = 0
        print("# green goals = {}".format(num_green_balls))
        print("# gold goals = {}".format(num_gold_balls))
        for i in range(len(grid)):
            for j in range(len(grid)):
                if k < len(list_of_idx) and len(grid) * i + j == list_of_idx[k]:
                    # print("{} == {}".format(len(grid) * i + j , list_of_idx[k]))
                    if k == len(list_of_idx) - 1:
                        grid[i][j] = 1
                        k += 1
                        continue
                    if num_green_balls > 0:
                        num_green_balls -= 1
                        grid[i][j] = 2
                    else:
                        num_gold_balls -= 1
                        grid[i][j] = 3
                    k += 1
        print(k)
        for i in grid:
            print(i)
            # if "".join([str(j) if j != " " else "" for j in i]) != "":
            #     print(" ".join([str(j) if j != " " else "" for j in i]))

generate_basic_good(10)

