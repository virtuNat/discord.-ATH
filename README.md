# discord.~ATH

A ~ATH interpreter written in python.

________________

Language specification


Old notes on the specification [over here!](https://docs.google.com/document/d/1G6urfNKDhPaQ1iEr9h0o7KPr6gEX80VzdnM1nMBINcY/edit)


________________

# Documentation

## Symbols:


Symbols are the basic units in ~ATH. They represent individual living pointers to a pair of values. The pair of values it refers to follow a simple set of rules: 


By convention the paired values are referred to as the `left` and `right` values of the symbol; the left value may only contain either an `integer`, `float`, `character`, `string`, or `complex` number while the right value may only contain functions.


A single exception is that either of a symbol’s values may instead themselves be other symbols.

## Basic Statements:

**Input Statement** - Syntax: `input NAME< PROMPT>;`


Takes a string input from the input buffer. This will automatically convert numbers in appropriate formats into integers and floats before saving the value to the left of NAME.


PROMPT may either be a string or a symbol with a left value that isn’t empty or a symbol. It will display the value as a string before requesting input from the user. Adding a prompt argument is optional, and if not included will cause it to request input without printing a string.


**Print Statement** - Syntax: `print(STR<, ARG1, ARG2, …>);`


Outputs a string to the console. The first argument is the string to be outputted and must either be a bare string or a symbol containing a string. If the string contains format substrings, it may be supplied an additional number of arguments equal to the number of format substrings.


Format substrings:
`~s` - output value as string
`~d` - output value as integer
`~<x.y>f ` - output value as float with x significant digits and y decimal places. Specifying x and y are optional.


To output tilde ~ symbols directly, escape them with backslash as such: `\~`


~ATH supports the following special characters in print statements:

```
\a Bell Character
\b Backspace Character
\f Line Feed Character
\r Carriage Return Character
\n Newline Character
\t Horizontal Tab Character
\v Vertical Tab Character
```


**Bifurcate Statement** - Syntax: `BIFURCATE PARENT[LEFT, RIGHT];`


Creates two new names LEFT and RIGHT that points to PARENT's values. The names used will be overwritten if they already exist.


If the value assigned is not a symbol, the name declared will reference a symbol with the same value.


If the value assigned is empty, the name declared will reference a copy of NULL.


If either name of LEFT and RIGHT are NULL, the value on that side will not be assigned.


**Aggregate Statement** - Syntax: `AGGREGATE [LEFT, RIGHT]NAME;`


Merges LEFT and RIGHT into a new symbol assigned to NAME. 


Implementation Note:
In order to avoid circular referencing when aggregating a symbol to itself, AGGREGATE will copy the old symbol into wherever its original instance would have been located down the tree and only keep all references on the new instance. This makes the operation O(log(n)) on average if aggregating to a name that is already declared.


**Die Statement** - Syntax: `NAME.DIE();`


Kills the symbol attached to NAME.


Dead symbols serve as falsey values in boolean checks, but the die statement additionally serves as the main form of control. When inside a scope (be it a loop or a function), if the scope's controlling name is killed as a result of the Die Statement, the scope ends immediately.


The current ~ATH script has a reserved name representing its global scope that can be killed by the Die Statement: THIS. If THIS is not killed in the script, the program will repeat itself upon reaching the last statement.


**Tildeath Loop Statement** - Syntax: `~ATH(<!>CONTROL){ /*Additionak graves...*/ } EXECUTE(NAME<, ARG1, ARG2, ...>);`


Loops through all statements inside the body for as long as CONTROL is still alive. If CONTROL is found to be dead at the end of the execution of the loop, the program will proceed to the first statement outside the loop. If CONTROL dies through the Die Statement, the loop will halt and the program will proceed to the first statement outside the loop.


If the loop clause is inverted with the boolean negation symbol `!`, the loop will instead run until the symbol is brought back to life somehow, or the name points to a living symbol. In these inverted loops, the Die Statement will not be able to break execution.


If the execute call attached to the end of the loop is NULL, the loop will behave normally. If the execute call instead calls a function name, the function will be executed concurrently with the contents of the loop. See the Execute statement for further details. (not implemented yet)


**Fabricate Statement** - Syntax: `FABRICATE FUNC(<ARG1, ARG2, ...>){ /*Additional graves*/ }`


Defines a function with the argument parameters in the parentheses and the body to be executed in the braces.


Inside function bodies, all statements can be written, in addition to a special Divulgate Statement.


**Divulgate Statement** - Syntax: `DIVULGATE EXPR;`


Evaluates the expression EXPR and passes the result back to where the function was called.


Note: This statement can only appear inside Fabricate Statement bodies, otherwise an error will occur and the program will fail.


**Execute Statement** - Syntax: `EXECUTE(NAME<, ARG1, ARG2, ...>);`


Calls the right value of NAME as a function with the supplied arguments. The statements inside the function body will be executed in order until the function either ends, the function name is killed within its scope, or a Divulgate Statement is reached.


If NAME's right value is not a function, an error will occur and the program will fail. If NAME is NULL, the function evaluates to NULL.


If the Execute Statement appears at the tail end of a ~ATH loop, it will run concurrently with the loop's contents.

[notes: implement being able to call builtins with execute, and implement the asynchronous bs]


**Import Statement** - Syntax: `import MODULE NAME;`


The first time MODULE is called in an import statement, it runs `<MODULE>.~ATH` until completion, and saves its globals. At any other time, MODULE's globals will be looked up instead.


It will then look for NAME in the globals of MODULE and copy it to the local scope under the same name.


If NAME is not found in the globals of MODULE, an error will occur and the program will fail.


[notes: prevent THIS from dying without the die statement, make import create a symbol MODULE that contains a tree of the globals]
