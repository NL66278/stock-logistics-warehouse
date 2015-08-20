#-*- coding: utf-8 -*-
"""Add immediately_usable_qty computed field to product.template."""
##############################################################################
#
#    This module is copyright (C) 2014 Numérigraphe SARL. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    """Add a field for the stock available to promise.
    Useful implementations need to be installed through the Settings menu or by
    installing one of the modules stock_available_*
    """
    _inherit = 'product.template'

    @api.multi
    @api.depends('virtual_available')
    def _immediately_usable_qty(self):
        """Immediately usable quantity calculated with the quant method."""
        location_model = self.env['stock.location']
        product_model = self.env['product.product']
        quant_model = self.env['stock.quant']
        internal_locations = location_model.search([
            ('usage', '=', 'internal')
        ])
        sublocation_ids = []
        for location in internal_locations:
            sublocation_ids += location_model.search([
                ('id', 'child_of', location.id),
                ('id', 'not in', sublocation_ids),
            ]).ids
        for product_template in self:
            product_ids = product_model.search([
                ('product_tmpl_id', '=', product_template.id),
            ]).ids
            quants = quant_model.search([
                ('location_id', 'in', sublocation_ids),
                ('product_id', 'in', product_ids),
                ('reservation_id', '=', False),
            ])
            availability = 0
            for quant in quants:
                availability += quant.qty
            product_template.immediately_usable_qty = availability

    immediately_usable_qty = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'),
        compute='_immediately_usable_qty',
        string='Available to promise (quant calculation)',
        help="Stock for this Product that can be safely proposed "
             "for sale to Customers.\n"
             "The definition of this value can be configured to suit "
             "your needs. This number is obtained by using the new odoo 8 "
             "quants, so it gives us the actual current quants minus reserved"
             "quants."
    )
