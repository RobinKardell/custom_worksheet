from odoo import models, fields, api

class CustomWorksheet(models.Model):
    _name = 'custom.worksheet'  # Namnet på modellen
    _description = 'Custom Worksheet'  # Beskrivning av modellen

    # Fält för Worksheet
    name = fields.Char(string="Worksheet Name", required=True)
    description = fields.Text(string="Description")

    # Customer relation (many2one till res.partner)
    customer_id = fields.Many2one(
        'res.partner',  # Relationen till modellen res.partner (kund)
        string="Customer",  # Etiketten på fältet
        ondelete='restrict'  # Förhindrar borttagning av relaterade kundposter
    )

    # Status relation (many2one till custom_worksheet_status)
    status_id = fields.Many2one(
        'custom.worksheet.status',  # Relationen till modellen custom_worksheet_status
        string="Status",  # Etiketten på fältet
        ondelete='restrict'  # Förhindrar borttagning av relaterade statusar
    )

    # Andra fält och funktioner som kan vara relevanta för modellen
    created_at = fields.Datetime('Created At', default=fields.Datetime.now)
    updated_at = fields.Datetime('Updated At')

    # Action: Automatiskt uppdatera updated_at när posten ändras
    @api.model
    def create(self, values):
        # Ställ in default för 'created_at'
        if not values.get('created_at'):
            values['created_at'] = fields.Datetime.now()
        return super(CustomWorksheet, self).create(values)

    def write(self, values):
        # Uppdatera 'updated_at' när posten ändras
        if 'customer_id' in values or 'status_id' in values:
            values['updated_at'] = fields.Datetime.now()
        return super(CustomWorksheet, self).write(values)

    # Exempel på en metod för att få ett fullständigt namn för worksheetet
    def get_full_name(self):
        for record in self:
            return f"{record.name} - {record.customer_id.name}"

    # För att kontrollera om det finns relaterade statusar eller kunder
    def check_related_records(self):
        for record in self:
            # Exempel på kontroll av relaterade objekt, du kan lägga till egen logik här
            if not record.status_id:
                raise ValueError("Status is missing for worksheet")
            if not record.customer_id:
                raise ValueError("Customer is missing for worksheet")
        return True
