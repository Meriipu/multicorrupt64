# multicorrupt64
terminal7 several times at once

Take a .n64 rom and make several corrupted roms.

Launch them all at once and cascade the windows evenly out

Makes finding interesting byte regions inside rom easier.



Moving/cascading mupen64plus across screen as of now requires a patched 

mupen version that accepts a --position x,y parameter 



given a rom it creates corruptions based on settings in multicorrupt.py

afterwards opens all of them in individual mupen64plus instances 

the mupen windows are moved to be evenly spaced on desktop

```python3 multicorrupt.py original_roms/PS.n64```


relevant settings in multicorrupt.py:

mupen_instances is number of corruptions to make and open (4-20~ suggested)

instance_res is size of one mupen_window

screen_res is size of actual screen




inside __init__ of the Corruption class in multicorrupt.py:

make as many calls to self.mutate(mutation_count, start_percentage, step_percentage) as desired

mutation_count is number of individual changes per corrupted rom

start_percentage [0,100) is which percentage of bytes in rom to seek to before selecting bytes to corrupt

stop_percentage = start_percentage + step_percentage





Debugging a corrupted rom to find which change (maybe) made something happen

given original uncorrupted rom;  changefile from a corrupted rom;  number N

creates N new corruptions by dividing the changes in the changefile into N groups

```python3 debug_changes.py original_roms/PS.n64 output_roms/ramdisk/PS_corrupted_19.n64.changes 28```

these debug corruptions are placed in output_roms/ramdisk/DEBUG/




script files most likely will not work on most systems without larger changes 

and even if they work they are unstable so yeah
