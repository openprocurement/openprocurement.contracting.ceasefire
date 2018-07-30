.. _milestone_workflow:

Milestone Workflow
==================

.. graphviz::

    digraph G {
        subgraph cluster_1 {
            node [style=filled, fillcolor=seashell2]
            edge[style=solid,  arrowhead="vee"]
            "scheduled" -> "processing"
            "processing" -> "met"
            color=white
        }  

        subgraph cluster_2 {
            "processing" -> "partiallyMet"
            color=white
        }

        subgraph cluster_3 {
            edge[style=dashed,  arrowhead="vee"]
            "processing" -> "notMet"
            color=white
        }
    }

Legend
--------

   * dashed line - user action
    
   * solid line - action is done automatically
