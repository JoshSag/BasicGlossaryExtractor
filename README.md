# BasicGlossaryExtractor
Extracting unique words from files

The script (gloosery.py) runs on a file and extracts legitimate words (letters only).  
It saves the found *unique* words as a simple text file with one word in each line.  


You can feed it with file or directory again and again to collect more words.  
In the first run (the first input), use --load_glossary 0, because there is no existing glossary yet.  
And then continue feeding it with new inputs but now with --load_glossary 1.


The script is always limited to pre-defined accepted extensions when you run on a directory.  
If you want to collect words from files in the root directory only – use recursively 0.  
If you want to collect words from all internal files – use recursively 1.


NOTE: There is no leakage of any information except for the very existence of those words. The code is very simple for anyone to review.  


* See help (python glossery.py -h) for more information.  
* See test.py for code-example.  
* See usage_examplel.png to see an example.  
    There you can see:
    1.	The help message with detailed information about the cmd parameters. 
    2.	A running example on a directory (“…xlog”) recursively. Note that at the first input (or whenever you want to start fresh), you should use –load_glossary 0.
    3.	A running example on another directory(“…_code”) recursively. Note that we use –load_glossary 1 at this input to load our results from the previous run and build upon it. 
    4.	The output glossary file is defined in –glossary_path
