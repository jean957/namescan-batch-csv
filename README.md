python 2.7
tested on mac and linux

Sign up on the namescan website and get your free api keys. (1000 calls per key)

put one in a file private.json as "api-key" (you may have guessed from the name, use json ;)

Put your userdata in a file input.csv in the first  with the first line:

Name,First Name,Middle Name,Last Name,DOB,Gender,Country,

and the entries in the successive lines. Use either the name field for the full name or split the name on the next three columns (middle name can remain empty)
Additional columns will be ignored and can be used as you please.
The input format for DOB is 5/25/1955, the output format is 25/05/1955 ... because reasons!
Empty fields can be "n/a" or left blank.
DOB and country are mandatory
Gender is "f" for female and otherwise counts as male

Change names for in and output files. (line 10, 11, 12)
the output.csv (line 11) contains the relevant info, output_raw.txt has the full logs, just in case.

the process will stop after maxRequests (line 16) or on unexpected error
restarting the process will continue where it was interrupted. (counting from the number of lines that have been written into the output file)

