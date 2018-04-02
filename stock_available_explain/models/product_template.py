# -*- coding: utf-8 -*-
# Copyright 2018 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def button_stock_available_explain(self):
        self.ensure_one()
        product = self.product_variant_ids[0]
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.available.explain',
            'target': 'new',
            'nodestroy': True,
            'context': dict(self.env.context, default_product_id=product.id),
            'view_type': 'form',
            'view_mode': 'form'}
