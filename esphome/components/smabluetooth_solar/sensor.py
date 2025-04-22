import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, text_sensor
from esphome.const import (
    CONF_ACTIVE_POWER,
    CONF_CURRENT,
    CONF_FREQUENCY,
    CONF_ID,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    ICON_CURRENT_AC,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_HERTZ,
    UNIT_VOLT,
    UNIT_WATT,
)


from esphome.core import CORE

CONF_PHASE_A = "phase_a"
CONF_PHASE_B = "phase_b"
CONF_PHASE_C = "phase_c"

CONF_ENERGY_PRODUCTION_DAY = "energy_production_day"
CONF_TOTAL_ENERGY_PRODUCTION = "total_energy_production"
CONF_TOTAL_GENERATION_TIME = "total_generation_time"
CONF_TODAY_GENERATION_TIME = "today_generation_time"
CONF_PV1 = "pv1"
CONF_PV2 = "pv2"
UNIT_KILOWATT_HOURS = "kWh"
UNIT_HOURS = "h"
UNIT_KOHM = "kΩ"
UNIT_MILLIAMPERE = "mA"

#CONF_INVERTER_STATUS = "inverter_status"
#CONF_INVERTER_STATUS_CODE = "inverter_status_code"
CONF_PV_ACTIVE_POWER = "pv_active_power"
CONF_INVERTER_MODULE_TEMP = "inverter_module_temp"
CONF_PROTOCOL_VERSION = "protocol_version"

CONF_SMA_INVERTER_BLUETOOTH_MAC = "sma_inverter_bluetooth_mac"
CONF_SMA_INVERTER_PASSWORD = "sma_inverter_password"

#CONF_GRID_RELAY = "grid_relay"
#CONF_GRID_RELAY_CODE = "grid_relay_code"

AUTO_LOAD = ["text_sensor"]
DEPENDENCIES = ["esp32", "sensor", "network"]
CODEOWNERS = ["@keerekeerweere"]


smabluetooth_solar_ns = cg.esphome_ns.namespace("smabluetooth_solar")
SmaBluetoothSolar = smabluetooth_solar_ns.class_(
    "SmaBluetoothSolar", cg.PollingComponent
)

PHASE_SENSORS = {
    CONF_VOLTAGE: sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    CONF_CURRENT: sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    CONF_ACTIVE_POWER: sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}
PV_SENSORS = {
    CONF_VOLTAGE: sensor.sensor_schema(
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=1,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    CONF_CURRENT: sensor.sensor_schema(
        unit_of_measurement=UNIT_AMPERE,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    CONF_ACTIVE_POWER: sensor.sensor_schema(
        unit_of_measurement=UNIT_WATT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}

PHASE_SCHEMA = cv.Schema(
    {cv.Optional(sensor): schema for sensor, schema in PHASE_SENSORS.items()}
)
PV_SCHEMA = cv.Schema(
    {cv.Optional(sensor): schema for sensor, schema in PV_SENSORS.items()}
)

SmaBluetoothProtocolVersion = smabluetooth_solar_ns.enum("SmaBluetoothProtocolVersion")
PROTOCOL_VERSIONS = {
    "SMANET2": SmaBluetoothProtocolVersion.SMANET2
}


CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(SmaBluetoothSolar),
            cv.Required(CONF_SMA_INVERTER_BLUETOOTH_MAC ): cv.string,
            cv.Required(CONF_SMA_INVERTER_PASSWORD): cv.string,

            cv.Optional(CONF_PROTOCOL_VERSION, default="SMANET2"): cv.enum(
                PROTOCOL_VERSIONS, upper=True
            ),
            cv.Optional(CONF_PHASE_A): PHASE_SCHEMA,
            cv.Optional(CONF_PHASE_B): PHASE_SCHEMA,
            cv.Optional(CONF_PHASE_C): PHASE_SCHEMA,
            cv.Optional(CONF_PV1): PV_SCHEMA,
            cv.Optional(CONF_PV2): PV_SCHEMA,
#            cv.Optional(CONF_INVERTER_STATUS_CODE): sensor.sensor_schema(),
#            cv.Optional(CONF_GRID_RELAY_CODE): sensor.sensor_schema(),
            cv.Optional(CONF_INVERTER_STATUS): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_GRID_RELAY): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_FREQUENCY): sensor.sensor_schema(
                unit_of_measurement=UNIT_HERTZ,
                icon=ICON_CURRENT_AC,
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_ACTIVE_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PV_ACTIVE_POWER): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_ENERGY_PRODUCTION_DAY): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TOTAL_ENERGY_PRODUCTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
#            cv.Optional(CONF_INVERTER_MODULE_TEMP): sensor.sensor_schema(
#                unit_of_measurement=UNIT_CELSIUS,
#                accuracy_decimals=1,
#                state_class=STATE_CLASS_MEASUREMENT,
#            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
#    .extend(modbus.modbus_device_schema(0x01))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
#    await modbus.register_modbus_device(var, config)

    cg.add(var.set_sma_inverter_bluetooth_mac(config[CONF_SMA_INVERTER_BLUETOOTH_MAC]))
    cg.add(var.set_sma_inverter_password(config[CONF_SMA_INVERTER_PASSWORD]))

    cg.add(var.set_protocol_version(config[CONF_PROTOCOL_VERSION]))

    if CONF_INVERTER_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_INVERTER_STATUS])
        cg.add(var.set_inverter_status_sensor(sens))

    if CONF_GRID_RELAY in config:
        sens = await text_sensor.new_text_sensor(config[CONF_GRID_RELAY])
        cg.add(var.set_grid_relay_sensor(sens))

    if CONF_INVERTER_STATUS_CODE in config:
        sens = await sensor.new_sensor(config[CONF_INVERTER_STATUS_CODE])
        cg.add(var.set_inverter_status_code_sensor(sens))

    if CONF_GRID_RELAY_CODE in config:
        sens = await sensor.new_sensor(config[CONF_GRID_RELAY_CODE])
        cg.add(var.set_grid_relay_code_sensor(sens))

    if CONF_FREQUENCY in config:
        sens = await sensor.new_sensor(config[CONF_FREQUENCY])
        cg.add(var.set_grid_frequency_sensor(sens))

    if CONF_ACTIVE_POWER in config:
        sens = await sensor.new_sensor(config[CONF_ACTIVE_POWER])
        cg.add(var.set_grid_active_power_sensor(sens))

    if CONF_PV_ACTIVE_POWER in config:
        sens = await sensor.new_sensor(config[CONF_PV_ACTIVE_POWER])
        cg.add(var.set_pv_active_power_sensor(sens))

    if CONF_ENERGY_PRODUCTION_DAY in config:
        sens = await sensor.new_sensor(config[CONF_ENERGY_PRODUCTION_DAY])
        cg.add(var.set_today_production_sensor(sens))

    if CONF_TOTAL_ENERGY_PRODUCTION in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ENERGY_PRODUCTION])
        cg.add(var.set_total_energy_production_sensor(sens))

    if CONF_INVERTER_MODULE_TEMP in config:
        sens = await sensor.new_sensor(config[CONF_INVERTER_MODULE_TEMP])
        cg.add(var.set_inverter_module_temp_sensor(sens))

    for i, phase in enumerate([CONF_PHASE_A, CONF_PHASE_B, CONF_PHASE_C]):
        if phase not in config:
            continue

        phase_config = config[phase]
        for sensor_type in PHASE_SENSORS:
            if sensor_type in phase_config:
                sens = await sensor.new_sensor(phase_config[sensor_type])
                cg.add(getattr(var, f"set_{sensor_type}_sensor")(i, sens))

    for i, pv in enumerate([CONF_PV1, CONF_PV2]):
        if pv not in config:
            continue

        pv_config = config[pv]
        for sensor_type in pv_config:
            if sensor_type in pv_config:
                sens = await sensor.new_sensor(pv_config[sensor_type])
                cg.add(getattr(var, f"set_{sensor_type}_sensor_pv")(i, sens))


    if CORE.using_arduino:
        if CORE.is_esp32 | CORE.is_esp8266:
            cg.add_library("BluetoothSerial", None)

