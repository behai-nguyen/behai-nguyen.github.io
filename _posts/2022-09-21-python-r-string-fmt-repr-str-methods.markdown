---
layout: post
title: "Python: the !r string format and the __repr__() and __str__() methods."
description: The !r string format is a convenient one to use in certain cases. It is related closely to the __repr__() dunder method; and this method and the __str__() are often discussed together. In this post, we review __repr__() and __str__() methods and then the !r string format.
tags:
- Python 
- !r
- string format
- dunder method
- __repr__
- __str__

---

The **!r** string format is a convenient one to use in certain cases. It is related closely to the 
**__repr__()** dunder method; and this method and the **__str__()** are often discussed 
together. In this post, we review **__repr__()** and **__str__()** methods and then the 
**!r** string format.

| ![039-feature-image.png](https://behainguyen.files.wordpress.com/2022/09/039-feature-image.png) |
|:--:|
| *Python: the !r string format and the &#95;&#95;repr__() and &#95;&#95;str__() methods.* |

An usage example of the string format 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
!r</span>:

```python
fmt_data = '{!r:^12} {!r:^15} {!r:^10}'
```

On
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
!r</span>, 
<a href="https://peps.python.org/pep-3101/"
title="PEP 3101 – Advanced String Formatting" 
target="_blank">PEP 3101 – Advanced String Formatting</a> states:

>!r - convert the value to a string using repr().
>
><a href="https://peps.python.org/pep-3101/#explicit-conversion-flag" title="Explicit Conversion Flag" target="_blank">https://peps.python.org/pep-3101/#explicit-conversion-flag</a>

<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
repr()</span> and 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
str()</span> official documentations can be found in the following links 
<a href="https://docs.python.org/3/library/functions.html#repr"
title="repr(object)" target="_blank">repr(object)</a>,
<a href="https://docs.python.org/3/library/stdtypes.html#str"
title="class str(object='')" target="_blank">class str(object='')</a>,
<a href="https://docs.python.org/3/reference/datamodel.html#object.__repr__"
title="object.__repr__(self)" target="_blank">object.&#95;&#95;repr__(self)</a> and 
<a href="https://docs.python.org/3/reference/datamodel.html#object.__str__"
title="object.__str__(self)" target="_blank">object.&#95;&#95;str__(self)</a>

Basically: 

<ul>
<li style="margin-top:5px;">
<a href="https://docs.python.org/3/library/functions.html#repr"
title="repr(object)" target="_blank">repr(object)</a> calls 
<a href="https://docs.python.org/3/reference/datamodel.html#object.__repr__"
title="object.__repr__(self)" target="_blank">object.&#95;&#95;repr__(self)</a>; 
and we implement the later in our own codes.
</li>
<li style="margin-top:10px;">
<a href="https://docs.python.org/3/library/stdtypes.html#str"
title="class str(object='')" target="_blank">class str(object='')</a>
calls 
<a href="https://docs.python.org/3/reference/datamodel.html#object.__str__"
title="object.__str__(self)" target="_blank">object.&#95;&#95;str__(self)</a>;
and we implement the later in our own codes.
</li>

<li style="margin-top:10px;">
The purpose of 
<a href="https://docs.python.org/3/reference/datamodel.html#object.__str__"
title="object.__str__(self)" target="_blank">object.&#95;&#95;str__(self)</a>
is to provide a friendly human readable string presentation of an object 
instance.
</li>
<li style="margin-top:10px;">
The purpose of 
<a href="https://docs.python.org/3/reference/datamodel.html#object.__repr__"
title="object.__repr__(self)" target="_blank">object.&#95;&#95;repr__(self)</a> 
is to provide a string representation of an object instance, 
<strong>AND</strong> the 
<a href="https://docs.python.org/3/library/functions.html#eval"
title="eval(expression[, globals[, locals]])"
target="_blank">eval(expression[, globals[, locals]])</a> function 
should be able to take this string and convert it to the same original
object instance from which the string is generated from.
</li>
</ul>

Let's illustrate this with an example:

```python
class Person( object ):
    def __init__( self, given_name, surname ):
        self.__given_name = given_name
        self.__surname = surname
		
    def __repr__( self ):
        fmt = u"{}(given_name='{}', surname='{}')"
		
        return fmt.format( self.__class__.__name__, \
            self.__given_name, self.__surname )

    def __str__( self ):
        fmt = u"{}: Given Name: '{}', Surname: '{}')"
		
        return fmt.format( self.__class__.__name__, \
            self.__given_name, self.__surname )
```

<em>-- Please note, in case you wonder if I've copied this example 
from elsewhere... I have 😂, it is a very popular example used to 
illustrate this topic, I've also made some minor adjustments to it.</em>

Let's see how it works:

```python
person = Person( 'Văn Bé Hai', 'Nguyễn' ) 
# My full name, written in Vietnamese: Nguyễn Văn Bé Hai 😂

print( person.__str__() )
print( str( person ) )
print( '---' )
print( person.__repr__() )
print( repr( person ) )
```

As expected, the output of 
<span class="keyword">
object_instance.&#95;&#95;str__()</span> and 
<span class="keyword">
str( object_instance )</span> are the same; and so do
<span class="keyword">
object_instance.&#95;&#95;repr__()</span> and 
<span class="keyword">
repr( object_instance )</span>.

```
Person: Given Name: 'Văn Bé Hai', Surname: 'Nguyễn')
Person: Given Name: 'Văn Bé Hai', Surname: 'Nguyễn')
---
Person(given_name='Văn Bé Hai', surname='Nguyễn')
Person(given_name='Văn Bé Hai', surname='Nguyễn')
```

Continue on, let's see how 
<span class="keyword">
person.&#95;&#95;repr__()</span> works with 
<a href="https://docs.python.org/3/library/functions.html#eval"
title="eval(expression[, globals[, locals]])"
target="_blank">eval(expression[, globals[, locals]])</a>:

```python
repr_str = person.__repr__()
person1 = eval( repr_str )
print( str( person1 ) )
```

And it does work as expected:

```
Person: Given Name: 'Văn Bé Hai', Surname: 'Nguyễn')
```

Now, we try out 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
!r</span> string format with object instances
<span class="keyword">
person</span> and
<span class="keyword">
person1</span>:

```python
print( '"person" instance reads: {!r}'.format(person) )
print( '"person1" instance reads: {!r}'.format(person1) )
```

And we get:

```
"person" instance reads: Person(given_name='Văn Bé Hai', surname='Nguyễn')
"person1" instance reads: Person(given_name='Văn Bé Hai', surname='Nguyễn')
```

-- The 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
!r</span> format does eventually call 
<span class="keyword">
&#95;&#95;repr__()</span>.

Back to 
<span class="keyword">
class Person</span>, we could get rid of the double single quote around
the curly bracket pairs ( 
 <span class="keyword">
'{}'</span> ) in the two variables
<span class="keyword">
fmt</span>, and use 
<span class="keyword">
{!r}</span>:

```python
class Person( object ):
    ...

    def __repr__( self ):
        # fmt = u"{}(given_name='{}', surname='{}')"
        fmt = u"{}(given_name={!r}, surname={!r})"
        ...		

    def __str__( self ):
        # fmt = u"{}: Given Name: '{}', Surname: '{}')"
        fmt = u"{}: Given Name: {!r}, Surname: {!r})"
        ...		
```

Finally, let's look at the example listed in the beginning of this post:
<span class="keyword">
fmt_data = '{!r:^12} {!r:^15} {!r:^10}'</span> -- please see this official document 
<a href="https://docs.python.org/3/library/string.html#grammar-token-format-spec-width"
title="Format Specification Mini-Language"
target="_blank">Format Specification Mini-Language</a> for much more info. 
In a nutshell, 
<span style="background-color:#d1d1d1;padding-top:0.125em;padding-right:0.25em;padding-bottom:0.125em;padding-left:0.25em;">
^</span> centres the string within the specified width, in this 
example, widths are 12, 15 and 10 respectively -- I have three ( 3 ) 
<span class="keyword">
Boolean</span> fields, and I would like to display them in tabular 
format, in the middle of three ( 3 ) headers with different lengths:

```python
create_own = False
create_other = False 
view_own = True

fmt_header = '{:^12} {:^15} {:^10}'
fmt_data = '{!r:^12} {!r:^15} {!r:^10}'
	
print( fmt_header.format('Create Own', 'Create Other', 'View Own' ) )
print( fmt_data.format(create_own, create_other, view_own) )
```

And the output looks like:

```
 Create Own   Create Other    View Own
   False          False         True
```

This is what I mean in the beginning 
<em>“The !r string format is a convenient one to use in certain cases.”</em>

It seems 
<span class="keyword">
Python</span> offers a lot in term of string formatting.
I find this information very useful. And I hope you do too. I certainly 
enjoy writing this post. Thank you for reading and stay safe as always.
