#  plotter.py
import json
import matplotlib.pyplot as plt
import numpy as np

with open("results.json", "r") as f:
    results = json.load(f)

labels = list(results.keys())
# Add a small constant (e.g., 1e-10) to avoid log(0) issues
x_wins = [matchup["X"] + 1e-10 for matchup in results.values()]
o_wins = [matchup["O"] + 1e-10 for matchup in results.values()]
draws = [matchup["Draw"] + 1e-10 for matchup in results.values()]



x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, x_wins, width, label='X Wins')
rects2 = ax.bar(x, o_wins, width, label='O Wins')
rects3 = ax.bar(x + width, draws, width, label='Draws')

from matplotlib.ticker import FuncFormatter

# Define a custom function to format the tick labels
def formatter(x, _):
    return f'{x:.0f}'

# Apply the custom formatter to the y-axis
ax.yaxis.set_major_formatter(FuncFormatter(formatter))
ax.xaxis.set_major_formatter(FuncFormatter(formatter))

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Number of games')
ax.set_yscale('log')
ax.set_title('Results of AI vs AI Tic-Tac-Toe simulations')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend()

# Attach a text label above each bar in rects, displaying its height.
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()
plt.show()
