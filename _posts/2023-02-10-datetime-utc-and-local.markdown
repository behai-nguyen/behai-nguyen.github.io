---
layout: post
title: "Python: local date time and UTC date time."
description: Understanding the relationship between local date time and UTC date time. We will look at the following issues -- ⓵ local time, time zone, UTC offset, local date time and UTC date time; ⓶ assign UTC time zone to MySQL and PostgreSQL UTC date time values which are stored with no time zone information.

gallery-image-list:
    - "https://behainguyen.files.wordpress.com/2023/02/058-01-mysql.png"
    - "https://behainguyen.files.wordpress.com/2023/02/058-02-postgresql.png"

tags:
- Python
- UTC
- datetime
- MySQL
- PostgreSQL
---

*Understanding the relationship between local date time and UTC date time. We will look at the following issues -- ⓵ local time, time zone, UTC offset, local date time and UTC date time; ⓶ assign UTC time zone to MySQL and PostgreSQL UTC date time values which are stored with no time zone information.*

| ![058-feature-image.png](https://behainguyen.files.wordpress.com/2023/02/058-feature-image.png) |
|:--:|
| *Python: local date time and UTC date time.* |

I've done some studies on this subject, and have written some 
investigative code. I will just start off at the point most relevant to what we are going to look at.

We will be using only the Python standard date time library 
<a href="https://docs.python.org/3/library/datetime.html"
title="datetime — Basic date and time types" target="_blank">datetime — Basic date and time types</a>,
no third party packages involved.

❶ First, let's have a look at local time, time zone, 
<a href="https://en.wikipedia.org/wiki/UTC_offset"
title="UTC offset" target="_blank">UTC offset</a>, local date time and 
UTC date time.

```python
import time

local_time = time.localtime()

print("Time Zone: ", time.tzname)
print("Time Zone: ", time.strftime("%Z", local_time))
print("Date and Time Zone: ", time.strftime("%Y-%m-%d %H:%M:%S %Z", local_time) )
print("UTC Offset: ", time.strftime("%z", local_time))
```

Output:

```
Time Zone:  ('AUS Eastern Standard Time', 'AUS Eastern Summer Time')
Time Zone:  AUS Eastern Summer Time
Date and Time Zone:  2023-02-10 15:19:18 AUS Eastern Summer Time
UTC Offset:  +1100
```

The most important piece of information is <code>UTC Offset:  +1100</code>,
the first two (2) digits, positive <code>11</code>, is the number of hours,
the second two (2) digits, <code>00</code>, is the number of minutes. I am
in the beautiful state of Victoria, Australia; and at the time of this writing,
we are 11 (eleven) hours ahead of the UTC date time. Of course, depending on 
where we are, this UTC offset figure could be a negative, which would indicate
that we are behind the UTC date time.

Let's look at this 11 (eleven) hours ahead of the UTC date time:

```python
from datetime import datetime, timezone

local_datetime = datetime.now()
utc_datetime = datetime.now(timezone.utc)

local_iso_str = datetime.strftime(local_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]
utc_iso_str = datetime.strftime(utc_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]

print(f"local dt: {local_iso_str}, tzname: {local_datetime.tzname()}")
print(f"  utc dt: {utc_iso_str}, tzname: {utc_datetime.tzname()}")

print("\n")

print(f"local dt: {local_datetime.isoformat()}")
print(f"  utc dt: {utc_datetime.isoformat()}")
```

Output:

```
local dt: 2023-02-10T15:46:08.407, tzname: None
  utc dt: 2023-02-10T04:46:08.407, tzname: UTC

local dt: 2023-02-10T15:46:08.407281
  utc dt: 2023-02-10T04:46:08.407281+00:00
```

We can see that my local date time is <strong>11 hours ahead of UTC</strong>.
The UTC offset for UTC date time is <code>00:00</code> -- which is understandable.

The time zone name for the local date time is <code>None</code>, and <code>UTC</code>
for UTC date time. These are in conformance with
<a href="https://docs.python.org/3/library/datetime.html#datetime.datetime.tzname"
title="datetime.tzname()"target="_blank">datetime.tzname()</a>. However, the first
time I wrote this code, I was expecting either <code>AUS Eastern Standard Time</code> 
or <code>AUS Eastern Summer Time</code> for the local date time! 😂 This leads to 
<a href="https://docs.python.org/3/library/datetime.html#datetime.datetime.astimezone"
title="datetime.astimezone(tz=None)" target="_blank">datetime.astimezone(tz=None)</a>.

Add the following 5 (five) lines to the end of the last example:

```python
print("\n")

utc_to_local_datetime = utc_datetime.astimezone()
utc_2_local_iso_str = datetime.strftime(utc_to_local_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]

print( f"utc to local dt: {utc_2_local_iso_str}, tzname: {utc_to_local_datetime.tzname()}" )
print( f"utc to local dt: {utc_to_local_datetime.isoformat()}" )
```

The last two (2) output lines are from the new code:

```
local dt: 2023-02-10T16:24:40.089, tzname: None
  utc dt: 2023-02-10T05:24:40.089, tzname: UTC

local dt: 2023-02-10T16:24:40.089415
  utc dt: 2023-02-10T05:24:40.089415+00:00

utc to local dt: 2023-02-10T16:24:40.089, tzname: AUS Eastern Summer Time
utc to local dt: 2023-02-10T16:24:40.089415+11:00
```

We can see that 
<a href="https://docs.python.org/3/library/datetime.html#datetime.datetime.astimezone"
title="datetime.astimezone(tz=None)" target="_blank">datetime.astimezone(tz=None)</a>
converts a UTC date time into local date time correctly, and the converted value now
also has local time zone name; and furthermore, it still retains the original UTC 
offset value.

We can also calculate the UTC offset from our local date time:

```python
from datetime import datetime, timezone

local_now = datetime.now()
utc_now = local_now.astimezone(timezone.utc)
local_as_utc = local_now.replace(tzinfo=timezone.utc)

print( f"{local_now}, tzname: {local_now.tzname()}" )
print( f"{utc_now}, tzname: {utc_now.tzname()}" )
print( f"{local_as_utc}, tzname: {local_as_utc.tzname()}" )
print( f"{local_as_utc - utc_now}" )
```

The last output line, <code>11:00:00</code>, is the UTC offset:

```
2023-02-11 10:08:22.023929, tzname: None
2023-02-10 23:08:22.023929+00:00, tzname: UTC
2023-02-11 10:08:22.023929+00:00, tzname: UTC
11:00:00
```

❷ Consider cases where date time data are UTC date time, but stored with no time zone
information. The <code>expiry</code> column of the following MySQL table:

```sql
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(255) DEFAULT NULL,
  `data` blob,
  `expiry` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
```

If you are familiar with the Python 
<a href="https://flask.palletsprojects.com/en/2.2.x/"
title="Flask Web Development Framework" target="_blank">Flask Web Development Framework</a>,
you might recognise that the above <code>sessions</code> table is
the server-side session table implemented by the package 
<a href="https://flask-session.readthedocs.io/en/latest/"
title="Flask-Session" target="_blank">Flask-Session</a>.

And a PostgreSQL equivalence:

```sql
CREATE TABLE IF NOT EXISTS ompdev1.sessions
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY 
        ( CYCLE INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 
        2147483647 CACHE 1 ),
    session_id character varying(255) COLLATE 
        pg_catalog."default",
    data bytea,
    expiry timestamp without time zone,
    CONSTRAINT sessions_pkey PRIMARY KEY (id),
    CONSTRAINT sessions_session_id_key UNIQUE (session_id)
)
```

Values for <code>sessions.expiry</code> are stored as:

● MySQL: <code>2023-02-09 05:00:45</code>, <code>2023-02-09 03:58:36</code>, etc.

● PostgreSQL: <code>2023-01-07 11:18:32.442136</code>, <code>2023-02-06 21:33:06.190584</code>, etc.

We know these are UTC date time: because that's how they are in the 
<a href="https://flask-session.readthedocs.io/en/latest/"
title="Flask-Session" target="_blank">Flask-Session</a> package code,
when checking if a particular server session has expired, the package
code also uses UTC date time comparison.

<strong><em>Suppose we want to check when 
a particular abandoned session has expired in our own local date time. 
How do we do the conversion?</em></strong>

Let's have a look at two (2) methods which will help to accomplish 
the conversion.

⓵ Method 
<a href="https://docs.python.org/3/library/datetime.html?timetuple#datetime.datetime.timetuple"
title="datetime.timetuple()" target="_blank">datetime.timetuple()</a> breaks 
a date time value into individual components, and returns 
<a href="https://docs.python.org/3/library/time.html#time.struct_time"
title="class time.struct_time" target="_blank">class time.struct_time</a>, 
which we can access as a tuple:

```python
time.struct_time((d.year, d.month, d.day,
                  d.hour, d.minute, d.second,
                  d.weekday(), yday, dst))
```

In the following example, we get the local date time, call the above
method, then write out individual elements:

```python
from datetime import datetime

local_datetime = datetime.now()

print(f"local dt: {local_datetime.isoformat()}")

dt_tuple = local_datetime.timetuple()

print("\n")

print(dt_tuple[0], dt_tuple[1], dt_tuple[2])
print(dt_tuple[3], dt_tuple[4], dt_tuple[5])
print(dt_tuple[6], dt_tuple[7], dt_tuple[8])
```

```
local dt: 2023-02-10T23:34:00.062678

2023 2 10
23 34 0
4 41 -1
```

We're interested in the first 6 (six) elements, which are <code>year</code>,
<code>month</code>, <code>day</code>, <code>hour</code>, <code>minute</code>
and <code>second</code>.

⓶ Next, the 
<a href="https://docs.python.org/3/library/datetime.html#datetime.datetime"
title="datetime constructor" target="_blank">datetime constructor</a> reads:

```python
class datetime.datetime(year, month, day, hour=0, minute=0, 
    second=0, microsecond=0, tzinfo=None, *, fold=0)
```

What that means is, if we have <code>year</code>, <code>month</code>, 
<code>day</code>, <code>hour</code>, <code>minute</code>, <code>second</code>,
<code>microsecond</code> and <code>time zone</code>, we can create a time zone
aware date time. We'll ignore <code>microsecond</code>, and default it to 
<code>0</code> from here onward.

Let's pick one of the <code>sessions.expiry</code> value from above,
<code>2023-02-06 21:33:06.190584</code>, and see how this constructor
works with the following example:

```python
from datetime import datetime, timezone

utc_datetime = datetime(2023, 2, 6, 21, 33, 6, 0, timezone.utc)

utc_iso_str = datetime.strftime(utc_datetime, "%Y-%m-%dT%H:%M:%S.%f")[:-3]
utc_2_local_iso_str = datetime.strftime(utc_datetime.astimezone(), "%Y-%m-%dT%H:%M:%S.%f")[:-3]

print( "         utc dt: ", utc_iso_str, "tzname: ", utc_datetime.tzname() )
print( "utc to local dt: ", utc_2_local_iso_str, "tzname: ", utc_datetime.astimezone().tzname() )
```

```
         utc dt:  2023-02-06T21:33:06.000 tzname:  UTC
utc to local dt:  2023-02-07T08:33:06.000 tzname:  AUS Eastern Summer Time
```

In short, converting <code>sessions.expiry</code> date time to UTC date time, 
or more precisely, assigning UTC time zone to the <code>sessions.expiry</code> 
values, there are two (2) steps involved:

<ul>
<li style="margin-top:10px;">
Use 
<a href="https://docs.python.org/3/library/datetime.html?timetuple#datetime.datetime.timetuple"
title="datetime.timetuple()" target="_blank">datetime.timetuple()</a> to break
a <code>sessions.expiry</code> value into individual components.
</li>

<li style="margin-top:10px;">
Call 
<a href="https://docs.python.org/3/library/datetime.html#datetime.datetime"
title="datetime constructor" target="_blank">datetime constructor</a> with
these components and <code>timezone.utc</code> to create a UTC date time.
</li>
</ul>

<em>I am not sure if this is the most effective way of doing this, please keep
a look out for a better approach.</em>

I have tried this successfully with MySQL and PostgreSQL:

{% include image-gallery.html list=page.gallery-image-list %}

✿✿✿

I hope you find the information in this post useful and helpful. Thank you
for reading and stay safe as always.
