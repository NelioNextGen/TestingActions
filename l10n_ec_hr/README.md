# Ecuador - HR Base

## Resumen

Este módulo proporciona características adicionales para la nómina de Ecuador, incluyendo:

- Registro de discapacidad y enfermedades catastróficas de los empleados
- Registro de familiares a cargo del empleado
- Cálculo de antigüedad laboral
- Registro de tipos de contrato y códigos sectoriales
- Seguimiento de cambios en el puesto de trabajo y salario de los empleados

## Instalación

Este módulo depende de los siguientes módulos de Odoo:

- `hr`
- `base_vat`
- `hr_contract`
- `hr_contract_reference`
- `hr_employee_age`
- `hr_employee_relative`
- `hr_employee_lastnames`
- `l10n_ec_base`

Asegúrate de tener instalados estos módulos antes de instalar el módulo "Ecuador - HR Base".

## Configuración

El módulo no requiere configuración adicional, pero tiene algunos parámetros en los modelos que empiezan con `res.`:

- `hr.employee.relative`: Aquí se definen los tipos de familiares y si se requiere o no la fecha de nacimiento y/o fecha de matrimonio.
- `hr.contract.type`: Aquí se definen los tipos de contrato, si son de antigüedad o de pasantía.
- `hr.sectorial.code`: Aquí se definen los códigos sectoriales utilizados para la nómina.

## Uso y Ejemplos

1. **Registro de discapacidad y enfermedades catastróficas de los empleados:**

   - En la ficha del empleado, se pueden registrar los datos de discapacidad y enfermedades catastróficas.

2. **Registro de familiares a cargo del empleado:**

   - En la ficha del empleado, se pueden registrar los datos de los familiares a cargo, incluyendo si tienen discapacidad o son una carga familiar.

3. **Cálculo de antigüedad laboral:**

   - El módulo calcula automáticamente la antigüedad laboral de los empleados en base a los períodos de trabajo registrados.

4. **Registro de tipos de contrato y códigos sectoriales:**

   - Los tipos de contrato y los códigos sectoriales se pueden configurar en el menú de Recursos Humanos.

5. **Seguimiento de cambios en el puesto de trabajo y salario de los empleados:**
   - Cuando se realiza un cambio en el puesto de trabajo o el salario de un empleado, el módulo registra el historial de estos cambios.

## Licencia

Este módulo se distribuye bajo la Licencia Pública General Affero de GNU v3.0 (AGPL-3.0).
