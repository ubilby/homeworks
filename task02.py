plate = int(input("Введите количество тарелок: "))
detergent = int(input("Введите количество моющего средства: "))

while plate > 0 and detergent > 0:

    plate -= 1
    detergent -= 0.5

    print("Осталось", detergent,"ед. моющего средства")
    if detergent == 0:
        print("Моющее средство закончилось, но осталось", plate, "грязных тарелок")
    elif plate == 0:
        print("Все тарелки вымыты, но осталось", detergent, "ед. моющего средства")
