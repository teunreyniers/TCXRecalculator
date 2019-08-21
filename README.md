# TCXRecalculator

Python program to re-embed distance metrics into a TCX file, so you can keep valid
distance, time, and heart rate statistics. The distance is recalculated using the 
GPS coordinates 

## Usage

Install de dependenties
```bash
# pip install -r requirements.txt
```

Run de file

```bash
# python tcxrecalc.py input.tcx output.tcx
```

## Dependencies

* XML parsing and generation
  * lxml

* Geographical calculations
  * http://www.movable-type.co.uk/scripts/latlong.html
