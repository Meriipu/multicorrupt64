from multiprocessing import Pool, TimeoutError, cpu_count
from functools import partial
from sys import argv
import math
import random, array, os, subprocess, time
def calc_mupen_size(W,H):
    results = []
    for row_N in range(1,mupen_instances+1):
      row_width = math.floor(W/float(row_N))
      col_height = math.floor(row_width*(480/640.))
      if col_height*sum(divmod(mupen_instances, row_N)) <= H:
        results.append((row_width, col_height))
    return max(results)
#fit to region with space saved on right and bottom edge
mupen_instances = 25

screen_res = (1920,1200)
savespace = (400, 150)

RESW, RESH = screen_res[0]-savespace[0],  screen_res[1]-savespace[1]
instance_res = calc_mupen_size(RESW, RESH)

#USAGE:  python3 multicorrupt.py original_roms/BK64.n64
#outputs a bunch of roms to output_roms/ramdisk/ and launches them with mupen64plus
#depends on patched version of mupen that accepts --position parameter for window

class Corruption(object):
  def __init__(self, L, id, static_changes_string=None):
    self.id = id
    self.L = L[:]
    if static_changes_string:
      self.make_static_changes(static_changes_string)
    else:
      
      #self.mutate(20,  spot=mupen_instances*4 + id-1, step=1)
      
      #self.mutate(50,  spot=83.5, step=3)
      
      #self.mutate(100, 3 + 0.75, 6.25)
      self.mutate(100, 3 + 0.75, 6.25 + 10)
      
      
  def mutate(self, mutation_count, spot, step):
      '''count=number of changes to make in each instance,
         spot=byte to skip to in percent of total rom length (including 4096 first bytes)
         step=length of range to affect in percent of total rom length (overshooting rounds to full length)
      '''
      start_byte = int(max(4096 + 1,  (len(self.L)/100.0)*spot))
      end_byte = int(min(len(self.L)-1,  (len(self.L)/100.0)*(spot+step)))
      self.change_generator(start_byte,end_byte,mutation_count)
 
        
  def save(self, out_dir, basename='generic_filename.n64'):
    s2 = array.array('B', self.L)
    
    ext_index = basename.rindex('.')
    filename = '{}_corrupted_{}{}'.format(basename[0:ext_index],
                                          self.id,
                                          basename[ext_index:])
    
    out_path = os.path.join(out_dir, filename)
    print(out_path)
    #write the corrupted ROM
    with open(out_path, 'wb') as f:
      f.write(s2)
    
    #write a textfile where each line is an index (for rom byte), a space, and the new value for that index
    with open(out_path + '.changes', 'w') as f:
      f.write('\n'.join(' '.join(str(x) for x in tup) for tup in self.changes_made))
    
    return out_path

  def make_static_changes(self, static_changes_string):
    changelist = [[int(x) for x in x.split()] for x in static_changes_string.split('\n') if '#' not in x]
    self.changes_made = changelist
    for index,new_value in changelist:
      self.L[index] = new_value
  
  def change_generator(self, start_byte, end_byte, mutation_count):
    self.changes_made = []
    for i in range(mutation_count):
      index = random.randint(start_byte, end_byte)
      change = random.randint(0,255)
      self.L[index] = change
      #self.L[index] = (self.L[index] + random.randint(1,2)) % 255
      
      self.changes_made.append((index, self.L[index]))
      
def launch_single(path, instance_number):
  def calc_instance_position(i):  
    instances_per_row = (RESW)//instance_res[0]
    #X = [0,1,2, ... ,0,1,2,...]*width  + pixel_offset
    x = (i%instances_per_row)*instance_res[0]    +   2*(i%instances_per_row)
    #y = height*[0,0,0,...,1,1,1,...,2,2,2,...]  + pixel_offset
    y = instance_res[1]*(i//instances_per_row)   +   2*(i//instances_per_row)
    return x,y
  
  res = "%dx%d" % instance_res
  pos = "%d,%d" % calc_instance_position(instance_number)
  p = subprocess.Popen(['mupen64plus', '--resolution', res, '--position', pos, path])

def launch_many(path_list):
  for instance_number,out_path in enumerate(path_list):
    launch_single(out_path, instance_number)
      

def generate_corrupted_rom(L, out_dir, rom_path, i):
  corruption = Corruption(L, i+1) #start counting from 1
  path = corruption.save(out_dir=out_dir, basename=os.path.basename(rom_path))  
  return path

def load_rom(rom_path):
    with open(rom_path, 'rb') as f:
      return list(f.read())


def main(rom_path, changelist):
    L = load_rom(rom_path)
    if changelist:
      corruption = Corruption(L, 'static', changelist)
      out_path = corruption.save(out_dir=out_dir, basename=os.path.basename(rom_path))
      launch_single(out_path, 0)
    else:
      #generate corruptions first, then launch. Generating takes a while, so launching
      #all at once makes them almost synced, so that it is easier to notice differences
      pool = Pool(processes=cpu_count())
      func = partial(generate_corrupted_rom, L, out_dir, rom_path)
      out_paths = pool.map(func, range(mupen_instances))
      time.sleep(1)
      launch_many(out_paths)

if __name__ == '__main__':
    out_dir = os.path.join( os.path.dirname(argv[0]), 'output_roms', 'ramdisk' )
    if not os.path.exists(out_dir):
      os.mkdir(out_dir)

    if len(argv) > 2:
      with open(argv[2]) as f:
        static_changes_string = f.read().strip()
    else:
      static_changes_string = None
    in_path = argv[1]
    main(in_path, static_changes_string)