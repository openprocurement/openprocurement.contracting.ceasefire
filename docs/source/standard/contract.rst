.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Contract
.. _Contract:

Contract
========

Schema
------

:id:
    uid, auto-generated

    |ocdsDescription|
    The identifier for this contract.

:awardID:
    string, required

    |ocdsDescription|
    The `Award.id` against which this contract is being issued.

:contractID:
    string, auto-generated, read-only

    |ocdsDescription|
    ID of the same contract, bound to auction resource.

:contractNumber:
    string

:title:
    string, required

    |ocdsDescription|
    Contract title

:description:
    string

    |ocdsDescription|
    Contract description

:status:
    string, required

    |ocdsDescription|
    The current status of the contract.

    Possible values are:

    * `active.confirmation` - ???
    * `active.payment` - ???
    * `active.approval` - ???
    * `active` - this contract has been signed by all the parties, and is
      now legally in force.
    * `active` - ???
    * `pending.terminated` - ???
    * `pending.unsuccessful` - ???
    * `terminated` - this contract was signed and in force, and has now come
      to a close.  This may be due to a successful completion of the contract,
      or may be early termination due to some non-completion issue.
    * `unsuccessful` - ???

:items:
    List of :ref:`Item` objects, auto-generated, read-only

    |ocdsDescription|
    The goods, services, and any intangible outcomes in this contract. Note: If the items are the same as the award do not repeat.

:procuringEntity:
   :ref:`ProcuringEntity`

   |ocdsDescription|
   The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:suppliers:
    List of :ref:`Organization` objects, auto-generated, read-only

:value:
    `Value` object, auto-generated, read-only

    |ocdsDescription|
    The total value of this contract.

:dateSigned:
    string, :ref:`date`, auto-generated

    |ocdsDescription|
    The date the contract was signed. In the case of multiple signatures, the date of the last signature.

:documents:
    List of :ref:`Document` objects

    |ocdsDescription|
    All documents and attachments related to the contract, including any notices.

:changes:
    List of :ref:`Change` objects.

:amountPaid:

    :amount: float, required
    :currency: string, required, auto-generated
    :valueAddedTaxIncluded: bool, required , auto-generated

    Amount of money actually paid.

:merchandisingObject:
    Id of related :ref:`Lot`

:milestones:
    List of :ref:`Milestone` objects.

    There are 3 milestones, that will be associated with contract after acquiring him `active.payment` status:

    * `financing`
    * `approval`
    * `reporting`

:owner:
    UserID of user, that owns this contract.

:dateModified:
    string, :ref:`date`, auto-generated

    Time, when contract was changed last time.

:contractType:
    string

    Type of the contract.
