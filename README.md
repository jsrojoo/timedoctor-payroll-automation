Too lazy to get timesheet from timedoctor that's why this script was born.
The script spits out a csv of your work logs so you can easily copy pasta.

### Usage:
 - Get a timedoctor access token: https://webapi.timedoctor.com/doc#documentation
 - create a `config.ini` file and place your access token under `[timedoctor]` section
 ```
 [timedoctor]
 access_token=youraccesstoken
 ```
 - run: ```python main.py```

### Output:
 - worklog.csv

#### Requirements:

__pyenv__ for managing python environment (optional)<br>
__python__ version 3.7.0<br>
```
pip install -r requirements.txt
```
Installs __requests__ module<br>
