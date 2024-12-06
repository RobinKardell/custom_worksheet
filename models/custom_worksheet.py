from odoo import models, fields, api

class CustomWorksheet(models.Model):
    _name = 'custom.worksheet'
    _description = 'Custom Worksheet'

    name = fields.Char(string='Worksheet Name', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    product_ids = fields.One2many('custom.worksheet.product', 'worksheet_id', string='Products')
    status_id = fields.Many2one('custom.worksheet.status', string='Status', required=True)
    date_created = fields.Datetime(string='Creation Date', default=fields.Datetime.now)

    @api.model
    def create(self, values):
        # Rensa felaktiga relationer vid skapande
        if 'customer_id' in values:
            customer_id = values.get('customer_id')
            if customer_id:
                customer = self.env['res.partner'].browse(customer_id)
                if not customer.exists():
                    values['customer_id'] = None

        if 'status_id' in values:
            status_id = values.get('status_id')
            if status_id:
                status = self.env['custom.worksheet.status'].browse(status_id)
                if not status.exists():
                    values['status_id'] = None

        return super(CustomWorksheet, self).create(values)

    def write(self, values):
        # Rensa felaktiga relationer vid uppdatering
        if 'customer_id' in values:
            customer_id = values.get('customer_id')
            if customer_id:
                # Kontrollera om kundposten existerar
                customer = self.env['res.partner'].browse(customer_id)
                if not customer.exists():  # Om posten inte finns, sätt till None
                    values['customer_id'] = None

        if 'status_id' in values:
            status_id = values.get('status_id')
            if status_id:
                # Kontrollera om statusposten existerar
                status = self.env['custom.worksheet.status'].browse(status_id)
                if not status.exists():  # Om posten inte finns, sätt till None
                    values['status_id'] = None

        return super(CustomWorksheet, self).write(values)


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
