# -*- coding: utf-8 -*-
import base64
import io
import math

from barcode import Code128

from odoo import api, models, fields
from odoo.tools import barcode
from barcode.writer import ImageWriter

class ProductProduct(models.Model):
    """Inherit product_product model for adding EAN13 Standard Barcode"""
    _inherit = 'product.product'

    barcode_image = fields.Binary("Barcode", compute='_compute_barcode_image', store=True)

    @api.model
    def create(self, vals):
        """Function to add EAN13 Standard barcode at the time
        create new product"""
        res = super(ProductProduct, self).create(vals)
        ean = generate_ean(str(res.id))
        res.barcode = '21' + ean[2:]
        return res

    @api.depends('barcode')
    def _compute_barcode_image(self):
        for product in self:
            if product.barcode:
                barcode = product.barcode
                # Generate the barcode image using Odoo's built-in tools
                barcode_image = self._generate_barcode_image(barcode)
                product.barcode_image = barcode_image
            else:
                product.barcode = ''

    def _generate_barcode_image(self, barcode):
        barcode_obj = Code128(barcode, writer=ImageWriter())
        buffer = io.BytesIO()
        barcode_obj.write(buffer)
        barcode_image = base64.b64encode(buffer.getvalue())
        return barcode_image

    def action_barcode_generator(self):
        for rec in self:
            ean = generate_ean(str(rec.id))
            rec.barcode = '21' + ean[2:]


def ean_checksum(eancode):
    """Returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    odd_sum = 0
    even_sum = 0
    for rec in range(len(eancode[::-1][1:])):
        if rec % 2 == 0:
            odd_sum += int(eancode[::-1][1:][rec])
        else:
            even_sum += int(eancode[::-1][1:][rec])
    total = (odd_sum * 3) + even_sum
    return int(10 - math.ceil(total % 10.0)) % 10


def check_ean(eancode):
    """Returns True if ean code is a valid ean13 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode)


def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    product_identifier = '00000000000' + ean
    ean = product_identifier[-11:]
    check_number = check_ean(ean + '00')
    return f'{ean}0{check_number}'
