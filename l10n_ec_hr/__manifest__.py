{
    "name": "Ecuador - HR Base",
    "summary": """Payroll Ecuador""",
    "author": "NextGen S.A.",
    "website": "https://nextgen.ec",
    "category": "Payroll",
    "version": "18.0.0.0.0",
    "depends": [
        "hr",  # ok
        "base_vat",  # ok
        "hr_contract",  # ok
        "hr_contract_reference",  # Ok
        "hr_employee_age",  # OK
        "hr_employee_relative",  # OK
        "hr_employee_lastnames",  # OK
        "l10n_ec_base",  # ok
    ],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "data/hr_relative.xml",
        "data/hr.contract.type.csv",
        "data/hr_contract_finish.xml",
        "data/disability_type.xml",
        "data/hr.sectorial.code.csv",
        "views/hr_employee.xml",
        "views/hr_contract.xml",
        "views/hr_contract_type.xml",
        "views/hr_sectorial_code.xml",
        "views/view_hr_job_form.xml",
        "views/hr_contract_finish_reason.xml",
        "wizards/hr_contract_finish.xml",
        "wizards/hr_contract_update.xml",
    ],
    "installable": True,
    "auto_install": False,
}
