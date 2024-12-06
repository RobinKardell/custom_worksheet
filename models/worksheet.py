from odoo import models, fields, api
from odoo.exceptions import UserError

class Worksheet(models.Model):
    _name = 'custom.worksheet'
    _description = 'Custom Worksheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, default="New", tracking=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    contact_id = fields.Many2one(
        'res.partner', 
        string="Contact Person", 
        domain="[('parent_id', '=', customer_id)]", 
        help="Specific contact person for this worksheet."
    )
    place = fields.Char(string="Place", help="Location of the worksheet.")
    product_id = fields.Many2one('product.product', string="Product/Item", required=True)
    quantity = fields.Integer(string="Quantity", required=True, default=1)
    status_id = fields.Many2one(
        'custom.worksheet.status', 
        string="Status", 
        required=True, 
        tracking=True,
        help="Current status of the worksheet."
    )
    note = fields.Text(string="Notes")
    create_date = fields.Datetime(string="Created On", readonly=True)

    def generate_service_report(self):
        """
        Generate a PDF report for the worksheet.
        """
        return self.env.ref('custom_worksheet.report_service_worksheet').report_action(self)
