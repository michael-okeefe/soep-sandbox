# This example is from the JModelica User's Guide 1.17.0 Chapter 9
# It includes a few fixes to enable it to run (example itself doesn't run as
# written).
# See http://www.jmodelica.org/api-docs/usersguide/1.17.0/ch09.html
# To run from JModelica on Windows:
# 1. Launch the JModelica IPython window
# 2. from within IPython:
#    - %cd <path to folder of this file>
#    - %run ast_example.py
# Note: I have not had success in rerunning this file from the same IPython
# instance...

# Import library for path manipulations
import os.path

# Import the JModelica.org Python packages
import pymodelica
from pymodelica.compiler_wrappers import ModelicaCompiler

# Import numerical libraries
import numpy as N
import ctypes as ct
import matplotlib.pyplot as plt

# Import JPype
import jpype

# Create a reference to the java package 'org'
org = jpype.JPackage('org')

# Create a compiler and compiler target object
mc = ModelicaCompiler()

# Build trees as if for an FMU or Model Exchange v 1.0
target = mc.create_target_object("me", "1.0")

# Don't parse the file if it has already been parsed
try:
    source_root.getProgramRoot()
except:
    # Parse the file CauerLowPassAnalog.mo and get the root node
    # of the AST
    model = mc.get_modelicapath() + "\\Modelica"
    source_root = mc.parse_model(model)

# Don't load the standard library if it is already loaded
try:
    modelica.getName().getID()
except NameError, e:
    # Load the Modelica standard library and get the class
    # declaration AST node corresponding to the Modelica
    # package.
    modelica = source_root.getProgram().getLibNode(0). \
            getStoredDefinition().getElement(0)

def count_classes(class_decl, depth):
    """
    Count the number of classes hierarchically contained
    in a class declaration.
    """
    # get an iterator over all local classes using the method
    # ClassDecl.classes() which returns a Java Iterable object
    # over ClassDecl objects
    local_classes = class_decl.classes().iterator()

    num_classes = 0
    # Loop over all local classes
    while local_classes.hasNext():
        # Call count_classes recursively for all local classes
        # (including the contained class itself)
        num_classes += 1 + count_classes(local_classes.next(), depth + 1)

    # If the class declaration corresponds to a package, print
    # the number of hierarchically contained classes
    if class_decl.isPackage() and depth <= 1:
        print("The package %s has %d hierarchically contained classes"%(
            class_decl.qualifiedName(), num_classes))

    # Return the number of hierarchically contained classes
    return num_classes

# Call count_classes for 'Modelica'
num_classes = count_classes(modelica, 0)

try:
    filter_source.getProgramRoot()
except:
    filter_source = mc.parse_model("CauerLowPassAnalog.mo")

# Don't instantiate if instance has been computed already
try:
    filter_instance.components()
except:
    # Retrieve the node
    filter_instance = mc.instantiate_model(
            filter_source, "CauerLowPassAnalog", target)

def dump_inst_ast(inst_node, indent, fid):
    """
    Pretty print an instance node, including its merged environment.
    """

    # Get the merged environment of an instance node
    env = inst_node.getMergedEnvironment()

    # Create a string containing the type and name of the instance node
    str = indent + inst_node.prettyPrint("")
    str = str + " {"

    # Loop over all elements in the merged modification environment
    for i in range(env.size()):
        str = str + env.get(i).toString()
        if i < env.size() - 1:
            str = str + ", "
        str = str + "}"

    # Print
    fid.write(str + "\n")

    # Get all components and dump them recursively
    components = inst_node.instComponentDeclList

    for i in range(components.getNumChild()):
        # Assume the primitive variables are leafs in the instance AST
        if (inst_node.getClass() is \
                org.jmodelica.modelica.compiler.InstPrimitive) is False:
            dump_inst_ast(components.getChild(i), indent + "  ", fid)

    # Get all extends clauses and dump them recursively
    extends = inst_node.instExtendsList
    for i in range(extends.getNumChild()):
        # Assume that primitive variables are leafs in the instance AST
        if (inst_node.getClass() is \
                org.jmodelica.modelica.compiler.InstPrimitive) is False:
            dump_inst_ast(extends.getChild(i), indent + "  ", fid)

# dump the filter instance
with open('out.txt', 'w') as fid:
    dump_inst_ast(filter_instance, "", fid)

print("Done!")

