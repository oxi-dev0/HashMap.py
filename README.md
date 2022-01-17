# HashMap.py
 This is a hashmap system in python. I have made it as a personal project to challenge myself, but feel free to iterate upon it.
 The system handles things like collisions and overwrites
 
 ## To Do
 - Dynamic Scaling - Currently the developer has to specify the map size + hash length
 - Make documentation easier to read + prettier
 
 ## Documentation
 ### Files
 - `HashMap.py` contains the `HashMap` class that actually provides functionality.
 - `test.py`, `findcollisions.py` and `sizecalc.py` are all test scripts that allow interfacing / debugging for the class.

 ### Defining a map
 ```python
 hashmap = HashMap(size=500, hashlength=5, debugPrinting=False)
 ```
 - `size` = the size of the internal 2D array.
 - `hashlength` = the length of the hashed integer to use to locate a hash in the map. this will need to be compared with `size` to make sure it will not run over. Consult `sizecalc.py` or the comments within `HashMap.py` to find set size + hashlength combinations to use.
 - `debugPrinting` = enabling printing within the class.

 ### HashMap class functions
 ```python
 hashmap.Add(key, value)
 ```
 Adds a value under the key. It will relocate this hash if there is a collision, or overwrite the value if the key matches.
 
  <br>
 
 ```python
 hashmap.Find(key)
 ```
 Finds the value at the key with an ideal speed of O(1). It will traverse collision relocations, but this will result in the time notation no longer being O(1). Larger map sizes result in lower collisions.
 
  <br>
 
 ```python
 hashmap.Remove(key)
 ```
 Removes the value at the key. It will update collision references, and move one of any collided objects to the new free slot.
 
  <br>
 
 ```python
 hashmap.GetKeys()
 ```
 Returns a list of all the keys within the map. This will simply search the array, and so is O(n).
 
 <br>
 
 ```python
 hashmap.GetValues()
 ```
 Returns a list of all the values within the map. This just calls `.GetKeys()` internally, and so is O(n).
 
  <br>
 
 ```python
 hashmap.DebugPrint()
 ```
 Prints out the internal array for debugging purposes. Any maps with a size >10 will likely spam the output.

 
