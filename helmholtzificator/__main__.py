from .load_data import load

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

class EigenSlider:
    func_map = {
        r'$f(\vec{x})$': lambda f: f,
        r'$f(\vec{x})^2$': lambda f: f**2
    }

    def __init__(self, fig, equation, save_name, **opts):
        self.fig = fig
        self.ax = fig.subplots()
        self.ax.set_axis_off()

        self.equation = equation
        self.save_name = save_name
        self.opts = opts
        self.cur_display = list(self.func_map.values())[1]

        self.set_vect(self.equation.min_eigenvector(**self.opts))
        self.image = self.ax.imshow(self.get_data())

        self.fig.subplots_adjust(bottom=0.25)

        self.ax_slider = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])
        max_eig = self.equation.eigenstats(self.equation.max_eigenvector(fail='ignore', max_iter=100))[0]
        self.slider = Slider(
            self.ax_slider,
            label=r'Target $\lambda$:',
            valmin=min(-self.cur_val, 0),
            valmax=-self.cur_val + (-max_eig + self.cur_val) / 10,
            valinit=-self.cur_val,
        )
        self.slider.on_changed(self.on_update)

        self.ax_refresh = self.fig.add_axes([0.25, 0.025, 0.1, 0.04])
        self.refresh_button = Button(self.ax_refresh, 'Refresh')
        self.refresh_button.on_clicked(self.on_update)

        self.ax_save = self.fig.add_axes([0.8, 0.025, 0.1, 0.04])
        self.save_button = Button(self.ax_save, 'Save')
        self.save_button.on_clicked(self.on_save)

        self.ax_func_selector = self.fig.add_axes([0.24, 0.13, 0.1, 0.1])
        self.ax_func_selector.set_axis_off()
        self.func_selector = RadioButtons(
            self.ax_func_selector,
            labels=list(self.func_map),
            active=list(self.func_map.values()).index(self.cur_display)
        )
        self.func_selector.on_clicked(self.on_func_select)
        self.ax_func_selector.text(
            -0.025, 0.5, 'Plotted:',
            verticalalignment='center',
            horizontalalignment='right',
            transform=self.ax_func_selector.transAxes
        )


    def set_vect(self, vect):
        self.cur_vect = vect
        self.cur_val, self.cur_uncertainty = self.equation.eigenstats(vect)

    def get_data(self):
        return self.cur_display(self.equation.func(self.cur_vect))

    def on_update(self, _):
        self.set_vect(self.equation.find_eigenvector(-self.slider.val, **self.opts))
        self.replot()

    def on_func_select(self, func):
        self.cur_display = self.func_map[func]
        self.replot()

    def replot(self):
        self.ax.set_title(rf'$\lambda =$ {self.cur_val} $\pm$ {self.cur_uncertainty}')
        self.image.set_data(self.get_data())
        self.image.autoscale()
        self.fig.canvas.draw_idle()

    def on_save(self, event):
        fname = f'{self.save_name}_{self.cur_val}.npy'
        np.save(fname, self.equation.func(self.cur_vect))
        print(f'Saved as {fname}')


if __name__ == '__main__':
    import sys
    import os

    fname = sys.argv[1]
    base, ext = os.path.splitext(fname)

    eigenslider = EigenSlider(plt.figure(), load(sys.argv[1], 1), base)
    plt.show()
