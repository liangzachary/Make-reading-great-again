
input_text = 'Is it not crystal clear, then, comrades, that all the evils of this life of ours spring from the tyranny of human beings? Only get rid of Man, and the produce of our labour would be our own. Almost overnight we could become rich and free. What then must we do? Why, work night and day, body and soul, for the overthrow of the human race! That is my message to you, comrades: Rebellion! I do not know when that Rebellion will come, it might be in a week or in a hundred years, but I know, as surely as I see this straw beneath my feet, that sooner or later justice will be done. Fix your eyes on that, comrades, throughout the short remainder of your lives! And above all, pass on this message of mine to those who come after you, so that future generations shall carry the struggle until it is victorious.'

page = '<html> <head> <title>repl.it</title>   </head> <body>'

entity_map = {}

for entity in entity_map:
  input_text = input_text.replace(entity, '<a href="' + entity_map[entity] + '">' + entity + '</a>')


