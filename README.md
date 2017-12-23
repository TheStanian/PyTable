# PyTable
A python ascii-art table drawing library with support for multi-line cells (so tables inside of tables work as expected), vertical and horizontal alignment, ...


## Example
An example (code in example.py) of the generated table:

```
+-PyTable----------------+--------------------+----------------------------------------+
| Hello world.           | This is PyTable.   | It is a table printing library.        |
+------------------------+--------------------+----------------------------------------+
| It has support for     |                    |                  and horizontal align. |
| multi-line strings,    | vertical align     |                                        |
+------------------------+--------------------+----------------------------------------+
|                        |                    |                                        |
|        padding         |      is also       |               supported.               |
|                        |                    |                                        |
+------------------------+--------------------+----------------------------------------+
| This means it can      | like so:           | #=Subtable============#==============# |
| do tables in tables,   |                    | # This is a subtable. | Neat, right? # |
|                        |                    | #=====================#==============# |
+------------------------+--------------------+----------------------------------------+
| Because I expand tabs, | have a look:       | def main():                            |
| it also means it can   |                    |     print "Hello world!"               |
| handle code pretty     |                    |                                        |
| nicely..               |                    | if __name__ == "__main__":             |
|                        |                    |     main()                             |
+------------------------+--------------------+----------------------------------------+
| There's still a lot    | but I think it can | So if you need to output data          |
| to be improved         | be useful already  | in a structured fashion, why not       |
|                        |                    | give PyTable a go?                     |
+------------------------+--------------------+----------------------------------------+
```
