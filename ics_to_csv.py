#!/usr/bin/env/python3

import csv
from datetime import datetime
from ics import Calendar
import sys


inputfile = sys.argv[1]
outputfile = sys.argv[1] + '.csv'


def duration_in_min(begin, end):
    result = round((end - begin).total_seconds() / 60)
    return result


def main():
    sys.stdout.write(f"\n|======================|\n")
    sys.stdout.write(  f"| ICS to CSV Converter |\n")
    sys.stdout.write(  f"|======================|\n")
    sys.stdout.write(f"  => Parsing .ics file at '{inputfile}'...\n")

    # Parse the input file as an ICS calendar
    icsfile = open(inputfile)
    c = Calendar(icsfile.read())
    icsfile.close()

    sys.stdout.write(f"  => Read {len(c.events)} events from input file.\n")

    # Get the set of all attributes in the input calendar's events
    all_keys = set().union(*[e.__dict__.keys() for e in c.events])

    sys.stdout.write(f"  => Writing events to .csv file at '{outputfile}'...\n")

    # Process the events data
    results = []
    for e in c.events:
        event = e.__dict__
        event['date'] = e._begin.date()
        if event['date'] == None:
            sys.exit(f"Bad date data: {event['date']}, {event['name']}")
        event['minutes'] = duration_in_min(e._begin, e._end_time)
        results.append(event)

    # Write each event to the output CSV
    with open(outputfile, 'w') as handle:
        fieldnames = ['date', 'name', 'minutes', 'location']
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        results = sorted(results, key=lambda e: e['date'])
        for row in results:
            writer.writerow(row)

    sys.stdout.write(f" Conversion complete. Goodbye!\n\n")

if __name__ == "__main__":
    main()