from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_msp_mpn = fields.Char(string="MPN", tracking=True)
    x_msp_brand = fields.Char(string="Brand", tracking=True)
    x_msp_supplier_sku = fields.Char(string="Supplier SKU", tracking=True)
    x_msp_is_serialized = fields.Boolean(string="Serialized", tracking=True)
    x_msp_is_recurring = fields.Boolean(string="Recurring", tracking=True)
    x_msp_is_recommended = fields.Boolean(string="Recommended", tracking=True)
    x_msp_gallery_attachment_ids = fields.Many2many(
        "ir.attachment",
        "msp_product_tmpl_attachment_rel",
        "product_tmpl_id",
        "attachment_id",
        string="Gallery Images (Upload)",
        domain=[("mimetype", "ilike", "image/")],
    )
    x_msp_image_ids = fields.One2many("msp.product.image", "product_tmpl_id", string="Gallery Images")
    x_msp_margin_pct = fields.Float(string="Margin %", compute="_compute_msp_metrics", store=True)
    x_msp_profit = fields.Float(string="Profit", compute="_compute_msp_metrics", store=True)

    @api.onchange("x_msp_gallery_attachment_ids")
    def _onchange_gallery_sync_main_image(self):
        self._sync_main_image_from_gallery()

    def _sync_main_image_from_gallery(self):
        for template in self:
            first_image = template.x_msp_gallery_attachment_ids[:1]
            if first_image and first_image.datas:
                template.image_1920 = first_image.datas

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_main_image_from_gallery()
        return records

    def write(self, vals):
        result = super().write(vals)
        if "x_msp_gallery_attachment_ids" in vals and "image_1920" not in vals:
            self._sync_main_image_from_gallery()
        return result

    @api.depends("list_price", "standard_price")
    def _compute_msp_metrics(self):
        for template in self:
            profit = template.list_price - template.standard_price
            template.x_msp_profit = profit
            if template.list_price:
                template.x_msp_margin_pct = (profit / template.list_price) * 100
            else:
                template.x_msp_margin_pct = 0.0
