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
times = [matchup["Time"] for matchup in results.values()]

x = np.arange(len(labels))
width = 0.2

fig, ax1 = plt.subplots()
rects1 = ax1.bar(x - 1.5*width, x_wins, width, label='X Wins')
rects2 = ax1.bar(x - 0.5*width, o_wins, width, label='O Wins')
rects3 = ax1.bar(x + 0.5*width, draws, width, label='Draws')

ax1.set_ylabel('Number of games')
ax1.set_title('Results of AI vs AI Tic-Tac-Toe simulations')
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=45, ha='right')
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.set_yscale('log')
ax2.set_ylim(min(times), max(times)*1.1)
ax2.plot(x, times, marker='o', label='Time per game (s)', color='purple', linestyle=(0, (1, 2)))
ax2.set_ylabel('Time per game (s)')
ax2.legend(loc='upper right')

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax1.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()
plt.show()
