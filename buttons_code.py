## Detect AOVs
import nuke, fnmatch, math

aovNodeName = nuke.thisNode().name()
aovNode = nuke.toNode(aovNodeName)

aovs = []
aovsSorted = []
count = 0

try:
    node = aovNode.input(0)
    channels = list(set([x.split('.')[0] for x in node.channels()]))
    width = node.width()
    height = node.height()

    for c,l in enumerate(sorted(channels)):
        aovs.append(l)
        count = count+1

    rows = math.ceil(math.sqrt(count))
    columns = math.ceil(count/rows)

    aovNode.knob('rows').setValue(int(rows))
    aovNode.knob('columns').setValue(int(columns))

    aovNode.knob('width').setValue(width)
    aovNode.knob('height').setValue(height)
    
    kbs = []
    for n in range(aovNode.getNumKnobs()):
        kbs.append(aovNode.knob(n).name())

    for k in kbs:
        if fnmatch.fnmatch(k, 'kb_*'):
            aovNode.removeKnob(aovNode.knob(k))

    with aovNode:
        posx = nuke.toNode('AOV_Input').xpos()
        posy = nuke.toNode('AOV_Input').ypos()+40

    for c,a in enumerate(sorted(aovs)):
        if a == 'rgba':
            rgbaIdx = c
            break

    aovsSorted.append(aovs[rgbaIdx])

    for c,a in enumerate(sorted(aovs)):
        if a != 'rgba':
            aovsSorted.append(aovs[c])

    aovs = aovsSorted

    for c,a in enumerate(aovs):
        aovCb = nuke.Boolean_Knob( ('kb_'+ a), a )
        aovCb.setValue(1)
        aovCb.setFlag(nuke.STARTLINE)
        aovNode.addKnob(aovCb)

    with aovNode:
        nodes = ['Read', 'Text2', 'ContactSheet', 'ShuffleCopy', 'Transform', 'Shuffle', 'Merge', 'Reformat']
        for node in nodes:
            for n in nuke.allNodes(node):
                nuke.delete(n)

    layers = []
    offset = -100 
    with aovNode:
        inputdot = nuke.toNode('AOV_Input')
        for c in range(count):
            offset = offset+100

            shuffle = nuke.nodes.Shuffle(label=aovs[c], inputs=[inputdot], xpos=posx+offset, ypos=posy)
            shuffle['in'].setValue(aovs[c])

            reformat = nuke.nodes.Reformat(xpos=shuffle.xpos(), ypos=shuffle.ypos()+40)
            reformat['resize'].setValue('fit')
            reformat.setInput(0, shuffle)

            merge = nuke.nodes.Merge(xpos=shuffle.xpos(), ypos=shuffle.ypos()+80)
            layers.append(merge)
            merge.setInput(0, reformat)

            text = nuke.nodes.Text2(inputs=[], message=aovs[c], xpos=shuffle.xpos(), ypos=shuffle.ypos()+120)
            text['box'].setValue(0, 0, width, height)
            text['center'].setValue(0,1)
            text['center'].setValue(0,0)
            text['yjustify'].setValue('bottom')
            text['font'].setValue('Verdana', 'Regular')
            text['global_font_scale'].setExpression(aovNodeName+'.txt_scale')
            text['enable_background'].setExpression(aovNodeName+'.enable_bg')
            text['background_opacity'].setExpression(aovNodeName+'.bgop')
            text['background_color'].setExpression(aovNodeName+'.bgcolor')

            merge.setInput(1, text)

        output = nuke.toNode('Output1')
        contactSheet = nuke.nodes.ContactSheet(inputs=layers, rows=rows, columns=columns, xpos=posx, ypos=posy + 160)
        contactSheet['width'].setExpression(aovNodeName+'.knob.width')
        contactSheet['height'].setExpression(aovNodeName+'.knob.height')
        contactSheet['rows'].setExpression(aovNodeName+'.rows')
        contactSheet['columns'].setExpression(aovNodeName+'.columns')
        contactSheet['center'].setExpression(aovNodeName+'.center')
        contactSheet['xpos'].setValue(posx)
        contactSheet['roworder'].setValue('TopBottom')
        output.setInput(0, contactSheet)

except:
    nuke.message("Connect an input which contains AOVs.")
    

## Clean AOVs
import nuke, fnmatch

aovNodeName = nuke.thisNode().name()
aovNode = nuke.toNode(aovNodeName)

try:
	kbs = []
	for n in range(aovNode.getNumKnobs()):
		kbs.append(aovNode.knob(n).name())
		
	if kbs != []:
		for k in kbs:
			if fnmatch.fnmatch(k, 'kb_*'):
				aovNode.removeKnob(aovNode.knob(k))

    with aovNode:
        nodes = ['Read', 'Text2', 'ContactSheet', 'ShuffleCopy', 'Transform', 'Shuffle', 'Merge', 'Reformat']
        for node in nodes:
            for n in nuke.allNodes(node):
                nuke.delete(n)
except:
	nuke.message("Connect an input which contains AOVs.")
  
  
## Update
import nuke, fnmatch, math

aovNodeName = nuke.thisNode().name()
aovNode = nuke.toNode(aovNodeName)

aovsSorted = []
count = 0

try:
    node = aovNode.input(0)
    
    aovs = []
    for n in range(aovNode.getNumKnobs()):
        if 'kb_' in aovNode.knob(n).name() and aovNode.knob(n).getValue() == 1:
            kbname = aovNode.knob(n).name()
            aovs.append(kbname.replace("kb_", ""))
            count = count + 1
    
    width = node.width()
    height = node.height()

    rows = math.ceil(math.sqrt(count))
    columns = math.ceil(count/rows)

    aovNode.knob('rows').setValue(int(rows))
    aovNode.knob('columns').setValue(int(columns))

    aovNode.knob('width').setValue(width)
    aovNode.knob('height').setValue(height)

    with aovNode:
        posx = nuke.toNode('AOV_Input').xpos()
        posy = nuke.toNode('AOV_Input').ypos()+40

    for c,a in enumerate(sorted(aovs)):
        if a == 'rgba':
            rgbaIdx = c
            break

    aovsSorted.append(aovs[rgbaIdx])

    for c,a in enumerate(sorted(aovs)):
        if a != 'rgba':
            aovsSorted.append(aovs[c])

    aovs = aovsSorted

    with aovNode:
        nodes = ['Read', 'Text2', 'ContactSheet', 'ShuffleCopy', 'Transform', 'Shuffle', 'Merge', 'Reformat']
        for node in nodes:
            for n in nuke.allNodes(node):
                nuke.delete(n)

    layers = []
    offset = -100 
    with aovNode:
        inputdot = nuke.toNode('AOV_Input')
        for c in range(count):
            offset = offset+100

            shuffle = nuke.nodes.Shuffle(label=aovs[c], inputs=[inputdot], xpos=posx+offset, ypos=posy)
            shuffle['in'].setValue(aovs[c])

            reformat = nuke.nodes.Reformat(xpos=shuffle.xpos(), ypos=shuffle.ypos()+40)
            reformat['resize'].setValue('fit')
            reformat.setInput(0, shuffle)

            merge = nuke.nodes.Merge(xpos=shuffle.xpos(), ypos=shuffle.ypos()+80)
            layers.append(merge)
            merge.setInput(0, reformat)

            text = nuke.nodes.Text2(inputs=[], message=aovs[c], xpos=shuffle.xpos(), ypos=shuffle.ypos()+120)
            text['box'].setValue(0, 0, width, height)
            text['center'].setValue(0,1)
            text['center'].setValue(0,0)
            text['yjustify'].setValue('bottom')
            text['font'].setValue('Verdana', 'Regular')
            text['global_font_scale'].setExpression(aovNodeName+'.txt_scale')
            text['enable_background'].setExpression(aovNodeName+'.enable_bg')
            text['background_opacity'].setExpression(aovNodeName+'.bgop')
            text['background_color'].setExpression(aovNodeName+'.bgcolor')

            merge.setInput(1, text)

        output = nuke.toNode('Output1')
        contactSheet = nuke.nodes.ContactSheet(inputs=layers, rows=rows, columns=columns, xpos=posx, ypos=posy + 160)
        contactSheet['width'].setExpression(aovNodeName+'.knob.width')
        contactSheet['height'].setExpression(aovNodeName+'.knob.height')
        contactSheet['rows'].setExpression(aovNodeName+'.rows')
        contactSheet['columns'].setExpression(aovNodeName+'.columns')
        contactSheet['center'].setExpression(aovNodeName+'.center')
        contactSheet['xpos'].setValue(posx)
        contactSheet['roworder'].setValue('TopBottom')
        output.setInput(0, contactSheet)

except:
    nuke.message("Connect an input which contains AOVs.")
    
