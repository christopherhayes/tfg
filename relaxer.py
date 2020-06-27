import tfg as tfg

print("Hello, world, testing.")

exampleAfC1x = """\draw (0, 0) -- (8, 8);
\draw (0, 8) -- (8, 0);"""

exampleSG2 = """\draw (0, 0) -- (5, 8.660254037844386);
\draw (5, 8.660254037844386) -- (10, 0);
\draw (10, 0) -- (0, 0)"""

SG0graph = tfg.tikztograph(exampleSG2)

SG2graph = tfg.graphfractalizer(SG0graph, 2)

print("Original graph, " + str(len(SG0graph.vertices)) + " vertices.")
print("Original graph, " + str(len(SG0graph.edges)) + " edges.")

print("Prior to deletion, " + str(len(SG2graph.vertices)) + " vertices.")
print("Prior to deletion, " + str(len(SG2graph.edges)) + " edges.")

for i in SG2graph.vertices:
    print(i.tikzform())

SG2graph.reduce()

print("After deletion, " + str(len(SG2graph.vertices)) + " vertices.")
print("After deletion, " + str(len(SG2graph.edges)) + " edges.")

for i in SG2graph.vertices:
    print(i.tikzform())
for j in SG2graph.edges:
    print(j.tikzform())
