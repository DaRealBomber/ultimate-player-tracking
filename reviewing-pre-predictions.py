from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

dir_path = Path(r"C:\Users\parent\Documents\GitHub\ultimate-player-tracking\night-pretrain\labels")
check_id = '0' #for multi object if necessary


lows = []
highs = []
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
    highs.append(float(max(confidence_list)))
    

print(f"""
        averages confidence = {sum(average) / len(average)}
        worse average = {min(average)}, frame number: {average.index(min(average))}
        lows: {min(lows)}, {sum(lows) / len(lows)}
        highs: {max(highs)}, {sum(highs) / len(highs)}
        
""")
        

#create graphs
def plotter(lst, name):
    x = []
    y = []
    
    for val in lst:
        x.append(lst.index(val))
        y.append(val)

    plt.plot(x, y, 'o', color='red')
    plt.title(name)
    plt.ylim(0.00, 1.00)
    plt.show()


#average confidence
plotter(average, 'average')
plotter(highs, 'highs')
plotter(lows, 'lows')