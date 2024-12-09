from graphviz import Digraph

# Initialize a new directed graph
dot = Digraph(comment='AWS AI Chip Timeline', format='png')

# Define the root node
dot.node('AWS_AI_Chips', 'AWS AI Chips', shape='ellipse', style='filled', color='lightblue')

# Define the years as child nodes of the root
years = {
    '2018': ['Inferentia', 'Graviton'],
    '2020': ['Trainium', 'Graviton2'],
    '2022': ['Inferentia2', 'Graviton3'],
    '2023': ['Trainium2'],
    '2024': ['Inferentia3', 'Trainium3', 'Graviton4']
}

# Iterate over each year and its corresponding chips
for year, chips in years.items():
    # Add the year node
    dot.node(year, year, shape='rectangle', style='filled', color='lightgrey')
    
    # Connect the year node to the root
    dot.edge('AWS_AI_Chips', year)
    
    # Add chip nodes and connect them to the year node
    for chip in chips:
        dot.node(chip, chip, shape='box', style='filled', color='white')
        dot.edge(year, chip)

# Render the graph to a file
# This will create a file named 'aws_ai_chip_timeline.png' in the current directory
dot.render('aws_ai_chip_timeline', view=True)

# If you want to see the source code of the graph, uncomment the following line:
print(dot.source)
