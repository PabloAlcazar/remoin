import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        self.X = X

        heptane_20 = 0.24
        gas_20 = 0.72
        stuff_20 = 2.68
        amo_20 = 0.72
        ele_20 = 0.104
        price_20 = 4.9104
        earn_20 = 0.4464

        heptane_22 = 0.4341
        gas_22 = 1.281
        stuff_22 = 2.8739
        amo_22 = 0.2
        ele_22 = 0.179
        price_22 = 5.501177
        earn_22 = 0.500107 

        self.legend = ['Price\n(paid by Bridgestone)', 'Cost\n(to Remoin)', 'Earning\n(to Remoin)']
        self.measurements = ['2020', '2022', 'Simulator']

        self.data = [[price_20, price_22, 0],
                    [heptane_20+gas_20+amo_20+stuff_20+ele_20, heptane_22+gas_22+amo_22+stuff_22+ele_22, 0],
                    [earn_20, earn_22, 0]]

        self.onupdatedata()


    def onupdatedata(self, event=0):
        # Update data
        self.data[1][-1] = self.get_cost()
        self.data[2][-1] = self.get_earning()
        self.data[0][-1], _ = self.get_price()
        self.update()

    def update(self):
        # create plot
        self.ax.cla()
        self.ax.set_title('Evolution of costs')
        self.ax.set_ylabel('€ per unit')
        self.ax.set_ylim([0,10])

        index = np.arange(len(self.measurements))
        bar_width = 0.2
        opacity = 0.8

        price = self.ax.bar(index, self.data[0], bar_width, alpha=opacity, color='r', label=self.legend[0])
        cost = self.ax.bar(index+bar_width, self.data[1], bar_width, alpha=opacity, color='b', label=self.legend[1])
        earn = self.ax.bar(index+2*bar_width, self.data[2], bar_width, alpha=opacity, color='g', label=self.legend[2])

        self.ax.set_xticks(index + bar_width, ('2020', '2022', 'Simulator'))
        self.ax.legend()

        self.ax.bar_label(price)
        self.ax.bar_label(cost)
        self.ax.bar_label(earn)

        roi = 0.72*7/self.X[3].val
        self.X[5].set_text(f"{round(roi,2)} Years of amortization\n* The smaller the amortization, the longer the contract needs to go on in order to obtain ROI")

    
    def get_cost(self):
        # Get actual cost
        return self.X[0].val + self.X[1].val + self.X[2].val + self.X[3].val + self.X[4].val 

    def get_price(self):
        # Proposed by accenture
        proposed = 0
        # proposed = self.data[0][1]
        # if self.X[0].val > 1.1*self.initial_heptane:
        #     proposed = proposed*1.0035
        # if self.X[1].val > 1.1*self.initial_gas:
        #     proposed = proposed*1.01

        # Fair price
        
        price = self.data[1][-1] + self.data[2][-1]

        return price, proposed

    def get_earning(self):
        # Earn 10% over total price
        return self.data[1][-1] *0.1/0.9 


root = tk.Tk()
root.title("Remoin")

lowest_scroll= 0.08
scroll_margin= 0.06

fig = Figure()
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(fill="both", expand=True)
ax = fig.subplots(1,1)
fig.subplots_adjust(bottom=0.45, top = 0.95)

# Amortization
years = fig.text(0.05,0.03,"* The smaller the amortization, the longer the contract needs to go on in order to obtain ROI")
axmax  = fig.add_axes([0.2, lowest_scroll, 0.6, 0.015])
amo = Slider(axmax, 'Amortization (€/unit)*', 0, 1, valinit=0.2, color="r")
lowest_scroll = lowest_scroll+scroll_margin

# Treatments + Staff + Services
axmax  = fig.add_axes([0.2, lowest_scroll, 0.6, 0.015])
stuff = Slider(axmax, 'Treatments + Staff\n+ Services (€/unit)', 0, 5, valinit=2.90697)
lowest_scroll = lowest_scroll+scroll_margin

# Electricity
axmax  = fig.add_axes([0.2, lowest_scroll, 0.6, 0.015])
electricity = Slider(axmax, 'Electricity (€/unit)', 0, 1, valinit=0.179)
lowest_scroll = lowest_scroll+scroll_margin

# Heptano
axmax  = fig.add_axes([0.2, lowest_scroll, 0.6, 0.015])
heptane = Slider(axmax, 'Heptane (€/unit)', 0, 2, valinit=0.4341)
lowest_scroll = lowest_scroll+scroll_margin

# Gas-oil
axmax  = fig.add_axes([0.2, lowest_scroll, 0.6, 0.015])
gas = Slider(axmax, 'Gas-oil (€/unit)', 0, 2, valinit=1.281)

# Trackers
tracker = IndexTracker(ax, [heptane, gas, stuff, amo, electricity, years])

canvas.mpl_connect('button_press_event', tracker.onupdatedata) #add this for contrast change
canvas.mpl_connect('scroll_event', tracker.onupdatedata) #add this for contrast change

root.mainloop()