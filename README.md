# LocystLogging

A python logger library to make logging and managing logs easier. The default and unchangable format for logs are "[Time of log] [Log file caller/Log level] [Msg]".

## How to use

- Clone the repository
- Import the `Logger` class to your python environment
- Follow the example code below for creating new logs

## Usage

```python
from LocystLogger import Logger

my_logger = Logger()
my_logger.init()

my_logger.info('This is an information message')
my_logger.warn('This is a warning message')
my_logger.error('This is an error message')
my_logger.debug('This is a debug message')
my_logger.critical('This is a critical message')

my_logger.flush()
```

## Configuration
The Logger class constructor takes the following parameters:

- filePath: Optional parameter to specifiy the file path for the log file (default: ./data/logging.txt)
- maxSize: Optional parameter to specifiy the maximum size of the log file in bytes (default: 20560)
- autoFlush: Optional parameter to specifiy whether to automatically flush the log file after each write (default: False)

## To-do

- Add the ability to change the format
- Add file location grabbers to each function to make it best show where a log is coming from
- Add more supported files
