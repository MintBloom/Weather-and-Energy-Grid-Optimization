# Weather-and-Energy-Grid-Optimization

## Requirements
 - external libraries via pip install --> requests pandas sqlalchemy psycopg2-binary


---
## Challenges
 - Learning to use Pandas DataFrames and exporting DF to postgreSQL
    My first time using most if not all of these data-orientated python modules, so it took me a fair bit to write the DataGather&Export.py script
 - How to actually forecast the weather from the data I've gathered
    
 - What "kind" of database to use for energy
    going with the csv files for the UK wide demand. the api documentation seemed more strenuous to use, or at least finding information on how to use it was tiring so opted for the csv datasets instead.

 - what time increments/frequency to use for analysis (hourly, daily, etc..)
    going with at least hourly data, but will briefly look at weather and energy data first. Based on how detailed the trends and spikes in each set are, I will switch both to either hourly or half-hourly
 - where to analyse and plot graphs of my data
    jupyter notebooks?