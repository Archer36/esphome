import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor, number
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_STEP,
    STATE_CLASS_MEASUREMENT,
)

CONF_WIPER_VALUE = "wiper_value"

CODEOWNERS = ["@Archer36"]
DEPENDENCIES = ["i2c"]

ds3502_ns = cg.esphome_ns.namespace("ds3502")
DS3502Component = ds3502_ns.class_(
    "DS3502Component", cg.PollingComponent, number.Number i2c.I2CDevice
)

def validate_min_max(config):
    if config[CONF_MAX_VALUE] <= config[CONF_MIN_VALUE]:
        raise cv.Invalid("max_value must be greater than min_value")
    if config[CONF_MIN_VALUE] < 1:
        raise cv.Invalid("max_value must be greater than 0")
    if config[CONF_MAX_VALUE] > 126:
        raise cv.Invalid("max_value must not be greater than 126")
    return config


CONFIG_SCHEMA = cv.All(
    number.number_schema(DS3502Component)
    .extend(cv.polling_component_schema("60s"))
    .extend(i2c.i2c_device_schema(0x28))
    .extend(
        {
            cv.Optional(CONF_VALUE_TYPE, default="U_WORD"): cv.enum(SENSOR_VALUE_TYPE),
            cv.Optional(CONF_WRITE_LAMBDA): cv.returning_lambda,
            cv.Optional(CONF_MAX_VALUE, default=126): cv.positive_int,
            cv.Optional(CONF_MIN_VALUE, default=1): cv.positive_int,
            cv.Optional(CONF_STEP, default=1): cv.positive_int,
        }
    ),
    validate_min_max,
)


CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(DS3502Component),
            cv.Optional(CONF_INITIAL_VALUE, default=1): cv.int_range(
                min=1, max=126
            ),
            cv.Optional(CONF_WIPER_VALUE): sensor.sensor_schema(
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(i2c.i2c_device_schema(0x28))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    cg.add(var.set_initial_value(config[CONF_INITIAL_VALUE]))

    if CONF_WIPER_VALUE in config:
        conf = config[CONF_WIPER_VALUE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_wiper_value(sens))
