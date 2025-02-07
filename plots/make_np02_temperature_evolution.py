import numpy as np
import glob
import copy 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import datetime as dt
import colorcet as cc
import matplotlib.gridspec as gridspec

params = {'figure.figsize': (12, 6),
          'legend.fontsize':'x-large',              
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize':'x-large',
          'ytick.labelsize':'x-large'}

mpl.rcParams.update(params)


heights = {}
with open('np02_temperature_height.csv', mode='r', encoding='utf-8-sig') as f:
    for lines in f.readlines():
        lines = lines.rstrip('\n')
        lines = lines.rstrip('\ufeff')
        li = lines.split(';')
        heights[li[0]] = float(li[1])


print(heights)

march_dates = glob.glob('../temp_evo_filling/*np02.npz')
dates = sorted(march_dates)

fig = plt.figure(figsize=(12,8))
gs = gridspec.GridSpec(nrows=2, ncols=3, height_ratios=[1, 20], width_ratios=[6,4,6])

ax = [fig.add_subplot(gs[1,i]) for i in range(3)]
ax_col = fig.add_subplot(gs[0,:])


day_loc = [2,9,2]

for a,d in zip(ax,day_loc):
    xfmt = md.DateFormatter('%d/%m')
    a.xaxis.set_major_formatter(xfmt)
    days = md.DayLocator(interval = d)
    a.xaxis.set_major_locator(days)

my_cmap = copy.copy(mpl.cm.get_cmap('cet_fire_r'))
my_cmap.set_under('c')


sensors=['TE0805', 'TE0806', 'TE0807', 'TE0808', 'TE0801', 'TE0802', 'TE0803', 'TE0804', 'TE0721', 'TE0722', 'TE0723', 'TE0724', 'TE0717', 'TE0718', 'TE0719', 'TE0720', 'TE0713', 'TE0714', 'TE0715', 'TE0716', 'LT0501', 'LT0502', 'LT0503', 'LT0504', 'LT0505', 'LT0506', 'LT0507', 'LT0508', 'LT0509', 'TE0605', 'TE0606', 'TE0607', 'TE0608', 'TE0601', 'TE0602', 'TE0603', 'TE0604', 'TE0521', 'TE0522', 'TE0523', 'TE0524', 'TE0517', 'TE0518', 'TE0519', 'TE0520', 'TE0513', 'TE0514', 'TE0515', 'TE0516']



#hours = [2,8,14,20]#[3, 11, 19]
hours_fine = [3,9,15,21]#[2,6,10,14,18,22]#[3, 11, 19]
hours_large = [12]
iplot = 0
for d in dates:
    print(d)
    with np.load(d) as data:
        print('has ', len(data))
        if(len(data) == 0):
                continue
        for s in sensors:
            
            height = heights[s]
            try:
                values = data[s]
            except KeyError:
                continue
            
            ts = values[0,0]
            
            if(ts < 1734134400 or ts > 1736640000):
                
                hours = hours_fine
                iplot = 2
                if(ts < 1734134400):
                    iplot=0
            else:
                hours = hours_large
                iplot = 1
                
            nval = len(values)
            for h in hours:
                if(h >= nval):
                    continue
                v = values[h]

                ts = dt.datetime.fromtimestamp(v[0])
                temp = v[1]
                if(temp < 80):
                    continue
            
                im = ax[iplot].scatter(ts, height, c=temp, cmap=my_cmap,s=4, vmin=88, vmax=330)
                
cb = fig.colorbar(im, cax=ax_col, orientation='horizontal', extend='min')
cb.ax.xaxis.set_ticks_position('top')
cb.ax.xaxis.set_label_position('top')
cb.set_label('Temperature [K]')

title = ['NP04 Transfer', 'Christmas Break', 'Truck Filling']

for a,t  in zip(ax, title):
    a.set_ylim(0, 7.8)#8.1)
    a.set_title(t)
ax[0].set_ylabel('NP02 Temperature Sensors Height [m]')
ax[1].set_xlabel('Date')
ax[1].yaxis.set_ticklabels([])
ax[2].yaxis.set_ticklabels([])

ax[0].set_xlim(left=dt.date(2024, 12,5), right=dt.date(2024, 12,14))
ax[1].set_xlim(left=dt.date(2024, 12,14), right=dt.date(2025, 1,12))
ax[2].set_xlim(left=dt.date(2025, 1,14), right=dt.date(2025, 1,23))

plt.tight_layout()
plt.subplots_adjust(wspace=0.03, hspace = 0.25)
fig.savefig('np02_temperature_evolution.png', dpi=200)
plt.show()
