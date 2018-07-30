.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Contract

.. _Contract:

Contract
========

Schema
------

:id:
    uuid, auto-generated, read-only

    Internal identifier for this contract.

:awardID:
    string, required, read-only

    |ocdsDescription|
    The `Award.id` against which this contract is being issued.

:contractID:
    string, auto-generated, read-only

    |ocdsDescription|
    ID of the same contract, bound to auction resource.

:contractNumber:
    string, optional

    Contract number within the paper documentation.

:title:
    string, multilingual, optional
    
    * Ukrainian by default - Ukrainian title

    * ``title_en`` (English) - English title

    * ``title_ru`` (Russian) - Russian title

    |ocdsDescription|
    Contract title.

:description:
    string, multilingual, optional
    
    * Ukrainian by default - Ukrainian decription
    
    * ``decription_en`` (English) - English decription
    
    * ``decription_ru`` (Russian) - Russian decription
    
    |ocdsDescription|
    Contract description.

:status:
    string, required

    |ocdsDescription|
    The current status of the contract.

+-------------------------+---------------------------------------------------------------------------------+
|        Status           |                             Description                                         |
+=========================+=================================================================================+
| :`active.confirmation`: | draft contract                                                                  |
+-------------------------+---------------------------------------------------------------------------------+
| :`active.payment`:      | payment period                                                                  |
+-------------------------+---------------------------------------------------------------------------------+
| :`active.approval`:     | the period for downloading the final Order on the privatization of the facility |
+-------------------------+---------------------------------------------------------------------------------+
| :`active`:              | this contract has been signed by all the parties, and is now legally in force   |
+-------------------------+---------------------------------------------------------------------------------+
| :`active`:              | period for fulfillment of other conditions                                      |
+-------------------------+---------------------------------------------------------------------------------+
| :`pending.terminated`:  | a vaiting transition to the next status                                         |
+-------------------------+---------------------------------------------------------------------------------+
| :`pending.unsuccessful`:| a vaiting transition to the next status                                         |
+-------------------------+---------------------------------------------------------------------------------+
| :`terminated`:          | this contract was signed and in force, and has now come to a close. This may be |
|                         | due to a successful completion of the contract or may be early termination      |
|                         | due to some non-completion issue                                                |
+-------------------------+---------------------------------------------------------------------------------+
| :`unsuccessful`:        | this contract is unsuccessful                                                   |
+-------------------------+---------------------------------------------------------------------------------+

:items:
    Array of :ref:`Item` objects, auto-generated, read-only

    |ocdsDescription|
    The goods, services, and any intangible outcomes in this contract.

:procuringEntity:
    :ref:`Organization`, optional

    |ocdsDescription|
    The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:suppliers:
    List of :ref:`Organization` objects, auto-generated, read-only

    Buyer. Indicates the winner of the auction whom the given contract has been signed with.

:value:
    `Value` object, auto-generated, read-only

    |ocdsDescription|
    The total value of this contract.

:dateSigned:
    string, :ref:`date`, auto-generated, read-only

    |ocdsDescription|
    The date the contract was signed. In the case of multiple signatures, the date of the last signature.

:documents:
    Array of :ref:`Document` objects, optional

    |ocdsDescription|
    All documents and attachments related to the contract, including any notices.

:changes:
    Array of :ref:`Change` objects, optional

:merchandisingObject:
    string, auto-generated, read-only

    Id of related :ref:`Lot`

:milestones:
    Array of :ref:`Milestones` objects.

    There are 3 milestones, that will be associated with contract after acquiring him `active.payment` status:

    * `financing`
    * `approval`
    * `reporting`

:owner:
    string, auto-generated, read-only

    The entity whom the contract has been created by.

:dateModified:
    string, :ref:`date`, auto-generated, read-only

    Time, when contract was changed last time.

:contractType:
    string, auto-generated, read-only

    Type of the contract.
