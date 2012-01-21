
from copy import copy

from lxml import etree, objectify

from pyte.unit import inch, pt
from pyte.font import Font, TypeFace, TypeFamily
from pyte.font.style import REGULAR, BOLD, ITALIC
from pyte.paper import Paper, Letter
from pyte.document import Document, Page, Orientation
from pyte.layout import Container, Chain
from pyte.paragraph import ParagraphStyle, Paragraph, Justify
from pyte.number import CHARACTER_UC, ROMAN_UC
from pyte.text import StyledText
from pyte.text import Bold, Emphasized, SmallCaps
from pyte.text import boldItalicStyle
from pyte.math import MathFonts, MathStyle, Equation, EquationStyle
from pyte.math import Math as PyteMath
from pyte.structure import Heading, List, Reference, REFERENCE
from pyte.structure import HeadingStyle, ListStyle
from pyte.structure import Header, Footer, HeaderStyle, FooterStyle
from pyte.bibliography import Bibliography, BibliographyFormatter
from pyte.flowable import Flowable, FlowableStyle
from pyte.float import Figure as PyteFigure, CaptionStyle
from pyte.table import Tabular as PyteTabular, MIDDLE
from pyte.table import HTMLTabularData, CSVTabularData, TabularStyle, CellStyle
from pyte.draw import LineStyle, RED



# use Gyre Termes instead of (PDF Core) Times
use_gyre = False

# fonts
# ----------------------------------------------------------------------------
if use_gyre:
    from pyte.font.style import REGULAR, MEDIUM, BOLD, ITALIC

    termes_roman = Font("fonts/qtmr", weight=REGULAR)
    termes_italic = Font("fonts/qtmri", weight=REGULAR, slant=ITALIC)
    termes_bold = Font("fonts/qtmb", weight=BOLD)
    termes_bold_italic = Font("fonts/qtmbi", weight=BOLD, slant=ITALIC)

    termes = TypeFace("TeXGyreTermes", termes_roman, termes_bold,
                      termes_italic, termes_bold_italic)

    ieeeFamily = TypeFamily(serif=termes)

    schola_roman = Font("fonts/qcsr", weight=REGULAR)
    schola_italic = Font("fonts/qcsri", weight=REGULAR, slant=ITALIC)
    schola_bold = Font("fonts/qcsb", weight=BOLD)
    heros_roman = Font("fonts/qhvr", weight=REGULAR)
    cursor_regular = Font("fonts/qcrr", weight=REGULAR)
    chorus = Font("fonts/qzcmi", weight=MEDIUM)
    standard_symbols = Font("fonts/usyr", weight=REGULAR)
    cmex9 = Font("fonts/cmex9", weight=REGULAR)

    mathfonts = MathFonts(schola_roman, schola_italic, schola_bold,
                          heros_roman, cursor_regular, chorus, standard_symbols,
                          cmex9)
else:
    from pyte.fonts.adobe14 import pdf_family as ieeeFamily
    #from pyte.fonts.adobe35 import avantgarde, palatino, zapfchancery
    #from pyte.fonts.adobe35 import newcenturyschlbk, bookman
    #ieeeFamily = TypeFamily(serif=palatino)
    from pyte.fonts.adobe35 import postscript_mathfonts as mathfonts


# paragraph styles
# ----------------------------------------------------------------------------
bodyStyle = ParagraphStyle('body',
                           typeface=ieeeFamily.serif,
                           fontWeight=REGULAR,
                           fontSize=10*pt,
                           lineSpacing=12*pt,
                           indentFirst=0.125*inch,
                           spaceAbove=0*pt,
                           spaceBelow=0*pt,
                           justify=Justify.Both)

ParagraphStyle.attributes['typeface'] = bodyStyle.typeface
ParagraphStyle.attributes['hyphenLang'] = 'en_US'
ParagraphStyle.attributes['hyphenChars'] = 4

mathstyle = MathStyle('math', fonts=mathfonts)

equationstyle = EquationStyle('equation', base=bodyStyle,
                              math_style=mathstyle,
                              indentFirst=0*pt,
                              spaceAbove=6*pt,
                              spaceBelow=6*pt,
                              justify=Justify.Center)

bibliographyStyle = ParagraphStyle('bibliography', base=bodyStyle,
                                   fontSize=9*pt)

titleStyle = ParagraphStyle("title",
                            typeface=ieeeFamily.serif,
                            fontWeight=REGULAR,
                            fontSize=18*pt,
                            lineSpacing=1.2*18*pt,
                            spaceAbove=6*pt,
                            spaceBelow=6*pt,
                            justify=Justify.Center)

authorStyle = ParagraphStyle("author",
                             base=titleStyle,
                             fontSize=12*pt,
                             lineSpacing=1.2*12*pt)

affiliationStyle = ParagraphStyle("affiliation",
                                  base=authorStyle,
                                  spaceBelow=6*pt + 12*pt)

abstractStyle = ParagraphStyle("abstract",
                               typeface=ieeeFamily.serif,
                               fontWeight=BOLD,
                               fontSize=9*pt,
                               lineSpacing=10*pt,
                               indentFirst=0.125*inch,
                               spaceAbove=0*pt,
                               spaceBelow=0*pt,
                               justify=Justify.Both)

listStyle = ListStyle("list", base=bodyStyle,
                      spaceAbove=5*pt,
                      spaceBelow=5*pt,
                      indentLeft=0*inch,
                      indentFirst=0*inch,
                      ordered=True,
                      itemSpacing=bodyStyle.lineSpacing,
                      numberingStyle=ROMAN_UC, # not yet implemented
                      numberingSeparator=')')

hd1Style = HeadingStyle("heading",
                        typeface=ieeeFamily.serif,
                        fontWeight=REGULAR,
                        fontSize=10*pt,
                        smallCaps=True,
                        justify=Justify.Center,
                        lineSpacing=12*pt,
                        spaceAbove=18*pt,
                        spaceBelow=6*pt,
                        numberingStyle=ROMAN_UC)

acknowledgement_heading_style = HeadingStyle("acknowledgement", base=hd1Style,
                                             numberingStyle=None)

hd2Style = HeadingStyle("subheading", base=hd1Style,
                        fontSlant=ITALIC,
                        fontSize=10*pt,
                        smallCaps=False,
                        justify=Justify.Left,
                        lineSpacing=12*pt,
                        spaceAbove=6*pt,
                        spaceBelow=6*pt,
                        numberingStyle=CHARACTER_UC)
#TODO: should only specify style once for each level!

heading_styles = [hd1Style, hd2Style]

header_style = HeaderStyle('header', base=bodyStyle,
                           fontSize=9 * pt)

footer_style = FooterStyle('footer', base=header_style,
                           justify=Justify.Center)

figure_style = FlowableStyle('figure',
                             spaceAbove=10 * pt,
                             spaceBelow=12 * pt)

fig_caption_style = CaptionStyle('figure caption',
                                 typeface=ieeeFamily.serif,
                                 fontWeight=REGULAR,
                                 fontSize=9*pt,
                                 lineSpacing=10*pt,
                                 indentFirst=0*pt,
                                 spaceAbove=20*pt,
                                 spaceBelow=0*pt,
                                 justify=Justify.Both)

red_line_style = LineStyle('tabular line', width=0.2*pt, color=RED)
thick_line_style = LineStyle('tabular line')
tabular_style = TabularStyle('tabular',
                             typeface=ieeeFamily.serif,
                             fontWeight=REGULAR,
                             fontSize=10*pt,
                             lineSpacing=12*pt,
                             indentFirst=0*pt,
                             spaceAbove=0*pt,
                             spaceBelow=0*pt,
                             justify=Justify.Center,
                             vertical_align=MIDDLE,
                             left_border=red_line_style,
                             right_border=red_line_style,
                             bottom_border=red_line_style,
                             top_border=red_line_style,
                             )
first_row_style = CellStyle('first row', fontWeight=BOLD,
                            bottom_border=thick_line_style)
first_column_style = CellStyle('first column', fontSlant=ITALIC,
                               right_border=thick_line_style)
numbers_style = CellStyle('numbers', typeface=ieeeFamily.mono)
tabular_style.set_cell_style(first_row_style, rows=0)
tabular_style.set_cell_style(first_column_style, cols=0)
tabular_style.set_cell_style(numbers_style, rows=slice(1,None),
                             cols=slice(1,None))

# custom paragraphs
# ----------------------------------------------------------------------------

class Abstract(Paragraph):
    def __init__(self, text):
        label = StyledText("Abstract &mdash; ", boldItalicStyle)
        return super().__init__([label, text], abstractStyle)


class IndexTerms(Paragraph):
    def __init__(self, terms):
        label = StyledText("Index Terms &mdash; ", boldItalicStyle)
        text = ", ".join(sorted(terms)) + "."
        text = text.capitalize()
        return super().__init__([label, text], abstractStyle)


# render methods
# ----------------------------------------------------------------------------

# ElementBase restrictions!!
# http://codespeak.net/lxml/element_classes.html

# is it a good idea to inherit from ObjectifiedElement (not documented)?
class CustomElement(objectify.ObjectifiedElement):
#class CustomElement(etree.ElementBase):
    def parse(self, document):
        raise NotImplementedError('tag: %s' % self.tag)


class Section(CustomElement):
    def parse(self, document, level=1):
        #print('Section.render() %s' % self.attrib['title'])
        for element in self.getchildren():
            if isinstance(element, Title):
                elem = element.parse(document, level=level, id=self.get('id', None))
            elif type(element) == Section:
                elem = element.parse(document, level=level + 1)
            else:
                elem = element.parse(document)
            if isinstance(elem, Flowable):
                yield elem
            else:
                for flw in elem:
                    yield flw


class Title(CustomElement):
    def parse(self, document, level=1, id=None):
        #print('Title.render()')
        return Heading(document, self.text, style=heading_styles[level - 1],
                          level=level, id=id)


class P(CustomElement):
    def parse(self, document):
        #print('P.render()')
        if self.text is not None:
            content = self.text
        else:
            content = ''
        for child in self.getchildren():
            content += child.parse(document)
            if child.tail is not None:
                content += child.tail
        return Paragraph(content, style=bodyStyle)


class B(CustomElement):
    def parse(self, document):
        #print('B.render()')
        return Bold(self.text)


class Em(CustomElement):
    def parse(self, document):
        #print('Em.render()')
        return Emphasized(self.text)


class SC(CustomElement):
    def parse(self, document):
        #print('SC.render()')
        return SmallCaps(self.text)


class OL(CustomElement):
    def parse(self, document):
        #print('OL.render()')
        items = []
        for item in self.getchildren():
            items.append(item.parse(document))
        return List(items, style=listStyle)


class LI(CustomElement):
    def parse(self, document):
        #print('LI.render()')
        content = self.text
        for child in self.getchildren():
            content += child.parse(document)
            if child.tail is not None:
                content += child.tail
        return content


class Math(CustomElement):
    def parse(self, document):
        math = PyteMath(self.text, style=mathstyle)
        math.document = document
        return math


class Eq(CustomElement):
    def parse(self, document, id=None):
        equation = Equation(self.text, style=equationstyle)
        equation.document = document # TODO: do this properly
        for item in equation:
            item.document = document
        id = self.get('id', None)
        if id:
            document.elements[id] = equation
        return equation


class Cite(CustomElement):
    def parse(self, document):
        #print('Cite.render()')
        # TODO: general document getter in Textdocument/Chain/Container
        return document.bibliography.cite(self.get('id'))


class Ref(CustomElement):
    def parse(self, document):
        #print('Ref.render()')
        return Reference(document, self.get('id'), self.get('type', REFERENCE))


class Acknowledgement(CustomElement):
    def parse(self, document):
        #print('Acknowledgement.render()')
        yield Heading(document, 'Acknowledgement',
                      style=acknowledgement_heading_style, level=1)
        for element in self.getchildren():
            yield element.parse(document)


class Figure(CustomElement):
    def parse(self, document):
        #print('Figure.render()')
        caption_text = self.getchildren()[0].text
        scale = float(self.get('scale'))
        return PyteFigure(self.get('path'), caption_text, scale=scale,
                         style=figure_style, caption_style=fig_caption_style)


class Tabular(CustomElement):
    def parse(self, document):
        #print('Tabular.render()')
        data = HTMLTabularData(self)
        return PyteTabular(data, style=tabular_style)


class CSVTabular(CustomElement):
    def parse(self, document):
        #print('Tabular.render()')
        data = CSVTabularData(self.get('path'))
        return PyteTabular(data, style=tabular_style)


# bibliography style
# ----------------------------------------------------------------------------

class IEEEBibliographyFormatter(BibliographyFormatter):
    def format_citation(self, reference):
        try:
            index = self.bibliography.index(reference)
            return StyledText('[{}]'.format(index + 1))
        except:
            return StyledText('[ERROR]')

    def format_bibliography(self, target):
        if len(self.bibliography) == 0:
            return
        items = []
        heading = Heading(target.document, 'References',
                          style=acknowledgement_heading_style)
        target.add_flowable(heading)
        for i, ref in enumerate(self.bibliography):
            authors = ['{} {}'.format(name.given_initials(), name.family)
                       for name in ref.author]
            authors = ', '.join(authors)
            item = '[{}]&nbsp;{}, "{}", '.format(i + 1, authors, ref.title)
            item += Emphasized(ref['container_title'])
            item += ', {}'.format(ref.issued.year)
            items.append(item)
            paragraph = Paragraph(item, style=bibliographyStyle)
            target.add_flowable(paragraph)


# pages and their layout
# ----------------------------------------------------------------------------

class RFICPage(Page):
    topmargin = bottommargin = 1.125 * inch
    leftmargin = rightmargin = 0.85 * inch
    column_spacing = 0.25 * inch

    def __init__(self, document, first=False):
        super().__init__(document, Letter, Orientation.Portrait)

        body_width = self.width() - (self.leftmargin + self.rightmargin)
        body_height = self.height() - (self.topmargin + self.bottommargin)
        body = Container(self, self.leftmargin, self.topmargin,
                         body_width, body_height)

        column_height = body.height()
        column_width = (body.width() - self.column_spacing) / 2.0
        column_top = 0*pt

        if first:
            self.title_box = Container(body, 0*pt, 0*pt)
            column_height -= self.title_box.height()
            column_top = self.title_box.bottom()

        self.content = document.content

        self.column1 = Container(body, 0*pt, column_top,
                                 width=column_width, height=column_height,
                                 chain=document.content)
        self.column2 = Container(body, column_width + self.column_spacing, column_top,
                                 width=column_width, height=column_height,
                                 chain=document.content)

        self.header = Container(self, self.leftmargin, self.topmargin / 2,
                                body_width, 12*pt)
        footer_vert_pos = self.topmargin + body_height + self.bottommargin /2
        self.footer = Container(self, self.leftmargin, footer_vert_pos,
                                body_width, 12*pt)
        header_text = Header(self, header_style)
        self.header.add_flowable(header_text)
        footer_text = Footer(self, footer_style)
        self.footer.add_flowable(footer_text)


# main document
# ----------------------------------------------------------------------------
class RFIC2009Paper(Document):
    rngschema = 'rfic.rng'

    def __init__(self, filename, bibliography_source):
        lookup = etree.ElementNamespaceClassLookup()
        namespace = lookup.get_namespace('http://www.mos6581.org/ns/rficpaper')
        namespace[None] = CustomElement
        namespace.update(dict([(cls.__name__.lower(), cls)
                               for cls in CustomElement.__subclasses__()]))

        Document.__init__(self, filename, self.rngschema, lookup)

        self.bibliography = Bibliography(bibliography_source,
                                         IEEEBibliographyFormatter())

        authors = [author.text for author in self.root.head.authors.author]
        if len(authors) > 1:
            self.author = ', '.join(authors[:-1]) + ', and ' + authors[-1]
        else:
            self.author = authors[0]
        self.title = self.root.head.title.text
        self.keywords = [term.text for term in self.root.head.indexterms.term]

        self.parse_input()

    def parse_input(self):
        self.content_flowables = []
        for section in self.root.body.section:
            for flowable in section.parse(self):
                self.content_flowables.append(flowable)
        try:
            for flowable in self.root.body.acknowledgement.parse(self):
                self.content_flowables.append(flowable)
        except AttributeError:
            pass

    def setup(self):
        self.page_count = 1
        self.content = Chain(self)
        page = RFICPage(self, first=True)
        self.add_page(page, self.page_count)

        title = Paragraph(self.title, titleStyle)
        author = Paragraph(self.author, authorStyle)
        affiliation = Paragraph(self.root.head.affiliation.text,
                                affiliationStyle)
        abstract = Abstract(self.root.head.abstract.text)
        index_terms = IndexTerms(self.keywords)

        page.title_box.add_flowable(title)
        page.title_box.add_flowable(author)
        page.title_box.add_flowable(affiliation)

        page.content.add_flowable(abstract)
        page.content.add_flowable(index_terms)

        for flowable in self.content_flowables:
            self.content.add_flowable(flowable)

        #self.bibliography.bibliography(self.content)

    def add_to_chain(self, chain):
        page = RFICPage(self)
        self.page_count += 1
        self.add_page(page, self.page_count)
        return page.column1
