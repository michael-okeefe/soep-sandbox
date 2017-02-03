# Import the JModelica.org Python packages
import pymodelica
from pymodelica.compiler_wrappers import ModelicaCompiler

# Create a compiler and compiler target object
mc = ModelicaCompiler()

# Build trees as if for an FMU or Model Exchange v 1.0
#target = mc.create_target_object("me", "1.0")
source = mc.parse_model("CauerLowPassAnalog.mo")
indent_amount = 2

def dump(src, fid, indent=0):
    ind = " " * (indent_amount * indent)
    try:
        fid.write(ind + src.getNodeName() + "\n")
    except:
        fid.write(ind + "exception: " + str(src) + "\n")
    try:
        for idx in range(src.numChild):
            dump(src.children[idx], fid, indent+1)
    except:
        fid.write(ind + "(exception)\n")

# dump the filter instance
with open('out.txt', 'w') as fid:
    dump(source, fid, 0)
print "DONE!"
