# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Sensible limits on minimum stock rule processing",
    "summary": """Limit stock resupply to what is sensible""",
    "author": "Therp BV",
    "website": "https://therp.nl",
    "category": "Warehouse",
    "license": "AGPL-3",
    "version": "8.0.1.0.0",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_warehouse_orderpoint.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
}
