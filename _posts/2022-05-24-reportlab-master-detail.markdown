---
layout: post
title: "Python: ReportLab -- a Master Detail Report."

---

Constructing a master-detail report using the ReportLab library, where master information and detail column headers are repeated on every new page for long detail listing that spans over multiple pages.

| ![020-feature-image.png](https://behainguyen.files.wordpress.com/2022/05/020-feature-image.png) |
|:--:|
| *Python: ReportLab -- a Master Detail Report.* |

Using <span class="keyword">
ReportLab</span>, I discuss how to construct
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/main/demo/020/020-reportlab-master-detail.pdf" 
title="PDF master detail report" target="_blank">
this PDF master detail report ( this link goes to GitHub )</a>: it has 
a distinct cover page and an end page, page header and page footer, 
and page number in the format <span class="keyword">
“Page 99 of 999_total_pages”</span>.

## Table of contents

<ul>
	<li><a href="#source-output">Source Codes, Data, SQL Query and Output PDF</a></li>

	<li><a href="#features">Features Implemented For The Report In This Post</a></li>

	<li><a href="#environments">Environments</a></li>

	<li><a href="#references">References</a></li>

	<li><a href="#codes-walking">Walking Through The Codes</a>	
		<ul>
			<li><a href="#page-size-margins">Page Size and Margins</a></li>

			<li><a href="#document-canvasmaker">BaseDocTemplate.build( ..., canvasmaker=canvas.Canvas )</a></li>

			<li><a href="#lastpage">class LastPage( Flowable )</a></li>

			<li><a href="#document-frame-pagetemplate">BaseDocTemplate, Frame and PageTemplate</a></li>

			<li><a href="#master-detail-effect">Achieving the Master-Detail Effect</a></li>

			<li><a href="#contents-layout">Report Contents and Layout</a>		
				<ul>
					<li><a href="#contents">Report Contents</a></li>

					<li><a href="#contents">Report Layout</a></li>
				</ul>	
			</li>
		</ul>
	</li>
	
	<li><a href="#concluding-remarks">Concluding Remarks</a></li>

</ul>

<h2 style="color:teal;">
  <a id="source-output">Source Codes, Data, SQL Query and Output PDF</a>
</h2>

The source code, source data, source SQL query and the output PDF are in 
the following <span class="keyword">
GitHub</span> directory: 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/tree/main/demo/020/" 
title="" target="_blank">https://github.com/behai-nguyen/behai-nguyen.github.io/tree/main/demo/020/</a>.

<ol>
    <li>
	    020-depts-emps.json -- is an export resultset from 
		<span class="keyword">
        MySQL Workbench 6.3 CE</span>,
        the source query is “020-depts-emps.sql”. The source database is the
		<span class="keyword">
        MySQL test data </span>		
		released by Oracle Corporation. Downloadable from
		<a href="https://github.com/datacharmer/test_db" title="MySQL test data " target="_blank">https://github.com/datacharmer/test_db</a>.
	</li>
	
    <li style="margin-top:10px;">
	    020-depts-emps.sql -- <span class="keyword">
        MySQL query</span> to retrieve the result set in “020-depts-emps.json”.
	</li>
	
    <li style="margin-top:10px;">
	    020-reportlab-master-detail.py -- <span class="keyword">
        Python</span> source codes.
	</li>
	
    <li style="margin-top:10px;">
	    020-reportlab-master-detail.pdf -- output PDF.
	</li>
</ol>

<h2 style="color:teal;">
  <a id="features">Features Implemented For The Report In This Post</a>
</h2>

<ol>
<li>
Single-level master-detail report: listing of Departments and Employees 
within each department.
</li>

<li style="margin-top:10px;">
Repeat master record and detail header on new pages when spanning over 
several pages.
</li>

<li style="margin-top:10px;">
The report has a cover page and an end page. The formats of these two pages 
are different to the report page format.
</li>   
   
<li style="margin-top:10px;">
Force page breaks.
</li>

<li style="margin-top:10px;">
Select page templates on forcing page breaks.
</li>

<li style="margin-top:10px;">
Report pages header and footer.
</li>

<li style="margin-top:10px;">
Page count in the form of 
<span class="keyword">
“Page 99 of 999_total_pages”</span>.
Page count excludes cover page and end page.
</li>
</ol>
   
<h2 style="color:teal;">
  <a id="environments">Environments</a>
</h2>

<ol>
<li>
<span class="keyword">
Python 3.10.1</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">
ReportLab 3.6.9</span>.
</li>

<li style="margin-top:10px;">
<span class="keyword">
ReportLab User Guide</span> version 
<span class="keyword">
3.5.56</span>, 
<span class="keyword">
“Document generated on 2020/12/02 11:31:59”</span>;
henceforth <span class="keyword">
“User Guide”</span>, downloadable from 
<a href="https://www.reportlab.com/docs/reportlab-userguide.pdf" 
title="ReportLab User Guide version 3.5.56, Document generated on 2020/12/02 11:31:59" 
target="_blank">https://www.reportlab.com/docs/reportlab-userguide.pdf</a>
</li>

<li style="margin-top:10px;">
<span class="keyword">
simplejson 3.17.6</span>.
</li>
</ol>

<h2 style="color:teal;">
  <a id="references">References</a>
</h2>

<ul>
<li>
<a href="https://www.papersizes.org/" 
title="International Paper Sizes & Formats With Dimensions" 
target="_blank">https://www.papersizes.org/</a> and 
<a href="http://www.metricationmatters.com/docs/PageBordersInchesORmillimetres.pdf" 
title="Page borders — inches or millimetres?" 
target="_blank">http://www.metricationmatters.com/docs/PageBordersInchesORmillimetres.pdf</a>
-- these two discuss paper sizes and margins.
</li>

<li style="margin-top:10px;">
<a href="https://code.activestate.com/recipes/576832/" 
title="ActiveState Code Recipes 576832" 
target="_blank">https://code.activestate.com/recipes/576832/</a>   
-- this post discusses how to do page number in the format 
<span class="keyword">
“Page 99 of 999_total_pages”</span>.
</li>   
  
<li style="margin-top:10px;">  
<a href="https://reportlab-users.reportlab.narkive.com/HQgHhQiA/working-out-height-of-text" 
title="Working out height of text" 
target="_blank">https://reportlab-users.reportlab.narkive.com/HQgHhQiA/working-out-height-of-text</a> 
-- font height calculation.
</li>
</ul>

<h2 style="color:teal;">
  <a id="codes-walking">Walking Through The Codes</a>
</h2>

<p>
The discussion in this section is based on the assumption that we've 
gone through the 
<span class="keyword">
User Guide</span>.
</p>

<p>
The source code is a bit over 400 ( four hundreds ) lines, I will not
be listing it in this post, please see it at this 
<span class="keyword">
GitHub</span> address 
<a href="https://github.com/behai-nguyen/behai-nguyen.github.io/blob/main/demo/020/020-reportlab-master-detail.py" 
title="The Python source file on GitHub" 
target="_blank">https://github.com/behai-nguyen/behai-nguyen.github.io/blob/main/demo/020/020-reportlab-master-detail.py</a>.
Please see also comments and 
<span class="keyword">
docstrings</span> within the codes.
</p>

<h3 style="color:teal;">
  <a id="page-size-margins">Page Size and Margins</a>
</h3>

With <span class="keyword">ReportLab</span>, 
we need to manage page size and page margins ourselves.
In this post, we are using A4 in portrait orientation, the page size 
for A4 portrait is:

{% highlight python %}
PAGE_WIDTH  = defaultPageSize[ 0 ]
PAGE_HEIGHT = defaultPageSize[ 1 ]
{% endhighlight %}

See modules 
 <span class="keyword">
\Lib\site-packages\reportlab\lib\pagesizes.py</span> and 
<span class="keyword">
\Lib\site-packages\reportlab\lib\units.py</span>. We could easily print out 
<span class="keyword">
mm</span>, 
<span class="keyword">
PAGE_WIDTH</span> and 
<span class="keyword">
PAGE_HEIGHT </span> to verify.

I'm following the recommendations in this post
<a href="http://www.metricationmatters.com/docs/PageBordersInchesORmillimetres.pdf" 
title="Page borders — inches or millimetres?" 
target="_blank">http://www.metricationmatters.com/docs/PageBordersInchesORmillimetres.pdf</a>,
where for A4, margin top, right, bottom and left are defined as 
25.4mm, 31.7mm, 25.4mm and 31.7mm, respectively.

The two decimal numbers 19.55 and 26.44 give margins very closed to the ones
above. I verify this by printing out a page with a box using the four margin
coordinates, then using a ruler to measure. I'm not sure if this makes any
sense or not... We could certainly reduce these numbers to give us a larger
working area.

<span class="keyword">
effective_page_width</span> and 
<span class="keyword">
effective_page_height</span> define the working area.

<h3 style="color:teal;">
  <a id="document-canvasmaker">BaseDocTemplate.build( ..., canvasmaker=canvas.Canvas )</a>
</h3>

To achieve <span class="keyword">
“Page 99 of 999_total_pages”</span>, 
<a href="https://code.activestate.com/recipes/576832/" 
title="ActiveState Code Recipes 576832" 
target="_blank">https://code.activestate.com/recipes/576832/</a>
implements <span class="keyword">
canvasmaker</span>, which is the following class:

{% highlight python %}
class NumberedCanvas( canvas.Canvas )
{% endhighlight %}

This is my understanding of the codes. Each page is first interpreted 
from the given list of 
<span class="keyword">
Flowables</span> as 
<span class="keyword">
Python</span> dictionary, 
<span class="keyword">
NumberedCanvas</span> 
then stores these in its internal list, the total number of elements
in this internal list is the total of pages.

When all pages ( or dictionaries ) have been processed, 
<span class="keyword">
NumberedCanvas</span> 
then generates the actual PDF, as each dictionary is processed,
header and footer for each page is drawn onto the final PDF page.

I implement my own conditions to exclude cover page and end page 
from total pages, and also excluding header and footer drawing.

<h3 style="color:teal;">
  <a id="lastpage">class LastPage( Flowable )</a>
</h3>

This class is responsible for drawing the “content” of the last page.

I implement the last page as a
<span class="keyword">
Flowables</span>. Another method requires less codes, but I
feel it is a bit clunky, so I go with this.

<h3 style="color:teal;">
  <a id="document-frame-pagetemplate">BaseDocTemplate, Frame and PageTemplate</a>
</h3>

<span class="keyword">
Frame</span> and <span class="keyword">
PageTemplate</span> essentially define the skeleton structure of report pages. Method:

{% highlight python %}
def prepare_document_instance( output_filename ):
{% endhighlight %}

creates an instance of 
<span class="keyword">BaseDocTemplate</span>, 
parameters should be self-explanatory based on the 
<span class="keyword">User Guide</span>.

It then creates three ( 3 ) 
 <span class="keyword">
Frame</span> instances, and a 
<span class="keyword">
PageTemplate</span> instance for each 
<span class="keyword">
Frame</span> instance. Again, these are covered in the 
<span class="keyword">User Guide</span>.

Finally, all 
<span class="keyword">PageTemplate</span> 
instances are added to the document instance:

{% highlight python %}
pdf.addPageTemplates( [ cover_template, report_data_template, last_page_template ] )
{% endhighlight %}

Please note, the order of adding 
<span class="keyword">PageTemplate</span>
instances might be important: <span style="font-style:italic;font-weight:bold;color:blue;">
without explicitly selecting a 
<span class="keyword">PageTemplate</span>
instance, the first one will be used</span>.

<h3 style="color:teal;">
  <a id="master-detail-effect">Achieving the Master-Detail Effect</a>
</h3>

This is happening within method:

{% highlight python %}
def data_to_flowables( flowables, cols_width, table_style ):
{% endhighlight %}

It first calls to:

{% highlight python %}
data = prepare_data()
{% endhighlight %}

Think of this method as querying a database and getting back a recordset.

<span class="keyword">data</span>
is an array of object. Each object has Department's info ( master ), and a 
two-dimensional array, which is a list of employees ( details ).

Department info is formatted into a string, and wrapped within a
<span class="keyword">Paragraph</span>
instance -- which is also a 
<span class="keyword">Flowable</span>.

This <span class="keyword">Paragraph</span>
instance <span style="font-style:italic;font-weight:bold;color:blue;">
is wrapped within and array, and is then inserted into the employee data array 
-- ( in the code it is now 
<span class="keyword">report_data</span> )
-- as the first element! THIS LOOKS STRANGE, but 
<span class="keyword">ReportLab</span>
allows this. </span>

The column headers for employee records is also an array, and is inserted into
<span class="keyword">report_data</span>
at the second position.

<span class="keyword">report_data</span>
array is then fed to
<span class="keyword">Table</span> to
create an instance of this 
<span class="keyword">Flowable</span>.

{% highlight python %}
report_table = Table( report_data, colWidths=cols_width, style=table_style, repeatRows=2 )
{% endhighlight %}

<span style="font-style:italic;font-weight:bold;color:blue;">IMPORTANT TO NOTE: 
<span class="keyword">repeatRows=2</span> 
is to instruct the document to reprint the first two rows in
<span class="keyword">report_data</span>
on every new page which is occurring automatically</span> ( as opposed to being forced
manually ). <span style="color:blue;">And so the Department info and Employee header row
get repeated for detail records listing which spans several pages</span>.

Finally the 
<span class="keyword">Table ( Flowable )</span>
instance get added to the main flowable list:

{% highlight python %}
flowables.append( report_table )
{% endhighlight %}

<h3 style="color:teal;">
  <a id="contents-layout">Report Contents and Layout</a>
</h3>

This is the guts of this report's implementation. The method is:

{% highlight python %}
def prepare_flowables():
{% endhighlight %}

Let's discuss the content, which are the constituting flowables,
then discuss the layout last.

<h4>
  <a id="contents">Report Contents</a>
</h4>

The cover page -- the first page -- has two
<span class="keyword">Paragraph ( Flowable )</span>
instances. No 
<span class="keyword">PageTemplate</span>
instance was explicitly selected, so the first one is used. Please note the styles used 
in these two
<span class="keyword">Paragraph ( Flowable )</span>
instances.

Next comes report proper pages. The steps are:

{% highlight python %}
flowables.append( NextPageTemplate('dataTemplate') )
{% endhighlight %}

Selecting the
<span class="keyword">PageTempate ( Flowable )</span>
instance, whose Id is 
<span class="keyword">dataTemplate</span>.
Note <span class="keyword">NextPageTemplate( ... )</span>
is also a 
<span class="keyword">Flowable</span>.

{% highlight python %}
flowables.append( PageBreak() )
{% endhighlight %}

Then force a manual page break, as report proper should start on a new page.
Note <span class="keyword">PageBreak()</span>
is also a 
<span class="keyword">Flowable</span>.

{% highlight python %}
data_to_flowables( flowables, cols_width, table_style )
{% endhighlight %}

Finally, wrapping report data in 
<span class="keyword">Table ( Flowable )</span>
instances. This method is discussed in section
<a href="#master-detail-effect">Achieving the Master-Detail Effect</a>.

The last page should now be self-explanatory.

<h4>
  <a id="contents">Report Layout</a>
</h4>

There are 6 ( six ) columns in total. The width of each column is a 
percentage of 
<span class="keyword">effective_page_width</span>.
They are stored in array 
<span class="keyword">cols_width</span>.

The table style is pretty much self-explanatory too. Let's take a look at the first row:

{% highlight python %}
# Master row style.
( 'SPAN', (0,0), (5,0) ),
( 'TOPPADDING', (0,0), (5,0), 10 ),
( 'BOTTOMPADDING', (0,0), (5,0), 10 ),
( 'BACKGROUND', (0,0), (5,0), colors.yellow ),
{% endhighlight %}

There are 6 ( six ) columns in each row. The first row is Department 
info row, which is the master data, displayed in a single line, so 
the columns are merged into a single column. And then this row is made 
taller with top and bottom padding, finally the background is painted 
with yellow colour.

The rest of the styling should be apparent. 
<span style="font-weight:bold;">Chapter 7 Tables and TableStyles</span> in the
<span class="keyword">User Guide</span>
provides sufficient explanation.

<h2 style="color:teal;">
  <a id="concluding-remarks">Concluding Remarks</a>
</h2>

I started off using <span class="keyword">
xhtml2pdf</span> library, it is satisfactory. However, I found that the convenience of 
using <span class="keyword">
HTML</span> comes at a cost: some of the flexibilities are not accessible. 

<span class="keyword">
ReportLab</span> certainly requires more times to learn. But the knowledge will
come useful; and I like the flexibilities and the controls that I have 
via using 
<span class="keyword">
ReportLab</span>. The investment is certain worth the reward.

In this post, I discuss issues and questions that I have during 
investigating <span class="keyword">
ReportLab</span>. I hope you find this post useful and thank you for visiting.