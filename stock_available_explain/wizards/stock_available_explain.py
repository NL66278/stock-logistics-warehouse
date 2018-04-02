# -*- coding: utf-8 -*-
# Copyright 2018 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from openerp.tools.float_utils import float_round


class StockAvailableExplain(models.TransientModel):
    _name = 'stock.available.explain'

    @api.multi
    def _compute_product_available(self):
        context = self.env.context
        move_model = self.env['stock.move']
        quant_model = self.env['stock.quant']
        for this in self:
            product = this.product_id
            domain_products = [('product_id', '=', product.id)]
            domain_quant, domain_move_in, domain_move_out = [], [], []
            domain_quant_loc, domain_move_in_loc, domain_move_out_loc = \
                product._get_domain_locations()
            domain_move_in += \
                product._get_domain_dates() + \
                [('state', 'not in', ('done', 'cancel', 'draft'))] + \
                domain_products
            domain_move_out += \
                product._get_domain_dates() + \
                [('state', 'not in', ('done', 'cancel', 'draft'))] + \
                domain_products
            domain_quant += domain_products
            if context.get('owner_id'):
                domain_quant.append(
                    ('owner_id', '=', context['owner_id']))
                owner_domain = (
                    'restrict_partner_id', '=', context['owner_id'])
                domain_move_in.append(owner_domain)
                domain_move_out.append(owner_domain)
            if context.get('package_id'):
                domain_quant.append(('package_id', '=', context['package_id']))
            domain_move_in += domain_move_in_loc
            domain_move_out += domain_move_out_loc
            moves_in = move_model.read_group(
                domain_move_in, ['product_id', 'product_qty'], ['product_id'])
            moves_out = move_model.read_group(
                domain_move_out, ['product_id', 'product_qty'], ['product_id'])
            domain_quant += domain_quant_loc
            quants = quant_model.read_group(
                domain_quant, ['product_id', 'qty'], ['product_id'])
            quants = dict(
                map(lambda x: (x['product_id'][0], x['qty']), quants))
            moves_in = dict(
                map(lambda x:
                    (x['product_id'][0], x['product_qty']), moves_in))
            moves_out = dict(
                map(lambda x:
                    (x['product_id'][0], x['product_qty']), moves_out))
            qty_available = float_round(
                quants.get(product.id, 0.0),
                precision_rounding=product.uom_id.rounding)
            incoming_qty = float_round(
                moves_in.get(product.id, 0.0),
                precision_rounding=product.uom_id.rounding)
            outgoing_qty = float_round(
                moves_out.get(product.id, 0.0),
                precision_rounding=product.uom_id.rounding)
            virtual_available = float_round(
                quants.get(id, 0.0) + moves_in.get(id, 0.0) -
                moves_out.get(id, 0.0),
                precision_rounding=product.uom_id.rounding)
            product.write({
                'qty_available': qty_available,
                'incoming_qty': incoming_qty,
                'outgoing_qty': outgoing_qty,
                'virtual_available': virtual_available})

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True)
    state = fields.Selection(
        selection=[('select', 'Select arguments'), ('show', 'Show results')],
        default='select',
        required=True)
    # Related fields to show quantity's on product. To cross check the
    # computations in this wizard, with the computations on the actual
    # product.
    product_qty_available = fields.Float(
        string='Available on product',
        related='product_id.qty_available',
        readonly=True)
    product_incoming_qty = fields.Float(
        string='Incoming on product',
        related='product_id.incoming_qty',
        readonly=True)
    product_outgoing_qty = fields.Float(
        string='Outgoing on product',
        related='product_id.outgoing_qty',
        readonly=True)
    product_virtual_available = fields.Float(
        string='Virtual available on product',
        related='product_id.virtual_available',
        readonly=True)
    # Computed fields that should show how quantity fields in product
    # are derived
    qty_available = fields.Float(
        string='Available on product',
        compute='_compute_product_available',
        readonly=True)
    incoming_qty = fields.Float(
        string='Incoming on product',
        compute='_compute_product_available',
        readonly=True)
    outgoing_qty = fields.Float(
        string='Outgoing on product',
        compute='_compute_product_available',
        readonly=True)
    virtual_available = fields.Float(
        string='Virtual available on product',
        compute='_compute_product_available',
        readonly=True)

    @api.multi
    def redisplay(self):
        """Redisplay wizard screen."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.available.explain',
            'res_id': self.id,
            'target': 'current',
            'nodestroy': True,
            'view_type': 'form',
            'view_mode': 'form'}

    @api.multi
    def process(self):
        self.ensure_one()
        self.write({'state': 'show'})
        return self.redisplay()

    @api.multi
    def reset(self):
        self.ensure_one()
        self.write({'state': 'select'})
        return self.redisplay()
