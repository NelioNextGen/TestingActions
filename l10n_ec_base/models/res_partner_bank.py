# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    _ACCOUNT_TYPE = [
        ("savings", "Savings Account"),
        ("checking", "Checking Account"),
        ("credit_card", "Credit Card"),
        ("virtual", "Virtual"),
    ]

    l10n_ec_account_type = fields.Selection(
        _ACCOUNT_TYPE,
        string="Account Type",
        default="checking",
        help="Select here the type of account (savings or checking)",
    )
    country_id = fields.Many2one(
        comodel_name="res.country", related="partner_id.country_id", store=True
    )
    l10n_latam_identification_type_id = fields.Many2one(
        "l10n_latam.identification.type",
        string="Identification Type",
        index="btree_not_null",
        auto_join=True,
        help="The type of identification",
    )
    vat = fields.Char(
        string="Identification Number", help="Identification Number for selected type"
    )

    @api.constrains(
        "vat", "l10n_latam_identification_type_id", "country_id", "partner_id"
    )
    def check_vat(self):
        partner_obj = self.env["res.partner"]
        ecuadorian_partners = self.filtered(
            lambda x: x.partner_id.country_id == self.env.ref("base.ec") and x.vat
        )
        for row in ecuadorian_partners:
            msg = partner_obj.l10n_ec_check_vat(
                row.partner_id, row.l10n_latam_identification_type_id, row.vat
            )
            if row.vat and not row.l10n_latam_identification_type_id:
                msg += _("You have to select the type of identification!")
            if msg:
                raise ValidationError(msg)
        return True

    @api.model
    def _get_supported_account_types(self):
        rslt = super()._get_supported_account_types()
        rslt.append(("savings", _("Savings Account")))
        rslt.append(("checking", _("Checking Account")))
        rslt.append(("credit_card", _("Credit Card")))
        return rslt

    @api.depends("acc_number")
    def _compute_acc_type(self):
        for bank in self:
            if bank.company_id.country_code == "EC":
                bank.acc_type = bank.l10n_ec_account_type
            else:
                super()._compute_acc_type()
