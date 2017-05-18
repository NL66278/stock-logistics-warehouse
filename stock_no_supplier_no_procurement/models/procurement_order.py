# -*- coding: utf-8 -*-
# © 2017 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models, registry, _
from openerp.exceptions import Warning as UserError


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def create(self, vals):
        """Supress creation of procurement for orderpoint without supplier."""
        orderpoint_id = vals.get('orderpoint_id', False)
        if orderpoint_id:
            orderpoint_model = self.env['stock.warehouse.orderpoint']
            op = orderpoint_model.browse(orderpoint_id)
            op_template = op.product_id.product_tmpl_id
            if not op_template.seller_ids:
                if not op_template.missing_supplier:
                    # We have to mark product template using a separate cursor,
                    # else our change will rollback with the rest of the
                    # transaction, and we do not want to commit current tx:
                    template_cr = registry(self.env.cr.dbname).cursor()
                    template = op_template.with_env(self.env(cr=template_cr))
                    template.write({'missing_supplier': True})
                    template_cr.commit()
                    template_cr.close()
                raise UserError(
                    _('Product %s missing supplier') %
                    op_template.display_name
                )
        return super(ProcurementOrder, self).create(vals)
