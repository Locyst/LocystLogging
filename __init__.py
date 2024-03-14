import os, time, inspect
from datetime import datetime
from typing import Dict, List

DEBUG = 'DEBUG'
INFO = 'INFO'
WARN = 'WARN'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'


class Logger:

  def __init__(self,
               filePath=os.path.join(
                   os.path.dirname(os.path.abspath(__file__)),
                   'data/logging.txt'),
               maxSize=20560,
               autoFlush=False):
    """
    Sets up a basic config for the logger.

    Parameters:
     - filePath List(Str): The path to the file to log to.
     - maxSize Int: The maximum size of the file to log to. This is in bytes, not lines.
     - autoFlush Bool: Whether or not to automatically flush the file after each write.
    """
    self.name = 'LocystLogger'
    self.filePath = [filePath]
    self._cache = []
    self.maxSize = maxSize
    self.auto_flush = autoFlush
    self.INIT = False

    self._file_path_validity()
    self.info(
        f"Initialized logger with file path: {filePath}, and max size: {maxSize}"
    )

  def init(self):
    """
    Initiates the logger with the corrent file name. Can be ran multiple times with the only thing changing is the modules name when logging.
    """
    result = inspect.getouterframes(inspect.currentframe(), 2)
    self.name = os.path.split(result[1][1])[-1]
    self.INIT = True

    self.info("Hey, Listen!")

  def get_logs(self):
    return self._cache

  def _file_path_validity(self):
    """
    Check the validity of the log file path(s) and create directories if they do not exists
    """
    time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    for path in self.filePath:
      # Check if the directory exists
      directory = os.path.dirname(path)
      if not os.path.exists(directory):
        os.makedirs(directory)

      # Create a new file if it doesn't exist
      if not os.path.exists(path):
        with open(path, 'w') as file:
          file.write(f'{time_str}\n')

  def log(self, name: str, level: str, msg: str, *args, **kwargs):
    if not self.init:
      print(
          f"[{self.name}] Error: Logger is not initialized. Please call init() first."
      )
      return 0
    if not name:
      name = self.name
      print("Name not given, using default name")
    """
    Logs a message to the loggers cache
  
    Parameters:
     - level (str): The severity level of the message
     - msg (str): The main message content
     - args (list): Optional arguments to be appended
     - kwargs (dict): Optional key-value pairs to be appended
    """
    time = datetime.now().strftime("%H-%M-%S")

    log = f"[{time}] [{name}/{level}] {msg} {args if args else ''} {kwargs if kwargs else ''}"

    self._cache.append(log)
    if self.auto_flush:
      self.flush()

  def _clear_cache(self):
    """
    Clears the loggers cache
    """
    self._cache.clear()

# -------------- User logging methods -------------- #

  def debug(self, msg: str, *args: List[str], **kwargs: Dict[str, str]):
    caller_file = inspect.getouterframes(inspect.currentframe(), 2)
    caller_file = os.path.split(caller_file[1][1])[-1]
    caller_file = caller_file[:-3:].capitalize()
    """
    Log a message with severity 'DEBUG' to the cache.
    Used for information useful for debugging
  
    Parameters:
     - msg (str): Message to log
     - args (list): Optional arguments to be included
     - kwargs (dict): Optional key-value pairs to be included
    """
    self.log(name=caller_file, level=DEBUG, msg=msg, args=args, kwargs=kwargs)

  def info(self, msg: str, *args: List[str], **kwargs: Dict[str, str]):
    caller_file = inspect.getouterframes(inspect.currentframe(), 2)
    caller_file = os.path.split(caller_file[1][1])[-1]
    caller_file = caller_file[:-3:].capitalize()
    """
    Log a message with severity 'INFO' to the cache.
    Used for general information.
  
    Parameters:
     - msg (str): Message to log
     - args (list): Optional arguments to be included
     - kwargs (dict): Optional key-value pairs to be included
    """
    self.log(name=caller_file, level=INFO, msg=msg, args=args, kwargs=kwargs)

  def warn(self, msg: str, *args: List[str], **kwargs: Dict[str, str]):
    caller_file = inspect.getouterframes(inspect.currentframe(), 2)
    caller_file = os.path.split(caller_file[1][1])[-1]
    caller_file = caller_file[:-3:].capitalize()
    """
    Log a message with severity 'WARN' to the cache.
    Used for errors that could be fixed by the user
  
    Parameters:
     - msg (str): Message to log
     - args (list): Optional arguments to be included
     - kwargs (dict): Optional key-value pairs to be included
    """
    self.log(name=caller_file, level=WARN, msg=msg, args=args, kwargs=kwargs)

  def error(self, msg: str, *args: List[str], **kwargs: Dict[str, str]):
    caller_file = inspect.getouterframes(inspect.currentframe(), 2)
    caller_file = os.path.split(caller_file[1][1])[-1]
    caller_file = caller_file[:-3:].capitalize()
    """
    Log a message with severity 'ERROR' to the cache.
    Used for errors that cannot be fixed by the user
  
    Parameters:
     - msg (str): Message to log
     - args (list): Optional arguments to be included
     - kwargs (dict): Optional key-value pairs to be included
    """
    self.log(name=caller_file, level=ERROR, msg=msg, args=args, kwargs=kwargs)

  def critical(self, msg: str, *args: List[str], **kwargs: Dict[str, str]):
    caller_file = inspect.getouterframes(inspect.currentframe(), 2)
    caller_file = os.path.split(caller_file[1][1])[-1]
    caller_file = caller_file[:-3:].capitalize()
    """
    Log a message with severity 'CRITICAL' to the cache.
    Used for errors that crash the program
  
    Parameters:
     - msg (str): Message to log
     - args (list): Optional arguments to be included
     - kwargs (dict): Optional key-value pairs to be included
    """
    self.log(name=caller_file,
             level=CRITICAL,
             msg=msg,
             args=args,
             kwargs=kwargs)


# -------------- File manipulation -------------- #

  def flush(self):
    if not self.init:
      print(
          f"[{self.name}] Error: Logger is not initialized. Please call init() first."
      )
      return 0
    """
    Flushes the loggers cache to a file
    """
    for path in self.filePath:
      with open(path, 'a') as f:
        write = '\n'.join(self._cache)
        f.write(f'{write}\n')

    self._rotate_logs()
    self._clear_cache()

  def _rotate_logs(self):
    """
    Creates a new the log file if the size of the current
    one is too large
    """
    for path in self.filePath:
      if os.path.exists(path) is False:
        self.warn(f"File {path} does not exist")
        self.flush()

      if os.path.getsize(path) >= self.maxSize:
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        os.rename(path, f"{path}-{time}")
        self.debug(f'Rotated file from {path} to {path}-{time}')

  def clear_logs(self):
    """
    Clears every log file
    """

    nput = input("Are you sure you want to clear all logs? (y/n)")
    if nput.lower() != 'y':
      return

    for path in self.filePath:
      if os.path.exists(path):
        with open(path, 'w') as f:
          f.write('')
