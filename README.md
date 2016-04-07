About
-----

This script downloads Magic The Gathering expansion symbols images (if available) from mtgsalvation.gamepedia.com and store them into a folder,  creating an xml file with the following information:

* Expansion Name
* Expansion Image (in the form of relative path)

Prerequisites
-------------

This script need Python version 3 or greater

You also need the following python libraries: 

* BeautifulSoup (in Debian: python3-bs4)


Usage
-----

This script can create xml in two different ways: 

* With image name and image path as node elements
* Or with them as an attribute inside the element node. 

If you want to save elements as attributes, you must change the elementValuesAsAttributes to true


TODO
----

* Add argument parsing
* Code refactoring
