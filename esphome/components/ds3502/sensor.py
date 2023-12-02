import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, output
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    STATE_CLASS_MEASUREMENT,
)

CODEOWNERS = ["@Archer36"]
DEPENDENCIES = ["i2c"]

ds3502_ns = cg.esphome_ns.namespace("ds3502")
DS3502Component = ds3502_ns.class_(
    "DS3502Component", cg.PollingComponent, i2c.I2CDevice
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

    if CONF_INITIAL_VALUE in config:
        sens = await sensor.new_sensor(config[CONF_INITIAL_VALUE])
        cg.add(var.set_initial_value(sens))

    if CONF_WIPER_VALUE in config:
        conf = config[CONF_WIPER_VALUE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_wiper_value(sens))
