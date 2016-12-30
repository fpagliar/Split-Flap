from Calibrator import Calibrator
import TextBasedPin

if __name__ == "__main__":
  calibrator = Calibrator(TextBasedPin.GetPin)
  calibrator.calibrateInitialPosition()
