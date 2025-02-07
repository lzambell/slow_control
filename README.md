# Extract ProtoDUNE Slow Control data for NP02 and NP04
:warning: somehow the access method does not work anymore for NP04

The code `get_db_T_evolution.py`shows how to extract the temperature probe values for a given day. To run it :<br/>
`python get_db_T_evolution.py -det np04 -date DD-MM-YYYY -conf conf/np04_T_filling.txt`<br/>
You can also set start/stop timestamps instead of the date.<br/> 

The code needs a list of sensors `name\tID`. The ID is a 14-digit number unique to every sensor in the experiment, the provided name is up to your convenience.

In `plots/`, scripts to plot the NP04 & NP02 temperature evolution as a function of the thermometer height are provided.