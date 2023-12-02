#include "ds3502.h"
#include "esphome/core/log.h"

namespace esphome {
namespace ds3502 {

static const char *const TAG = "ds3502";

void DS3502Component::setup() {
  ESP_LOGCONFIG(TAG, "Setting up DS3502 Potentiometer with initial value of %f", this->initial_value_);
}

void DS3502Component::dump_config() {
  ESP_LOGCONFIG(TAG, "DS3502 Potentiometer Output:");
  ESP_LOGCONFIG(TAG, "  Initial Value: %f", this->initial_value_);
}

void DS3502Component::update() {
  uint8_t wr = 0;
  if (!this->read_byte(DS3502_REGISTER_WIPER_VALUE, &wr)) {
    this->status_set_warning();
    return;
  }
  if (this->wiper_value_sensor_ != nullptr) {
    this->wiper_value_sensor_->publish_state(wr);
  }
}


}  // namespace ds3502
}  // namespace esphome
