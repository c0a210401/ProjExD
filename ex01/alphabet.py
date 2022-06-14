import random
def main():
    mon = show_alp()
    kaitou(mon)

def show_alp():
    alpha_list = [chr(x+65) for x in range(26)]
    q_alp = random.sample(alpha_list, 8)
    del_list = [random.choice(q_alp) for de in range(2)]
    delcount = len(del_list)
    show_list = q_alp.copy()
    [show_list.remove(d) for d in del_list]
    print(f"対象文字:\n{q_alp}")
    print(f"表示文字:\n{show_list}")
    return del_list,delcount

def kaitou(mon):
    bad = 0
    count = input("欠損文字はいくつあるでしょうか:")
    if count == str(mon[1]):
        print("正解です。 それでは、具体的に欠損文字を一つずつ入力してください")
        for i in range(mon[1]):
            ans = input(f"{i+1}つ目の文字を入力してください:")
            if ans in mon[0]:
                pass
            else:
                bad += 1
                print("不正解です。 またチャレンジしてください")
                break
        if bad == 0:
            print("おみごと! 全問正解です")
    else:
        print("不正解です。 またチャレンジしてください")

if __name__ ==  "__main__":
    main()