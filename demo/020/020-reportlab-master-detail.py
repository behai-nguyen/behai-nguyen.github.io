"""
    Date Created: 21/05/2022.

	Single-level master-detail report with ReportLab using 
	MySQL Test Data: https://github.com/datacharmer/test_db
	
    Master: Departments.
            Has only a single data row.	
	
	Details: Employees.
             Various number of records, potentially spans over 
             several pages.

    On each new report pages:

        - Master data repeats on the new page.
        - Detail header repeats on the new page, after master data.
		
    Report also has the first cover page with its own page format. 
    The	last conclusion page also with its own format. Both of these
    pages are not counted as total pages for the report, and they 
    don't have report data.	  
"""

import simplejson as json
from operator import itemgetter

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.platypus import Paragraph, PageBreak, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.doctemplate import PageTemplate, NextPageTemplate, BaseDocTemplate
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4
from reportlab.platypus.frames import Frame
from reportlab.lib.units import inch, cm, mm
from reportlab.pdfbase.pdfmetrics import getAscentDescent

"""
    A4 portrait page global geometries. These are applicable to
    all A4 portrait format.

    References:

        https://www.papersizes.org/
        http://www.metricationmatters.com/docs/PageBordersInchesORmillimetres.pdf

    19.55 and 26.44 give margins very close to the ones
    recommended by Microsft.
"""
#
# 210 x 297 mm
#
PAGE_WIDTH  = defaultPageSize[ 0 ]
PAGE_HEIGHT = defaultPageSize[ 1 ]

margin_top = 19.55 * mm
margin_right = 26.44 * mm
margin_bottom = 19.55 * mm
margin_left = 26.44 * mm

effective_page_width = PAGE_WIDTH - margin_right - margin_left
effective_page_height = PAGE_HEIGHT - margin_top - margin_bottom

class NumberedCanvas( canvas.Canvas ):
    """
    Printing pages' header and footer for report pages, excluding
    the first page and the last page.

    The main feature of this implementation is to enable calculating
    total pages as in 'Page 99 of 999_total_pages'.

	Originally from https://code.activestate.com/recipes/576832/.

    Codes have been changed, but the original ideas and implementations
	remain in place.

    Font height calculation is from: https://reportlab-users.reportlab.narkive.com/HQgHhQiA/working-out-height-of-text
    """
    def __init__( self, *args, **kwargs ):
        canvas.Canvas.__init__( self, *args, **kwargs )
        self._saved_page_states = []

        self._header_footer_font_name = 'Helvetica'
        self._header_footer_font_size = 7

        ascent, descent = getAscentDescent( self._header_footer_font_name, self._header_footer_font_size )
        # Note: descent is a negative number.
        self._header_footer_font_height = ascent - descent

        self._left_header = 'Source: MySQL Test Data'
        self._right_header = 'Departments\' Employees Sample Listing'

        self._header_y = PAGE_HEIGHT - ( margin_bottom / 2 )
        self._header_y_line = self._header_y - self._header_footer_font_height

        self._footer_x = PAGE_WIDTH / 2
        self._footer_y = margin_bottom / 2
        self._footer_y_line = self._footer_y + self._header_footer_font_height + ascent

    def showPage( self ):
        self._saved_page_states.append( dict(self.__dict__) )
        self._startPage()

    def save( self ):
        """add page info to each page (page x of y)"""

        num_pages = len( self._saved_page_states )

        for state in self._saved_page_states:
            self.__dict__.update( state )

            """
            Excluding first page and last page.
            """
            if self._pageNumber > 1 and self._pageNumber < num_pages:
                self.draw_page_header_footer( num_pages )

            canvas.Canvas.showPage( self )

        canvas.Canvas.save( self )

    def draw_page_header_footer( self, page_count ):
        self.setFont( self._header_footer_font_name, self._header_footer_font_size )

        self.drawString( margin_left, self._header_y, self._left_header )
        self.drawRightString( PAGE_WIDTH - margin_right, self._header_y, self._right_header )
        self.line( margin_left, self._header_y_line, PAGE_WIDTH - margin_right, self._header_y_line )

        text = 'Page %d of %d' % (self._pageNumber - 1, page_count - 2 )
        self.drawCentredString( self._footer_x, self._footer_y, text )
        self.line( margin_left, self._footer_y_line, PAGE_WIDTH - margin_right, self._footer_y_line )

class LastPage( Flowable ):
    """
    Flowable to generate the content for the last page.	
    """	
    def __init__( self ):
        Flowable.__init__( self )
		
    def __repr__(self):
        return 'Report Last Page'
		
    def draw( self ):
        canvas = self.canv

        text = 'Produced for https://behainguyen.wordpress.com/'

        # Courier-Bold see User Guide, ReportLab Version 3.5.56, 
        # Document generated on 2020/12/02 11:31:59, page 29.
        font_name = 'Courier-Bold'
        font_size = 15

        canvas.setFont( font_name, font_size )

        ascent, descent = getAscentDescent( font_name, font_size )
        # Note: descent is a negative number.		
        font_height = ascent - descent
		
        """
        Please note, the first param value 0 -- it's a lucky magic guess
        for me!! My calculations did not work, out of frustration, I plugged
        0 in, and I have what wanted. I need to do more studies on this.		
        """
        canvas.drawString( 0, ( effective_page_height - (font_height*2) ) * -1, text )

def prepare_data():
    """
	Read "020-depts-emps.json" and transform data into a proper
	master-detail format nearly-ready to feed into ReportLab.

    "020-depts-emps.json" is an export resultset from MySQL Workbench 6.3 CE,
    the source query is in "020-depts-emps.sql". The source database is the
    MySQL test data realsed by Oracle Corporation. Downloadable from:

        https://github.com/datacharmer/test_db

	Returned array has the below format. Where 'dept_no' and 'dept_name'
    is a master record and 'employees' are detail one.

	[
		{
			'dept_no': '...',
			'dept_name': '...',
			'employees': [
			    [ '...', ..., '...' ],
                ...
			    [ '...', ..., '...' ]
			]
		},
		...,
		{
			'dept_no': '...',
			'dept_name': '...',
			'employees': [
			    [ '...', ..., '...' ],
                ...
			    [ '...', ..., '...' ]
			]
		}
	]
    """

    data = []

    f = open( '020-depts-emps.json' )
    raw_data = json.load( f )
    f.close()

    for item in raw_data:
        dept_no, dept_name = itemgetter( 'dept_no', 'dept_name' )( item )

        employee = itemgetter( 'birth_date', 'first_name', 'last_name',
                               'gender', 'from_date', 'to_date' )( item )

        existing_item = next( (itm for itm in data if itm[ 'dept_no' ] == dept_no), None ) \
            if len(data) > 0 else None

        if existing_item == None:
            new_item = {}
            new_item[ 'dept_no' ] = dept_no
            new_item[ 'dept_name' ] = dept_name
            new_item[ 'employees' ] = [ list(employee) ]
            data.append( new_item )
        else:
            existing_item[ 'employees' ].append( list(employee) )

    return data

def prepare_document_instance( output_filename ):
    """
    Creates a BaseDocTemplate instance, complete with Frames and PageTemplates.
    """

    pdf = BaseDocTemplate( output_filename,
                           pagesize=A4,
                           topMargin=margin_top,
                           rightMargin=margin_right,
                           bottomMargin=margin_bottom,
                           leftMargin=margin_left )

    """
    Cover page Frame and Template.
    """
    offset_x = margin_left
    offset_y = margin_bottom
    cover_frame = Frame( margin_left + offset_x,
	                     margin_bottom + ( offset_y * 2 ),
                         effective_page_width - ( offset_x * 2 ),
						 effective_page_height - ( offset_y * 4 ),
						 topPadding=12,
						 showBoundary=1, id='coverFrame' );
    cover_template = PageTemplate( id='coverTemplate',
                                   frames=[ cover_frame ] )

    """
	Report data ( pages ) Frame and PageTemplate.
    """
    report_data_frame = Frame( margin_left, margin_bottom,
                               effective_page_width, effective_page_height,
                               showBoundary=0, id='dataFrame' );
    report_data_template = PageTemplate( id='dataTemplate', frames=[ report_data_frame ] )

    """
	Report data ( pages ) Frame and PageTemplate.
    """
    last_page_frame = Frame( margin_left, margin_bottom,
                             effective_page_width, effective_page_height,
                             showBoundary=1, id='lastPageFrame' );
    last_page_template = PageTemplate( id='lastPageTemplate',
	                                   frames=[ last_page_frame ] )
	                                   # onPage=on_last_page )

    pdf.addPageTemplates( [ cover_template, report_data_template, last_page_template ] )

    return pdf

def data_to_flowables( flowables, cols_width, table_style ):
    """
    Transform the data into ReportLab Flowables to achieve
	master-detail "effect".

    This is only a single-level master-detail.

    The master record is made the first row of the detail data array.

    The detail records header is made the second row of the detail
	data array.

    The ReportTab Table for detail data array repeats the first two
    rows on every new report page.
    """
    data = prepare_data()

    for itm in data:
        master_para = Paragraph( '''Dept. Number <font color=blue>{}</font>,
            Dept. Name <font color=blue>{}</font>'''.format(itm['dept_no'], itm['dept_name']) )

        """
		Detail records array.
        """
        report_data = itm[ 'employees' ]

        """
		The master record is made the first row of the detail data array.
        """
        report_data.insert( 0, [ master_para ] )
        """
        The detail records header is made the second row of the detail
        data array.
        """
        report_data.insert( 1, ['Birth Date', 'First Name', 'Last Name', 'Gender', 'From Date', 'To Date'] )

        """
        The ReportTab Table for detail data array repeats the first two
        rows on every new report page.
        """
        report_table = Table( report_data, colWidths=cols_width, style=table_style, repeatRows=2 )

        flowables.append( report_table )

def prepare_flowables():
    """
    This is the body the report.
    """	
	
    # Birth Date, First Name, Last Name, Gender, From Date, To Date
    cols_width = [ ( 16.66 / 100 ) * effective_page_width,
                   ( 19.33 / 100 ) * effective_page_width,
                   ( 19.33 / 100 ) * effective_page_width,
                   ( 10.00 / 100 ) * effective_page_width,
                   ( 16.66 / 100 ) * effective_page_width,
                   ( 16.66 / 100 ) * effective_page_width ]

    table_style = TableStyle(
        [
            ( 'INNERGRID', (0,0), (-1,-1), 0.25, colors.black ),
            ( 'BOX', (0,0), (-1,-1), 0.25, colors.black ),

		    # Master row style.
		    ( 'SPAN', (0,0), (5,0) ),
		    ( 'TOPPADDING', (0,0), (5,0), 10 ),
		    ( 'BOTTOMPADDING', (0,0), (5,0), 10 ),
		    ( 'BACKGROUND', (0,0), (5,0), colors.yellow ),

		    # Detail header row.
		    ( 'FONTNAME', (0,1), (5,1), 'Helvetica-Bold' ),
		    # Detail header row: Birth Date column.
		    ( 'ALIGN', (0,1), (0,-1), 'CENTRE' ),
		    # Detail header row: Gender column.
		    ( 'ALIGN', (3,1), (3,-1), 'CENTRE' ),
		    # Detail header row: From Date column.
		    ( 'ALIGN', (4,1), (4,-1), 'CENTRE' ),
		    # Detail header row: To Date column.
		    ( 'ALIGN', (5,1), (5,-1), 'CENTRE' ),
        ]
    )

    flowables = []

    """
    First page: no report data.

    Using the cover page template: no need to select it,
    as it is the first page template in the document.
    """
    style = ParagraphStyle(
        name = 'Large',
        fontSize = 20,
        leading = 25,
        alignment = TA_CENTER
    )
    flowables.append( Paragraph('''Source: MySQL Test Data
	    Departments\' Employees Sample Listing
	    ''', style=style) )

    style = ParagraphStyle(
        name = 'Normal',
        fontSize = 10,
        leading = 12,
        alignment = TA_CENTER,
    )
    flowables.append( Paragraph('Author: Van Be Hai Nguyen', style=style) )

    """
    Proper report pages: report data pages.

    Start proper report pages.
    """
    # Select appropriate page template.
    flowables.append( NextPageTemplate('dataTemplate') )
    # Start first report content page on a new page.
    flowables.append( PageBreak() )
    # Getting data a flowables.
    data_to_flowables( flowables, cols_width, table_style )

    """
    Last page: no report data.
    """
    flowables.append( NextPageTemplate('lastPageTemplate') )
    flowables.append( PageBreak() )
    flowables.append( LastPage() )

    return flowables;

if __name__ == '__main__':

    pdf = prepare_document_instance( '020-reportlab-master-detail.pdf' )

    flowables = prepare_flowables()

    pdf.build( flowables, canvasmaker=NumberedCanvas )