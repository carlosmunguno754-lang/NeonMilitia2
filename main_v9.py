"
NEON MILITIA v9 - SOLO FUNCIONAL GARANTIDO
Estratégia: código mínimo e robusto, sem canvas.before, sem draw_mc complexo
"""
import kivy
kivy.require('2.0.0')
from kivy.config import Config
Config.set('input','mouse','mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Ellipse, Line, RoundedRectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp

import math, random, json, socket, threading, queue, traceback

# ── Landscape ─────────────────────────────────────────────────────────────────
def force_landscape():
    try:
        from android.runnable import run_on_ui_thread
        @run_on_ui_thread
        def _r():
            from jnius import autoclass
            AI  = autoclass('android.content.pm.ActivityInfo')
            act = autoclass('org.kivy.android.PythonActivity').mActivity
            act.setRequestedOrientation(AI.SCREEN_ORIENTATION_SENSOR_LANDSCAPE)
    except: pass
    try:
        if Window.height > Window.width:
            Window.size = (Window.height, Window.width)
    except: pass

# ── Cores ─────────────────────────────────────────────────────────────────────
C = {
    'bg':    (0.02,0.02,0.06,1),
    'cyan':  (0.0, 1.0, 1.0, 1),
    'mag':   (1.0, 0.0, 1.0, 1),
    'grn':   (0.0, 1.0, 0.4, 1),
    'yel':   (1.0, 1.0, 0.0, 1),
    'org':   (1.0, 0.5, 0.0, 1),
    'red':   (1.0, 0.2, 0.2, 1),
    'blu':   (0.1, 0.4, 1.0, 1),
    'pur':   (0.6, 0.0, 1.0, 1),
    'wht':   (1.0, 1.0, 1.0, 1),
    'gry':   (0.5, 0.5, 0.5, 1),
    'dk':    (0.1, 0.1, 0.2, 1),
}

PC = [(0,1,1,1),(1,0,1,1),(0,1,0.4,1),(1,0.5,0,1),
      (1,0.2,0.2,1),(0.6,0,1,1),(1,1,0,1),(1,0.2,0.6,1)]

SKIN = [(1.0,0.85,0.70,1),(0.93,0.73,0.55,1),(0.78,0.57,0.38,1),
        (0.55,0.35,0.20,1),(0.30,0.18,0.10,1)]
HAIR = [(0.1,0.06,0.02,1),(0.45,0.28,0.10,1),(0.90,0.72,0.12,1),
        (0.72,0.18,0.05,1),(0.75,0.75,0.75,1),(0.05,0.85,0.85,1)]
CLOTH= [(0.1,0.1,0.8,1),(0.8,0.1,0.1,1),(0.1,0.7,0.1,1),(0.7,0.5,0,1),
        (0.5,0.1,0.7,1),(0.1,0.1,0.1,1),(0.8,0.8,0.8,1),(0,0.85,0.85,1)]

# ── Armas ─────────────────────────────────────────────────────────────────────
WEAPONS = {
    'pistol':  {'name':'Pistola', 'dmg':20,'ammo':20,'res':50,'spd':620,'col':C['cyan'],'rate':0.38},
    'rifle':   {'name':'Rifle',   'dmg':30,'ammo':20,'res':50,'spd':820,'col':C['grn'], 'rate':0.14},
    'shotgun': {'name':'Shotgun', 'dmg':50,'ammo':20,'res':50,'spd':520,'col':C['org'], 'rate':0.78},
    'sniper':  {'name':'Sniper',  'dmg':50,'ammo':20,'res':50,'spd':1250,'col':C['mag'],'rate':1.20},
    'smg':     {'name':'SMG',     'dmg':20,'ammo':20,'res':50,'spd':720,'col':C['yel'], 'rate':0.07},
    'launcher':{'name':'Launcher','dmg':50,'ammo':20,'res':50,'spd':410,'col':C['red'], 'rate':1.50},
}

# ── Mundos ────────────────────────────────────────────────────────────────────
WORLDS = [
    {'id':0,'name':'Neon City',    'bg':(0.02,0.02,0.09,1),'pc':C['cyan'],'ac':C['mag'], 'grav':600,
     'plats':[(0,40,1280,26),(80,175,210,18),(380,175,210,18),(680,175,210,18),(970,175,210,18),
              (220,310,185,18),(520,310,185,18),(820,310,185,18),(80,445,260,18),(460,445,210,18),
              (800,445,260,18),(290,560,175,18),(660,560,175,18)]},
    {'id':1,'name':'Vulcão',       'bg':(0.11,0.02,0.02,1),'pc':C['org'],'ac':C['red'], 'grav':660,
     'plats':[(0,40,1280,26),(0,185,145,18),(265,185,145,18),(520,285,145,18),(775,185,145,18),
              (1020,185,145,18),(140,365,205,18),(445,405,205,18),(700,365,205,18),(950,405,205,18)]},
    {'id':2,'name':'Ártico',       'bg':(0.04,0.07,0.15,1),'pc':C['blu'],'ac':C['wht'], 'grav':545,
     'plats':[(0,40,1280,26),(45,150,255,18),(395,195,205,18),(695,150,255,18),(1005,195,205,18),
              (195,320,165,18),(475,340,165,18),(755,320,165,18),(95,470,310,18),(495,490,205,18)]},
    {'id':3,'name':'Floresta',     'bg':(0.02,0.06,0.02,1),'pc':C['grn'],'ac':C['cyan'],'grav':575,
     'plats':[(0,40,1280,26),(75,130,185,18),(325,195,185,18),(575,130,185,18),(825,195,185,18),
              (1075,130,185,18),(195,290,165,18),(475,330,165,18),(725,290,165,18),(95,450,225,18)]},
    {'id':4,'name':'Espaço',       'bg':(0.01,0.01,0.05,1),'pc':C['pur'],'ac':C['mag'], 'grav':275,
     'plats':[(0,40,1280,26),(45,110,205,14),(345,170,205,14),(645,110,205,14),(945,170,205,14),
              (195,265,155,14),(495,305,155,14),(795,265,155,14),(95,415,255,14),(445,455,255,14)]},
    {'id':5,'name':'Deserto',      'bg':(0.11,0.08,0.01,1),'pc':C['yel'],'ac':C['org'], 'grav':710,
     'plats':[(0,40,1280,26),(0,150,185,18),(245,210,185,18),(495,150,185,18),(745,210,185,18),
              (1045,150,185,18),(145,340,205,18),(425,380,205,18),(695,340,205,18),(80,500,245,18)]},
    {'id':6,'name':'Mar Profundo', 'bg':(0.01,0.04,0.11,1),'pc':C['cyan'],'ac':C['blu'],'grav':375,
     'plats':[(0,40,1280,26),(45,140,225,18),(375,190,225,18),(675,140,225,18),(975,190,225,18),
              (195,300,175,18),(495,340,175,18),(775,300,175,18),(95,460,285,18),(475,490,285,18)]},
    {'id':7,'name':'Custom',       'bg':(0.04,0.02,0.09,1),'pc':C['mag'],'ac':C['pur'], 'grav':600,
     'plats':[(0,40,1280,26),(95,190,205,18),(445,190,205,18),(795,190,205,18),
              (245,370,185,18),(635,370,185,18),(95,530,305,18),(875,530,305,18)]},
]

def def_av():
    return {'name':'Player','skin':0,'hair_style':1,'hair_color':0,'beard':0,
            'shirt':0,'shirt_col':0,'pants':0,'pants_col':5,
            'shoe':0,'shoe_col':5,'player_col':0,'weapon':'pistol'}

# ── Estado Global ─────────────────────────────────────────────────────────────
class GS:
    players   = {}
    zombies   = []
    local_pid = 0
    world_id  = 0
    net_role  = 'solo'
    avatar    = def_av()
    bullets   = []
    explosions= []
    bombs     = []
    gas_clouds= []
    smoke_clouds=[]
    pickups   = []
    hud_layout= {}

# ── Jogador ───────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, pid, av=None):
        if av is None: av = def_av()
        self.pid    = pid
        self.name   = av.get('name','Player')
        self.color  = PC[av.get('player_col',0) % len(PC)]
        self.avatar = dict(av)
        self.x = 200.0 + pid*90; self.y = 400.0
        self.vx= 0.0; self.vy = 0.0
        self.hp= 100; self.alive = True
        self.facing = 1; self.on_ground = False
        self.fuel = 100.0; self.turbo = False; self.shield = 0
        self.invisible = False; self.invis_t = 0.0
        self.kills = 0; self.deaths = 0
        self.weapons = {k: dict(v) for k,v in list(WEAPONS.items())[:2]}
        self.active = av.get('weapon','pistol')
        if self.active not in self.weapons:
            self.weapons[self.active] = dict(WEAPONS[self.active])
        self.fire_cd = 0.0
        self.bombs_n = 3; self.gas_n = 2; self.smoke_n = 2
        self.gas_dbf = 0.0
        self.w = 28; self.h = 44
        self.af = 0; self.at = 0.0

    def wep(self):
        return self.weapons.get(self.active, list(self.weapons.values())[0])

    def take_dmg(self, d):
        if self.invisible: return
        if self.gas_dbf > 0: d = max(1, int(d * 0.9))
        if self.shield > 0:
            ab = min(self.shield, d); self.shield -= ab; d -= ab
        self.hp = max(0, self.hp - d)
        if self.hp <= 0: self.alive = False

    def can_fire(self):
        return self.fire_cd <= 0 and self.wep()['ammo'] > 0

    def do_fire(self):
        if not self.can_fire(): return False
        self.wep()['ammo'] -= 1
        self.fire_cd = self.wep()['rate']
        return True

    def reload(self):
        k = self.active; w = self.weapons[k]
        need = WEAPONS[k]['ammo'] - w['ammo']
        take = min(need, w['res'])
        w['ammo'] += take; w['res'] -= take

    def cycle(self):
        keys = list(self.weapons.keys())
        i = keys.index(self.active)
        self.active = keys[(i+1) % len(keys)]

# ── Zumbi ─────────────────────────────────────────────────────────────────────
class Zombie:
    _id = 0
    def __init__(self, x, y):
        Zombie._id += 1; self.zid = Zombie._id
        self.x=float(x); self.y=float(y)
        self.vx=0.0; self.vy=0.0
        self.hp=50; self.alive=True; self.on_ground=False
        self.facing=1; self.af=0; self.at=0.0; self.attack_cd=0.0
        self.w=24; self.h=40

# ── Rede ──────────────────────────────────────────────────────────────────────
class Net:
    role='solo'; rx=queue.Queue()
    _srv=None; _conns=[]; _csock=None; _run=False; _lock=threading.Lock()

    @classmethod
    def start_host(cls):
        cls._run=True; cls.role='host'; cls._conns=[]
        threading.Thread(target=cls._host_loop,daemon=True).start()

    @classmethod
    def _host_loop(cls):
        try:
            srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            srv.bind(('',55433)); srv.listen(20); srv.settimeout(0.5); cls._srv=srv
            while cls._run:
                try:
                    conn,_=srv.accept(); conn.settimeout(0.5)
                    with cls._lock: cls._conns.append(conn)
                    threading.Thread(target=cls._recv,args=(conn,),daemon=True).start()
                except socket.timeout: pass
        except Exception as e: print('[HOST]',e)

    @classmethod
    def _recv(cls,conn):
        buf=b''
        while cls._run:
            try:
                d=conn.recv(4096)
                if not d: break
                buf+=d
                while b'\n' in buf:
                    line,buf=buf.split(b'\n',1)
                    try:
                        msg=json.loads(line.decode()); cls.rx.put(msg)
                        cls._bcast(line+b'\n',exclude=conn)
                    except: pass
            except socket.timeout: pass
            except: break
        with cls._lock:
            if conn in cls._conns: cls._conns.remove(conn)
        try: conn.close()
        except: pass

    @classmethod
    def _bcast(cls,data,exclude=None):
        with cls._lock:
            dead=[]
            for c in cls._conns:
                if c is exclude: continue
                try: c.sendall(data)
                except: dead.append(c)
            for d in dead: cls._conns.remove(d)

    @classmethod
    def start_client(cls,ip):
        cls._run=True; cls.role='client'
        threading.Thread(target=cls._client_loop,args=(ip,),daemon=True).start()

    @classmethod
    def _client_loop(cls,ip):
        buf=b''
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(6.0); s.connect((ip,55433)); s.settimeout(0.5); cls._csock=s
            while cls._run:
                try:
                    d=s.recv(4096)
                    if not d: break
                    buf+=d
                    while b'\n' in buf:
                        line,buf=buf.split(b'\n',1)
                        try: cls.rx.put(json.loads(line.decode()))
                        except: pass
                except socket.timeout: pass
                except: break
        except Exception as e: cls.rx.put({'type':'connect_error','msg':str(e)})
        cls._csock=None

    @classmethod
    def send(cls,msg):
        if cls.role=='solo': return
        data=(json.dumps(msg)+'\n').encode()
        if cls.role=='host': cls._bcast(data)
        elif cls.role=='client' and cls._csock:
            try: cls._csock.sendall(data)
            except: pass

    @classmethod
    def stop(cls):
        cls._run=False; cls.role='solo'
        for attr in ('_srv','_csock'):
            obj=getattr(cls,attr,None)
            if obj:
                try: obj.close()
                except: pass
                setattr(cls,attr,None)
        with cls._lock:
            for c in cls._conns:
                try: c.close()
                except: pass
            cls._conns.clear()

    @classmethod
    def my_ip(cls):
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(('8.8.8.8',80)); ip=s.getsockname()[0]; s.close(); return ip
        except: return '127.0.0.1'

# ── UI helpers ────────────────────────────────────────────────────────────────
def mk_btn(text, col=None, h=dp(52), sh=(1,None), **kw):
    if col is None: col = C['cyan']
    b = Button(text=text, size_hint=sh, height=h, font_size=sp(15), bold=True,
               background_normal='', background_color=C['dk'], color=col, **kw)
    with b.canvas.after:
        Color(*col[:3], 0.75)
        b._ln = Line(rounded_rectangle=(0,0,10,10,6), width=1.8)
    def _u(i,v): i._ln.rounded_rectangle = (*i.pos,*i.size,6)
    b.bind(pos=_u, size=_u)
    return b

def mk_lbl(text, col=None, fs=sp(18), **kw):
    if col is None: col = C['cyan']
    return Label(text=text, color=col, font_size=fs, bold=True, markup=True, **kw)

# ── Botão de acção (Widget puro, sem herdar Button) ───────────────────────────
class ABtn(Widget):
    def __init__(self, bid, label, col, cb, **kw):
        super().__init__(**kw)
        self.bid=bid; self._lbl=label; self._col=col; self._cb=cb
        self._uid=None; self._edit=False; self._lw=None
        self._drag_uid=None; self._drag_start=None
        self.bind(pos=self._draw, size=self._draw)

    def set_edit(self, v):
        self._edit = v; self._draw()

    def _draw(self, *a):
        if self.width < 4 or self.height < 4: return
        self.canvas.clear()
        if self._lw and self._lw.parent: self.remove_widget(self._lw)
        cx=self.x+self.width/2; cy=self.y+self.height/2
        r = max(4.0, min(self.width, self.height)/2 - dp(2))
        with self.canvas:
            if self._edit:
                Color(1,1,0,0.7); Line(circle=(cx,cy,r+dp(4)),width=2.5)
            Color(*self._col[:3], 0.45 if self._uid else 0.22)
            Ellipse(pos=(cx-r,cy-r), size=(r*2,r*2))
            Color(*self._col[:3], 1.0 if self._uid else 0.80)
            Line(circle=(cx,cy,r), width=2.2)
            if self._edit:
                Color(1,1,0,0.9)
                Line(points=[cx-r+dp(4),cy,cx+r-dp(4),cy],width=2)
                Line(points=[cx,cy-r+dp(4),cx,cy+r-dp(4)],width=2)
        lw = Label(text=self._lbl, color=(*self._col[:3],1),
                   font_size=sp(10), bold=True,
                   pos=self.pos, size=self.size,
                   halign='center', valign='middle')
        lw.text_size = self.size
        self.add_widget(lw); self._lw = lw

    def _hit(self, tx, ty):
        if self.width < 4: return False
        cx=self.x+self.width/2; cy=self.y+self.height/2
        return math.sqrt((tx-cx)**2+(ty-cy)**2) <= min(self.width,self.height)/2 + dp(6)

    def on_touch_down(self, t):
        if not self._hit(t.x, t.y): return False
        if self._edit and self._drag_uid is None:
            self._drag_uid = t.uid
            self._drag_start = (t.x, t.y, self.x, self.y)
            return True
        if self._uid is None and not self._edit:
            self._uid = t.uid; self._draw(); self._cb(); return True

    def on_touch_move(self, t):
        if self._edit and t.uid == self._drag_uid and self._drag_start:
            sx,sy,ox,oy = self._drag_start
            nx = max(0, min(Window.width-self.width,   ox + t.x - sx))
            ny = max(0, min(Window.height-self.height, oy + t.y - sy))
            self.pos = (nx, ny)
            GS.hud_layout[self.bid] = {'x':nx,'y':ny,'sz':self.width}
            return True

    def on_touch_up(self, t):
        if t.uid == self._drag_uid:
            self._drag_uid=None; self._drag_start=None; return True
        if t.uid == self._uid:
            self._uid=None; self._draw(); return True

    def resize(self, delta):
        sz = max(dp(36), min(dp(110), self.width+delta))
        self.size = (sz, sz)
        GS.hud_layout[self.bid] = {'x':self.x,'y':self.y,'sz':sz}

    def on_pos(self,*a):
        if self._lw: self._lw.pos=self.pos
    def on_size(self,*a):
        if self._lw: self._lw.size=self.size; self._lw.text_size=self.size

# ── Joystick ──────────────────────────────────────────────────────────────────
class Joystick(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.dx=0.0; self.dy=0.0; self._uid=None
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *a):
        if self.width < 4: return
        self.canvas.clear()
        cx=self.center_x; cy=self.center_y; ro=dp(54); ri=dp(21)
        with self.canvas:
            Color(0.1,0.1,0.3,0.6); Ellipse(pos=(cx-ro,cy-ro),size=(ro*2,ro*2))
            Color(*C['cyan'][:3],0.7); Line(circle=(cx,cy,ro),width=2.2)
            Color(*C['cyan'][:3],0.18)
            Line(points=[cx-ro,cy,cx+ro,cy],width=1)
            Line(points=[cx,cy-ro,cx,cy+ro],width=1)
            tx=cx+self.dx*ro; ty=cy+self.dy*ro
            Color(*C['cyan'][:3],0.95); Ellipse(pos=(tx-ri,ty-ri),size=(ri*2,ri*2))

    def on_touch_down(self,t):
        cx=self.center_x; cy=self.center_y
        if math.sqrt((t.x-cx)**2+(t.y-cy)**2)<=dp(62) and self._uid is None:
            self._uid=t.uid; self._calc(t.x,t.y); return True

    def on_touch_move(self,t):
        if t.uid==self._uid: self._calc(t.x,t.y); return True

    def on_touch_up(self,t):
        if t.uid==self._uid:
            self._uid=None; self.dx=0.0; self.dy=0.0; self._draw(); return True

    def _calc(self,tx,ty):
        cx=self.center_x; cy=self.center_y
        ddx=tx-cx; ddy=ty-cy; d=math.sqrt(ddx*ddx+ddy*ddy); ro=dp(54)
        if d>0: sc=min(1.0,d/ro); self.dx=ddx/d*sc; self.dy=ddy/d*sc
        else: self.dx=0.0; self.dy=0.0
        self._draw()

# ── Desenho avatar Minecraft (seguro) ─────────────────────────────────────────
def draw_avatar(canvas, av, ox, oy, sc=1.0, facing=1, af=0, alpha=1.0, gun_col=None):
    """Desenha avatar em blocos Minecraft. Totalmente seguro — sem tamanhos zero."""
    if sc < 0.5: return
    skin = SKIN[min(av.get('skin',0), len(SKIN)-1)]
    hcol = HAIR[min(av.get('hair_color',0), len(HAIR)-1)]
    scol = CLOTH[min(av.get('shirt_col',0), len(CLOTH)-1)]
    pcol = CLOTH[min(av.get('pants_col',5), len(CLOTH)-1)]
    ecol = CLOTH[min(av.get('shoe_col',5), len(CLOTH)-1)]
    hst  = av.get('hair_style',1)
    bst  = av.get('beard',0)
    sst  = av.get('shirt',0)
    pst  = av.get('pants',0)
    est  = av.get('shoe',0)
    gc   = gun_col if gun_col else C['cyan']

    def R(x,y,w,h,col):
        sw2 = max(1.0, w*sc); sh2 = max(1.0, h*sc)
        with canvas:
            Color(col[0],col[1],col[2],col[3]*alpha)
            Rectangle(pos=(ox+x*sc, oy+y*sc), size=(sw2,sh2))

    # Sapatos
    shoe_h = {0:8,1:11,2:5,3:7,4:11}.get(est,8)
    R(0,0,12,shoe_h,ecol); R(16,0,12,shoe_h,ecol)

    # Calças
    lb=shoe_h; lh=10 if pst==3 else 16
    R(0,lb,12,lh,pcol); R(16,lb,12,lh,pcol)
    if pst==1: R(0,lb+lh//2,12,2,(0.4,0.55,0.85,1)); R(16,lb+lh//2,12,2,(0.4,0.55,0.85,1))
    elif pst==3: R(0,lb+lh,12,6,skin); R(16,lb+lh,12,6,skin)

    # Cinto
    wy=lb+lh; R(0,wy,28,4,(0.2,0.15,0.08,1))

    # Corpo
    by2=wy+4; bh=20
    if sst==1: R(0,by2,28,bh,skin); R(4,by2,20,bh,scol)
    elif sst==2: R(0,by2,28,bh,scol); R(10,by2+2,8,max(1,bh-2),(0.9,0.9,0.9,1))
    elif sst==3: R(0,by2,28,bh,scol); R(2,by2+2,24,max(1,bh-4),(0.7,0.7,0.8,1))
    else: R(0,by2,28,bh,scol)

    # Braços com swing
    sw = int(math.sin(af*1.57)*3)
    R(-8,by2+sw,  8,max(1,bh-4),scol); R(-8,by2+6+sw,8,max(1,bh-10),skin)
    R(28,by2-sw,  8,max(1,bh-4),scol); R(28,by2+6-sw,8,max(1,bh-10),skin)

    # Arma
    if facing>0: R(28,by2+4,16,5,gc)
    else:        R(-16,by2+4,16,5,gc)

    # Pescoço
    ny=by2+bh; R(10,ny,8,4,skin)

    # Cabeça
    hy=ny+4; hw=28; hh=24
    R(0,hy,hw,hh,skin)
    with canvas:
        Color(0,0,0,0.4*alpha)
        Line(rectangle=(ox,oy+hy*sc,max(1,hw*sc),max(1,hh*sc)),width=1.2)

    # Dois olhos (sempre visíveis de frente)
    ey=hy+10
    R(5, ey,5,5,(0.05,0.05,0.05,1)); R(6, ey+1,2,3,(1,1,1,1))
    R(18,ey,5,5,(0.05,0.05,0.05,1)); R(19,ey+1,2,3,(1,1,1,1))
    R(13,ey+2,2,2,(0.5,0.3,0.2,1))   # nariz
    R(7, hy+4,14,2,(0.55,0.25,0.15,1))  # boca

    # Barba
    if bst==1: R(9,hy+1,10,4,hcol)
    elif bst==2: R(5,hy+1,18,5,hcol); R(3,hy+3,4,6,hcol); R(21,hy+3,4,6,hcol)
    elif bst==3: R(4,hy+1,20,8,hcol); R(2,hy+3,4,8,hcol); R(22,hy+3,4,8,hcol)
    elif bst==4: R(6,hy+6,7,3,hcol); R(15,hy+6,7,3,hcol)

    # Cabelo
    ht=hy+hh
    if hst==1: R(0,ht,hw,4,hcol); R(-2,ht-2,4,hh+2,hcol); R(hw-2,ht-2,4,hh+2,hcol)
    elif hst==2: R(0,ht,hw,6,hcol); R(-4,ht-6,6,hh+8,hcol); R(hw-2,ht-6,6,hh+8,hcol)
    elif hst==3: R(0,ht,hw,8,hcol); R(-4,ht-10,6,hh+12,hcol); R(hw-2,ht-10,6,hh+26,hcol)
    elif hst==4: R(10,ht,8,12,hcol); R(8,ht+8,12,6,hcol)

# ── Zumbi Minecraft ───────────────────────────────────────────────────────────
def draw_zombie(canvas, x, y, sc=1.0, facing=1, af=0):
    if sc < 0.5: return
    skin=(0.22,0.55,0.22,1); dark=(0.16,0.40,0.16,1); rag=(0.30,0.20,0.10,1)
    def R(rx,ry,rw,rh,col):
        with canvas:
            Color(*col)
            Rectangle(pos=(x+rx*sc,y+ry*sc),size=(max(1.0,rw*sc),max(1.0,rh*sc)))
    R(1,0,10,7,dark); R(15,0,10,7,dark)
    R(0,7,11,14,rag); R(15,7,11,14,rag)
    R(0,25,26,18,rag)
    if facing>0: R(26,31,8,16,dark); R(-8,25,8,16,skin)
    else:        R(-8,31,8,16,dark); R(26,25,8,16,skin)
    R(9,43,8,4,skin)
    R(0,47,26,22,skin)
    with canvas:
        Color(0,0,0,0.45); Line(rectangle=(x,y+47*sc,max(1,26*sc),max(1,22*sc)),width=1)
    R(0,69,26,5,dark); R(-2,67,4,22,dark); R(24,67,4,22,dark)
    R(3,55,5,5,(0.9,0.1,0.1,1)); R(4,56,2,3,(1,0.5,0.5,1))
    R(18,55,5,5,(0.9,0.1,0.1,1)); R(19,56,2,3,(1,0.5,0.5,1))
    R(7,49,12,3,(0.1,0.3,0.1,1))

# ── Portal ────────────────────────────────────────────────────────────────────
def draw_portal(canvas, px, py, t):
    pw=60; ph=90; pulse=0.7+0.3*math.sin(t*4)
    with canvas:
        Color(0.3,0.0,0.5,0.45*pulse)
        Ellipse(pos=(px-pw//2-8,py-4),size=(pw+16,ph+8))
        Color(0.0,0.8,0.2,0.65*pulse)
        Ellipse(pos=(px-pw//2,py),size=(pw,ph))
        Color(0.6,0.0,1.0,0.85)
        Line(ellipse=(px-pw//2,py,pw,ph),width=2.5)
        for i in range(6):
            ang=t*2+i*1.05; r2=pw*0.4
            ppx=px+math.cos(ang)*r2; ppy=py+ph*0.5+math.sin(ang)*ph*0.35
            Color(0.0,1.0,0.4,0.6); Ellipse(pos=(ppx-3,ppy-3),size=(6,6))

# ═══════════════════════════════════════════════════════════════════════════════
#  CAPA
# ═══════════════════════════════════════════════════════════════════════════════
class CoverScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw); self._t = 0.0
        root = FloatLayout(); self.add_widget(root)
        with root.canvas.before:
            self._bgc = Color(*C['bg'])
            self._bgr = Rectangle(pos=(0,0), size=Window.size)
        Window.bind(size=lambda *a: setattr(self._bgr,'size',Window.size))
        self._scene = Widget(size_hint=(1,1)); root.add_widget(self._scene)

        root.add_widget(Label(text='[b]NEON MILITIA[/b]',markup=True,
            font_size=sp(46),color=C['cyan'],bold=True,
            size_hint=(1,None),height=dp(64),pos_hint={'x':0,'top':0.99}))
        root.add_widget(Label(text='[i]Future Warfare  v9[/i]',markup=True,
            font_size=sp(15),color=C['mag'],
            size_hint=(1,None),height=dp(24),pos_hint={'x':0,'top':0.87}))

        menu = BoxLayout(orientation='vertical',spacing=dp(9),
                         size_hint=(None,None),size=(dp(265),dp(315)),
                         pos_hint={'x':0.02,'center_y':0.40})
        root.add_widget(menu)
        for txt,col,cb in [
            ('⚔  SOLO',         C['cyan'],self._solo),
            ('🌐 MULTIJOGADOR', C['grn'], self._multi),
            ('🎨 AVATAR',       C['mag'], self._avatar),
            ('🗺  MUNDOS',      C['yel'], self._worlds),
            ('⚙  CONFIG HUD',  C['pur'], self._hud),
        ]:
            b = mk_btn(txt,col,h=dp(56)); b.bind(on_release=lambda *a,fn=cb:fn())
            menu.add_widget(b)

        Clock.schedule_interval(self._anim, 1/30)

    def _anim(self, dt):
        self._t += dt; t=self._t; sc=self._scene
        sw=Window.width; sh=Window.height
        if sw < 10: return
        sc.canvas.clear()
        with sc.canvas:
            # Chão
            Color(0.04,0.06,0.04,1); Rectangle(pos=(0,0),size=(sw,sh*0.35))
            Color(0,0.8,0.2,0.14)
            for i in range(10):
                Line(points=[sw/2,sh*0.35,sw*i/9,0],width=1)
            # Prédios
            for bx,bw,bh in [(60,80,200),(200,65,260),(360,90,175),
                               (620,75,240),(840,95,190),(1070,80,220)]:
                Color(0.04,0.06,0.12,1); Rectangle(pos=(bx,sh*0.35),size=(bw,bh))
                Color(1,0.9,0.3,0.3+0.2*math.sin(t*1.2+bx*0.01))
                for wy in range(int(sh*0.35)+15, int(sh*0.35+bh)-10, 24):
                    for wx in range(bx+8, bx+bw-8, 16):
                        Rectangle(pos=(wx,wy),size=(9,13))
            Color(*C['cyan'][:3],0.55); Line(points=[0,sh*0.35,sw,sh*0.35],width=2)
            # Grade céu
            Color(0,1,1,0.04); step=dp(80)
            for xx in range(0,int(sw)+int(step),int(step)):
                Line(points=[xx,sh*0.35,xx,sh],width=1)
            for yy in range(int(sh*0.35),int(sh)+int(step),int(step)):
                Line(points=[0,yy,sw,yy],width=1)
            # Scan line
            sl=sh*0.35+((sh*0.65)*((t*0.08)%1.0))
            Color(0,1,1,0.10); Line(points=[0,sl,sw,sl],width=2)
            # Plataforma
            Color(*C['cyan'][:3],0.75); Rectangle(pos=(sw*0.3,sh*0.32),size=(sw*0.4,6))

        # 4 Guerreiros diferentes à direita
        warriors=[
            {'skin':0,'hair_style':2,'hair_color':0,'beard':2,'shirt':3,'shirt_col':1,
             'pants':4,'pants_col':5,'shoe':1,'shoe_col':5,'weapon':'rifle','player_col':4},
            {'skin':2,'hair_style':4,'hair_color':5,'beard':0,'shirt':2,'shirt_col':4,
             'pants':1,'pants_col':0,'shoe':0,'shoe_col':0,'weapon':'shotgun','player_col':5},
            {'skin':1,'hair_style':1,'hair_color':3,'beard':3,'shirt':1,'shirt_col':0,
             'pants':2,'pants_col':5,'shoe':4,'shoe_col':5,'weapon':'sniper','player_col':2},
            {'skin':3,'hair_style':0,'hair_color':1,'beard':4,'shirt':0,'shirt_col':7,
             'pants':3,'pants_col':2,'shoe':2,'shoe_col':3,'weapon':'smg','player_col':6},
        ]
        positions=[(sw*0.56,sh*0.32),(sw*0.67,sh*0.32),(sw*0.78,sh*0.32),(sw*0.89,sh*0.32)]
        for i,(wx,wy) in enumerate(positions):
            w=warriors[i]
            try:
                draw_avatar(sc.canvas,w,wx,wy,sc=dp(1.5),facing=1,
                            af=int(t*3+i)%4,
                            gun_col=WEAPONS[w['weapon']]['col'])
            except: pass
            aura_y=wy+dp(105)+math.sin(t*2+i)*dp(7)
            with sc.canvas:
                Color(*PC[w['player_col']][:3],0.55+0.28*math.sin(t*3+i))
                Ellipse(pos=(wx+dp(4),aura_y),size=(dp(16),dp(16)))

        # Personagem principal no centro
        try:
            draw_avatar(sc.canvas,GS.avatar,sw*0.46,sh*0.32,sc=dp(2.0),
                        facing=1,af=int(t*4)%4,
                        gun_col=WEAPONS[GS.avatar.get('weapon','pistol')]['col'])
        except: pass

    def _solo(self):
        # Limpar estado antes de entrar
        GS.net_role='solo'; Net.stop()
        GS.local_pid=0
        GS.players={0:Player(0,GS.avatar)}
        GS.zombies=[]
        GS.bullets=[]; GS.explosions=[]; GS.bombs=[]
        GS.gas_clouds=[]; GS.smoke_clouds=[]; GS.pickups=[]
        self.manager.current='game'

    def _multi(self):  self.manager.current='lobby'
    def _avatar(self): self.manager.current='avatar'
    def _worlds(self): self.manager.current='worlds'
    def _hud(self):    self.manager.current='hudcfg'

# ═══════════════════════════════════════════════════════════════════════════════
#  AVATAR — abas
# ═══════════════════════════════════════════════════════════════════════════════
class AvatarScreen(Screen):
    TABS=['NOME & COR','CABEÇA','CORPO','PERNAS','ARMA']
    def __init__(self,**kw):
        super().__init__(**kw); self._av=dict(GS.avatar); self._tab=0
        root=FloatLayout(); self.add_widget(root)
        with root.canvas.before:
            Color(*C['bg']); Rectangle(pos=(0,0),size=Window.size)
        root.add_widget(mk_lbl('[b]AVATAR[/b]',fs=sp(24),
            size_hint=(1,None),height=dp(40),pos_hint={'x':0,'top':1}))
        tbar=BoxLayout(size_hint=(None,None),size=(dp(530),dp(36)),
                       spacing=dp(4),pos_hint={'x':0.01,'top':0.90})
        root.add_widget(tbar); self._tbtns=[]
        for i,t in enumerate(self.TABS):
            b=Button(text=t,background_normal='',
                     background_color=C['cyan'] if i==0 else C['dk'],
                     color=C['bg'] if i==0 else C['wht'],font_size=sp(11),bold=True)
            b.bind(on_release=lambda btn,idx=i:self._switch(idx))
            tbar.add_widget(b); self._tbtns.append(b)
        self._ct=FloatLayout(size_hint=(None,None),size=(dp(550),dp(340)),
                              pos_hint={'x':0.01,'top':0.85})
        root.add_widget(self._ct)
        pnl=FloatLayout(size_hint=(None,None),size=(dp(186),dp(368)),
                        pos_hint={'right':0.99,'top':0.97})
        with pnl.canvas.before:
            Color(0.07,0.07,0.16,1); pnl._bg=Rectangle(pos=pnl.pos,size=pnl.size)
        pnl.bind(pos=lambda i,v:setattr(i._bg,'pos',i.pos),
                 size=lambda i,v:setattr(i._bg,'size',i.size))
        root.add_widget(pnl)
        pnl.add_widget(mk_lbl('Preview',fs=sp(12),col=C['gry'],
            size_hint=(1,None),height=dp(20),pos_hint={'x':0,'top':1}))
        self._prev=Widget(size_hint=(None,None),size=(dp(88),dp(145)),
                          pos_hint={'center_x':0.5,'center_y':0.50})
        pnl.add_widget(self._prev)
        self._pname=mk_lbl('',fs=sp(11),col=C['yel'],
            size_hint=(1,None),height=dp(20),pos_hint={'x':0,'y':0.02})
        pnl.add_widget(self._pname)
        br=BoxLayout(size_hint=(None,None),size=(dp(375),dp(46)),
                     spacing=dp(10),pos_hint={'x':0.01,'y':0.01})
        root.add_widget(br)
        bk=mk_btn('← VOLTAR',C['red'],h=dp(46)); bk.bind(on_release=self._back)
        sv=mk_btn('💾 SALVAR',C['grn'],h=dp(46)); sv.bind(on_release=self._save)
        br.add_widget(bk); br.add_widget(sv)
        self._build(0); Clock.schedule_interval(self._upd,1/15)

    def _switch(self,idx):
        self._tab=idx
        for i,b in enumerate(self._tbtns):
            b.background_color=C['cyan'] if i==idx else C['dk']
            b.color=C['bg'] if i==idx else C['wht']
        self._build(idx)

    def _build(self,idx):
        self._ct.clear_widgets()
        [self._t0,self._t1,self._t2,self._t3,self._t4][idx]()

    def _crow(self,c,lbl,key,pal,top):
        c.add_widget(mk_lbl(lbl,fs=sp(13),size_hint=(None,None),
            size=(dp(200),dp(22)),pos_hint={'x':0,'top':top}))
        g=GridLayout(cols=len(pal),spacing=dp(5),size_hint=(None,None),
                     size=(dp(len(pal)*36),dp(34)),pos_hint={'x':0,'top':top-0.08})
        for i,col in enumerate(pal):
            b=Button(background_normal='',background_color=col,
                     size_hint=(None,None),size=(dp(32),dp(30)))
            b.bind(on_release=lambda btn,k=key,v=i:self._av.update({k:v}))
            g.add_widget(b)
        c.add_widget(g)

    def _srow(self,c,lbl,key,opts,top,col):
        c.add_widget(mk_lbl(lbl,fs=sp(13),size_hint=(None,None),
            size=(dp(200),dp(22)),pos_hint={'x':0,'top':top}))
        row=BoxLayout(size_hint=(None,None),size=(dp(510),dp(36)),
                      spacing=dp(4),pos_hint={'x':0,'top':top-0.08})
        for opt in opts:
            b=mk_btn(opt['name'],col,h=dp(34))
            b.bind(on_release=lambda btn,k=key,v=opt['id']:self._av.update({k:v}))
            row.add_widget(b)
        c.add_widget(row)

    def _t0(self):
        c=self._ct
        c.add_widget(mk_lbl('Nome:',fs=sp(13),size_hint=(None,None),
            size=(dp(80),dp(22)),pos_hint={'x':0,'top':0.97}))
        ni=TextInput(text=self._av.get('name','Player'),multiline=False,
            font_size=sp(16),background_color=(0.08,0.08,0.22,1),
            foreground_color=C['wht'],cursor_color=C['cyan'],
            size_hint=(None,None),size=(dp(315),dp(42)),pos_hint={'x':0,'top':0.88})
        ni.bind(text=lambda i,v:self._av.update({'name':v}))
        c.add_widget(ni)
        self._crow(c,'Cor do Jogador:','player_col',PC,0.72)
        self._crow(c,'Tom de Pele:','skin',SKIN,0.45)

    def _t1(self):
        c=self._ct
        self._srow(c,'Cabelo:','hair_style',
            [{'name':'Careca','id':0},{'name':'Curto','id':1},{'name':'Médio','id':2},
             {'name':'Longo','id':3},{'name':'Moicano','id':4}],0.96,C['mag'])
        self._crow(c,'Cor Cabelo:','hair_color',HAIR,0.72)
        self._srow(c,'Barba:','beard',
            [{'name':'Sem','id':0},{'name':'Cavanha','id':1},{'name':'Curta','id':2},
             {'name':'Cheia','id':3},{'name':'Bigode','id':4}],0.46,C['org'])

    def _t2(self):
        c=self._ct
        self._crow(c,'Cor Camisa:','shirt_col',CLOTH,0.96)
        self._srow(c,'Camisa:','shirt',
            [{'name':'Básica','id':0},{'name':'Colete','id':1},{'name':'Jaqueta','id':2},
             {'name':'Armadura','id':3},{'name':'Havaiana','id':4}],0.70,C['cyan'])

    def _t3(self):
        c=self._ct
        self._crow(c,'Cor Calça:','pants_col',CLOTH,0.96)
        self._srow(c,'Calça:','pants',
            [{'name':'Lisa','id':0},{'name':'Jeans','id':1},{'name':'Cargo','id':2},
             {'name':'Shorts','id':3},{'name':'Armadura','id':4}],0.70,C['yel'])
        self._crow(c,'Cor Sapato:','shoe_col',CLOTH,0.46)
        self._srow(c,'Sapato:','shoe',
            [{'name':'Tênis','id':0},{'name':'Bota','id':1},{'name':'Sandália','id':2},
             {'name':'Sapatilha','id':3},{'name':'Armadura','id':4}],0.20,C['grn'])

    def _t4(self):
        c=self._ct
        c.add_widget(mk_lbl('Arma inicial:',fs=sp(14),size_hint=(None,None),
            size=(dp(280),dp(26)),pos_hint={'x':0,'top':0.96}))
        g=GridLayout(cols=2,spacing=dp(8),size_hint=(None,None),
                     size=(dp(480),dp(265)),pos_hint={'x':0,'top':0.87})
        for wk,wd in WEAPONS.items():
            b=mk_btn(f"{wd['name']}  dmg:{wd['dmg']}%",wd['col'],h=dp(62))
            b.bind(on_release=lambda btn,k=wk:self._av.update({'weapon':k}))
            g.add_widget(b)
        c.add_widget(g)

    def _upd(self,dt):
        w=self._prev
        if w.width<10: return
        w.canvas.clear()
        try: draw_avatar(w.canvas,self._av,w.x,w.y,sc=dp(1.38),facing=1,af=0)
        except: pass
        self._pname.text=self._av.get('name','Player')

    def on_pre_enter(self): self._av=dict(GS.avatar); self._switch(0)
    def _back(self,*a): self.manager.current='cover'
    def _save(self,*a): GS.avatar=dict(self._av); self.manager.current='cover'

# ═══════════════════════════════════════════════════════════════════════════════
#  MUNDOS
# ═══════════════════════════════════════════════════════════════════════════════
class WorldsScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        root=FloatLayout(); self.add_widget(root)
        with root.canvas.before:
            Color(*C['bg']); Rectangle(pos=(0,0),size=Window.size)
        root.add_widget(mk_lbl('[b]MUNDOS[/b]',fs=sp(24),
            size_hint=(1,None),height=dp(42),pos_hint={'x':0,'top':1}))
        g=GridLayout(cols=4,spacing=dp(10),size_hint=(None,None),
                     size=(dp(860),dp(440)),pos_hint={'center_x':0.5,'center_y':0.47})
        root.add_widget(g)
        for w in WORLDS:
            btn=Button(text=f"[b]{w['name']}[/b]",markup=True,font_size=sp(14),
                       background_normal='',background_color=C['dk'],
                       color=w['pc'],size_hint=(None,None),size=(dp(196),dp(106)))
            with btn.canvas.after:
                Color(*w['pc']); btn._ln=Line(rounded_rectangle=(0,0,10,10,6),width=2)
            def _u(i,v): i._ln.rounded_rectangle=(*i.pos,*i.size,6)
            btn.bind(pos=_u,size=_u,
                     on_release=lambda *a,wid=w['id']:self._sel(wid))
            g.add_widget(btn)
        bk=mk_btn('← VOLTAR',C['red'],sh=(None,None),h=dp(46),size=(dp(190),dp(46)))
        bk.pos_hint={'x':0.02,'y':0.02}
        bk.bind(on_release=lambda *a:setattr(self.manager,'current','cover'))
        root.add_widget(bk)

    def _sel(self,wid): GS.world_id=wid; self.manager.current='cover'

# ═══════════════════════════════════════════════════════════════════════════════
#  LOBBY
# ═══════════════════════════════════════════════════════════════════════════════
class LobbyScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        root=FloatLayout(); self.add_widget(root)
        with root.canvas.before:
            Color(*C['bg']); Rectangle(pos=(0,0),size=Window.size)
        root.add_widget(mk_lbl('[b]MULTIJOGADOR[/b]',fs=sp(24),
            size_hint=(1,None),height=dp(42),pos_hint={'x':0,'top':1}))
        root.add_widget(Label(
            text='1. Mesmo WiFi ou Hotspot\n2. Um toca HOST → anota IP\n3. Outro digita IP → ENTRAR\n4. Host toca INICIAR',
            color=C['yel'],font_size=sp(13),size_hint=(None,None),size=(dp(400),dp(88)),
            pos_hint={'center_x':0.5,'top':0.95},halign='left',valign='top'))
        hj=BoxLayout(size_hint=(None,None),size=(dp(420),dp(48)),
                     spacing=dp(12),pos_hint={'center_x':0.5,'top':0.70})
        root.add_widget(hj)
        hb=mk_btn('📡 HOST',C['grn'],h=dp(48)); hb.bind(on_release=self._host)
        jb=mk_btn('🔗 ENTRAR',C['cyan'],h=dp(48)); jb.bind(on_release=self._join)
        hj.add_widget(hb); hj.add_widget(jb)
        ip_r=BoxLayout(size_hint=(None,None),size=(dp(420),dp(42)),
                       spacing=dp(8),pos_hint={'center_x':0.5,'top':0.59})
        root.add_widget(ip_r)
        ip_r.add_widget(Label(text='IP:',color=C['cyan'],font_size=sp(13),
                              size_hint=(None,1),width=dp(40)))
        self._ip=TextInput(text='192.168.43.1',multiline=False,font_size=sp(14),
                           background_color=(0.08,0.08,0.22,1),
                           foreground_color=C['wht'],cursor_color=C['cyan'])
        ip_r.add_widget(self._ip)
        self._info=mk_lbl('—',fs=sp(13),col=C['wht'],
            size_hint=(1,None),height=dp(22),pos_hint={'x':0,'top':0.49})
        root.add_widget(self._info)
        self._plist=BoxLayout(orientation='vertical',spacing=dp(4),size_hint_y=None)
        self._plist.bind(minimum_height=self._plist.setter('height'))
        sv=ScrollView(size_hint=(None,None),size=(dp(360),dp(130)),
                      pos_hint={'center_x':0.5,'top':0.44})
        sv.add_widget(self._plist); root.add_widget(sv)
        br=BoxLayout(size_hint=(None,None),size=(dp(420),dp(48)),
                     spacing=dp(12),pos_hint={'center_x':0.5,'y':0.02})
        root.add_widget(br)
        bk=mk_btn('← VOLTAR',C['red'],h=dp(48)); bk.bind(on_release=self._back)
        st=mk_btn('▶ INICIAR',C['grn'],h=dp(48)); st.bind(on_release=self._start)
        br.add_widget(bk); br.add_widget(st)
        Clock.schedule_interval(self._tick,0.5)

    def _host(self,*a):
        Net.stop(); GS.local_pid=0
        GS.players={0:Player(0,GS.avatar)}; GS.zombies=[]
        GS.net_role='host'; Net.start_host()
        self._info.text=f'IP: [b]{Net.my_ip()}[/b]'

    def _join(self,*a):
        ip=self._ip.text.strip()
        if not ip: self._info.text='Digite o IP!'; return
        Net.stop(); GS.local_pid=1
        GS.players={1:Player(1,GS.avatar)}; GS.zombies=[]
        GS.net_role='client'; Net.start_client(ip)
        self._info.text=f'Conectando a {ip}...'
        Clock.schedule_once(lambda dt:Net.send(
            {'type':'join','pid':1,'name':GS.avatar.get('name','P1'),'av':GS.avatar}),1.2)

    def _tick(self,dt):
        while not Net.rx.empty():
            try:
                msg=Net.rx.get_nowait(); t=msg.get('type')
                if t=='connect_error': self._info.text=f'Erro: {msg.get("msg","")}'
                elif t=='join':
                    npid=msg['pid']
                    if npid not in GS.players:
                        nav=msg.get('av',def_av()); nav['name']=msg.get('name',f'P{npid}')
                        GS.players[npid]=Player(npid,nav)
                    p=GS.players.get(GS.local_pid)
                    if p: Net.send({'type':'join','pid':GS.local_pid,'name':p.name,'av':p.avatar})
                    self._info.text='Conectado!'
                elif t=='start':
                    GS.world_id=msg.get('world',GS.world_id); self.manager.current='game'
            except: pass
        self._plist.clear_widgets()
        for pid,p in GS.players.items():
            row=BoxLayout(size_hint_y=None,height=dp(28))
            row.add_widget(Label(text=f'{"👑" if pid==0 else "•"} {p.name}',
                                 color=p.color,font_size=sp(12),bold=True))
            self._plist.add_widget(row)

    def _back(self,*a): Net.stop(); GS.net_role='solo'; self.manager.current='cover'
    def _start(self,*a):
        if not GS.players: GS.players[0]=Player(0,GS.avatar)
        if GS.net_role=='host': Net.send({'type':'start','world':GS.world_id})
        self.manager.current='game'

# ═══════════════════════════════════════════════════════════════════════════════
#  HUD CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
class HUDCfgScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        root=FloatLayout(); self.add_widget(root)
        with root.canvas.before:
            Color(*C['bg']); Rectangle(pos=(0,0),size=Window.size)
        root.add_widget(mk_lbl('[b]CONFIG HUD[/b]',fs=sp(24),
            size_hint=(1,None),height=dp(42),pos_hint={'x':0,'top':1}))
        root.add_widget(Label(
            text='No jogo: toque ⚙ para modo edição.\nArraste botões. +/− para tamanho.',
            color=C['yel'],font_size=sp(13),size_hint=(1,None),height=dp(42),
            pos_hint={'x':0,'top':0.86},halign='center'))
        form=BoxLayout(orientation='vertical',spacing=dp(14),
                       size_hint=(None,None),size=(dp(440),dp(110)),
                       pos_hint={'center_x':0.5,'center_y':0.55})
        root.add_widget(form)
        r1=BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(8))
        r1.add_widget(Label(text='Joystick:',color=C['cyan'],font_size=sp(14),
                            size_hint=(None,1),width=dp(100)))
        for nome,k in [('Esquerda','left'),('Direita','right')]:
            b=Button(text=nome,background_normal='',background_color=C['dk'],
                     color=C['wht'],font_size=sp(13))
            b.bind(on_release=lambda *a,s=k:GS.hud_layout.update({'_joy':s}))
            r1.add_widget(b)
        form.add_widget(r1)
        bk=mk_btn('← VOLTAR',C['red'],sh=(None,None),size=(dp(185),dp(44)))
        bk.pos_hint={'center_x':0.5}
        bk.bind(on_release=lambda *a:setattr(self.manager,'current','cover'))
        form.add_widget(bk)

# ═══════════════════════════════════════════════════════════════════════════════
#  GAME SCREEN — on_enter garante tamanho antes de criar widgets
# ═══════════════════════════════════════════════════════════════════════════════
class GameScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        fl=FloatLayout()
        self.add_widget(fl)          # fl no layout PRIMEIRO
        gw=GameWorld(size_hint=(1,1))
        fl.add_widget(gw)
        hud=HUD(gw,size_hint=(1,1))
        fl.add_widget(hud)
        self._gw=gw; self._hud=hud

    def on_leave(self):
        if hasattr(self,'_gw'): self._gw.stop()

# ═══════════════════════════════════════════════════════════════════════════════
#  HUD
# ═══════════════════════════════════════════════════════════════════════════════
class HUD(Widget):
    def __init__(self,gw,**kw):
        super().__init__(**kw)
        self._gw=gw; self._pid=GS.local_pid; self._edit=False
        js=GS.hud_layout.get('_joy','left')
        bsz=dp(60)
        jx=dp(12) if js=='left' else Window.width-dp(148)-dp(12)
        self._joy=Joystick(size_hint=(None,None),size=(dp(144),dp(144)),pos=(jx,dp(10)))
        self.add_widget(self._joy)
        bx=Window.width-dp(284) if js=='left' else dp(12); by=dp(10)
        defs=[
            ('fire',  '🔴\nFIRE',  C['red'],  lambda:gw.fire(self._pid),       bx+dp(88), by+dp(74)),
            ('bomb',  '💣\nBOMBA', C['org'],  lambda:gw.bomb(self._pid,'n'),   bx+dp(8),  by+dp(74)),
            ('gas',   '☠\nGÁS',   C['grn'],  lambda:gw.bomb(self._pid,'g'),   bx+dp(162),by+dp(74)),
            ('smoke', '💨\nFUMC',  C['gry'],  lambda:gw.bomb(self._pid,'s'),   bx+dp(8),  by+dp(12)),
            ('shield','🛡\nGEL',   C['blu'],  lambda:gw.shield(self._pid),     bx+dp(88), by+dp(12)),
            ('wep',   '🔄\nARMA',  C['mag'],  lambda:gw.cycle(self._pid),      bx+dp(162),by+dp(12)),
            ('reload','↺\nRECARG', C['yel'],  lambda:gw.reload(self._pid),     bx+dp(232),by+dp(42)),
        ]
        self._btns=[]
        for bid,lbl,col,cb,dx2,dy2 in defs:
            saved=GS.hud_layout.get(bid,{})
            px2=saved.get('x',dx2); py2=saved.get('y',dy2); sz=saved.get('sz',bsz)
            b=ABtn(bid,lbl,col,cb,size_hint=(None,None),size=(sz,sz),pos=(px2,py2))
            self.add_widget(b); self._btns.append(b)
        self._ebtn=Button(text='⚙',size_hint=(None,None),size=(dp(36),dp(36)),
            pos=(Window.width/2+dp(22),Window.height-dp(46)),
            background_normal='',background_color=(0,0,0,0),
            color=C['wht'],font_size=sp(17))
        self._ebtn.bind(on_release=self._toggle_edit); self.add_widget(self._ebtn)
        self._rp=Button(text='+',size_hint=(None,None),size=(dp(34),dp(34)),
            pos=(Window.width/2+dp(60),Window.height-dp(46)),
            background_normal='',background_color=C['dk'],color=C['yel'],font_size=sp(17))
        self._rm=Button(text='-',size_hint=(None,None),size=(dp(34),dp(34)),
            pos=(Window.width/2+dp(96),Window.height-dp(46)),
            background_normal='',background_color=C['dk'],color=C['yel'],font_size=sp(17))
        self._rp.bind(on_release=lambda *a:[b.resize(+dp(8)) for b in self._btns])
        self._rm.bind(on_release=lambda *a:[b.resize(-dp(8)) for b in self._btns])
        self._rp.opacity=0; self._rm.opacity=0
        self.add_widget(self._rp); self.add_widget(self._rm)
        pb=Button(text='⏸',size_hint=(None,None),size=(dp(36),dp(36)),
                  pos=(Window.width/2-dp(18),Window.height-dp(46)),
                  background_normal='',background_color=(0,0,0,0),
                  color=C['wht'],font_size=sp(17))
        pb.bind(on_release=self._pause); self.add_widget(pb)
        # Delay tick — garante que widget tem tamanho antes do primeiro draw
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self._tick,1/30), 0.2)

    def _toggle_edit(self,*a):
        self._edit=not self._edit
        self._ebtn.color=C['yel'] if self._edit else C['wht']
        self._rp.opacity=1 if self._edit else 0
        self._rm.opacity=1 if self._edit else 0
        for b in self._btns: b.set_edit(self._edit)

    def _tick(self,dt):
        try:
            self._gw.move(self._pid,self._joy.dx,self._joy.dy)
            self._draw()
        except Exception as e:
            print('[HUD tick]',e); traceback.print_exc()

    def _draw(self):
        if self.width<4 or self.height<4: return
        if Window.width<10: return
        p=GS.players.get(self._pid)
        if p is None:
            p=GS.players.get(0)
            if p is None: return
            self._pid=0
        self.canvas.clear()
        bx=dp(10); by=Window.height-dp(20); bw=dp(196)
        with self.canvas:
            # HP
            Color(0,0,0,0.50)
            RoundedRectangle(pos=(bx-2,by-2),size=(bw+4,dp(14)),radius=[4])
            hf=max(0.0,p.hp/100.0)
            Color(*(C['grn'] if hf>0.5 else C['yel'] if hf>0.25 else C['red']))
            RoundedRectangle(pos=(bx,by),size=(max(1.0,bw*hf),dp(10)),radius=[3])
            # Shield
            if p.shield>0:
                Color(*C['blu'])
                RoundedRectangle(pos=(bx,by-dp(13)),size=(max(1.0,bw*p.shield/100),dp(6)),radius=[3])
            # Jetpack
            Color(*(C['mag'] if p.turbo else C['org']))
            RoundedRectangle(pos=(bx,by-dp(22)),size=(max(1.0,dp(100)*p.fuel/100),dp(5)),radius=[3])
            # Munição
            Color(*WEAPONS[p.active]['col'])
            for i in range(max(0,min(p.wep()['ammo'],25))):
                Rectangle(pos=(bx+i*dp(8),by-dp(36)),size=(dp(6),dp(9)))
            # Bombas
            Color(*C['org'])
            for i in range(min(p.bombs_n,5)):
                Ellipse(pos=(bx+i*dp(15),by-dp(50)),size=(dp(9),dp(9)))
            Color(*C['grn'])
            for i in range(min(p.gas_n,5)):
                Ellipse(pos=(bx+i*dp(15),by-dp(62)),size=(dp(9),dp(9)))
            Color(*C['gry'])
            for i in range(min(p.smoke_n,5)):
                Ellipse(pos=(bx+i*dp(15),by-dp(74)),size=(dp(9),dp(9)))
            # Invisibilidade
            if p.invisible and p.invis_t>0.1:
                Color(*C['pur'])
                Line(circle=(Window.width/2,Window.height-dp(55),
                             max(1.0,dp(11)*(p.invis_t/10.0))),width=3)
            # Scoreboard
            sx=Window.width-dp(140); sy=Window.height-dp(9); nh=max(1,len(GS.players))
            Color(0,0,0,0.42)
            RoundedRectangle(pos=(sx-dp(4),sy-nh*dp(16)-dp(4)),
                             size=(dp(134),nh*dp(16)+dp(8)),radius=[4])
            for i,(pid2,pp) in enumerate(sorted(GS.players.items(),key=lambda x:-x[1].kills)):
                Color(*pp.color); Rectangle(pos=(sx,sy-i*dp(16)),size=(dp(8),dp(11)))
            # Morte
            if not p.alive:
                Color(*C['red'][:3],0.48)
                RoundedRectangle(pos=(Window.width/2-dp(82),Window.height/2-dp(22)),
                                 size=(dp(164),dp(44)),radius=[8])
            # Modo edição
            if self._edit:
                Color(1,1,0,0.05); Rectangle(pos=(0,0),size=(Window.width,Window.height))
            # Solo: barra de wave
            if GS.net_role=='solo' and hasattr(self._gw,'_zombie_interval'):
                zi=max(0.1,self._gw._zombie_interval)
                zt=max(0.0,self._gw._zombie_timer)
                prog=max(0.0,1.0-zt/zi)
                Color(0,0,0,0.45)
                RoundedRectangle(pos=(Window.width-dp(88),Window.height-dp(115)),
                                 size=(dp(72),dp(7)),radius=[3])
                Color(0.3,1.0,0.2,0.88)
                RoundedRectangle(pos=(Window.width-dp(88),Window.height-dp(115)),
                                 size=(max(1.0,dp(72)*prog),dp(7)),radius=[3])

    def _pause(self,*a):
        c=BoxLayout(orientation='vertical',spacing=dp(10),padding=dp(12))
        c.add_widget(Label(text='[b]PAUSADO[/b]',markup=True,color=C['cyan'],
                           font_size=sp(20),size_hint_y=None,height=dp(32)))
        rb=mk_btn('▶ CONTINUAR',C['grn'],h=dp(44))
        lb=mk_btn('🚪 SAIR',C['red'],h=dp(44))
        c.add_widget(rb); c.add_widget(lb)
        pop=Popup(title='',content=c,size_hint=(None,None),size=(dp(270),dp(182)),
                  separator_height=0,background_color=(0.06,0.06,0.14,0.96))
        rb.bind(on_release=lambda *a:pop.dismiss())
        def _sair(*a):
            pop.dismiss(); Net.stop()
            try: self.parent.parent.manager.current='cover'
            except: pass
        lb.bind(on_release=_sair); pop.open()

# ═══════════════════════════════════════════════════════════════════════════════
#  MUNDO DO JOGO
# ═══════════════════════════════════════════════════════════════════════════════
class GameWorld(Widget):
    def __init__(self,**kw):
        super().__init__(**kw)
        self._run=True; self._wld=WORLDS[GS.world_id]
        self._ptcl=[]; self._t=0.0; self._resp={}
        # Garantir jogador existe
        if not GS.players:
            GS.local_pid=0; GS.players[0]=Player(0,GS.avatar)
        self._solo=(GS.net_role=='solo')
        self._zombie_timer=10.0; self._zombie_interval=10.0; self._wave=0
        self._portal_x=640; self._portal_y=200
        self._init_players(); self._spawn_pickups()
        if self._solo: self._place_portal()
        # Delay 0.2s antes do primeiro tick — Android pode precisar de tempo
        Clock.schedule_once(lambda dt: Clock.schedule_interval(self._tick,1/60), 0.2)

    def stop(self): self._run=False; Clock.unschedule(self._tick)

    def _spawns(self):
        pts=[(pl[0]+pl[2]*0.5-14,pl[1]+pl[3]) for pl in self._wld['plats'][1:]]
        return pts or [(200,200),(600,200),(1000,200)]

    def _init_players(self):
        sps=self._spawns()
        if not GS.players: GS.local_pid=0; GS.players[0]=Player(0,GS.avatar)
        for i,(pid,p) in enumerate(GS.players.items()):
            sx,sy=sps[i%len(sps)]
            p.x=sx; p.y=sy; p.vx=0; p.vy=0; p.hp=100; p.alive=True
            p.shield=0; p.fuel=100; p.invisible=False; p.invis_t=0

    def _spawn_pickups(self):
        plats=list(self._wld['plats'][1:]); random.shuffle(plats)
        for i,t in enumerate(['ammo','ammo','ammo','fuel','fuel','turbo','invis','hp','hp']):
            if i<len(plats):
                pl=plats[i]
                GS.pickups.append({'type':t,'x':pl[0]+pl[2]*0.5,
                    'y':pl[1]+pl[3]+8,'alive':True,'bob':random.uniform(0,6.28)})

    def _place_portal(self):
        plats=self._wld['plats'][1:]
        if plats:
            pl=max(plats,key=lambda p:p[0])
            self._portal_x=pl[0]+pl[2]//2; self._portal_y=pl[1]+pl[3]

    def _tick(self,dt):
        if not self._run: return
        try:
            dt=min(dt,0.05); self._t+=dt
            g=self._wld['grav']
            if self._solo: self._zombie_tick(dt,g)
            if GS.net_role!='solo': self._net_tick()
            self._player_tick(dt,g)
            self._bullet_tick(dt)
            self._bomb_tick(dt)
            self._cloud_tick(dt)
            self._particle_tick(dt)
            self._pickup_tick()
            self._render()
        except Exception as e:
            print('[GameWorld._tick ERROR]',e); traceback.print_exc()

    def _zombie_tick(self,dt,g):
        self._zombie_timer-=dt
        if self._zombie_timer<=0:
            self._wave+=1
            for _ in range(10):
                GS.zombies.append(Zombie(
                    self._portal_x+random.randint(-20,20),
                    self._portal_y+random.randint(0,25)))
            self._zombie_interval=max(2.0,self._zombie_interval-2.0)
            self._zombie_timer=self._zombie_interval
        alive=[]
        for z in GS.zombies:
            if not z.alive: continue
            tgt=None; td=999999
            for pid,p in GS.players.items():
                if not p.alive: continue
                d=math.sqrt((p.x-z.x)**2+(p.y-z.y)**2)
                if d<td: td=d; tgt=p
            if tgt:
                dx=tgt.x+tgt.w/2-(z.x+z.w/2)
                z.facing=1 if dx>0 else -1; z.vx=z.facing*dp(68)
                if z.on_ground and abs(dx)<dp(55) and tgt.y>z.y+dp(18):
                    z.vy=dp(290); z.on_ground=False
                if td<dp(32) and z.attack_cd<=0:
                    tgt.take_dmg(10); z.attack_cd=1.5
            if not z.on_ground: z.vy-=g*dt
            z.x+=z.vx*dt; z.y+=z.vy*dt; z.on_ground=False
            for pl in self._wld['plats']:
                px,py,pw,ph=pl
                if(z.x+z.w>px and z.x<px+pw and
                   z.y+z.h>py and z.y+z.h<py+ph+max(abs(z.vy)*0.016,6) and z.vy<=0.5):
                    z.y=py+ph; z.vy=0; z.on_ground=True
            z.x=max(0,min(Window.width-z.w,z.x))
            if z.y<0: z.y=0; z.vy=0; z.on_ground=True
            if z.attack_cd>0: z.attack_cd-=dt
            z.at+=dt
            if z.at>0.12: z.at=0; z.af=(z.af+1)%4
            alive.append(z)
        GS.zombies=alive

    def _net_tick(self):
        while not Net.rx.empty():
            try:
                msg=Net.rx.get_nowait(); t=msg.get('type')
                if t=='state' and GS.net_role=='client':
                    for sp,sd in msg.get('ps',{}).items():
                        pid=int(sp)
                        if pid==GS.local_pid: continue
                        if pid not in GS.players:
                            GS.players[pid]=Player(pid,sd.get('av',def_av()))
                        pp=GS.players[pid]
                        pp.x=sd['x']; pp.y=sd['y']; pp.hp=sd['hp']
                        pp.alive=sd['alive']; pp.facing=sd.get('facing',1)
                elif t=='fire' and msg.get('own')!=GS.local_pid:
                    GS.bullets.append({'x':msg['x'],'y':msg['y'],'vx':msg['vx'],'vy':msg['vy'],
                        'dmg':msg['dmg'],'own':msg['own'],'col':tuple(msg['col']),'life':2.0})
                elif t=='bomb' and msg.get('own')!=GS.local_pid:
                    GS.bombs.append({'x':msg['x'],'y':msg['y'],'own':msg['own'],
                        'bt':msg['bt'],'armed':False,'timer':30.0})
            except: pass
        if GS.net_role=='host' and len(GS.players)>1:
            if int(self._t*15)!=int((self._t-0.016)*15):
                ps={str(pid):{'x':p.x,'y':p.y,'hp':p.hp,'alive':p.alive,
                               'facing':p.facing,'av':p.avatar}
                    for pid,p in GS.players.items()}
                Net.send({'type':'state','ps':ps})

    def _player_tick(self,dt,g):
        for pid,p in list(GS.players.items()):
            if not p.alive: self._resp_tick(pid,dt); continue
            if not p.on_ground: p.vy-=g*dt
            p.x+=p.vx*dt; p.y+=p.vy*dt; p.on_ground=False
            for pl in self._wld['plats']: self._pcol(p,pl)
            p.x=max(0,min(Window.width-p.w,p.x))
            if p.y<0: p.y=0; p.vy=0; p.on_ground=True
            if p.fire_cd>0: p.fire_cd=max(0,p.fire_cd-dt)
            if p.invis_t>0:
                p.invis_t-=dt
                if p.invis_t<=0: p.invisible=False
            if p.gas_dbf>0: p.gas_dbf-=dt
            if p.on_ground and p.fuel<100:
                p.fuel=min(100,p.fuel+(3 if not p.turbo else 1.5)*dt)
            p.at+=dt
            if p.at>0.11: p.at=0; p.af=(p.af+1)%4

    def _bullet_tick(self,dt):
        nb=[]
        for b in GS.bullets:
            b['x']+=b['vx']*dt; b['y']+=b['vy']*dt; b['life']-=dt
            if b['life']<=0: continue
            if not(0<=b['x']<=Window.width and 0<=b['y']<=Window.height): continue
            wall=False
            for pl in self._wld['plats']:
                if pl[0]<=b['x']<=pl[0]+pl[2] and pl[1]<=b['y']<=pl[1]+pl[3]:
                    self._sparks(b['x'],b['y'],b['col'],3); wall=True; break
            if wall: continue
            hit=False
            for pid,p in GS.players.items():
                if pid==b['own'] or not p.alive or p.invisible: continue
                if p.x<=b['x']<=p.x+p.w and p.y<=b['y']<=p.y+p.h:
                    p.take_dmg(b['dmg']); self._sparks(b['x'],b['y'],C['red'],5)
                    if not p.alive:
                        if b['own'] in GS.players: GS.players[b['own']].kills+=1
                        p.deaths+=1
                    hit=True; break
            if not hit and self._solo:
                for z in GS.zombies:
                    if not z.alive: continue
                    if z.x<=b['x']<=z.x+z.w and z.y<=b['y']<=z.y+z.h:
                        z.hp-=b['dmg']
                        self._sparks(b['x'],b['y'],C['grn'],4)
                        if z.hp<=0: z.alive=False
                        hit=True; break
            if not hit: nb.append(b)
        GS.bullets=nb

    def _bomb_tick(self,dt):
        for bm in GS.bombs[:]:
            bm['timer']-=dt
            if bm['armed'] and bm['timer']<=0: self._explode(bm); GS.bombs.remove(bm); continue
            if not bm['armed']:
                for pid,p in GS.players.items():
                    if pid==bm['own'] or not p.alive: continue
                    if math.sqrt((p.x-bm['x'])**2+(p.y-bm['y'])**2)<dp(80):
                        bm['armed']=True; bm['timer']=1.5
                for z in GS.zombies:
                    if not z.alive: continue
                    if math.sqrt((z.x-bm['x'])**2+(z.y-bm['y'])**2)<dp(80):
                        bm['armed']=True; bm['timer']=1.5

    def _cloud_tick(self,dt):
        for gc in GS.gas_clouds[:]:
            gc['timer']-=dt
            if gc['timer']<=0: GS.gas_clouds.remove(gc); continue
            for pid,p in GS.players.items():
                if math.sqrt((p.x-gc['x'])**2+(p.y-gc['y'])**2)<gc['r']:
                    p.gas_dbf=max(p.gas_dbf,3.0)
        for sc2 in GS.smoke_clouds[:]:
            sc2['timer']-=dt
            if sc2['timer']<=0: GS.smoke_clouds.remove(sc2)
        for ex in GS.explosions[:]:
            ex['t']-=dt
            if ex['t']<=0: GS.explosions.remove(ex)

    def _particle_tick(self,dt):
        np2=[]
        for pt in self._ptcl:
            pt['x']+=pt['vx']*dt; pt['y']+=pt['vy']*dt
            pt['vy']-=180*dt; pt['life']-=dt
            if pt['life']>0: np2.append(pt)
        self._ptcl=np2

    def _pickup_tick(self):
        for pu in GS.pickups:
            if not pu['alive']: continue
            pu['bob']=(pu['bob']+0.05)%6.28
            for pid,p in GS.players.items():
                if not p.alive: continue
                if abs(p.x+p.w/2-pu['x'])<dp(22) and abs(p.y+p.h/2-pu['y'])<dp(22):
                    self._pickup_apply(p,pu)

    def _resp_tick(self,pid,dt):
        if pid not in self._resp: self._resp[pid]=3.0
        self._resp[pid]-=dt
        if self._resp[pid]<=0:
            del self._resp[pid]; p=GS.players[pid]
            sx,sy=random.choice(self._spawns())
            p.x=sx; p.y=sy; p.vx=0; p.vy=0; p.hp=100; p.alive=True
            p.shield=0; p.invisible=False
            for k in p.weapons: p.weapons[k]['ammo']=WEAPONS[k]['ammo']

    def _pcol(self,p,pl):
        px,py,pw,ph=pl
        if(p.x+p.w>px and p.x<px+pw and
           p.y+p.h>py and p.y+p.h<py+ph+max(abs(p.vy)*0.016,6) and p.vy<=0.5):
            p.y=py+ph; p.vy=0; p.on_ground=True

    def _pickup_apply(self,p,pu):
        pu['alive']=False; t=pu['type']
        if t=='ammo':
            for k in p.weapons: p.weapons[k]['res']=min(200,p.weapons[k]['res']+50)
        elif t=='fuel': p.fuel=min(100,p.fuel+30)
        elif t=='turbo': p.turbo=True
        elif t=='invis': p.invisible=True; p.invis_t=10.0
        elif t=='hp': p.hp=min(100,p.hp+30)
        self._sparks(p.x+p.w/2,p.y+p.h/2,C['grn'],8)

    def _explode(self,bm):
        r=dp(100); bt=bm.get('bt','n')
        GS.explosions.append({'x':bm['x'],'y':bm['y'],'r':r,'t':0.6,'mt':0.6,'col':C['org']})
        self._sparks(bm['x'],bm['y'],C['org'],20)
        if bt=='g': GS.gas_clouds.append({'x':bm['x'],'y':bm['y'],'r':r*1.2,'timer':8.0})
        elif bt=='s': GS.smoke_clouds.append({'x':bm['x'],'y':bm['y'],'r':r*1.5,'timer':5.0})
        else:
            for pid,p in GS.players.items():
                if pid==bm['own'] or not p.alive: continue
                d=math.sqrt((p.x+p.w/2-bm['x'])**2+(p.y+p.h/2-bm['y'])**2)
                if d<r: p.take_dmg(int(80*(1-d/r)))
            for z in GS.zombies:
                if not z.alive: continue
                d=math.sqrt((z.x+z.w/2-bm['x'])**2+(z.y+z.h/2-bm['y'])**2)
                if d<r: z.hp-=int(80*(1-d/r));
                if z.hp<=0: z.alive=False

    def _sparks(self,x,y,col,n=6):
        for _ in range(n):
            a=random.uniform(0,6.28); spd=random.uniform(dp(50),dp(180))
            self._ptcl.append({'x':x,'y':y,'vx':math.cos(a)*spd,
                'vy':math.sin(a)*spd,'col':col,'life':random.uniform(0.28,0.68)})

    def _render(self):
        if self.width<10 or self.height<10: return
        self.canvas.clear()
        W=self._wld; sw=Window.width; sh=Window.height
        with self.canvas:
            Color(*W['bg']); Rectangle(pos=(0,0),size=(sw,sh))
            a=0.045+0.015*math.sin(self._t); Color(*(W['ac'][:3]),a); step=dp(80)
            for xx in range(0,int(sw)+int(step),int(step)):
                Line(points=[xx,0,xx,sh],width=1)
            for yy in range(0,int(sh)+int(step),int(step)):
                Line(points=[0,yy,sw,yy],width=1)
            if W['id']==4:
                random.seed(77); Color(1,1,1,0.6)
                for _ in range(50):
                    Ellipse(pos=(random.randint(0,int(sw)),random.randint(0,int(sh))),size=(2,2))
                random.seed()
            for pl in W['plats']:
                px,py,pw,ph=pl
                Color(*W['pc'][:3],0.16); RoundedRectangle(pos=(px-3,py-3),size=(pw+6,ph+6),radius=[6])
                Color(*W['pc'][:3],0.90); RoundedRectangle(pos=(px,py),size=(pw,ph),radius=[4])
                Color(1,1,1,0.15); Rectangle(pos=(px+2,py+ph-3),size=(pw-4,3))
            PKUP_COLS={'ammo':C['yel'],'fuel':C['org'],'turbo':C['mag'],'invis':C['pur'],'hp':C['grn']}
            for pu in GS.pickups:
                if not pu['alive']: continue
                col=PKUP_COLS[pu['type']]; sz=dp(19)
                by2=pu['y']+math.sin(pu['bob'])*dp(5)
                Color(*(col[:3]),0.20); Ellipse(pos=(pu['x']-sz,by2-sz),size=(sz*2,sz*2))
                Color(*col); Ellipse(pos=(pu['x']-sz/2,by2-sz/2),size=(sz,sz))
            for bm in GS.bombs:
                f=0.5+0.5*math.sin(self._t*8) if bm['armed'] else 1.0
                Color(1.0,f*0.5,0,1); Ellipse(pos=(bm['x']-8,bm['y']-8),size=(16,16))
                Color(*C['red']); Line(circle=(bm['x'],bm['y'],12),width=2)
            for ex in GS.explosions:
                p2=1-ex['t']/ex['mt']; al=max(0,1-p2*1.4); r2=ex['r']*p2
                Color(*(ex['col'][:3]),al*0.82); Ellipse(pos=(ex['x']-r2,ex['y']-r2),size=(r2*2,r2*2))
                Color(1,0.8,0.2,al*0.45); Ellipse(pos=(ex['x']-r2*0.6,ex['y']-r2*0.6),size=(r2*1.2,r2*1.2))
            for gc in GS.gas_clouds:
                Color(0.35,1.0,0.15,min(0.30,gc['timer']/8)); r3=gc['r']
                Ellipse(pos=(gc['x']-r3,gc['y']-r3),size=(r3*2,r3*2))
            for sc2 in GS.smoke_clouds:
                Color(0.55,0.55,0.55,min(0.40,sc2['timer']/5)); r4=sc2['r']
                Ellipse(pos=(sc2['x']-r4,sc2['y']-r4),size=(r4*2,r4*2))
            for b in GS.bullets:
                Color(*b['col']); Ellipse(pos=(b['x']-4,b['y']-4),size=(8,8))
            for pt in self._ptcl:
                Color(*(pt['col'][:3]),max(0,pt['life']/0.68))
                Ellipse(pos=(pt['x']-3,pt['y']-3),size=(6,6))

        # Portal
        if self._solo:
            try: draw_portal(self.canvas,self._portal_x,self._portal_y,self._t)
            except: pass

        # Jogadores
        for pid,p in list(GS.players.items()):
            if not p.alive: continue
            al=0.28 if p.invisible else 1.0
            try:
                draw_avatar(self.canvas,p.avatar,p.x-2,p.y,sc=dp(0.95),
                            facing=p.facing,af=p.af,alpha=al,
                            gun_col=WEAPONS[p.active]['col'])
            except Exception as e:
                print('[draw_avatar]',e)
            if p.shield>0:
                with self.canvas:
                    Color(*C['blu'][:3],p.shield/100*0.35*al)
                    Ellipse(pos=(p.x-10,p.y-8),size=(p.w+20,p.h+20))
            with self.canvas:
                hw=dp(28); hx=p.x+p.w/2-hw/2; hy=p.y+dp(50)
                Color(0,0,0,0.50*al)
                Rectangle(pos=(hx-1,hy-1),size=(hw+2,dp(5)+2))
                hf=max(0.0,p.hp/100.0)
                Color(*(C['grn'] if hf>0.5 else C['yel'] if hf>0.25 else C['red'])[:3],al)
                Rectangle(pos=(hx,hy),size=(max(1.0,hw*hf),dp(5)))

        # Zumbis
        for z in list(GS.zombies):
            if not z.alive: continue
            try: draw_zombie(self.canvas,z.x,z.y,sc=dp(0.88),facing=z.facing,af=z.af)
            except Exception as e: print('[draw_zombie]',e)
            with self.canvas:
                hw=dp(24); hx=z.x+z.w/2-hw/2; hy=z.y+dp(46)
                Color(0,0,0,0.48); Rectangle(pos=(hx-1,hy-1),size=(hw+2,dp(4)+2))
                Color(0.3,0.9,0.2,0.88)
                Rectangle(pos=(hx,hy),size=(max(1.0,hw*max(0,z.hp/50)),dp(4)))

    # ── Acções ────────────────────────────────────────────────────────────────
    def move(self,pid,dx,dy):
        p=GS.players.get(pid)
        if not p or not p.alive: return
        p.vx=dx*(dp(238) if not p.turbo else dp(370))
        if dx!=0: p.facing=1 if dx>0 else -1
        if dy>0.45 and p.on_ground: p.vy=dp(360); p.on_ground=False
        if dy>0.25 and not p.on_ground and p.fuel>0:
            p.fuel=max(0,p.fuel-(5 if p.turbo else 2.5)/60)
            p.vy=min(p.vy+(dp(830) if p.turbo else dp(515))/60,dp(380))

    def fire(self,pid):
        p=GS.players.get(pid)
        if not p or not p.alive: return
        if not p.do_fire(): p.reload(); return
        w=WEAPONS[p.active]; bx=p.x+(p.w if p.facing>0 else 0); by=p.y+p.h*0.55
        bvx=w['spd']*p.facing
        if p.active=='shotgun':
            for _ in range(5):
                sp3=random.uniform(-0.28,0.28)
                GS.bullets.append({'x':bx,'y':by,'vx':bvx+sp3*80,'vy':sp3*150,
                    'dmg':w['dmg']//5,'own':pid,'col':w['col'],'life':1.2})
        else:
            GS.bullets.append({'x':bx,'y':by,'vx':bvx,'vy':0,
                'dmg':w['dmg'],'own':pid,'col':w['col'],'life':2.0})
        self._sparks(bx,by,w['col'],2)
        Net.send({'type':'fire','x':bx,'y':by,'vx':bvx,'vy':0,
            'dmg':w['dmg'],'own':pid,'col':list(w['col'])})

    def shield(self,pid):
        p=GS.players.get(pid)
        if p and p.alive and p.shield<80:
            p.shield=80; self._sparks(p.x+p.w/2,p.y+p.h/2,C['blu'],6)

    def bomb(self,pid,bt='n'):
        p=GS.players.get(pid)
        if not p or not p.alive: return
        attr={'n':'bombs_n','g':'gas_n','s':'smoke_n'}[bt]
        if getattr(p,attr)<=0: return
        setattr(p,attr,getattr(p,attr)-1)
        bm={'x':p.x+p.w/2,'y':p.y,'own':pid,'bt':bt,'armed':False,'timer':30.0}
        GS.bombs.append(bm)
        Net.send({'type':'bomb','x':bm['x'],'y':bm['y'],'own':pid,'bt':bt})

    def cycle(self,pid):
        p=GS.players.get(pid)
        if p and p.alive: p.cycle()

    def reload(self,pid):
        p=GS.players.get(pid)
        if p and p.alive: p.reload()

# ═══════════════════════════════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════════════════════════════
class NeonMilitia(App):
    def build(self):
        force_landscape()
        Window.bind(on_resize=lambda *a:Clock.schedule_once(
                    lambda dt:force_landscape(),0.15))
        sm=ScreenManager(transition=FadeTransition(duration=0.18))
        sm.add_widget(CoverScreen(name='cover'))
        sm.add_widget(AvatarScreen(name='avatar'))
        sm.add_widget(WorldsScreen(name='worlds'))
        sm.add_widget(LobbyScreen(name='lobby'))
        sm.add_widget(HUDCfgScreen(name='hudcfg'))
        sm.add_widget(GameScreen(name='game'))
        return sm

    def on_stop(self): Net.stop()

if __name__=='__main__':
    NeonMilitia().run()
