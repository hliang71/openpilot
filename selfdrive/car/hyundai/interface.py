#!/usr/bin/env python3
from cereal import car
from selfdrive.config import Conversions as CV
from selfdrive.car.hyundai.values import Ecu, ECU_FINGERPRINT, CAR, FINGERPRINTS
from selfdrive.car import STD_CARGO_KG, scale_rot_inertia, scale_tire_stiffness, is_ecu_disconnected, gen_empty_fingerprint
from selfdrive.car.interfaces import CarInterfaceBase

class CarInterface(CarInterfaceBase):

  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 3.0

  @staticmethod
  def get_params(candidate, fingerprint=gen_empty_fingerprint(), has_relay=False, car_fw=[]):  # pylint: disable=dangerous-default-value
    ret = CarInterfaceBase.get_std_params(candidate, fingerprint, has_relay)

    ret.carName = "hyundai"
    ret.safetyModel = car.CarParams.SafetyModel.hyundai
    ret.radarOffCan = True

    # Most Hyundai car ports are community features for now
    ret.communityFeature = candidate not in [CAR.SONATA]

    ret.steerActuatorDelay = 0.1  # Default delay
    ret.steerRateCost = 0.5
    ret.steerLimitTimer = 0.4
    tire_stiffness_factor = 1.

    if candidate == CAR.SANTA_FE:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3982. * CV.LB_TO_KG + STD_CARGO_KG
      ret.wheelbase = 2.766
      # Values from optimizer
      ret.steerRatio = 16.55  # 13.8 is spec end-to-end
      tire_stiffness_factor = 0.82
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[9., 22.], [9., 22.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.2, 0.35], [0.05, 0.09]]
    elif candidate == CAR.SONATA:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1513. + STD_CARGO_KG
      ret.wheelbase = 2.84
      ret.steerRatio = 13.27 * 1.15   # 15% higher at the center seems reasonable
      tire_stiffness_factor = 0.65
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.SONATA_2019:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 4497. * CV.LB_TO_KG
      ret.wheelbase = 2.804
      ret.steerRatio = 13.27 * 1.15   # 15% higher at the center seems reasonable
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.PALISADE:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1999. + STD_CARGO_KG
      ret.wheelbase = 2.90
      ret.steerRatio = 13.75 * 1.15
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KIA_SORENTO:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1985. + STD_CARGO_KG
      ret.wheelbase = 2.78
      ret.steerRatio = 14.4 * 1.1   # 10% higher at the center seems reasonable
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate in [CAR.ELANTRA, CAR.ELANTRA_GT_I30]:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1275. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 15.4            # 14 is Stock | Settled Params Learner values are steerRatio: 15.401566348670535
      tire_stiffness_factor = 0.385    # stiffnessFactor settled on 1.0081302973865127
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.HYUNDAI_GENESIS:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 2060. + STD_CARGO_KG
      ret.wheelbase = 3.01
      ret.steerRatio = 16.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.16], [0.01]]
      ret.minSteerSpeed = 60 * CV.KPH_TO_MS
    elif candidate == CAR.GENESIS_G80:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 2060. + STD_CARGO_KG
      ret.wheelbase = 3.01
      ret.steerRatio = 16.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.16], [0.01]]
    elif candidate == CAR.GENESIS_G90:
      ret.mass = 2200
      ret.wheelbase = 3.15
      ret.steerRatio = 12.069
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.16], [0.01]]
    elif candidate in [CAR.KIA_OPTIMA, CAR.KIA_OPTIMA_H]:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KIA_STINGER:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1825. + STD_CARGO_KG
      ret.wheelbase = 2.78
      ret.steerRatio = 14.4 * 1.15   # 15% higher at the center seems reasonable
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KONA:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1275. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73  # Spec
      tire_stiffness_factor = 0.385
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KIA_NIRO_EV:
      ret.lateralTuning.init('indi')
      ret.lateralTuning.indi.innerLoopGain = 2.3595 #2.3595#2.3195#5 #1.75 #1.8468                                     #2.3085 #2.565 #2.85 #4.73 #5
      ret.lateralTuning.indi.outerLoopGain = 2.268                #4.8 #1.72 #1.8144                                   #2.268 #2.52 #2.8 #4.6 #4.85  # 4.8
      ret.lateralTuning.indi.timeConstant = 1.392                 #1.16 x 1.83#1.16x0.8424#1.16 x 0.936                #1.16 x 1.2#1.16x1.4#1.16 x 1.7# 1.16 x 1.8
      ret.lateralTuning.indi.actuatorEffectiveness = 1.582        #1.13 x 1.83#1.13x0.8424#1.13x0.936                  #1.13x1.2#1.13x1.4#1.13 x 1.7 # 1.13 x 1.8
      # ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 1737. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.75  # Spec 13.73
      tire_stiffness_factor = 0.385
      ret.steerActuatorDelay = 0.255 #0.253 #0.255 #0.28  # 0.3
      ret.steerLimitTimer = 0.4  # 0.8
      ret.steerMaxBP = [0.]
      ret.steerMaxV = [0.9] #[0.85]
      # ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      # ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.KONA_EV:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1685. + STD_CARGO_KG
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73  # Spec
      tire_stiffness_factor = 0.385
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate in [CAR.IONIQ, CAR.IONIQ_EV_LTD]:
      ret.lateralTuning.pid.kf = 0.00006
      ret.mass = 1490. + STD_CARGO_KG   #weight per hyundai site https://www.hyundaiusa.com/ioniq-electric/specifications.aspx
      ret.wheelbase = 2.7
      ret.steerRatio = 13.73   #Spec
      tire_stiffness_factor = 0.385
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
      ret.minSteerSpeed = 32 * CV.MPH_TO_MS
    elif candidate == CAR.KIA_FORTE:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]
    elif candidate == CAR.VELOSTER:
      ret.lateralTuning.pid.kf = 0.00005
      ret.mass = 3558. * CV.LB_TO_KG
      ret.wheelbase = 2.80
      ret.steerRatio = 13.75 * 1.15
      tire_stiffness_factor = 0.5
      ret.lateralTuning.pid.kiBP, ret.lateralTuning.pid.kpBP = [[0.], [0.]]
      ret.lateralTuning.pid.kpV, ret.lateralTuning.pid.kiV = [[0.25], [0.05]]

    # these cars require a special panda safety mode due to missing counters and checksums in the messages
    if candidate in [CAR.HYUNDAI_GENESIS, CAR.IONIQ_EV_LTD, CAR.IONIQ, CAR.KONA_EV, CAR.KIA_SORENTO, CAR.SONATA_2019, CAR.KIA_OPTIMA, CAR.VELOSTER, CAR.KIA_STINGER, CAR.KIA_NIRO_EV]:
      ret.safetyModel = car.CarParams.SafetyModel.hyundaiLegacy

    ret.centerToFront = ret.wheelbase * 0.4

    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = scale_rot_inertia(ret.mass, ret.wheelbase)

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront, ret.tireStiffnessRear = scale_tire_stiffness(ret.mass, ret.wheelbase, ret.centerToFront,
                                                                         tire_stiffness_factor=tire_stiffness_factor)

    ret.enableCamera = is_ecu_disconnected(fingerprint[0], FINGERPRINTS, ECU_FINGERPRINT, candidate, Ecu.fwdCamera) or has_relay

    return ret

  def update(self, c, can_strings):
    self.cp.update_strings(can_strings)
    self.cp_cam.update_strings(can_strings)

    ret = self.CS.update(self.cp, self.cp_cam)
    ret.canValid = self.cp.can_valid and self.cp_cam.can_valid

    events = self.create_common_events(ret)
    #TODO: addd abs(self.CS.angle_steers) > 90 to 'steerTempUnavailable' event

    # low speed steer alert hysteresis logic (only for cars with steer cut off above 10 m/s)
    if ret.vEgo < (self.CP.minSteerSpeed + 2.) and self.CP.minSteerSpeed > 10.:
      self.low_speed_alert = True
    if ret.vEgo > (self.CP.minSteerSpeed + 4.):
      self.low_speed_alert = False
    if self.low_speed_alert:
      events.add(car.CarEvent.EventName.belowSteerSpeed)

    ret.events = events.to_msg()

    self.CS.out = ret.as_reader()
    return self.CS.out

  def apply(self, c):
    can_sends = self.CC.update(c.enabled, self.CS, self.frame, c.actuators,
                               c.cruiseControl.cancel, c.hudControl.visualAlert, c.hudControl.leftLaneVisible,
                               c.hudControl.rightLaneVisible, c.hudControl.leftLaneDepart, c.hudControl.rightLaneDepart)
    self.frame += 1
    return can_sends
