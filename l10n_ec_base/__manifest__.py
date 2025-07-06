{
    "name": "Ecuador - Base",
    "version": "18.0.1.0.1",
    "summary": "Localizacion Ecuador Base",
    "category": "Account",
    "author": "NextGen S.A.",
    "website": "https://nextgen.ec",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_latam_invoice_document",
        "l10n_latam_base",
        "partner_email_check",
        "partner_email_duplicate_warn",
        "partner_manual_rank",
    ],
    "data": [
        # Data
        "data/l10n_latam_identification_type_data.xml",
        "data/account.fiscal.position.csv",
        "data/res_bank.xml",
        # "data/res_partner_data.xml",
        # Views
        "views/l10n_latam_identification_type.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "views/res_partner_bank_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "pre_init_hook": "_pre_init_update",
}
