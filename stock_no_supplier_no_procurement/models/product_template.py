# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ProductTemplate(models.Model):
    """Add a field to signal missing supplier for minimum stock rule."""
    _inherit = 'product.template'

    @api.onchange('seller_ids')
    def onchange_seller_ids(self):
        """Reset missing supplier if supplier added."""
        for this in self:
            if this.seller_ids:
                this.missing_supplier = False

    missing_supplier = fields.Boolean(
        string='Missing supplier',
        readonly=True,
        help="Creating procurement was prevented when processing miminum"
             " stock rules for this product.\n"
        )
