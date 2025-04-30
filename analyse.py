

def show_habits_by_periodicity(habit_list):
    done = False
    while not done:
        num = 1
        x = input("What do you want to see?\n 1. Daily \n 2. Weekly \n 3. monthly\n")
        try:
            x = int(x)
        except ValueError:
            print("wrong input")
            continue

        match x:
            case 1:
                for y in range(len(habit_list)):
                    if habit_list[y].get_frequency() == 1:
                        print(f"{num}. {habit_list[y].get_name()}")
                        num +=1
            case 2:
                for y in range(len(habit_list)):
                    if habit_list[y].get_frequency() == 2:
                        print(f"{num}. {habit_list[y].get_name()}")
                        num += 1
            case 3:
                for y in range(len(habit_list)):
                    if habit_list[y].get_frequency() == 3:
                        print(f"{num}. {habit_list[y].get_name()}")
                        num += 1
            case _:
                print("wrong input")
                continue
        done = True


def show_streaks(habit_list):
    #lists all habits and there active streaks
    for x in range (0, len(habit_list), 1):
        print(f"{x + 1}.", habit_list[x].get_name(), habit_list[x].get_streak())

def show_problems(habit_list):
    print("you have missed:")
    temp_list = []
    for x in range(0, len(habit_list), 1):
        for y in range(0, len(temp_list) + 1, 1):
            if y == len(temp_list):
                temp_list.insert(y, habit_list[x])
            elif habit_list[x].get_failed() > temp_list[y].get_failed():
                temp_list.insert(y, habit_list[x])
                break
    for z in range(0, len(temp_list), 1):
        print(f"{z + 1}.", temp_list[z].get_name(), temp_list[z].get_failed())

def show_longest_streaks(habit_list):
    print("the longest you got:")
    temp_list = []
    for x in range(0, len(habit_list), 1):
        for y in range(0, len(temp_list) + 1, 1):
            if y == len(temp_list):
                temp_list.insert(y, habit_list[x])
            elif habit_list[x].get_longest_streak() > temp_list[y].get_longest_streak():
                temp_list.insert(y, habit_list[x])
                break
    for z in range(0, len(temp_list), 1):
        print(f"{z + 1}.", temp_list[z].get_name(), temp_list[z].get_longest_streak())

def analyse_menu(habit_list):
    x = input("What do you want to do?\n 1. Show active streaks \n 2. show problems \n 3. show longest streaks\n 4. show habits by periodicity\n")
    match x:
        case "1":
            show_streaks(habit_list)
        case "2":
            show_problems(habit_list)
        case "3":
            show_longest_streaks(habit_list)
        case "4":
            show_habits_by_periodicity(habit_list)
        case _:
            print("wrong input")
            analyse_menu(habit_list)