#!/usr/bin/env python
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class L10nLatamIdentificationType(models.Model):
    _inherit = "l10n_latam.identification.type"

    l10n_ec_tpidprov = fields.Char(string="Type Supplier", size=2)
    l10n_ec_tpidcliente = fields.Char(string="Type Customer", size=2)
    l10n_ec_tipoidinformante = fields.Char(string="Type ID Informant", size=1)
    l10n_ec_tpidclienteex = fields.Char(string="Type ID Exports", size=2)
