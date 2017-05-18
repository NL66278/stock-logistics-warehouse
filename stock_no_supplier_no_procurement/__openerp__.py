# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name' : 'Prevent exceptions for no supplier',
    'version' : '8.0.1.0.0',
    'author' : 'Therp BV,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category' : 'Stock Logistics',
    'website': 'https://therp.nl',
    'depends' : [
        'purchase',
    ],
    'data' : [
        'views/product_template.xml',
    ],
    'installable': True
}
