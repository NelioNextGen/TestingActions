from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


def verify_final_consumer(vat):
    return vat == "9" * 13  # final consumer is identified with 9999999999999


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _default_country_id(self):
        country = self.env["res.country"].search([("code", "=ilike", "EC")])
        return country

    country_id = fields.Many2one(default=_default_country_id, string="Country")

    @api.model
    def l10n_ec_check_vat(self, partner, l10n_latam_identification, vat):
        msg = ""
        it_ruc = self.env.ref("l10n_ec_base.ec_ruc", False)
        it_dni = self.env.ref("l10n_ec_base.ec_dni", False)
        it_final = self.env.ref("l10n_ec_base.ec_final", False)
        if partner.vat:
            if (
                l10n_latam_identification.id
                in (
                    it_ruc.id,
                    it_dni.id,
                )
                and partner.type == "contact"
            ):
                if l10n_latam_identification.id == it_dni.id and len(vat) != 10:
                    msg += (
                        _("If your identification type is %s, it must be 10 digits \n")
                        % it_dni.display_name
                    )
                if l10n_latam_identification.id == it_ruc.id and len(vat) != 13:
                    msg += (
                        _("If your identification type is %s, it must be 13 digits \n")
                        % it_ruc.display_name
                    )
                parent = partner
                while parent.parent_id:
                    parent = parent.parent_id

                vat_partners = self.search(
                    [
                        ("vat", "=", vat),
                        ("vat", "!=", False),
                        ("company_id", "=", partner.company_id.id),
                    ]
                )
                if vat_partners:
                    partners = self.search(
                        [
                            ("id", "child_of", parent.id),
                            ("company_id", "=", partner.company_id.id),
                        ]
                    )
                    vat_partners = self.search(
                        [
                            ("id", "in", vat_partners.ids),
                            ("id", "not in", partners.ids),
                            ("company_id", "=", partner.company_id.id),
                        ]
                    )
                    if vat_partners:
                        msg += _(
                            "Partner vat must be unique per company except on partner "
                            "with parent/childe relationship. Partners with same vat"
                            " and not related, are:\n {}!".format(
                                "\n".join(x.name for x in vat_partners)
                            )
                        )
                        msg += _()
            if l10n_latam_identification == it_final:
                final_consumer = self.search_count(
                    [("l10n_latam_identification_type_id", "=", it_final.id)]
                )
                if final_consumer > 1:
                    msg += _(
                        "You cannot register more than one contact as "
                        "an Final Consumer!"
                    )
        return msg

    @api.constrains(
        "vat", "l10n_latam_identification_type_id", "country_id", "parent_id"
    )
    def check_vat(self):
        ecuadorian_partners = self.filtered(
            lambda x: x.country_id == self.env.ref("base.ec")
        )
        for partner in ecuadorian_partners:
            msg = self.l10n_ec_check_vat(
                partner, partner.l10n_latam_identification_type_id, partner.vat
            )
            if msg:
                raise ValidationError(msg)
        return super(ResPartner, self - ecuadorian_partners).check_vat()

    @api.onchange("country_id")
    def _onchange_country(self):
        country = (
            self.country_id
            or self.company_id.account_fiscal_country_id
            or self.env.company.account_fiscal_country_id
        )
        identification_type = self.l10n_latam_identification_type_id
        if not identification_type or (identification_type.country_id != country):
            self.l10n_latam_identification_type_id = self.env[
                "l10n_latam.identification.type"
            ].search(
                [("country_id", "=", country.id), ("is_vat", "=", True)], limit=1
            ) or self.env.ref("l10n_ec_base.ec_internacional", raise_if_not_found=False)
