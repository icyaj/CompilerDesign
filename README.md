# First Order Compiler Design–Summative 

# Install Packages

Please use python 3.7.4 for best results.

Packages used:

    graphviz
    sys
    datetime

sys and datetime come as standard libraries. To install graphviz:

    - Type into your console. 
    
        pip install graphviz
        
    - Add graphviz to your User Variables PATH.
        
        ;C:\Program Files(x86)\Graphviz2.38\bin

You are now ready to use the main program, hkxx26.py

# How To Use

Open up a terminal in the same directory as hkxx26.py.

Type in the following command into the terminal replacing [filename] with the grammar you wish to parse.
            
    python hkxx26.py [filename]
            
Upon completion there will be 4 files outputed. 

    - [filename]-grammer.txt --> This file contains the output grammar.
    - [filename]-ADT         --> This file contains the raw ADT graph nodes.
    - [filename]-ADT.pdf     --> This file is a pdf of the parsed ADT Graph.
    - log.txt                --> This is the log file. After every output a log will be appended to it.
                                
The log file is formatted as follows:
    
    | Input File: [inputfile] | Time: [time of completion] | Status: [Valid/inValid] | Message: 'Error code if invalid' |
     
TO NOTE:

    - All terminals (i.e. Variables, Constants & Predicates) are converted to lower case per norm.
    - All non-terminals (i.e. everything else) are converted to upper case.
        


# Examples

## Example 1 First Order Logic Input: 

    variables: w x y z
    constants: C D
    predicates: P[2] Q[1]
    equality: =
    connectives: \land \lor \implies \iff \neg
    quantifiers: \exists \forall
    formula: \forall x ( \exists y ( P(x,y) \implies \neg Q(x) )
    \lor \exists z ( ( (C = z) \land Q(z) ) \land P(x,z) ) )
    
The corresponding example grammar for said input:

    S -> F
    F -> (F) | R | QVF | G | FDF | \neg F | \epsilon
    R -> p(v, v) | q(v)
    Q -> \exists | \forall
    D -> \land | \lor | \implies | \iff
    G -> T = T
    T -> C | V
    C -> c | d
    V -> w | x | y | z

    
Please find attached file example1-ADT.pdf to see the parsed tree.

## Example 2 First Order Logic Input: 

    formula: A price E cost1 ( Same(cost1, price) AND ( NOT Non_zero(price) IFF (cost1 == 30) ) )
    equality: ==
    connectives: AND OR IMPLIES IFF NOT
    quantifiers: E A
    variables: price cost1
    constants: 30 Z
    predicates: Same[2] Non_zero[1] notEqual[3]
    
The corresponding example grammar for said input:

    S -> F
    F -> (F) | R | QVF | G | FDF | \epsilon
    R -> same(v, v) | non_zero(v) | notequal(v, v, v)
    Q -> E | A
    D -> AND | OR | IMPLIES | IFF | NOT
    G -> T == T
    T -> C | V
    C -> 30 | z
    V -> price | cost1
    
Please find attached file example2-ADT.pdf to see the parsed tree.


