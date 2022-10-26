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