from functools import partial
from multiprocessing import Pool
import tkinter as tk
import time
import os

import struct
import xcffib
import xcffib.xproto

import Xlib
import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.error
import Xlib.ext.xtest

#function copied/slightly modified from some post in a thread somewhere I forgot where
def get_client_list(winname):
    def get_property_value(property_reply):
        assert isinstance(property_reply, xcffib.xproto.GetPropertyReply)
        
        if property_reply.format == 8:
            if 0 in property_reply.value:
                ret = []
                s = ''
                for o in property_reply.value:
                    if o == 0:
                        ret.append(s)
                        s = ''
                    else:
                        s += chr(o)
            else:
                ret = property_reply.value.buf()
            return ret.decode('utf8')
        elif property_reply.format in (16, 32):
            return list(struct.unpack('I' * property_reply.value_len,
                                      property_reply.value.buf()))

        return None
    clients = []
    c = xcffib.connect()
    root = c.get_setup().roots[0].root

    _NET_CLIENT_LIST = c.core.InternAtom(True, len('_NET_CLIENT_LIST'),
                                         '_NET_CLIENT_LIST').reply().atom

    raw_clientlist = c.core.GetProperty(False, root, _NET_CLIENT_LIST,
                                        xcffib.xproto.GetPropertyType.Any,
                                        0, 2 ** 32 - 1).reply()
    clientlist = get_property_value(raw_clientlist)
    for ident in clientlist:
        cookie = c.core.GetProperty(False, ident, xcffib.xproto.Atom.WM_CLASS,
                                            xcffib.xproto.GetPropertyType.Any,
                                            0, 2 ** 32 - 1)

        winclass = get_property_value(cookie.reply())
        if winname in winclass.split('\x00'):
            clients.append(ident)
    c.disconnect()
    return clients

def send_event(client_id, keystate, shiftstate, keycode):
  display = Xlib.display.Display()
  Xlib_root_window = display.screen().root
  window = display.create_resource_object('window', client_id)
  if keystate == 2:
    XEVENT = Xlib.protocol.event.KeyPress
  elif keystate == 3:
    XEVENT = Xlib.protocol.event.KeyRelease
  else:
    raise
  
  event = XEVENT(
      time = int(time.time()),
      root = Xlib_root_window,
      window = window,
      same_screen = 0, child = Xlib.X.NONE,
      root_x = 0, root_y = 0, event_x = 0, event_y = 0,
      state = shiftstate,
      detail = keycode
      )
  display.sync()
  p = window.send_event(event, propagate=False)
  display.sync()
  display.close()
  return True
def _send_event(x):
  return send_event(*x)

def onKeyPress(event):
  
  #global counter
  #counter = (counter + 1) % 50
  #if counter == 0:
  #  global clients
  #  clients = get_client_list('mupen64plus')
  
  #refetch before restarting mupen too
  if event.keysym in ['F9']:
    global clients
    clients = get_client_list('mupen64plus')
    
  if event.keysym == 'Escape':
    root.destroy()
  
  elif event.keysym in ['F10', 'F12']:
  #  os.system('xset r off')
    global clients
    clients = get_client_list('mupen64plus')
  #elif event.keysym == 'F11':
  #  os.system('xset r on')
  else:
    args = ((client_id, int(event.type), int(event.state), 
             int(event.keycode)) for client_id in clients)
    p = pool.map(_send_event, args)
    x = event
    print(x.keysym,x.type)
  #print(clients)
  #print(x.char, x.delta, x.height, x.keycode, x.keysym, 
  #      x.num, x.send_event, x.serial, x.state, x.time, 
  #      x.type, x.widget,x.width, x.x, x.x_root, x.y, x.y_root)
  return True

global clients
#global counter
#counter = 0
if __name__ == '__main__':  
  pool = Pool(100)
  clients = get_client_list('mupen64plus')
  
  root = tk.Tk()
  root.configure(background='maroon3')
  root.geometry('400x300')
  root.bind('<KeyPress>', onKeyPress)
  root.bind('<KeyRelease>', onKeyPress)
  root.mainloop()

