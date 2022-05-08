from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    # Validating and setting defaults
    validators=[
        Validator("REQUEST_KEY", is_type_of=str, must_exist=True),
        Validator("POLLING_INTERVAL_SECONDS", is_type_of=int, default=5),
        Validator("BOX_ADDRESS", is_type_of=str, default="192.168.1.1"),
        Validator("EXPORTER_PORT", is_type_of=int, default=9877),
        Validator("EXPORTER_ADDRESS", is_type_of=str, default="0.0.0.0"),
    ],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
