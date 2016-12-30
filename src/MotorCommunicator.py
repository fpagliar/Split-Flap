
class MotorCommunicator:
  def __init__(self, multiplexor):
    self._multiplexor = multiplexor

  def send(self, motorId, sequence):    
    # Turn off the _multiplexor to avoid accidental messages while selecting the correct motor to communicate to
    self._multiplexor.off()
    
    # Activate the correct motor
    self._multiplexor.set(motorId)

    # Set the sequence
    sequence.apply()
    
    # Turn the pin we need on
    self._multiplexor.on()