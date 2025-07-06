from . import models


def _pre_init_update(env):
    # UPDATE ALL L10N_LATAM_IDENTIFICATION_TYPE RECORDS IN ACTIVE STATE FALSE
    env.cr.execute(
        """
	UPDATE l10n_latam_identification_type
	   SET active = FALSE
	 WHERE active = TRUE
    """
    )
