from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def button_confirm(self):
        for order in self:
            if not order.order_line:
                raise ValidationError(_("Please Select At Least One Product in the Order Lines."))
            for line in order.order_line:
                if line.price_unit <= 0:
                    raise ValidationError(_("Please Enter a Price Greater than 0 for All Order Lines Before Confirming the Order."))
        return super(InheritPurchaseOrder, self).button_confirm()