from tkinter import *
from tkinter import ttk

class SplitFlapGUI:
  def __init__(self):    
    self._window = Tk()
    self._window.title("Split-Flap")

    self._mainframe = ttk.Frame(self._window, padding="3 3 12 12")
    self._mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    self._mainframe.columnconfigure(0, weight=1)
    self._mainframe.rowconfigure(0, weight=1)

    self._characterLetters = []
    self._characterTicks = []
    self._characterSequence = []
    self._sequencePins = []
    self._multiplexorPins = []
    
    self.setupCharacters()
    self.setupTicks()
    self.setupSequences()
    
    ttk.Button(self._mainframe, text="Start", command=self.start).grid(column=12, row=0, sticky=W)
    ttk.Button(self._mainframe, text="Stop", command=self.stop).grid(column=12, row=1, sticky=W)
    ttk.Button(self._mainframe, text="Tick", command=self.tick).grid(column=12, row=2, sticky=W)
    
    self.setupSequencePins()
    self.setupMultiplexor()
    self.setupTarget()
    for child in self._mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
  
  def setupTarget(self):
    self._target = StringVar()
    ttk.Label(self._mainframe, text="Target:").grid(row=4,column=10, columnspan=3)
    ttk.Entry(self._mainframe, textvariable=self._target).grid(row=5,column=10, columnspan=3)
    ttk.Button(self._mainframe, text="Set", command=self.setTarget).grid(row=6, column=10, columnspan=3)

  def setupSequencePins(self):
    ttk.Label(self._mainframe, text="Sequence: ").grid(row=3,column=1, columnspan=3)
    self.createLabels(4, 2, 4, self._sequencePins, False, True)
    for label in self._sequencePins:
      label.configure(text="0")

  def setupMultiplexor(self):
    ttk.Label(self._mainframe, text="Multiplexor: ").grid(row=3,column=6, columnspan=3)
    self.createLabels(4, 7, 4, self._multiplexorPins, False, True)
    for label in self._multiplexorPins:
      label.configure(text="0")
    ttk.Label(self._mainframe, text="PWR: ").grid(row=9,column=5, columnspan=2)
    self._multiplexorPower = ttk.Label(self._mainframe, text="0").grid(row=9,column=7)
    
  def setupCharacters(self):
    ttk.Label(self._mainframe, text="Characters: ").grid(row=0,column=0)
    self.createLabels(0, 1, 10, self._characterLetters, True)
    for label in self._characterLetters:
      label.configure(text="A")
  
  def setupTicks(self):
    ttk.Label(self._mainframe, text="Ticks: ").grid(row=1,column=0)
    self.createLabels(1, 1, 10, self._characterTicks, False)
    for label in self._characterTicks:
      label.configure(text="1")
      
  def setupSequences(self):
    ttk.Label(self._mainframe, text="Sequence: ").grid(row=2,column=0)
    self.createLabels(2, 1, 10, self._characterSequence, False)
    for label in self._characterSequence:
      label.configure(text="1")
    
  def createLabels(self, startRow, startCol, quantity, collection=[], sunken= False, vertical=False):
    for i in range(quantity):
      if sunken:
        label = ttk.Label(self._mainframe, text="", relief=SUNKEN, borderwidth=1)
      else:
        label = ttk.Label(self._mainframe, text="")

      if vertical:
        label.grid(row=startRow+i,column=startCol)
      else:
        label.grid(row=startRow,column=startCol+ i)
      collection.append(label)
    return collection
  
  def tick(self):
    print("Tick")
  
  def start(self):
    print("Start")
  
  def stop(self):
    print("Stop")
  
  def setTarget(self):
    print("Set Target: " + str(self._target.get()))
    
  def run(self):
    self._window.mainloop()
