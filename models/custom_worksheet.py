from odoo import models, fields, api

class CustomWorksheet(models.Model):
    _name = 'custom.worksheet'
    _description = 'Custom Worksheet'

    name = fields.Char(string='Worksheet Name', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_ids = fields.One2many('custom.worksheet.product', 'worksheet_id', string='Products')
    status_id = fields.Many2one('custom.worksheet.status', string='Status', required=True)
    date_created = fields.Datetime(string='Creation Date', default=fields.Datetime.now)

class CustomWorksheetStatus(models.Model):
    _name = 'custom.worksheet.status'
    _description = 'Custom Worksheet Status'

    name = fields.Char(string='Status', required=True)

class CustomWorksheetProduct(models.Model):
    _name = 'custom.worksheet.product'
    _description = 'Product in Custom Worksheet'

    worksheet_id = fields.Many2one('custom.worksheet', string='Worksheet', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1)
    price_unit = fields.Float(string='Unit Price', related='product_id.lst_price', readonly=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.price_unit
