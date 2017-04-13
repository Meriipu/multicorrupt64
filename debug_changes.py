from sys import argv
import os
import time
import math
import multicorrupt

def chunks(L,splits):
  actual_splits = min(splits,len(L))
  chunksize, extra = divmod(len(L), actual_splits)
  for i in range(0, (actual_splits-extra)*chunksize, chunksize):
    yield L[i:i + chunksize]
  for j in range((actual_splits-extra)*chunksize, len(L), chunksize+1):
    yield L[j:j + chunksize + 1]

if __name__ == '__main__':
  output_dir = os.path.join( os.path.dirname(argv[0]), 'output_roms', 'ramdisk')
  debug_dir = os.path.join( output_dir, 'DEBUG' )
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)
  if not os.path.exists(debug_dir):
    os.mkdir(debug_dir)
      
  original_rom_path  = argv[1]
  changefile  = argv[2]
  splits = int(argv[3])
  L = multicorrupt.load_rom(original_rom_path)
  
  with open(changefile) as f:
    lines = f.readlines()
  
  out_paths = []
  basename = os.path.basename(original_rom_path)
  for i,chunk in enumerate(chunks(lines, splits)):
    static_changes_string = ''.join(chunk).strip()
    corruption = multicorrupt.Corruption(L, i, static_changes_string)
    out_paths.append(corruption.save(debug_dir,  '{}_DEBUG.n64'.format(basename)))
  time.sleep(1)
  multicorrupt.launch_many(out_paths)
