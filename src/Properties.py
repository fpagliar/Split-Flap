class Properties:
  def __init__(self):
    self.CHARACTERS_ARRAY = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', ' ', ' ', ' ']
    self.TICKS_PER_LETTER = 5
    self.PINS = [10, 11, 12, 13, 14, 15]
    self.MOTOR_SEQUENCE = [[1, 0, 0, 1],
           [1, 0, 0, 0],
           [1, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 1, 0],
           [0, 0, 1, 0],
           [0, 0, 1, 1],
           [0, 0, 0, 1]]
    self.FEED_FILENAME = ""
