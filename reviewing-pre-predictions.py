from pathlib import Path

dir_path = Path(r"C:\Users\Jairus\Desktop\ulti-player-detection\training-labels\night-pretrain\labels")
check_id = '0' #for multi object if necessary


lows = []
average = []



# result = [s.split(' ') for s in strings]




for item in dir_path.iterdir():
    confidence_list = []
    curr_sum = 0

    with open(item, "r") as file:
        lines = file.read().splitlines()
    formatted = [a.split(' ') for a in lines]

    
    for player in formatted:
        if not player[0] == check_id:
            print("Invalid player id found")
            break

        confidence_list.append(player[-1])

    for confidence in confidence_list:
        curr_sum += float(confidence)
    
    average.append(curr_sum / len(confidence_list))
    lows.append(float(min(confidence_list)))

# print(f"averages = {average}\n lows = {lows}")
print(f"averages of data = {sum(average) / len(average)}, {sum(lows) / len(lows)}")
        

