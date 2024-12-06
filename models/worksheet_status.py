from odoo import models, fields

class WorksheetStatus(models.Model):
    _name = 'custom.worksheet.status'
    _description = 'Worksheet Status'

    name = fields.Char(string="Status Name", required=True)
    description = fields.Text(string="Description")
