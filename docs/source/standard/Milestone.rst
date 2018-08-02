.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Milestones

.. _Milestones:

Milestone
=========

Schema
------

:id:
    string, auto-generated, read-only

    Internal identifier of the milestone.

:title:
    string, multilingual, optional

    * Ukrainian by default - Ukrainian title

    * ``title_en`` (English) - English title

    * ``title_ru`` (Russian) - Russian title

    Title of milestone.

:description:
    string, multilingual, optional 

    * Ukrainian by default - Ukrainian decription

    * ``decription_en`` (English) - English decription

    * ``decription_ru`` (Russian) - Russian decription    

    Description of milestone.

:type:
    string, auto-generated, read-only

    Type of milestone. Posible values are:

    * `financing`

    * `approval`

    * `reporting`

:dueDate:
    string, :ref:`date`, auto-generated, read-only

    The date when the execution time within milestone runs out.
    Optionally user can set dueDate for the 3rd milestone as long as it's in scheduled status.

:dateMet:
    string, :ref:`date`, required 

    Date when the relevant conditions were fulfilled.

:status:
    string, required 

+-------------------------+---------------------------------------------------------------------------+
|        Status           |                  Description                                              |
+=========================+===========================================================================+
| :`scheduled`:           |  when the milestone are not yet involved                                  |
+-------------------------+---------------------------------------------------------------------------+
| :`processing`:          |  when milestone is active                                                 |
+-------------------------+---------------------------------------------------------------------------+
| :`met`:                 |  if the dateMet value is within the allowed range                         |
+-------------------------+---------------------------------------------------------------------------+
| :`partiallyMet`:        |  if the dateMet value is outside the allowed range                        |
+-------------------------+---------------------------------------------------------------------------+
| :`notMet`:              |  if the conditions were not met, then milestone is considered unsuccessful|
+-------------------------+---------------------------------------------------------------------------+

:dateModified:
    string, :ref:`date`, auto-generated, read-only 

    |ocdsDescription|
    Date when the milestone was last modified.
