# UCF Variable Extraction for ASIST Hackathon (June 2020)
There are three categories of variables:
1. Temporal variables
2. Spacial variables
3. Performance variables

### Temporal Variables
Time spent on different types of events:
* **Event:Triage_time**: time spent triaging
* **Event:PlayerSprinting_time**: time spent sprinting
* **navigating_time**: time spent navigating.

### Spacial Variables
Percent of zones visited and revisited is calculated for the following situations:
* **simple**: percent zone visited and revisited in the entire mission
* **with_victim**: percent of zones _with victims_ visited and revisited
* **rooms**: percent of rooms visited and revisited
* **hallways**: percent of hallways visited and revisited
* **entrances**: percent of entrances visited and revisited
* **first_5min**: percent of zones visited and revisited during the first 5 minutes
* **second_5min**: percent of zones visited and revisited during the second 5 minutes

### Performance Variables
* **green_victims_saved_count**: the total number of green victims saved
* **yellow_victims_saved_count**: the total number of yellow victims saved

The order in which the victims are saved is also stored in the output file as a string.

## Usage
To extract all UCF variables use the following command:

`python3 main_extract_variables.py -d data_dir DataFrame.csv`

## Requirements
* pandas
* numpy
* matplotlib
* For animating traces install http://www.imagemagick.org/script/download.php

