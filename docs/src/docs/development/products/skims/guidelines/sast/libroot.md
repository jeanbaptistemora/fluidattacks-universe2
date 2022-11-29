---
id: libroot
title: Lib root vulnerabilities
sidebar_label: Libroot
slug: /development/products/skims/guidelines/sast/libroot
---

As mentioned in the introduction, for the languages supported by this library
and that are in active development, the following three-step procedure
is used:

## 1. Code parsing

Parse the code to a graph called the AST (Abstract Syntax Tree) using OS
libraries.

For C#, Java, JavaScript, TypeScript, the library is
[tree-sitter](https://github.com/tree-sitter/)

For Dart, the library is
[tree-sitter-dart](https://github.com/UserNobody14/tree-sitter-dart)

These graphs are generally very good representations of the code, however,
we have found that the AST graphs have two major problems:

First, they usually contain a lot of unnecessary information, such as
all the nodes for code syntax symbols, such as {}, ;, etc.
which makes search algorithms computationally more expensive and inefficient.

Second, the node label types change between languages, which makes it harder
to program the search methods. For example, in java, function invocation nodes
are identified as `method_invocation`, whereas in JavaScript, they are
identified as `call_expression`.

In order to solve these deficiencies, a re-parsing step is executed.

## 2. Syntax graph generation

This step converts the AST graph into an optimized graph called the
**syntax graph**.

As mentioned above, the purpose of the syntax graph is two-fold:

- Reduce the complexity and size of the AST.
- Generate a standard graph that uses common terminology to represent coding
  concepts that are similar between languages.

### 2.1 Node parsing

The algorithm uses recursion to re-parse the AST graph,
following this procedure:

1. Starting at the root node of the AST, a general recursive function
   (called `generic`) is in charge of dispatching a node
   to a relevant `reader`, that depends on the language and label type
   of the node.

1. This `reader` function extracts only the relevant
   information needed of the node and its children.
   After that, this information and the node ID is sent to a function called
   `builder` which depends only on the type of the node
   and is shared among all languages.

1. The builder function, as the name implies, builds the node
   for the syntax graph with all its relevant characteristics
   (such as name, children IDs, etc.) and adds the edges that connect to
   the children nodes.

1. The builder function also generates what is called a "fork",
   by calling the initial `generic` function with the children nodes
   as parameters.

1. The process starts again until all the nodes of the AST graph have
   been parsed.

1. After all the nodes have been parsed, the graph is sent to a similar
   recursive algorithm that generates the **control flow** connections
   between the main nodes.

### 2.2 Control Flow Connections

After all the nodes have been parsed and connected between them, another
important step is taken to improve the connectivity of the graph. This is
called the Control Flow.

Simply explained, and as the name implies, this adds a label to
certain edges of the graph that implies that two given nodes are connected
during the execution of the code.

As before, a recursive function iterates through all the nodes
of the syntax graph and, depending on each label type, it assigns the node to
a dispatcher function, in charge of generating the connections to the relevant
nodes that follow the code execution order. This is represented by
connecting each pair of nodes and adding a "CFG" label to the edge.

To best understand this process, run a simple code in the language
of your preference.

For example, use the following JS code:

```js
let my_var1 = 2;
let my_var2 = 3;
sum_vars(my_var1, my_var2);
```

See what nodes are created when you declare a variable and call a method,
and, see how the CFG labels are added to certain edges of the graph to
represent the flow of the code.

After that, you can try to use certain control structures like conditionals,
loops, or switch statements to see how the nodes are connected by different
paths.

### 2.3 Debugging

Before moving on to develop any methods using the syntax graph library,
it is recommended that you familiarize yourself with the node types and the
concept of the control flow, see how each part of the code is parsed and
fully understand how to debug the building process.

To see the parsed graphs (Both the AST and the syntax graph),
you can run skims using the --debug flag.

This will generate SVG files in the ~.skims folder in your home directory.
A total of four SVG files are currently generated, the first is the AST and
the last one is the Syntax graph.
(Note: The use and definition of the second and third SVG files is outside
the scope of this documentation because they are in the process of
being deprecated)

## 3. Vulnerability search

The last step of the process is programming the methods to search for
vulnerabilities in the code, by filtering and searching the syntax graph.

This last step can be classified according to two basic types
of vulnerabilities.

### 3.1 Direct vulnerabilities

When a vulnerability is a direct consequence of an unsafe object or
function, the method searches the nodes of the syntax graph for the method and
reports all the instances.

See the following pseudocode example:

```js
let vuln_var = new danger_object();
```

In this case, the vulnerability can be detected by filtering the syntax graph
and searching for any occurrences of the `danger_object`

Before moving on to the next type of vulnerabilities, it is recommended
that you try to understand and debug one of several methods in lib_root
that only use the syntax graph to search for a given vulnerability.

### 3.2 Compound Vulnerabilities

Some vulnerabilities cannot be checked directly by only filtering
the syntax graph, because they depend on one or several additional conditions
that have to be met simultaneously.

See the following pseudocode example:

```js
let dangerous_var = "danger";

let vuln_method = potential_danger("danger");
let vuln_method1 = potential_danger(dangerous_var);

let safe_method = potential_danger("safe_var");
```

In this case, the method called `potential_danger` is only a vulnerability
when the parameter `danger` is used.

In order for the method to deliver value to the clients, it needs to be able
to distinguish that the third call use of the method is safe,
and to report both of the first two occurrences of the vulnerability.

This is the purpose of the **symbolic evaluation** algorithm.

#### 3.2.1 Symbolic evaluation

This is a semi-recursive algorithm that follows the following procedure:

1. The node that could potentially generate the vulnerability is searched
   by filtering the graph or other search methods. (In the example, this
   would be the parameter of the potential_danger method)

1. Based on this node, all the paths that the control flow of the code that
   pass through it are calculated.

1. The node and its execution paths are sent to the general
   `generic` dispatcher function.

1. Depending on the label_type of the node, the node gets dispatched to a
   `evaluator` function.

1. Each node type has its own evaluator function that, depending on the node
   characteristics, searches and propagates the algorithm to other nodes
   that are somehow related to the initial node.

   For example, a `SymbolLookup` evaluator, searches in the graph
   where that symbol is defined and, if found, propagates the danger by
   calling the `generic` function using that node as parameter.
   A `VariableDeclaration` evaluator propagates the danger directly to the
   value node of the variable.

1. If the danger was propagated, the dispatcher function gets called with
   these new parameters and the process is repeated.

1. Depending on what the vulnerability is, each method has one or several
   specific `evaluator` functions, that check if the node is
   dangerous according to the vulnerability conditions and if so, marks the
   node as dangerous.

The algorithm finishes once all possible paths have been evaluated using this
same process, and returns two values:

- A boolean value called danger.
- A set of string values called the `triggers` (Maybe empty when not needed)

Before moving on to understanding and using the `triggers`, it is
recommended that you understand methods that only use the danger
value to evaluate a vulnerability.

#### 3.2.2 Symbolic evaluation Triggers

Sometimes, a boolean value is not enough to check for a vulnerability,
because it requires several conditions to be met at the same time.

See the following pseudocode example:

```js
let dangerous_var = "danger";

let transformed_val = danger_transformation(dangerous_var);
let vulnerability = potential_danger(transformed_val);

let safe_method = potential_danger(dangerous_var);
```

In this case, the `danger` variable, needs to go through a
`danger_transformation` method before being used in the `potential_danger`
to cause a true vulnerability.

Ensuring this double condition would not be possible only with the use
of a boolean value. This is the main use of the triggers.

The symbolic evaluation works the same way as explained above, only this time,
at the specific evaluator for the method, a value would get added
to the triggers to represent the additional vulnerable condition.

It is recommended that you use the triggers object only when you
fully understand its implications and use cases.
As guidelines, try to debug one of several existing methods that use them.
