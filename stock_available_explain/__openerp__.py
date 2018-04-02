# -*- coding: utf-8 -*-
# Copyright 2018 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Explain product stock available',
    'version': '8.0.1.0.0',
    "author": "Therp BV, Odoo Community Association (OCA)",
    'category': 'Warehouse',
    'depends': ['stock'],
    'license': 'AGPL-3',
    'data': [
        'views/product_template.xml',
        'wizards/stock_available_explain.xml',
    ]
}
