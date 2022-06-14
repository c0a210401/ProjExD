from random import randint
def main():
    print("問題:")
    mon = shutudai()
    kaitou(mon)

def shutudai():
    q = {0:("サザエの旦那の名前は？", "マスオ", "ますお"),
            1:("カツオの妹の名前は？", "ワカメ", "わかめ"),
            2:("タラオはカツオから見てどんな関係？", "甥", "おい", "甥っ子", "おいっこ")}
    s = randint(0, 2)
    print(q[s][0])
    return q[s]

def kaitou(mon):
    kai = input("答えるんだ:")
    if kai in mon:
        print("正解!!!")
    else:
        print("出直してこい")

if __name__ ==  "__main__":
    main()