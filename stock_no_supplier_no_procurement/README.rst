.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===========================
No supplier, no procurement
===========================

Running the planner for can result in a lot of exceptions when processing
minimum stock rules for products that do not have a supplier. Subsequent runs
of the planner will then not create new procurements, even if a supplier has
been added to the product in the meantime.

Usage
=====

This module prevents the creation of procurements for products that do not
have a supplier. When this happens, the product templates (that carry the
supplier information) are marked, so that all products that have missing
supplier information can be found easily.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/153/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/stock-logistics-warehouse/issues>`_.
In case of trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Ronald Portier (Therp BV) <ronald@therp.nl>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
