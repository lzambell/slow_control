import numpy as np
import glob
import copy 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import datetime as dt
import colorcet as cc
import matplotlib.gridspec as gridspec

heights = {}
with open('temp_height.csv', mode='r', encoding='utf-8-sig') as f:
    for lines in f.readlines():
        lines = lines.rstrip('\n')
        lines = lines.rstrip('\ufeff')
        li = lines.split(';')
        heights[li[0]] = float(li[1])




dates = glob.glob('../temp_evo_filling/*npz')
dates = sorted(dates) #to be checked once we're in April ...


fig = plt.figure(figsize=(6,8))
gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[1, 20])

ax = fig.add_subplot(gs[1,0])
ax_col = fig.add_subplot(gs[0,0])


xfmt = md.DateFormatter('%d/%m')
ax.xaxis.set_major_formatter(xfmt)
hours = md.DayLocator(interval = 1)
ax.xaxis.set_major_locator(hours)

my_cmap = copy.copy(mpl.colormaps.get_cmap('cet_fire_r'))
my_cmap.set_under('c')


sensors= [''.join(['TE','%.04d'%x]) for x in range(1, 73)]
sensors.extend([''.join(['TE','%.04d'%x]) for x in range(115, 120)])


""" NB : there is a problem with TE0049 """

hours = [3, 9, 15, 21]
for d in dates:
    with np.load(d) as data:
        for s in sensors:
            height = heights[s]
            values = data[s]
        
            for h in hours:
                v = values[h]

                ts = dt.datetime.fromtimestamp(v[0])
                temp = v[1]

                im = ax.scatter(ts, height, c=temp, cmap=my_cmap,s=4, vmin=88, vmax=330)
cb = fig.colorbar(im, cax=ax_col, orientation='horizontal', extend='min')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')
cb.set_label('Temperature [k]')

ax.set_ylim(0, 8.1)

ax.set_ylabel('NP04 Temperature Sensors Height [m]')
ax.set_xlabel('Date')

plt.tight_layout()
fig.savefig('temperature_evolution.png', dpi=200)

plt.show()
