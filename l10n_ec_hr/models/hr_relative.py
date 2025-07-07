#!/usr/bin/env python
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrEmployeeRelative(models.Model):
    _inherit = "hr.employee.relative"

    family_burden = fields.Boolean(string="Family burden")
    identification_id = fields.Char(string="Identification")
    disability = fields.Boolean()
    conadis_id = fields.Char("CONADIS")
    disability_type_id = fields.Many2one("hr.disability.type", "Disability Type")
    disability_percent = fields.Float()
    required_date_of_birth = fields.Boolean(
        "Required Date of Birth",
        related="relation_id.birthday_required",
        store=True,
    )
    required_date_of_marriage = fields.Boolean(
        "Required Date of Marriage",
        related="relation_id.marriage_date_required",
        store=True,
    )
    date_of_marriage = fields.Date(string="Date of Marriage")
    years = fields.Float("Years of Marriage", compute="_compute_marriage")

    @api.depends("date_of_marriage")
    def _compute_marriage(self):
        for row in self:
            marriage = relativedelta(datetime.now(), row.date_of_marriage)
            row.years = marriage.years + (marriage.months / 12)
        return True

    @api.constrains("relation_id", "date_of_birth", "date_of_marriage")
    def _check_date(self):
        for row in self:
            if row.relation_id.birthday_required and not row.date_of_birth:
                raise ValidationError(
                    _(
                        f"The date of birth is required for "
                        f"this type of relative {row.relation_id.name}"
                    )
                )
            if row.relation_id.marriage_date_required and not row.date_of_marriage:
                raise ValidationError(
                    _(
                        f"The date of marriage is required for "
                        f"this type of relative {row.relation_id.name}"
                    )
                )

    @api.model
    def get_charges(self, employee=None, date_to=None):
        child = self.env.ref("hr_employee_relative.relation_child")
        spouse = self.env.ref("hr_employee_relative.relation_spouse")
        family_charges = 0
        for fml in employee.relative_ids.filtered(
            lambda x: x.disability or x.family_burden
        ):
            if (
                fml.relation_id == child
                and fml.date_of_birth <= date_to
                and not fml.disability
                and fml.age_year <= 21
            ):
                family_charges += 1
            if fml.relation_id == spouse and fml.date_of_marriage <= date_to:
                family_charges += 1
            if fml.relation_id not in (spouse, child) and fml.family_burden:
                family_charges += 1
            if fml.relation_id == child and fml.age_year > 21 and fml.disability:
                family_charges += 1
            if employee.catastrophic_illness or family_charges > 5:
                family_charges = 5
        return family_charges


class HrEmployeeRelativeRelation(models.Model):
    _inherit = "hr.employee.relative.relation"

    birthday_required = fields.Boolean()
    marriage_date_required = fields.Boolean()
