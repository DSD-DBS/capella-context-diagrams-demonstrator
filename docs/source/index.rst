..
   Copyright DB InfraGO AG and contributors
   SPDX-License-Identifier: Apache-2.0

Welcome to capella-context-diagrams-demonstrator's documentation!
=================================================================

The Capella Context Diagrams Demonstrator (CCDD) lets you interactively edit a textual description of a diagram while the corresponding diagram is generated on demand.

Quickstart
----------

1.  Inside the `Target Browser` panel's search field, start typing the name or UUID of the model element you want to create a diagram for and select it from the list of suggestions. This will load and set the diagram target.

2.  Inside the `Editor`, type the accessor name of a pre-defined diagram type (e.g. `context_diagram`). The `Editor` supports auto-completion for diagram types. Start typing the name of a diagram type and press `Tab` to auto-complete it.

.. code-block:: yaml
    :linenos:

    context_diagram

.. note::

    For more pre-defined diagram types, check out the `capellambse-context-diagrams documentation <https://dsd-dbs.github.io/capellambse-context-diagrams>`_.

3.  Click `Run` or press `Ctrl + Enter`. This will generate the diagram and display it in the `Preview` panel.

.. note::

    You can save the diagram as an SVG by right clicking inside the `Preview` panel and selecting `Save`.

Render parameters
-----------------

All render parameters and their default values are as described in the `capellambse-context-diagrams documentation <https://dsd-dbs.github.io/capellambse-context-diagrams>`_.

They can be set in the `Editor` as follows:

.. code-block:: yaml
    :linenos:

    context_diagram:
        display_parent_relation: false

This will generate a context diagram without displaying the parent relation.

Custom diagram collection description
-------------------------------------
The `Custom Diagram <https://dsd-dbs.github.io/capellambse-context-diagrams/realization_view/>`_ is a special diagram type that allows you to define your own diagram collection. To define the Custom Diagram collection in CCDD, you can provide a YAML description of the collection in the `Editor`, e.g.:

.. code-block:: yaml
    :linenos:

    custom_diagram:
        unify_edge_direction: UNIFORM
        display_parent_relation: true
        collect:
            get:
                - name: inputs
                include:
                    - name: exchanges

`get` and `include`
~~~~~~~~~~~~~~~~~~~

At every step of the collection, you can either `get` or `include` elements. `get` will simply get the element and `include` will include the element in the collection. `name` is the attribute name.

.. code-block:: yaml
    :linenos:

    get:
        - name: inputs
        include:
            - name: exchanges
            - name: links
        - name: outputs
        include:
            - name: exchanges
            - name: links
        - name: ports
        include:
            - name: exchanges
            - name: links

In the example above, we first `get` all the inputs of our target element and iterate over them. For each input, we include all the exchanges and links in the resulting diagram. We do the same for outputs and ports. Note that `get` does not include the element in the diagram, it just gets the element, but calling `include` on an edge will also include the edge's source and target ports.

`filter`
~~~~~~~~

Whenever you have a list of elements and you want to filter them, you can use the `filter` keyword. The `filter` keyword takes a dictionary as an argument, which should have the key as the attribute name and the value as the value you want to filter on.

.. code-block:: yaml
    :linenos:

    get:
        - name: inputs
        include:
            - name: exchanges
                filter:
                    kind: "FunctionalExchange"

In the example above, we get all the inputs of our target element and include all the exchanges that are of kind `FunctionalExchange` in the resulting diagram.

`repeat`
~~~~~~~~

With the `repeat` keyword, you can repeat the collection. The value of `repeat` should be an integer. If the value is -1, the collection will repeat until no new elements are found. If the value is 0, the collection will not repeat. If the value is 1, the collection will repeat once and so on.

.. code-block:: yaml
    :linenos:

    repeat: -1
    get:
        - name: source
        include:
            name: links
        - name: target
        include:
            name: links

In the example above, we get the source and target of our target element and include all the links in the resulting diagram. For each link we again get the source and target and include all the links in the resulting diagram. This will repeat until no new elements are found.

Examples
--------

For more examples, navigate to `File` > `Load` in the top menu and select one of the example YAML files.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. toctree::
   :maxdepth: 3
   :caption: API reference

   code/modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
