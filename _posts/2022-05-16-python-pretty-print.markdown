---
layout: post
title: "Python: Pretty Print pprint.pprint( ... )"

---

“Pretty print” output over multiple lines in a readable format.

| ![019-feature-image.png](https://behainguyen.files.wordpress.com/2022/05/019-feature-image.png) |
|:--:|
| *Python: “pretty print”.* |

<span class="keyword">Python</span> standard library <span class="keyword">pprint</span> 
enables “pretty print” output in a readable format.

Consider the following test script:

```
File: pretty_print.py
```

{% highlight python %}
import pprint

timesheet = {
    "data":{
        "periodStart": "February 28 2019",
        "periodEnd": "July 31 2014",
        "clientName": "Central Intelligence Agency ( CIA ) Pty Ltd",
        "contractorName": "NGUYEN Van Be Hai",
        "timesheetChargeable": "no",
        "timesheetTotal": "164 hrs 00 mins",
        "entries": [
            {
                "periodDate": "February 01 2019",
                "shortDayName": "Fri",
                "startTime": "09:08 AM",
                "endTime": "07:32 PM",
                "breakTime": "02:24",
                "dailyTotal": "08:00",
                "chargeable": "Yes"
            },
            {
                "periodDate": "February 02 2019",
                "shortDayName": "Sat",
                "startTime": "00:00 AM",
                "endTime": "00:00 PM",
                "breakTime": "00:00",
                "dailyTotal": "00:00",
                "chargeable": ""
            },
            {
                "periodDate": "February 03 2019",
                "shortDayName": "Sun",
                "startTime": "00:00 AM",
                "endTime": "00:00 PM",
                "breakTime": "00:00",
                "dailyTotal": "00:00",
                "chargeable": ""
            },
            {
                "periodDate": "February 04 2019",
                "shortDayName": "Mon",
                "startTime": "09:20 AM",
                "endTime": "05:35 PM",
                "breakTime": "01:15",
                "dailyTotal": "07:00",
                "chargeable": "Yes"
            }
			
		]
    }
}

print( timesheet )

print( '\n\n-----------------------\n\n' )

pprint.pprint( timesheet )
{% endhighlight %}

And this is its output:

```
{'data': {'periodStart': 'February 28 2019', 'periodEnd': 'July 31 2014', 'clientName': 'Central Intelligence Agency ( CIA ) Pty Ltd', 'contractorName': 'NGUYEN Van Be Hai', 'timesheetChargeable': 'no', 'timesheetTotal': '164 hrs 00 mins', 'entries': [{'periodDate': 'February 01 2019', 'shortDayName': 'Fri', 'startTime': '09:08 AM', 'endTime': '07:32 PM', 'breakTime': '02:24', 'dailyTotal': '08:00', 'chargeable': 'Yes'}, {'periodDate': 'February 02 2019', 'shortDayName': 'Sat', 'startTime': '00:00 AM', 'endTime': '00:00 PM', 'breakTime': '00:00', 'dailyTotal': '00:00', 'chargeable': ''}, {'periodDate': 'February 03 2019', 'shortDayName': 'Sun', 'startTime': '00:00 AM', 'endTime': '00:00 PM', 'breakTime': '00:00', 'dailyTotal': '00:00', 'chargeable': ''}, {'periodDate': 'February 04 2019', 'shortDayName': 'Mon', 'startTime': '09:20 AM', 'endTime': '05:35 PM', 'breakTime': '01:15', 'dailyTotal': '07:00', 'chargeable': 'Yes'}]}}


-----------------------


{'data': {'clientName': 'Central Intelligence Agency ( CIA ) Pty Ltd',
          'contractorName': 'NGUYEN Van Be Hai',
          'entries': [{'breakTime': '02:24',
                       'chargeable': 'Yes',
                       'dailyTotal': '08:00',
                       'endTime': '07:32 PM',
                       'periodDate': 'February 01 2019',
                       'shortDayName': 'Fri',
                       'startTime': '09:08 AM'},
                      {'breakTime': '00:00',
                       'chargeable': '',
                       'dailyTotal': '00:00',
                       'endTime': '00:00 PM',
                       'periodDate': 'February 02 2019',
                       'shortDayName': 'Sat',
                       'startTime': '00:00 AM'},
                      {'breakTime': '00:00',
                       'chargeable': '',
                       'dailyTotal': '00:00',
                       'endTime': '00:00 PM',
                       'periodDate': 'February 03 2019',
                       'shortDayName': 'Sun',
                       'startTime': '00:00 AM'},
                      {'breakTime': '01:15',
                       'chargeable': 'Yes',
                       'dailyTotal': '07:00',
                       'endTime': '05:35 PM',
                       'periodDate': 'February 04 2019',
                       'shortDayName': 'Mon',
                       'startTime': '09:20 AM'}],
          'periodEnd': 'July 31 2014',
          'periodStart': 'February 28 2019',
          'timesheetChargeable': 'no',
          'timesheetTotal': '164 hrs 00 mins'}}
```

<span class="keyword">pprint.pprint( ... )</span>
gives a much nicer output. I hope you like it as much as I do. And thank you for visiting.	
