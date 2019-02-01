Overview
========

Ceasefire contracting

Features
--------

 * On contract activation in award, the object `contract` is formed in the `Contracting Module` component
 * For object activation in the system the owner has to use the transfer token and assign the status `active.payment` to the object
 * The created `contract` contains three `milestones`
 * Each `milestone` corresponds to certain contract terms and conditions
 * Each `milestone` contains dueDate corresponding to the final date until which all the indicated terms and conditions are to be fulfilled
 * In order to confirm the completion of the `financing milestone` conditions the Organiser is obliged to set the `dateMet`  for identification of payment reception from the participant
 * On condition that the payment was not received the Organiser has the right to set the milestone to status `notMet` upon which the `contract` will be assigned the status `pending.unsuccessful`
 * In order to confirm the completion of the `approval milestone` conditions the Organiser has to upload the document (`documentType:approvalProtocol`) into the contract having provided the indications `documentOf:milestone` and `relatedItem` with the corresponding milestone identifier and to set the `dateMet` 
 * In order to assign the `notMet` status to `pproval mileston` it is necessary to upload the document (`documentType:rejectionProtocol`) upon which the contract status will be changed to `pending.unsuccessful`
 * In order to confirm the completion of the `reporting milestone` conditions the Organiser has to set `dateMet` 
 * In order to assign the `notMet` status to rejection milestone it is necessary to upload the document (`documentType:rejectionProtocol`) upon which the contract status will be changed to `pending.unsuccessful`
 * If dateMet precedes the `dueDate`, the `milestone` status should be changed to met, if not - to `partiallyMet`
 * All the actions must be carried out by the Organiser



Conventions
-----------

API accepts `JSON <http://json.org/>`_ or form-encoded content in
requests.  It returns JSON content in all of its responses, including
errors.  Only the UTF-8 character encoding is supported for both requests
and responses.

All API POST and PUT requests expect a top-level object with a single
element in it named `data`.  Successful responses will mirror this format. 
The data element should itself be an object, containing the parameters for
the request.  In the case of creating a new auction, these are the fields we
want to set on the auction itself.

If the request was successful, we will get a response code of `201`
indicating the object was created.  That response will have a data field at
its top level, which will contain complete information on the new auction,
including its ID.

If something went wrong during the request, we'll get a different status
code and the JSON returned will have an `errors` field at the top level
containing a list of problems.  We look at the first one and print out its
message.

Main responsibilities
---------------------

Project status
--------------

The project has beta status.

The source repository for this project is on GitHub: https://github.com/openprocurement/openprocurement.contracting.ceasefire

You can leave feedback by raising a new issue on the `issue tracker <https://github.com/openprocurement/openprocurement.contracting.ceasefire/issues>`_ (GitHub registration necessary).  

Documentation of related packages
---------------------------------

* `OpenProcurement API <http://api-docs.openprocurement.org/en/latest/>`_
* `Assets Registry <http://assetsbounce.api-docs.registry.ea2.openprocurement.io/en/latest/>`_
* `Lots Registry <http://lotsloki.api-docs.registry.ea2.openprocurement.io/en/latest/>`_
* `Sellout.english <http://sellout-english.api-docs.ea2.openprocurement.io/en/latest/>`_
* `Tessel <https://openprocurementauctionstessel.readthedocs.io/en/latest/>`_

API stability
-------------

API is relatively stable. The changes in the API are communicated via `Open Procurement API
<https://groups.google.com/group/open-procurement-api>`_ maillist.

Next steps
----------
You might find it helpful to look at the :ref:`tutorial`.
