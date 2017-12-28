from os import linesep
from PyTable.Table import RowMajorTable, Cell, CellFormatOptions, TableFormatOptions

def main():
    main_table = RowMajorTable(title="Hello world", 
        table_format_options = TableFormatOptions(box_hsep_char = "#", box_isep_char = "#", box_vsep_char = "#",
        vsep = False, hsep = False),
        cell_format_options = CellFormatOptions(halign="center", valign="center"))

    hw_python2 = RowMajorTable(title="Python 2")
    hw_python2.add_row("""
print "Hello world!"
""")
    hw_python3 = RowMajorTable(title="Python 3")
    hw_python3.add_row("""
print("Hello world!")
""")
    hw_cpp = RowMajorTable(title="C++")
    hw_cpp.add_row("""
#include <iostream>
int main() {
    std::cout << "Hello world!" << std::endl;
    return 0;
}""")
    hw_java = RowMajorTable(title="Java")
    hw_java.add_row("""
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello world!");
    }
}""")

    main_table.add_row(hw_python2, hw_python3)
    main_table.add_row(hw_cpp, hw_java)
    
    print main_table


if __name__ == "__main__":
    main()

