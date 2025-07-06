from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Se cambia al l10n_ec_sri_base y ahi va en el res config setting de contabilidad
    l10n_latam_identification_type_id = fields.Many2one(
        "l10n_latam.identification.type",
        string="Identification Type",
        index=True,
        auto_join=True,
        inverse="_inverse_typepayer",
        default=lambda self: self.env.ref(
            "l10n_latam_base.it_vat", raise_if_not_found=False
        ),
        help="The type of identification",
    )
    vat = fields.Char(
        string="Identification Number", help="Identification Number for selected type"
    )
    property_account_position_id = fields.Many2one(
        "account.fiscal.position",
        string="Fiscal Position",
        related="partner_id.property_account_position_id",
        domain="[('company_id', '=', current_company_id)]",
        inverse="_inverse_taxpayer",
        readonly=False,
        help="The fiscal position determines the taxes/accounts used for this contact.",
    )

    def _inverse_typepayer(self):
        for company in self:
            company.partner_id.l10n_latam_identification_type_id = (
                company.l10n_latam_identification_type_id
            )

    @api.onchange("country_id")
    def _onchange_country(self):
        country = (
            self.country_id
            or self.account_fiscal_country_id
            or self.env.company.account_fiscal_country_id
        )
        identification_type = self.l10n_latam_identification_type_id
        if not identification_type or (identification_type.country_id != country):
            self.l10n_latam_identification_type_id = self.env[
                "l10n_latam.identification.type"
            ].search(
                [("country_id", "=", country.id), ("is_vat", "=", True)], limit=1
            ) or self.env.ref("l10n_ec_base.ec_passport", raise_if_not_found=False)
