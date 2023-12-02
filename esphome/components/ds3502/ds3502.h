#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/i2c/i2c.h"

namespace esphome {
namespace ds3502 {

static const uint8_t DS3502_REGISTER_WIPER_VALUE = 0x00;
static const uint8_t DS3502_REGISTER_CONTROL_MODE = 0x02;

class DS3502Component : public PollingComponent, public i2c::I2CDevice {
 public:
  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::DATA; }
  void update() override;

  void set_initial_value(uint8_t initial_value) { initial_value_ = initial_value; }
  void set_wiper_value(sensor::Sensor *wiper_value) { this->wiper_value_sensor_ = wiper_value; }

 protected:
  uint8_t initial_value_;
  sensor::Sensor *wiper_value_sensor_{nullptr};
};

}  // namespace ds3502
}  // namespace esphome