.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Item, Parameter, Classification, CPV, Unit

.. _Item:

Item
====

Schema
------

:id:
    string, auto-generated

:description:
    string, multilingual, required

    |ocdsDescription|
    A description of the goods, services to be provided.

    Auction subject / asset description.

:classification:
    :ref:`Classification`, required

    |ocdsDescription|
    The primary classification for the item. See the
    `itemClassificationScheme` to identify preferred classification lists,
    including CAV and GSIN.

    It is required for `classification.scheme` to be `CPV` or `CAV-PS`. The
    `classification.id` should be valid CPV or CAV-PS code.

    The CPV & CAV-PS codes accuracy should be equal to the class (XXXX0000-Y) at least.

:additionalClassifications:
    List of :ref:`Classification` objects, optional

    |ocdsDescription|
    An array of additional classifications for the item. See the
    `itemClassificationScheme` codelist for common options to use in OCDS. 
    This may also be used to present codes from an internal classification
    scheme.

    E.g.`CPVS`, `DK018`, `cadastralNumber` & `UA-EDR` can be chosen from the list. 
    The codes are to be noted manually for `cadastralNumber` & `UA-EDR`.

:unit:
    :ref:`Unit`

    |ocdsDescription| 
    Description of the unit which the good comes in e.g.  hours, kilograms. 
    Made up of a unit name, and the value of a single unit.

:quantity:
    integer, required

    |ocdsDescription|
    The number of units required

:deliveryAddress:
    :ref:`Address`, required

    Address, where the item should be delivered.

:deliveryLocation:
    dictionary, optional

    Geographical coordinates of delivery location. Element consist of the following items:

    :latitude:
        string, required
    :longitude:
        string, required
    :elevation:
        string, optional, usually not used

    `deliveryLocation` usually takes precedence over `deliveryAddress` if both are present.

:relatedLot:
    string

    Id of related :ref:`lot`.

:registrationDetails:
    List of :ref:`registrationDetails`

:address:
    :ref:`Address`

    Address, where the item is located


.. _Classification:

Classification
==============

Schema
------

:scheme:
    string

    |ocdsDescription|
    A classification should be drawn from an existing scheme or list of
    codes.  This field is used to indicate the scheme/codelist from which
    the classification is drawn.  For line item classifications, this value
    should represent a known Item Classification Scheme wherever possible.

:id:
    string

    |ocdsDescription|
    The classification code drawn from the selected scheme.

:description:
    string

    |ocdsDescription|
    A textual description or title for the code.

:uri:
    uri

    |ocdsDescription|
    A URI to identify the code. In the event individual URIs are not
    available for items in the identifier scheme this value should be left
    blank.

.. _Unit:

Unit
====

Schema
------

:code:
    string, required

    UN/CEFACT Recommendation 20 unit code.

:name:
    string

    |ocdsDescription|
    Name of the unit


.. _registrationDetails:

Registration Details
====================

Schema
------

:status:
    string, required

    Possible values are:

    :`unknown`: 
        default value;
    :`registering`:
        item is still registering;
    :`complete`:
        item has already been registered.

:registrationID:
    string, optional

    The document identifier to refer to in the `paper` documentation.

    Available for mentioning in status: complete.

:registrationDate:
    :ref:`Date`, optional

    |ocdsDescription|
    The date on which the document was first published.

    Available for mentioning in status: complete.
