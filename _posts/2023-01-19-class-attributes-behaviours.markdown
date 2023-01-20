---
layout: post
title: "Python: class attributes, some behaviours we should be aware of."
description: We look at some behaviours of class attributes which can help to make life easier for us -- mere programmers.
tags:
- Python
- class
- attribute
- class attribute
---

*We look at some behaviours of class attributes which can help to make life easier for us -- mere programmers.*

| ![054-feature-image.png](https://behainguyen.files.wordpress.com/2023/01/054-feature-image.png) |
|:--:|
| *Python: class attributes, some behaviours we should be aware of.* |

We will look at the following three (3) behaviours:

<ol>
<li style="margin-top:10px">
From the Python official documentation:
<blockquote class="wp-block-quote">
<p>9.4. Random Remarks</p>
<p>If the same attribute name occurs in both an instance and in a class, then attribute lookup prioritizes the instance.</p>
<cite><a href="https://docs.python.org/3/tutorial/classes.html" rel="nofollow">https://docs.python.org/3/tutorial/classes.html</a>:</cite></blockquote>
</li>

<li style="margin-top:10px">
Setting the value of a class attribute via the class will propagate the 
new value to class instances, whom have not overridden the value of this 
class attribute. This is in conformance with the documentation above.
</li>

<li style="margin-top:10px">
Setting the value of a class attribute via the class will propagate the 
new value down to child classes, but no vice versa.
</li>
</ol>

Let's explore these points via examples.

❶ Attribute lookup prioritises the instance.

This is an example from the documentation page quoted above, I have tweaked it a tiny bit.

```python
class Warehouse:
    purpose = 'Storage'
    region = 'west'
```

Then:

```python
w1 = Warehouse()
print("1: ", w1.purpose, w1.region)
```

Output -- these are default class attributes' values:

```
1:  Storage west
```

```python
w2 = Warehouse()
w2.region = 'east'
print("2: ", w2.purpose, w2.region)
```

We just instantiate an instance of <code>Warehouse</code>, then override the 
value of the <code>region</code> attribute with <code>'east'</code> <em>(*)</em>:

```
2:  Storage east
```

-- <em>(*)</em>: <strong>please note</strong>, <em>what I've just written 
above might not be correct... According to the quoted documentation, 
the statement <code>w2.region = 'east'</code> might actually mean assigning 
the new attribute <code>region</code> to instance <code>w2</code>, rather 
than <strong>override</strong> as I've written.</em>

❷ Setting the value via class propagates the new value to instances whom 
have not provided their own value.

We continue with examples in ❶:

```python
Warehouse.region = 'north'
w3 = Warehouse()
print("3: ", w3.purpose, w3.region)
```

Instance <code>w3</code> is created with whatever the class attributes' 
values of <code>Warehouse</code> class:

```
3:  Storage north
```

<strong>Setting <code>Warehouse.region = 'north'</code>, how does this affect
the existing two (2) instances <code>w1</code> and <code>w2</code>?</strong>

```python
print(f"4: w1.region: {w1.region}, w2.region: {w2.region}")
```

```
4: w1.region: north, w2.region: east
```

<code>w1</code> has not set its own value for the <code>region</code> attribute, 
setting the new value via the class <code>Warehouse</code> does propagate 
back to instance <code>w1</code>. <code>w2</code>, on the hand, has set its 
own, so it was not affected.

❸ Setting the value propagates from the parent class to child classes, but 
not vice versa.

Consider the following classes:

```python
class Engine:
    started = False;

class TwoStrokeEngine(Engine):
    pass
	
class FourStrokeEngine(Engine):
    pass
```

In their initial state, <code>started</code> is <code>False</code> for all classes:

```python
print(f"1. Engine.started: {Engine.started}")
print(f"1. TwoStrokeEngine.started: {TwoStrokeEngine.started}")
print(f"1. FourStrokeEngine.started: {FourStrokeEngine.started}\n")
```

```
1. Engine.started: False
1. TwoStrokeEngine.started: False
1. FourStrokeEngine.started: False
```

Let's set <code>Engine.started</code> to <code>True</code>:

```python
Engine.started = True

print(f"2. Engine.started: {Engine.started}")
print(f"2. TwoStrokeEngine.started: {TwoStrokeEngine.started}")
print(f"2. FourStrokeEngine.started: {FourStrokeEngine.started}\n")
```

```
2. Engine.started: True
2. TwoStrokeEngine.started: True
2. FourStrokeEngine.started: True
```

Let's switch <code>Engine.started</code> back to <code>False</code>:

```python
Engine.started = False

print(f"3. Engine.started: {Engine.started}")
print(f"3. TwoStrokeEngine.started: {TwoStrokeEngine.started}")
print(f"3. FourStrokeEngine.started: {FourStrokeEngine.started}\n")
```

```
3. Engine.started: False
3. TwoStrokeEngine.started: False
3. FourStrokeEngine.started: False
```

Let's set <code>FourStrokeEngine.started</code> to <code>True</code>:

```python
FourStrokeEngine.started = True

print(f"4. Engine.started: {Engine.started}")
print(f"4. TwoStrokeEngine.started: {TwoStrokeEngine.started}")
print(f"4. FourStrokeEngine.started: {FourStrokeEngine.started}\n")
```

```
4. Engine.started: False
4. TwoStrokeEngine.started: False
4. FourStrokeEngine.started: True
```

-- We can see that, setting the value propagates from the parent class to 
child classes, but not vice versa.

What about their instances? Continue on with the examples above:

```python
"""
FourStrokeEngine.started is True from above.
"""

engine = Engine()
two_stroke_engine = TwoStrokeEngine()
four_stroke_engine = FourStrokeEngine()
four_stroke_engine1 = FourStrokeEngine()

print(f"5. engine.started: {engine.started}")
print(f"5. two_stroke_engine.started: {two_stroke_engine.started}")
print(f"5. four_stroke_engine.started: {four_stroke_engine.started}")
print(f"5. four_stroke_engine1.started: {four_stroke_engine1.started}\n")

Engine.started = True

print(f"6. engine.started: {engine.started}")
print(f"6. two_stroke_engine.started: {two_stroke_engine.started}")
print(f"6. four_stroke_engine.started: {four_stroke_engine.started}")
print(f"6. four_stroke_engine1.started: {four_stroke_engine1.started}\n")
```

Output:

```
5. engine.started: False
5. two_stroke_engine.started: False
5. four_stroke_engine.started: True
5. four_stroke_engine1.started: True

6. engine.started: True
6. two_stroke_engine.started: True
6. four_stroke_engine.started: True
6. four_stroke_engine1.started: True
```

Let's set <code>TwoStrokeEngine.started</code> to <code>False</code>,
and see what happens to existing instances:

```python
TwoStrokeEngine.started = False

print(f"7. engine.started: {engine.started}")
print(f"7. two_stroke_engine.started: {two_stroke_engine.started}")
print(f"7. four_stroke_engine.started: {four_stroke_engine.started}")
print(f"7. four_stroke_engine1.started: {four_stroke_engine1.started}\n")
```

```
7. engine.started: True
7. two_stroke_engine.started: False
7. four_stroke_engine.started: True
7. four_stroke_engine1.started: True
```

It makes sense that only <code>two_stroke_engine.started</code> was affected.

I did get caught out on some of these issues... And hence this post. I do hope
you find this post useful. Thank you for reading and stay safe as always.
