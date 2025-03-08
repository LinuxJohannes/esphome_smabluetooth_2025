#pragma once

#ifndef SMABLUETOOTH_SOLAR_H
#define SMABLUETOOTH_SOLAR_H

/* MIT License

Copyright (c) 2023 keerekeerweere

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Disclaimer
A user of the esphome component software acknowledges that he or she is 
receiving this software on an "as is" basis and the user is not relying on 
the accuracy or functionality of the software for any purpose. The user further
acknowledges that any use of this software will be at his own risk and the 
copyright owner accepts no responsibility whatsoever arising from the use or 
application of the software.

SMA, Speedwire are registered trademarks of SMA Solar Technology AG

*/

#define PHASES 3  // Type of inverter, one or 3 phases
#define HAVE_MODULE_TEMP false

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "SMA_Inverter.h"

#include <vector>
#include <map>

#define SIZE_INVETER_DATA_TYPE_QUERY 9


namespace esphome {
namespace smabluetooth_solar {

static const float TWO_DEC_UNIT = 0.01;
static const float ONE_DEC_UNIT = 0.1;

enum SmaBluetoothProtocolVersion {
  SMANET2 = 0
};

//states to cycle through
enum class SmaInverterState {
  Off, //when starting up ESP
  Begin, //begin the bluetooth stack
  Connect, //connect to the inverter
  Initialize, //init SMA connection
  SignalStrength,//get signal quality
  Logon,//logon to inverter
  ReadValues,//read values (piece by piece)
  DoneReadingValues,
  Disconnect,//disconnect again from the inverter
  NightTime//nighttime, nothing to do here, wait for next sunlight
};

class SmaBluetoothSolar;

class SmaBluetoothSolar : public PollingComponent {
 public:
    SmaBluetoothSolar() {
      initMap();
    };

    void initMap() {

      codeMap[50]="Status";
      codeMap[51]="Closed";

      codeMap[300]="Nat";
      codeMap[301]="Grid failure";
      codeMap[302]="-------";
      codeMap[303]="Off";
      codeMap[304]="Island mode";
      codeMap[305]="Island mode";
      codeMap[306]="SMA Island mode 60 Hz";
      codeMap[307]="OK";
      codeMap[308]="On";
      codeMap[309]="Operation";
      codeMap[310]="General operating mode";
      codeMap[311]="Open";
      codeMap[312]="Phase assignment";
      codeMap[313]="SMA Island mode 50 Hz";

      codeMap[16777213]="Information not available";

    }


    std::string getInverterCode(int invCode) {
      std::map<int, std::string>::iterator it = codeMap.find(invCode);
      if (it != codeMap.end())
        return it->second;
      else
        return std::to_string(invCode);
    }

  float get_setup_priority() const override { return setup_priority::LATE; }

  void loop() override;
  void setup() override;

  void update() override;
  void updateSensor( text_sensor::TextSensor *sensor,  String sensorName,  std::string publishValue);
  void updateSensor( sensor::Sensor *sensor,  String sensorName,  int32_t publishValue);
  void updateSensor( sensor::Sensor *sensor,  String sensorName,  float publishValue);
  void on_inverter_data(const std::vector<uint8_t> &data) ;
  void dump_config() override;

  void set_protocol_version(SmaBluetoothProtocolVersion protocol_version) { this->protocol_version_ = protocol_version; }

  void set_sma_inverter_bluetooth_mac(std::string sma_inverter_bluetooth_mac) { this->sma_inverter_bluetooth_mac_ = sma_inverter_bluetooth_mac; }
  void set_sma_inverter_password(std::string sma_inverter_password) {this->sma_inverter_password_ = sma_inverter_password; }

  void set_inverter_status_code_sensor(sensor::Sensor *sensor) { this->inverter_status_sensor_ = sensor; }
  void set_grid_relay_code_sensor(sensor::Sensor *sensor) { this->grid_relay_sensor_ = sensor; }

  // TEXT_SENSORS
  void set_inverter_status_sensor(text_sensor::TextSensor *text_sensor) { status_text_sensor_ = text_sensor; }
  void set_grid_relay_sensor(text_sensor::TextSensor *text_sensor) { grid_relay_text_sensor_ = text_sensor; }
  // END_TEXT_SENSORS

  void set_grid_frequency_sensor(sensor::Sensor *sensor) { this->grid_frequency_sensor_ = sensor; }
  void set_grid_active_power_sensor(sensor::Sensor *sensor) { this->grid_active_power_sensor_ = sensor; }
  void set_pv_active_power_sensor(sensor::Sensor *sensor) { this->pv_active_power_sensor_ = sensor; }

  void set_today_production_sensor(sensor::Sensor *sensor) { this->today_production_ = sensor; }
  void set_total_energy_production_sensor(sensor::Sensor *sensor) { this->total_energy_production_ = sensor; }
#ifdef HAVE_MODULE_TEMP
  void set_inverter_module_temp_sensor(sensor::Sensor *sensor) { this->inverter_module_temp_ = sensor; }
#endif
  void set_voltage_sensor(uint8_t phase, sensor::Sensor *voltage_sensor) {
    this->phases_[phase].voltage_sensor_ = voltage_sensor;
  }
  void set_current_sensor(uint8_t phase, sensor::Sensor *current_sensor) {
    this->phases_[phase].current_sensor_ = current_sensor;
  }
  void set_active_power_sensor(uint8_t phase, sensor::Sensor *active_power_sensor) {
    this->phases_[phase].active_power_sensor_ = active_power_sensor;
  }
  void set_voltage_sensor_pv(uint8_t pv, sensor::Sensor *voltage_sensor) {
    this->pvs_[pv].voltage_sensor_ = voltage_sensor;
  }
  void set_current_sensor_pv(uint8_t pv, sensor::Sensor *current_sensor) {
    this->pvs_[pv].current_sensor_ = current_sensor;
  }
  void set_active_power_sensor_pv(uint8_t pv, sensor::Sensor *active_power_sensor) {
    this->pvs_[pv].active_power_sensor_ = active_power_sensor;
  }

  void loopNotification();

 protected:
  bool waiting_to_update_;
  uint32_t last_send_;

  uint32_t nextTime = 0;
  bool nightTime = false;
  bool firstTime = true;
  bool hasBegun = false;
  bool hasSetup = false;

  bool running_update_ = false;

  struct SmaPhase {
    sensor::Sensor *voltage_sensor_{nullptr};
    sensor::Sensor *current_sensor_{nullptr};
    sensor::Sensor *active_power_sensor_{nullptr};
  } phases_[3];
  struct SmaPV {
    sensor::Sensor *voltage_sensor_{nullptr};
    sensor::Sensor *current_sensor_{nullptr};
    sensor::Sensor *active_power_sensor_{nullptr};
  } pvs_[2];

  sensor::Sensor *inverter_status_sensor_{nullptr};
  sensor::Sensor *grid_relay_sensor_{nullptr};

  text_sensor::TextSensor *status_text_sensor_{nullptr};
  text_sensor::TextSensor *grid_relay_text_sensor_{nullptr};

  sensor::Sensor *grid_frequency_sensor_{nullptr};
  sensor::Sensor *grid_active_power_sensor_{nullptr};

  sensor::Sensor *pv_active_power_sensor_{nullptr};

  sensor::Sensor *today_production_{nullptr};
  sensor::Sensor *total_energy_production_{nullptr};
#ifdef HAVE_MODULE_TEMP
  sensor::Sensor *inverter_module_temp_{nullptr};
#endif
  SmaBluetoothProtocolVersion protocol_version_;

  std::string sma_inverter_bluetooth_mac_ ;
  std::string sma_inverter_password_ ;


  std::map<int, std::string> codeMap;

  private:
    ESP32_SMA_Inverter *smaInverter;
    SmaInverterState inverterState = SmaInverterState::Off;
    getInverterDataType invDataTypes[SIZE_INVETER_DATA_TYPE_QUERY] =
       {EnergyProduction, SpotGridFrequency, SpotDCPower, SpotDCVoltage, SpotACPower, SpotACTotalPower, SpotACVoltage, DeviceStatus/*, GridRelayStatus */};

    int indexOfInverterDataType = 0;
};


}  // namespace smabluetooth_solar
}  // namespace esphome


#endif