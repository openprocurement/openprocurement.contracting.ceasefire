.. _tutorial:

Tutorial
========

Exploring basic rules
---------------------

Let's try exploring the `/contracts` endpoint:

.. include:: tutorial/contracts-listing-empty.http
    :code:

Just invoking it reveals an empty set.

Contract is transferred from the auction system by an automated process.

.. index:: Contracts

Creating contract
-----------------

Let's say that we have conducted procedure and it has ``complete`` status. When the procedure is completed, contract (that has been created in the auction system) is transferred to the contract system **automatically**.

*Brokers (eMalls) can't create contracts in the contract system.*

The contract initially receives `active.confirmaition` status.  

.. include:: tutorial/created-contract.http
    :code:

Getting contract
----------------

Let's access the URL of the created object. The internal identification of the contract (id) is noted within the Lots Registry (`lot.contracts.relatedProcessID`): 

.. include:: tutorial/get-created-contract.http
    :code:

Getting access
--------------

In order to get rights for future contract editing, you need to use `access transfer mechanism <http://relocation.api-docs.openprocurement.org/en/latest/tutorial.html>`_.

Let's create a transfer:

.. include:: tutorial/create-transfer.http
    :code:

To acquire ownership on the contract, we must to use that transfer:

.. include:: tutorial/use-transfer.http
    :code:

For futher actions to be applied you need to activate the contract. Using `access_token` change status of the contract to `active.payment`:

.. include:: tutorial/patch-contract-to-active-payment.http
    :code:

Now let's view contracts.


.. include:: tutorial/view-contracts-after-create.http
    :code:

Milestones
----------
There are 3 milestones within:

* **financing** milestone;
* **approval** milestone;
* **reporting** milestone.


Working with the financing milestone 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The milestone initially receives `processing` status with an auto-generated `dueDate` equal to (dateSigned + 60 days):

.. include:: tutorial/get-financing-milestone-processing.http
    :code:

It is then when the winner has to introduce the payment (the sum suggested within the auction). 
As soon as the payment is received, the Organizer has to mention this date within the `dateMet` field.
If `dateMet` lies within the suggested frames (up to `dueDate`), the milestone status will be automatically switched to `met`:

.. include:: tutorial/patch-financing-to-met.http
    :code:


If `dateMet` is after `dueDate`, the milestone status will be switched to `partiallyMet`:

.. include:: tutorial/patch-financing-to-partially-met.http
    :code:

Both of the described actions result in contract being changed its status from `active.payment` to `active.approval`:

.. include:: tutorial/get-contract-after-financing-partiallyMet.http
    :code:

The Organizer can also switch the milestone status to `notMet` if the payment has not been introduced at all. This one will change the contract status to `pending.unsuccessful`. As long as the lot becomes `pending.dissolution`, the contract receives `unsuccessful` status.

We don't show a request for this, because it's irreversable action, and after it we cannot fully demonstrate the work with contracts.

Working with the approval milestone 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The milestone initially receives `scheduled` status. As long as the contract receives `active.approval`, status of the approval milestone is changed to `processing`. The `dueDate` here is equal to (financing milestone’s dateMet + 20 business days) 

.. include:: tutorial/get-approval-milestone.http
    :code:

The Organizer can also optionally set the `dueDate` of the **reporting** milestone.
It can be done only when the reporting milestone has status `scheduled`.
If `dueDate` will not be set manually, it will be set automatically.

.. include:: tutorial/patch-reporting-due-date.http
    :code:

It is then when the Organizer has to upload the Small-Scale Privatization Completion Report (documentType: approvalProtocol), note the date when the Report has been signed (`dateMet` field) and change status of the current milestone to `met` (if `dateMet` lies within the suggested frames) or `partiallyMet` (if not) by setting actual `dateMet`:

.. include:: tutorial/patch-approval-to-met.http
    :code:

The actions performed lead to the contract being changed its status from `active.approval` to `active`:

.. include:: tutorial/get-contract-after-approval-met.http
    :code:

In case of the Completion Report has not been introduced, the Organizer has to manually switch milestone status to `notMet`. This one will change the contract status to `pending.unsuccessful`. As long as the lot becomes `pending.dissolution`, the contract receives `unsuccessful` status.


Working with the reporting milestone 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The milestone initially receives `scheduled` status. As long as the contract receives `active`, status of the reporting milestone is changed to `processing`. The `dueDate` here is equal to either (reporting milestone’s dateMet + 3 years) or the date mentioned before. 

.. include:: tutorial/get-reporting-processing.http
    :code:

As long as all of the contract conditions have been met, the Organizer has to mention the appropriate `dateMet` and change status of the current milestone to `met` (if `dateMet` lies within the suggested frames) or `partiallyMet` (if not):

.. include:: tutorial/patch-reporting-to-met.http
    :code:

The actions performed lead to the contract being changed its status from `active` to `pending.terminated`:

.. include:: tutorial/get-contract-after-reporting-met.http
    :code:

As long as the lot becomes `pending.sold`, the contract receives `terminated` status so that any future modification to the contract are not allowed.

In case of the conditions have not been met, the Organizer has to manually switch milestone status to `notMet`. This one will change the contract status to `pending.unsuccessful`. As long as the lot becomes `pending.dissolution`, the contract receives `unsuccessful` status.

Uploading milestone document
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Document has to be added in two stages:

* you should upload document


* you should set document properties ``"documentOf": "milesone"`` and ``"relatedItem": "{milestone.id}"`` in order to bind the uploaded document to the `milestone`:

.. include:: tutorial/upload-document-to-milestone.http
    :code:

Uploading documentation
-----------------------

Procuring entity can upload PDF files into the created contract. Uploading should
follow the :ref:`upload` rules.

.. include:: tutorial/upload-contract-document.http
   :code:

`201 Created` response code and `Location` header confirm document creation.
We can additionally query the `documents` collection API endpoint to confirm the
action:

.. include:: tutorial/get-contract-documents.http
   :code:

.. index:: Enquiries, Question, Answer
