from multiprocessing import Pool
from functools import partial
import os,re,time,subprocess

from scripts import super_mario as SCRIPT

def get_window_ids():
  args = ['wmctrl', '-l']
  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
  s = p.stdout.read().decode('utf8').strip()
  L = s.split('\n')
  L = [x.split() for x in [re.sub('\s+', ' ', x) for x in L]]
  return [x[0] for x in L if 'Glide64mk2' in x[3]]


def recheck_id(id):
  return id in get_window_ids()

def exec_script(id):
  for j,line in enumerate(SCRIPT.main()):
    cmd = line.split()
    if cmd[0] == 'sleep':
      time.sleep(float(cmd[1]))
    else:
      args = ['xdotool', cmd[0], '--delay', '150', '--window', id, cmd[1]]
      p = subprocess.Popen(args)
      if j == 5 or (j % 50 == 0 and not recheck_id(id)):
        print('Cleared {}'.format(id))
        return False

def mainloop(ids):
  pool = Pool(processes=30)
  pool.map(exec_script, ids)
  
if __name__ == '__main__':
  ids = get_window_ids()
  mainloop(ids)
