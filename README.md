# Extract ProtoDUNE Slow Control data

The code `get_db_T_evolution.py`shows how to extract the temperature probe values for a given day. To run it :<br/>
`python get_db_T_evolution.py -date DD-MM-YYY -conf conf/np04_T_filling.txt`<br/>
You can also set start/stop timestamps instead of the date.<br/> 

The code needs a list of sensors `name ID`. The ID is a 14-digit number unique to every sensor in the experiment, the provided name is up to your convenience.

In `plots/`, a script to plot the NP04 temperature evolution as a function of the height is provided.