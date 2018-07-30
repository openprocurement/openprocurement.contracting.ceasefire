.. _contract_workflow:

Contract Workflow
=================

.. graphviz::

    digraph G {
       subgraph cluster_0 {
         node [style=filled, fillcolor=seashell2];
         edge[style=dashed,  arrowhead="vee"];
         "active.confirmaition" -> "active.payment"
         edge[style=solid,  arrowhead="vee"];
         "active.payment" -> "active.approval"
         "active.approval" -> "active"
         "active" -> "pending.terminated"
         "pending.terminated" -> "terminated"
         color=white;
       }

       "active.payment" -> "pending.unsuccessful"
       "active.approval" -> "pending.unsuccessful"
       "active" -> "pending.unsuccessful"
       "pending.unsuccessful" -> "unsuccessful"
    }

Legend
--------

   * dashed line - user action
    
   * solid line - action is done automatically
