.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Document, Attachment, File, Notice, Bidding Documents, Technical Specifications, Evaluation Criteria, Clarifications

.. _Document:

Document
========

Schema
------

:id:
    string, auto-generated, read-only

    Internal identifier of the object within an array.

:documentType:
    string, optional

    Possible values for :ref:`contract`

    * `notice` - **Contract notice**

    The formal notice that gives details of a contract being signed and valid to start implementation. This may be a link to a downloadable document, to a web page, or to an official gazette in which the notice is contained.

    * `contractSigned` - **Signed Contract**

    A copy of the signed contract. Consider providing both machine-readable (e.g. original PDF, Word or Open Document format files), and a separate document entry for scanned-signed pages where this is required.

    * `contractAnnexe` - **Annexes to the Contract**

    Copies of annexes and other supporting documentation related to the contract.

    * `rejectionProtocol` - **Rejection Protocol**

    Documents containing the reasons for termination of work with the participant.

    * `act` - **Act**

    Documents containing the reasons for termination of work with the participant.

    * `approvalProtocol` - **Approval Protocol**

    Confirming the presence of the order on privatization.

:title:
    string, multilingual, required
    
    |ocdsDescription|
    The document title. 
    
:description:
    string, multilingual, optional
    
    |ocdsDescription|
    A short description of the document. In the event the document is not accessible online, the description field can be used to describe arrangements for obtaining a copy of the document.
    
:format:
    string, optional
    
    |ocdsDescription|
    The format of the document taken from the `IANA Media Types code list <http://www.iana.org/assignments/media-types/>`_, with the addition of one extra value for 'offline/print', used when this document entry is being used to describe the offline publication of a document. 
    
:url:
    string, auto-generated, read-only
    
    |ocdsDescription|
    Direct link to the document or attachment. 

:index:
    integer, optional

    Sorting (display order) parameter used for illustrations. The smaller number is, the higher illustration is in the sorting. If index is not specified, illustration will be displayed the last. If two illustrations have the same index, they will be sorted depending on their publishing date.

:datePublished:
    string, :ref:`date`, auto-generated, read-only
    
    |ocdsDescription|
    The date on which the document was first published. 
    
:dateModified:
    string, :ref:`date`, auto-generated, read-only
    
    |ocdsDescription|
    Date that the document was last modified
    
:language:
    string, optional
    
    |ocdsDescription|
    Specifies the language of the linked document using either two-digit `ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_, or extended `BCP47 language tags <http://www.w3.org/International/articles/language-tags/>`_. 

:documentOf:
    string, required

    Possible values are:

    * `contract`
    * `milestone`

:relatedItem:
    string, required

    Id of related :ref:`Milestones`