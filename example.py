from os import linesep
from PyTable.Table import RowMajorTable, Cell, CellFormatOptions

if __name__ == "__main__":
    table = RowMajorTable()
    table.table_format_options.title = "PyTable"
    table.add_row("Hello world.", "This is PyTable.", "It is a table printing library.")
    table.add_row("It has support for" + linesep + "multi-line strings,", 
                    Cell("vertical align", cell_format_options=CellFormatOptions(valign="bottom")),
                    Cell("and horizontal align.", cell_format_options=CellFormatOptions(halign="right")))
    center_padded = CellFormatOptions(hpadding=2, vpadding=1, valign="center", halign="center")
    table.add_row(Cell("padding", cell_format_options=center_padded),
                    Cell("is also", cell_format_options=center_padded),
                    Cell("supported.", cell_format_options=center_padded))
    
    subtable = RowMajorTable()
    subtable.table_format_options.title = "Subtable"
    subtable.table_format_options.box_hsep_char = "="
    subtable.table_format_options.box_vsep_char = "#"
    subtable.table_format_options.box_isep_char = "#"
    subtable.add_row("This is a subtable.", "Neat, right?")
    
    table.add_row("This means it can" + linesep + "do tables in tables,", "like so:", subtable)
    table.add_row("Because I expand tabs," + linesep + "it also means it can" + linesep + "handle code pretty" + linesep + "nicely..", "have a look:",
"""
def main():
    print "Hello world!"

if __name__ == "__main__":
    main()
"""    
    )
    table.add_row("There's still a lot" + linesep + "to be improved", 
                    "but I think it can" + linesep + "be useful already", 
                    "So if you need to output data" + linesep +
                    "in a structured fashion, why not" + linesep +
                    "give PyTable a go?")


    print table