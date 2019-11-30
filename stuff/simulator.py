"""
Run some simulations of shuffles

"""


import random


def shuffle():
    deck = [True] *30 + [False] * 30
    random.shuffle(deck)
    cnt = float(sum(deck[0:7]))
    return cnt


def do_run(N):
    tot = 0.0
    for i in range(0, N):
        tot += shuffle()
    print(tot / float(N))
    return tot



def main():
    tot = 0
    for i in range(0,30):
        tot += do_run(100)
        print('>', i+1, tot/(100.*float(i+1)))





if __name__ == '__main__':
    main()