# TCXRecalculator

Python scripts to modify tcx files

*Recalculate distance*
Python script to re-embed distance metrics into a TCX file using the 
GPS coordinates.

*Set timings*
Python program to set the timestamp for each trackpoint. You can specify the 
total amound of seconds and starttime. The amound of time between two timestamps 
will be set equal.

## Usage

Install de dependenties
```bash
# pip install -r requirements.txt
```

Recalculate distance 

```bash
# python tcx_recalc_dist.py input.tcx output.tcx
```

Set timings 

```bash
# python tcx_set_timings.py <input file> <output file> <starttime> <totalseconds>
```

Example:

```bash
# python tcx_set_timings.py input.tcx output.tcx "2019-08-22T15:00:05Z" 1910
```

## Dependencies

* XML parsing and generation
  * lxml

* Geographical calculations
  * http://www.movable-type.co.uk/scripts/latlong.html
