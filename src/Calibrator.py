from DisplayFactory import DisplayFactory
from Logger import log
import Utils
import time
from Configuration import SystemStatus

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
    controller = _CalibratorSequencePublisher(self._pinBuilder, 4, self._config)
    while True:
      controller.tick(0)
      controller.tick(1)
      controller.tick(2)
      controller.tick(3)

  def calibrateTicksPerLetter(self, status, calibration):
    characters, publisher = DisplayFactory(self._pinBuilder, self._config).buildCharacters(status)

    # Create alphabet
    alphabet = self._config.alphabet()
    # Appending the first letter on the end, so that we calibrate the change from the last letter to the first one.
    alphabet.append(alphabet[0])
    # Removing the first letter
    alphabet = alphabet[1:]

    for i in range(len(characters)):
      if Utils.askForConfirmation("Do you want to calibrate character: " + str(i + 1)):
        character = characters[i]
        print("Now calibrating the character " + str(i + 1))
        characterPublisher = _CharacterPublisher(character, publisher)
        calibration.set(i + 1, self._calibrateTicks(lambda : characterPublisher.tick(i), calibration.ticksConfiguration(i), alphabet))
        status.set(i + 1, 0, status.sequence(i + 1))
        calibration.save()
    print("Great, calibration ended")
    calibration.save()

  def _calibrateTicks(self, tickFunction, currentTicksConfiguration, alphabet):
    ticks = 0
    newTicksConfiguration = []
    previousTicksConfiguration = currentTicksConfiguration
    for letterIndex in range(len(alphabet)):
      if previousTicksConfiguration:
        fastForwaredTicks = self._fastForwardIfCalibrated(tickFunction, previousTicksConfiguration, letterIndex)
        ticks = ticks + fastForwaredTicks
      ticks = ticks + self._stepUntilInterrupted(tickFunction, "Is it showing character " + alphabet[letterIndex] + "?")
      if letterIndex == 0 and not previousTicksConfiguration:
        previousTicksConfiguration = [ticks * (i + 1) for i in range(len(alphabet))]
      newTicksConfiguration.append(ticks)
      print("So far: " + str(newTicksConfiguration))
    return newTicksConfiguration

  def _fastForwardIfCalibrated(self, tickFunction, currentTicksConfiguration, index):
    ticks = 0
    intervalEnd = currentTicksConfiguration[index]
    intervalStart = currentTicksConfiguration[index - 1] if index > 0 else 0
    ticksToGetClose = int((intervalEnd - intervalStart) * 0.8)
    for _ in range(ticksToGetClose):
      tickFunction()
      ticks = ticks + 1
    return ticks

  def calibrateInitialPosition(self):
    numberOfMotors = self._config.numberOfMotors()
    controller = _CalibratorSequencePublisher(self._pinBuilder, numberOfMotors, self._config)
    systemStatus = SystemStatus(numberOfMotors)
    systemStatus.default()
    systemStatus.cleanup()
    target = self._config.alphabet()[0]

    for i in range (1, numberOfMotors + 1):
      print("Now configuring the character " + str(i))
      self._keepTurningUntilInterrupted(lambda : controller.tick(i - 1), "Is it close to " + target + "?", 0.01)
      self._stepUntilInterrupted(lambda : controller.tick(i - 1), "Is it showing letter " + target + "?")
      sequence = controller.getSequences()[i - 1]
      sequence.inform(lambda index: systemStatus.set(i, 0, index))
    print("Great, now the split-flap start position is correctly configured")

#   def _moveUntilInterrupted(self, tickFunction, message, wait):
#     self._stepUntilInterrupted(tickFunction, message, wait)

  def _keepTurningUntilInterrupted(self, tickFunction, message, wait):
    print(message)
    ticks = 0
    # Will run until it hears the interruption
    try:
      while True:
        tickFunction()
        ticks = ticks + 1
        time.sleep(wait)
    except KeyboardInterrupt:
      pass
    return ticks

  def _stepUntilInterrupted(self, tickFunction, message):
    print(message)
    ticks = 0
    while not Utils.askForConfirmation("Did it change yet?"):
      tickFunction()
      ticks = ticks + 1
      print(str(ticks) + " so far")
    return ticks

class _CharacterPublisher:
  def __init__(self, character, publisher):
    self._character = character
    self._publisher = publisher

  def tick(self, index):
    self._character.tick()
    self._publisher.publish()

class _CalibratorSequencePublisher:
  def __init__(self, pinBuilder, quantity, config):
    factory = DisplayFactory(pinBuilder, config)
    self._sequences, self._connection = factory.buildCharacterCalibrator(quantity)

  def getSequences(self):
    return self._sequences

  def tick(self, index):
    self._sequences[index].next()
    self._connection.publish()

