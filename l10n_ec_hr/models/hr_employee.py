from datetime import timedelta

from dateutil.relativedelta import relativedelta
from stdnum.ec import ci

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    disability = fields.Boolean()
    conadis_id = fields.Char("CONADIS No")
    disability_type_id = fields.Many2one("hr.disability.type", string="Disability Type")
    disability_percent = fields.Float()
    catastrophic_illness = fields.Boolean(default=False)
    sectorial_code = fields.Many2one("hr.sectorial.code")
    section = fields.Selection(
        selection=[
            ("administrative", "Administrativo"),
            ("operative", "Operativo"),
        ],
        required=False,
    )

    work_period_ids = fields.One2many(
        "hr.employee.work.period", "employee_id", string="Work Periods"
    )
    state = fields.Selection(
        [("active", _("Active")), ("inactive", _("Inactive"))],
        string="Employee Status",
        default="active",
    )
    certificate = fields.Selection(
        selection_add=[
            ("tercer_nivel", "Tercer Nivel"),
            ("bachiller", "Bachiller"),
            ("bachiller_tecnico", "Bachiller Técnico"),
            ("universitario", "Universitario"),
            ("primaria", "Primaria"),
        ],
        ondelete={
            "tercer_nivel": "cascade",
            "bachiller_tecnico": "cascade",
            "bachiller": "cascade",
            "universitario": "cascade",
            "primaria": "cascade",
        },
    )
    job_id = fields.Many2one("hr.job", domain=lambda self: self._compute_job_domain())

    @api.depends("department_id")
    def _compute_job_domain(self):
        for employee in self:
            domain = []
            if employee.department_id:
                domain = [("department_id", "=", employee.department_id.id)]
            return {"domain": {"job_id": domain}}

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     context = self._context or {}
    #     states = ["active"]
    #     if context.get("show_fired", False):
    #         states.append("inactive")
    #     args += [("state", "in", states)]
    #     return super(HrEmployee, self).search(
    #         args, offset=offset, limit=limit, order=order, count=count
    #     )

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if not res.get("country_id", False):
            res["country_id"] = self.env.company.country_id.id
        return res

    def check_vat_ec(self, vat):
        if len(vat) == 10:
            return ci.is_valid(vat), "Cedula"
        elif len(vat) == 13:
            valid = False
            type_doc = ""
            return valid, type_doc
        else:
            return False, False

    @api.constrains("identification_id", "country_id", "address_id")
    def check_vat(self):
        if self.sudo().env.ref("base.module_base_vat").state == "installed":
            if self.country_id == self.env.ref("base.ec"):
                if not self.identification_id:
                    raise UserError(
                        _(
                            "The Identification Number is required with "
                            "the Ecuadorian format \n "
                            "it must be like this form 0953865188, "
                            "must be 10 digits"
                        )
                    )
                if self.identification_id:
                    valid, vat_type = self.check_vat_ec(self.identification_id)
                    if not valid:
                        raise UserError(
                            _(
                                "The Identification Number %s is not valid"
                                " with the Ecuadorian format \n "
                                "it must be like this form "
                                "0953865188, must be 10 digits"
                            )
                            % self.identification_id
                        )
                # self.set_address_home(self)
            return True
        else:
            return True

    # address_home_id
    # @api.model
    # def set_address_home(self, employee_id):
    #     if not employee_id.address_home_id:
    #         partner_obj = self.env["res.partner"]
    #         partner_id = partner_obj.search(
    #             [("vat", "=", employee_id.identification_id)]
    #         )
    #         if not partner_id:
    #             partner_id = partner_obj.create(
    #                 {
    #                     "name": employee_id.name,
    #                     "l10n_latam_identification_type_id": self.env.ref(
    #                         "l10n_ec_base.ec_dni"
    #                     ).id,
    #                     "vat": employee_id.identification_id,
    #                     "country_id": employee_id.country_id.id,
    #                 }
    #             )
    #         if partner_id:
    #             self.address_home_id = partner_id.id
    #     return True


class HrDisabilityType(models.Model):
    _name = "hr.disability.type"
    _description = __doc__

    name = fields.Char(required=True)


class HrEmployeeContract(models.Model):
    """Employee work periods"""

    _name = "hr.employee.work.period"
    _order = "date_start"
    _description = __doc__

    period_type = fields.Selection(
        [("past", _("Past")), ("current", _("Current"))],
        string="Type",
        default="past",
    )
    employee_id = fields.Many2one("hr.employee", string="Employee")
    contract_id = fields.Many2one("hr.contract", string="Contract")
    contract_type_id = fields.Many2one(
        comodel_name="hr.contract.type",
        string="Type",
        related="contract_id.contract_type_id",
        store=True,
    )
    date_start = fields.Date("From")
    date_end = fields.Date(
        string="To",
        help="Final date of the contract or of the last registered payroll",
    )
    number_of_days_reserve_funds = fields.Integer(
        "Days (Reserve funds)", compute="_compute_get_duration", store=True
    )
    number_of_days = fields.Integer(
        "Days (Calendar)", compute="_compute_get_duration", store=True
    )
    number_of_years = fields.Integer(
        "Number of Years", compute="_compute_get_duration", store=True
    )

    @api.depends("date_start", "date_end")
    def _compute_get_duration(self):
        for row in self:
            if row.date_start and row.date_end:
                date_start = row.date_start
                date_end = row.date_end + timedelta(days=1)
                delta = date_end - date_start
                relative = relativedelta(date_end, date_start)
                if relative:
                    total = 0
                    if relative.days:
                        total += relative.days + 1
                    if relative.months:
                        total += relative.months * 30  # TODO Configurable?
                    if relative.years:
                        total += relative.years * 12 * 30  # TODO Configurable?
                    row.number_of_days_reserve_funds = total
                if delta:
                    row.number_of_days = delta.days
                    row.number_of_years = relativedelta(
                        row.date_end, row.date_start
                    ).years
        return True

    @api.model
    def get_antiquity_days(self, employee, date_to=fields.Date.today()):
        days = 0.0
        for work in employee.work_period_ids.filtered(
            lambda x: x.period_type == "past"
        ):
            if work.contract_type_id and work.contract_type_id.antiquity:
                days += work.number_of_days_reserve_funds
            if not work.contract_type_id:
                days += work.number_of_days_reserve_funds
        for row in employee.work_period_ids.filtered(
            lambda x: x.period_type == "current"
        ):
            period = False
            if row.contract_type_id and row.contract_type_id.antiquity:
                period = row
            if not row.contract_type_id:
                period = row
            if period:
                date_start = period.date_start
                date_end = date_to
                date_end += timedelta(days=1)
                relative = relativedelta(date_end, date_start)
                if relative and relative.days:
                    days += relative.days
                if relative and relative.months:
                    days += relative.months * 30
                if relative and relative.years:
                    days += relative.years * 12 * 30
        return days


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    state = fields.Selection(
        [("active", "Active"), ("inactive", "Inactive")],
        string="Employee Status",
        default="active",
    )
