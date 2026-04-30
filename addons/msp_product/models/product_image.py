from odoo import fields, models


class MspProductImage(models.Model):
    _name = "msp.product.image"
    _description = "MSP Product Image"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char()
    product_tmpl_id = fields.Many2one("product.template", required=True, ondelete="cascade")
    image_1920 = fields.Image(string="Image", required=True, attachment=True)
    active = fields.Boolean(default=True)
