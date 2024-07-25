from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        for order in self:
            for line in order.order_line:
                if line.price_unit <= 0:
                    raise ValidationError(
                        _("Please Enter a Price Greater than Zero for All Order Lines Before Confirming the Order."))
        return super(InheritPurchaseOrder, self).button_confirm()