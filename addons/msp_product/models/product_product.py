from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Allow editing template gallery even when the variant form is opened.
    x_msp_image_ids = fields.One2many(
        related="product_tmpl_id.x_msp_image_ids",
        readonly=False,
        string="Gallery Images",
    )
    x_msp_gallery_attachment_ids = fields.Many2many(
        related="product_tmpl_id.x_msp_gallery_attachment_ids",
        readonly=False,
        string="Gallery Images (Upload)",
    )
