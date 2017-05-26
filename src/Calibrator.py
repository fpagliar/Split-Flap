from DisplayFactory import DisplayFactory
from Logger import log
import Utils
import time
from Configuration import SystemCalibration, SystemStatus

# This class takes care of the calibration of each character.
# calibrateInitialPosition will help us set the start position of the system. This is the way the program will be able to
# know which letter it is showing at the moment, what step is the motor sequence in, and how many steps till the next letter shows.
# Once you calibrate the initial position, it will be saved to a file and there is not need to set it again unless something bad happens
# The other part is calibrateTicksPerLetter, and this will save which is the composition of the characters and the physical system
# and will be saved and shouldn't be run again unless you change/replace a character.
class Calibrator:
  def __init__(self, pinBuilder, config):
    self._pinBuilder = pinBuilder
    self._config = config

  def infiniteRun(self):
    controller = _CalibratorSequencePublisher(self._pinBuilder, 1, self._config)
    while True:
      controller.tick(0)
      time.sleep(0.005)

  def calibrateTicksPerLetter(self):
    self.calibrateInitialPosition()

    numberOfMotors = self._config.numberOfMotors()
    status = SystemStatus(numberOfMotors)
    status.load()
    characters, publisher = DisplayFactory(self._pinBuilder, self._config).buildCharacters(status)
    calibration = SystemCalibration(numberOfMotors)

    # Create alphabet
    alphabet = self._config.alphabet()
    # Appending the first letter on the end, so that we calibrate the change from the last letter to the first one.
    alphabet.append(alphabet[0])

    for i in range(1, len(characters) + 1):
      if Utils.askForConfirmation("Do you want to calibrate character: " + str(i)):
        character = characters[i - 1]
        print("Now calibrating the character " + str(i))
        ticksConfiguration = []
        ticks = 0
        for letter in alphabet[:1]:  # We start with A showing, so the next letter should be the first target
          ticks = ticks + self._moveUntilInterrupted(_CharacterPublisher(character, publisher), i - 1 , "Is it showing character " + letter + "?", 1)
          ticksConfiguration.append(ticks)
        calibration.set(i, ticksConfiguration)
    print("Great, calibration ended")
    calibration.save()

  def calibrateInitialPosition(self):
    numberOfMotors = self._config.numberOfMotors()
    controller = _CalibratorSequencePublisher(self._pinBuilder, numberOfMotors, self._config)
    systemStatus = SystemStatus(numberOfMotors)
    systemStatus.default()
    systemStatus.cleanup()
    target = self._config.alphabet()[0]

    for i in range (1, numberOfMotors + 1):
      print("Now configuring the character " + str(i))
      self._moveUntilInterrupted(controller, i - 1, "Is it close to " + target + "?", 0.01)
      self._moveUntilInterrupted(controller, i - 1, "Is it showing letter " + target + "?", 1)
      sequence = controller.getSequences()[i - 1]
      sequence.inform(lambda index: systemStatus.set(i, 0, index))
    print("Great, now the split-flap start position is correctly configured")

  def _moveUntilInterrupted(self, controller, motorId, message, wait):
    print(message)
    ticks = 0
    # Will run until it hears the interruption
    try:
      while True:
        controller.tick(motorId)
        ticks = ticks + 1
        time.sleep(wait)
    except KeyboardInterrupt:
      pass
    return ticks

class _CharacterPublisher:
  def __init__(self, character, publisher):
    self._character = character
    self._pubisher = publisher

  def tick(self, index):
    self._character.tick()
    self._punlisher.publish()

class _CalibratorSequencePublisher:
  def __init__(self, pinBuilder, quantity, config):
    factory = DisplayFactory(pinBuilder, config)
    self._sequences, self._connection = factory.buildCharacterCalibrator(quantity)

  def getSequences(self):
    return self._sequences

  def tick(self, index):
    self._sequences[index].next()
    self._connection.publish()
