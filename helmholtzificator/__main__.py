from .load_data import load

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class EigenSlider:
    def __init__(self, fig, equation, save_name, **opts):
        self.fig = fig
        self.ax = fig.subplots()
        self.ax.set_axis_off()

        self.equation = equation
        self.save_name = save_name
        self.opts = opts

        vect = self.equation.min_eigenvector(**self.opts)
        self.image = self.ax.imshow(self.get_data(vect))
        self.set_vect(vect)

        self.fig.subplots_adjust(bottom=0.25)
        self.ax_slider = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])

        max_eig = self.equation.eigenstats(self.equation.max_eigenvector(fail='ignore', max_iter=100))[0]
        self.slider = Slider(
            ax=self.ax_slider,
            label=r'Target $\lambda$:',
            valmin=min(-self.cur_val, 0),
            valmax=-self.cur_val + (-max_eig + self.cur_val) / 10,
            valinit=-self.cur_val,
        )
        self.slider.on_changed(self.on_update)

        self.ax_save = self.fig.add_axes([0.8, 0.025, 0.1, 0.04])
        self.save_button = Button(self.ax_save, 'Save')
        self.save_button.on_clicked(self.on_save)

        self.ax_refresh = self.fig.add_axes([0.25, 0.025, 0.1, 0.04])
        self.refresh_button = Button(self.ax_refresh, 'Refresh')
        self.refresh_button.on_clicked(self.on_update)

    def set_vect(self, vect):
        self.cur_vect = vect
        self.cur_val, uncertainty = self.equation.eigenstats(vect)
        self.ax.set_title(rf'$\lambda =$ {self.cur_val} $\pm$ {uncertainty}')
        self.image.set_data(self.get_data(self.cur_vect))
        self.image.autoscale()
        self.fig.canvas.draw_idle()

    def get_data(self, vect):
        return self.equation.func(vect)**2

    def on_update(self, _):
        self.set_vect(self.equation.find_eigenvector(-self.slider.val, **self.opts))

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
