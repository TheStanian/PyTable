import os, copy
import Utils

# TODO:
#       column major tables
#       support for starting index for row without having to manually pad
#       clean up configuration of tables, rows and cells.
#       Document more
#       Allow title width to be larger than data
#       Make box and seps more configurable (e.g. left and right vs just 1 character)
#       Multi-character sequences for boxes and separation? ;o

class CellFormatOptions:
    def __init__(self, halign="left", valign="top", 
                    htrim=True, vtrim=True, 
                    vtrim_whitespace=True, 
                    pad_char = " ", hpadding=1, 
                    vpadding=0, tab_expansion = 4):
        self.halign = halign
        self.valign = valign
        self.htrim = htrim
        self.vtrim = vtrim
        self.vtrim_whitespace = vtrim_whitespace
        self.pad_char = pad_char
        self.hpadding = hpadding
        self.vpadding = vpadding
        self.tab_expansion = tab_expansion


class TableFormatOptions:
    def __init__(self, title = None, box = True,
                    box_hsep_char = "-", box_vsep_char = "|", box_isep_char = "+", 
                    hsep_char = "-", vsep_char = "|", 
                    isep_char = "+", hsep = True,
                    vsep = True):
        self.title = title
        self.box = box
        self.box_hsep_char = box_hsep_char
        self.box_vsep_char = box_vsep_char
        self.box_isep_char = box_isep_char
        self.hsep_char = hsep_char
        self.vsep_char = vsep_char
        self.isep_char = isep_char
        self.hsep = hsep
        self.vsep = vsep        


class Cell:
    def __init__(self, content, cell_format_options=CellFormatOptions()):
        self.necessary_width = 0
        self.necessary_height = 0
        self.content = ""
        self.cell_format_options = cell_format_options
        if content != None:
            self.necessary_width, self.necessary_height, self.content \
            = Utils.string_dimensions(str(content), self.cell_format_options.htrim,
                                        self.cell_format_options.vtrim, 
                                        self.cell_format_options.vtrim_whitespace,
                                        self.cell_format_options.tab_expansion)
            self.necessary_width += 2*self.cell_format_options.hpadding
            self.necessary_height += 2*self.cell_format_options.vpadding

        self.lines = [] # Will get set when cell gets formatted


class Row:
    def __init__(self, *args, **kwargs):
        self.cell_format_options = kwargs.get("cell_format_options",CellFormatOptions())

        self.cells = []
        for arg in args:
            if isinstance(arg, Row):
                arg.flatten()
                for item in arg: # append row subcells
                    self.cells.append(item)
            elif isinstance(arg, Cell):
                self.cells.append(arg)
            else:
                self.cells.append(self._default_cell(arg))


    def _default_cell(self, content):
        return Cell(content, self.cell_format_options)


    def __len__(self):
        return len(self.cells)


    def insert(self, index, item):
        if not isinstance(item, Row):
            self.cells.insert(index, self._default_cell(item) if not isinstance(item, Cell) else item)
        else: # Allow row in row insertions by splicing the row into the other
            for cell in reversed(item.flatten().cells):
                self.cells.insert(index, cell)
        return self


    def append(self, item):
        if not isinstance(item, Row):
            self.cells.append(self._default_cell(item) if not isinstance(item, Cell) else item)
        else: # Allow appending of rows by adding the appended row to this row.
            for cell in item.flatten().cells:
                self.cells.append(cell)
        return self


    def flatten(self): # recursively flatten rows. cells will retain their parameters. 
        for index, item in enumerate(self.cells):
            if isinstance(item, Row):
                item.flatten()
                del self.cells[index]
                for subitem in reversed(item.cells):
                    self.cells.insert(index, subitem)
                
        return self


class RowMajorTable:
    def __init__(self, table_format_options = TableFormatOptions(), 
                       cell_format_options = CellFormatOptions()):
        self.table_format_options = copy.copy(table_format_options)
        self.cell_format_options = cell_format_options

        self.rows = []


    def add_row(self, *args):
        if len(args) == 0:
            raise ValueError("add_row called without arguments.")
        elif len(args) == 1 and isinstance(args[0], Row):
            self.rows.append(args[0])
        elif len(args) == 1 and isinstance(args[0], list):
            self.add_row(*args[0])
        else:
            self.rows.append(self._default_row(*args))
            

    def _default_row(self, *args):
        return Row(*args, cell_format_options=self.cell_format_options)


    def __str__(self):
        # Calculate number of columns & ensure rows are of that length
        num_cols = 0
        for row in self.rows:
            num_cols = max(num_cols, len(row))

        for row in self.rows:
            while len(row) < num_cols:
                row.append(None)

        column_widths = [0 for i in range(num_cols)]
        row_heights = [0 for i in range(len(self.rows))]

        # Calculate column widths and row heights
        for row_index, row in enumerate(self.rows):
            for cell_index, cell in enumerate(row.cells):
                column_widths[cell_index] = max(column_widths[cell_index], cell.necessary_width)
                row_heights[row_index] = max(row_heights[row_index], cell.necessary_height)

        
        # Shorten grabbing data from the format options
        box = self.table_format_options.box
        title = self.table_format_options.title
        b_hsep_c = self.table_format_options.box_hsep_char
        b_vsep_c = self.table_format_options.box_vsep_char
        b_isep_c = self.table_format_options.box_isep_char
        hsep_c = self.table_format_options.hsep_char
        vsep_c = self.table_format_options.vsep_char
        isep_c = self.table_format_options.isep_char
        hsep = self.table_format_options.hsep
        vsep = self.table_format_options.vsep


        # Init string lines
        lines = []

        # Top box line
        if box:
            top_box_line = b_isep_c + b_hsep_c
            if title:
                top_box_line += title

            # Account for title
            col = 0
            acc_len_col = 1
            while len(top_box_line) > acc_len_col:
                if col >= num_cols:
                    raise ValueError("Title \"{}\" too big for table.".format(title))
                acc_len_col += column_widths[col]
                col += 1
            top_box_line = Utils.halign(top_box_line, acc_len_col + (col-1) * int(vsep), pad_char = b_hsep_c)

            for i in range(col, num_cols):
                if vsep:
                    top_box_line += b_isep_c
                top_box_line += b_hsep_c * column_widths[i]

            top_box_line += b_isep_c
            lines.append(top_box_line)

        
        # Prepare cells for printing 
        # ensure they are all equal height for every row
        # and equal width for every column 
        # pad cells according to their spec
        for row_index, row in enumerate(self.rows):
            for cell_index, cell in enumerate(row.cells):
                s = Utils.halign(Utils.valign(cell.content, row_heights[row_index] - 2 * cell.cell_format_options.vpadding, 
                    align=cell.cell_format_options.valign), column_widths[cell_index] - 2 * cell.cell_format_options.hpadding, 
                    align=cell.cell_format_options.halign, pad_char = cell.cell_format_options.pad_char)

                s = Utils.string_padding(s, hpad=cell.cell_format_options.hpadding, 
                                            vpad=cell.cell_format_options.vpadding,
                                            pad_char=cell.cell_format_options.pad_char)

                cell.lines = s.split(os.linesep) # Cell is prepared and split into lines


        # Calculate row separation lines
        row_sep_line = ""
        if box:
            row_sep_line += b_isep_c

        for col_index, column_width in enumerate(column_widths):
            row_sep_line += hsep_c * column_width
            if vsep and col_index < len(column_widths) - 1:
                row_sep_line += isep_c

        if box:
            row_sep_line += b_isep_c


        # Print rows
        for row_index, row in enumerate(self.rows):
            row_height = row_heights[row_index]
            for row_line_index in range(row_height):
                s = ""
                if box:
                    s += b_vsep_c

                for cell_index, cell in enumerate(row.cells):
                    s += cell.lines[row_line_index]
                    if vsep and cell_index < len(row.cells) - 1:
                        s += vsep_c

                if box:
                    s += b_vsep_c

                lines.append(s)

            if hsep and row_index < len(self.rows) - 1:
                lines.append(row_sep_line)
                
        
        # Calculate bottom box line
        if box:
            s = ""
            s += b_isep_c

            for col_index, column_width in enumerate(column_widths):
                s += b_hsep_c * column_width
                if vsep and col_index < len(column_widths) - 1:
                    s += b_isep_c

            s += b_isep_c

            lines.append(s)


        return os.linesep.join(lines)



