# tfg
Generates tikz code for the result of iterated function systems applied to points in tikz code. 

tfg stands for "tikz fractal generator". Currently the script is a mess not fit for public use, but I figured I would put it out there anyway. To use:

1.) Write up or select an example tikz block to apply an IFS to.
2.) Write up or select a complex-valued set of maps under the "similitudes" function with a key label.
3.) In the main() function, replace the second argument of fractalizer2 or newfractalizer2 with your example tikz block.
4.) In the similitudes function, replace the default value of key (third argument) with your key label.
5.) Run the script as in the following Linux CLI way: python3 tfg.py (filename) (level)

The output will be filename.tex in the same directory. 

Currently it is set for the heptagasket complete graphs. I would run:

python3 tfg.py hept0 0 
python3 tfg.py hept1 1
python3 tfg.py hept2 2

which would generate levels 0, 1, and 2 of the complete-graph heptagasket approximations V_0, V_1, and V_2, following standard analysis on fractals notation. 
