# plotter.py -  Plotter class to graph the tabulated results of the simulations.
import json
import matplotlib.pyplot as plt
import numpy as np

with open("results.json", "r") as f:
    results = json.load(f)

labels = list(results.keys())
x_wins = [matchup["X"] for matchup in results.values()]
o_wins = [matchup["O"] for matchup in results.values()]
draws = [matchup["Draw"] for matchup in results.values()]

x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, x_wins, width, label='X Wins')
rects2 = ax.bar(x, o_wins, width, label='O Wins')
rects3 = ax.bar(x + width, draws, width, label='Draws')

ax.set_ylabel('Number of games')
ax.set_title('Results of AI vs AI Tic-Tac-Toe simulations')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend()

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()
plt.show()
