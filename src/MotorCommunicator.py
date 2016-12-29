
class MotorCommunicator:
  def __init__(self, multiplexor):
    self.multiplexor = multiplexor

  def send(self, motorId, sequence):    
    # Turn off the multiplexor to avoid accidental messages while selecting the correct motor to communicate to
    self.multiplexor.off()
    
    # Activate the correct motor
    self.multiplexor.set(motorId)

    # Set the sequence
    sequence.apply()
    
    # Turn the pin we need on
    self.multiplexor.on()