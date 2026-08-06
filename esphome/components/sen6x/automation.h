#pragma once

#include "esphome/core/automation.h"
#include "esphome/core/helpers.h"
#include "sen6x.h"

namespace esphome::sen6x {

template<typename... Ts> class StartFanAction final : public Action<Ts...>, public Parented<SEN6XComponent> {
 public:
  explicit StartFanAction(SEN6XComponent *parent) { this->parent_ = parent; }

  void play(const Ts &...x) override { this->parent_->start_fan_cleaning(); }
};

}  // namespace esphome::sen6x
