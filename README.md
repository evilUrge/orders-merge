# Orders merge
This repository is part of a Python assignment.
I tried to not implement it in a functional way as much as possible (got used for it from ES6).


## Prerequisites
Python 3.6.5


~~Install requirements by:~~
```
pip3 install -r requirements.txt
````

**Wait - there are no requirements; it's all pure vanilla**
 
To use just execute run.py with the required flags.

For example with the attached example files:
```
python run.py -o $PWD/example/orders.csv -b $PWD/example/barcodes.csv
``` 

#### Bonus points:
 - To show top users use `-t 5` with a integer as the amount for the top customers.
 - The unused barcodes are being showed both in the STDOUT and the log level.
 - Please find the log file in the project root `merge.log` for debug and error logs.
 - If not specify, a file name `result.csv` will be generate. you can use the `-j` flag for having a JSON format instead.
 - To execute it debug mode please use the env_param `PY_ENV=DEV`.
 - If I had time, I would've add some unitests, but as it wasn't required I allowed myself to release this without any.
 - Last point, Personally I would've store it in a collection base(NOSQL);
 But base on the 2 tables attached, I've created the following schema for 3 tables (and the little fields I had to work with)
 ![UML](https://firebasestorage.googleapis.com/v0/b/shell-gems.appspot.com/o/tmp%2Fuml.png?alt=media&token=eecdcdd2-d5ea-432d-aead-0c96caab6512)
 
 
 
## Optional arguments:
  * **-h, --help** show this help message and exit
  * **-b Barcodes source, --barcodes Barcodes source** Path for the barcodes_source csv file
  * **-o Orders Source, --orders Orders Source** Path for the orders source csv file
  * **-t Top customers, --top Top customers** Integer of the top customers
  * **-f Filename of the output, --filename Filename of the output** Give a name for the output file (default result
  * **-j Export to JSON, --json Export to JSON** Export to JSON instead of CSV
  * **-v, --version** show program's version number and exit
  * **-h, --help** show this help message and exit
----------------------------------------------------------

