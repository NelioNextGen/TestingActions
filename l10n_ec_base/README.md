# Ecuador - Base

## Descripción general del módulo

Este módulo de Odoo proporciona la localización base para Ecuador. Incluye:

- Tipos de identificación y validación de números de identificación para Ecuador.
- Posiciones fiscales y bancos predefinidos para Ecuador.
- Validaciones y funcionalidades adicionales para socios y cuentas bancarias relacionadas con Ecuador.

## Instalación

Para instalar este módulo, sigue estos pasos:

1. Asegúrate de tener instalados los módulos dependientes: `account`, `l10n_latam_invoice_document`, `l10n_latam_base`,
   `partner_email_check`, `partner_email_duplicate_warn` y `partner_manual_rank`.
2. Instala el módulo `l10n_ec_base` a través del módulo de aplicaciones de Odoo.

## Configuración

Este módulo no requiere configuración adicional, a menos que necesites establecer la siguiente información:

- **Tipo de identificación de la compañía**: Puedes configurar el tipo de identificación de la compañía en la
  configuración de la empresa.
- **Posición fiscal de la compañía**: Puedes configurar la posición fiscal de la compañía en la configuración de la
  empresa.

## Uso y ejemplos

Una vez instalado el módulo, podrás:

1. Crear nuevos socios con tipos de identificación y números de identificación válidos para Ecuador.
2. Crear cuentas bancarias para socios con los tipos de cuenta bancaria y números de identificación correspondientes.
3. Utilizar las posiciones fiscales y bancos predefinidos en las facturas y otros documentos relacionados.

## Licencia

Este módulo se distribuye bajo la licencia AGPL-3.
