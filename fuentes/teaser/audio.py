import numpy as np, scipy.signal as sg, wave
SR=48000
import sys
MUSIC = '--sin-musica' not in sys.argv
OUT = sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '/home/claude/teaser/banda.wav'
HOLDS=[[5.3,1.6],[6.5,0.8],[17.2,3.0],[18.6,2.2],[21.95,2.6],[30.15,2.6],[31.2,1.0],[37.0,1.2],[38.95,2.4],[44.5,2.2],[46.7,2.2],[50.1,3.3],[57.6,1.2],[63.3,3.2],[66.7,3.4],[67.4,3.4],[68.1,3.6],[68.8,4.4],[69.5,1.0]]
def RT(s): return s+sum(d for h,d in HOLDS if s>h)
DUR=80.5+sum(d for h,d in HOLDS); N=int(SR*DUR)
L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(x,t,gain=1.0,pan=0.0): addr(x,RT(t),gain,pan)
def addr(x,t,gain=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(x)); x=x[:j-i]
    L[i:j]+=x*gain*(1-max(0,pan)); R[i:j]+=x*gain*(1+min(0,pan))
def env(n,a,d):
    e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na)
    e*=np.exp(-np.arange(n)/(d*SR)); return e
def bp(x,lo,hi,o=2): b,a=sg.butter(o,[lo/(SR/2),hi/(SR/2)],'band'); return sg.lfilter(b,a,x)
def lp(x,f,o=2): b,a=sg.butter(o,f/(SR/2)); return sg.lfilter(b,a,x)
def hp(x,f,o=2): b,a=sg.butter(o,f/(SR/2),'high'); return sg.lfilter(b,a,x)
def noise(d): return rng.standard_normal(int(d*SR))
# --- teletipo: golpes de tecla mecánica ---
t=0.35
while t<3.85:
    n=int(.012*SR); x=bp(noise(.012),1800,6000)*env(n,.0005,.003)
    th=np.sin(2*np.pi*rng.uniform(180,260)*np.arange(n)/SR)*env(n,.0005,.006)*.6
    add(x+th,t,rng.uniform(.3,.45),rng.uniform(-.3,.3)); t+=rng.uniform(.035,.07)
def bell(t,f=2093,g=.12):
    n=int(1.6*SR); k=np.arange(n)/SR; x=(np.sin(2*np.pi*f*k)+.4*np.sin(2*np.pi*f*2.76*k))*env(n,.001,.45); add(x,t,g)
bell(3.9)
# --- impactos ---
def hit(t,g=.9):
    n=int(1.2*SR); k=np.arange(n)/SR; f=np.linspace(95,38,n)
    boom=np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.002,.35)
    sn=lp(noise(.25),2500)*env(int(.25*SR),.001,.05)
    add(boom,t,g); add(sn,t,g*.35)
for t in [4.3,5.9,13.9,14.7,15.5,59.0,60.3,60.9,61.5]: hit(t-.02,.8 if t not in (5.9,61.5) else 1.0)
# --- barridos de transición ---
def whoosh(t,d=.7,g=.28):
    n=int(d*SR); x=noise(d); k=np.linspace(0,1,n)
    out=np.zeros(n); seg=int(.02*SR)
    for s in range(0,n,seg):
        f=300+5000*k[s]**2; out[s:s+seg]=bp(x[s:s+seg+400],f*.6,min(f*1.6,20000))[:len(out[s:s+seg])]
    add(out*np.sin(np.pi*k)**2,t-d*.8,g,0)
for t in [7.2,13.6,21.0,58.6,65.2,72.6]: whoosh(t)
# --- plumilla sobre papel ---
def scratch(t,d=.95,g=.22):
    n=int(d*SR); x=bp(noise(d),2500,9000); m=.6+.4*np.sin(2*np.pi*23*np.arange(n)/SR)
    add(x*m*np.sin(np.pi*np.linspace(0,1,n))**.5,t,g)
scratch(8.0); scratch(73.4)
# --- música: pulso a 100 ppm con progresión Lam-Fa-Do-Sol ---
BEAT=.6; start=RT(7.2); end=RT(72.6)
chords=[[110,130.81,164.81],[87.31,110,130.81],[130.81,164.81,196],[98,123.47,146.83]]
def pad(t0,d,fr,g):
    if not MUSIC: return
    n=int(d*SR); k=np.arange(n)/SR; x=np.zeros(n)
    for f in fr:
        for det in (-.6,.6): x+=sg.sawtooth(2*np.pi*(f+det)*k)*.5
    x=lp(x,1700); e=np.minimum(1,k/.4)*np.minimum(1,(d-k)/.4)
    addr(x*e,t0,g,0)
bar=4*BEAT; t=start; i=0
while t<end:
    d=min(bar*2,end-t); 
    lvl=.035 if t<RT(21) else (.045 if t<RT(58.6) else .04)
    pad(t,d,chords[i%4],lvl); t+=bar*2; i+=1
def kick(t,g=.55):
    if not MUSIC: return
    n=int(.35*SR); f=np.linspace(130,42,n); x=np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.001,.12); addr(x,t,g)
def hat(t,g=.06):
    if not MUSIC: return
    n=int(.05*SR); x=hp(noise(.05),7000)*env(n,.0005,.012); addr(x,t,g,rng.uniform(-.2,.2))
def bass(t,f,g=.16):
    if not MUSIC: return
    n=int(BEAT*.9*SR); k=np.arange(n)/SR; x=lp(sg.square(2*np.pi*f*k),400)*env(n,.005,.25); addr(x,t,g)
t=start; b=0
while t<end:
    if t>=RT(9.6) and not (RT(58.6)<=t<RT(59.0)): kick(t, .5 if t>=RT(21) else .35)
    if t>=RT(21) and t<RT(58.6): hat(t+BEAT/2); 
    if t>=RT(21) and t<RT(72.6):
        root=chords[(int((t-start)//(bar*2)))%4][0]/2
        bass(t,root,.12)
    t+=BEAT; b+=1
def pluck(t,f,g=.05):
    if not MUSIC: return
    n=int(.5*SR); k=np.arange(n)/SR; x=(np.sin(2*np.pi*f*k)+.35*np.sin(2*np.pi*2*f*k)+.12*np.sin(2*np.pi*3*f*k))*env(n,.002,.18); addr(x,t,g,rng.uniform(-.35,.35))
t=RT(21.0); j=0
while t<RT(58.4):
    ch=chords[(int((t-start)//(bar*2)))%4]; f=[ch[0]*2,ch[1]*2,ch[2]*2,ch[1]*4][j%4]
    pluck(t,f,.045 if j%2==0 else .03); t+=BEAT/2; j+=1
t=RT(65.2); j=0
while t<RT(72.4):
    ch=chords[(int((t-start)//(bar*2)))%4]; pluck(t,[ch[0]*2,ch[2]*2,ch[1]*4,ch[2]*4][j%4],.04); t+=BEAT/2; j+=1
# --- interfaz ---
def blip(t,f=880,g=.12):
    n=int(.12*SR); k=np.arange(n)/SR; x=np.sin(2*np.pi*f*k)*env(n,.002,.04)+.5*np.sin(2*np.pi*f*1.5*k)*env(n,.002,.03); add(x,t,g)
for t in [21.1,26.4,29.9,39.3,43.7,49.4,50.9,52.3,53.7,55.0]: blip(t, 1320 if t in (26.4,49.4) else 880)
n=int(.03*SR); add(bp(noise(.03),2000,7000)*env(n,.0005,.006),31.55,.25)
for t in [32.0,33.0,33.7,34.4,35.1,35.8,36.5]:
    n=int(.35*SR); x=bp(noise(.35),3000,8000)*np.sin(np.pi*np.linspace(0,1,n)); add(x,t,.07,rng.uniform(-.3,.3)); blip(t+.3,1760,.05)
t=40.0
while t<42.6:
    n=int(.02*SR); x=bp(noise(.02),1500,5000)*env(n,.0005,.004); add(x,t,rng.uniform(.10,.16),rng.uniform(-.2,.2)); t+=rng.uniform(.06,.11)
def thud(t,g=.5):
    n=int(.4*SR); f=np.linspace(160,60,n); x=np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.001,.07); add(x,t,g); add(lp(noise(.08),1500)*env(int(.08*SR),.001,.02),t,g*.4)
for t in [51.15,52.55,53.95,55.25]: thud(t)
for t in [50.9,52.3,53.7,55.0]: whoosh(t+.55,.5,.09)
whoosh(49.9,.45,.1)
for t in [66.0,66.7,67.4,68.1,68.8]:
    whoosh(t+.35,.45,.12); blip(t+.2,660,.07)
n=int(.03*SR); add(bp(noise(.03),2000,7000)*env(n,.0005,.006),45.55,.3)
whoosh(46.1,.5,.12); whoosh(49.2,.4,.08)
# --- cierre: acorde final ---
n=int(7.5*SR); k=np.arange(n)/SR; x=np.zeros(n)
for f in [110,164.81,220,261.63,329.63]:
    x+=np.sin(2*np.pi*f*k)+.3*np.sin(2*np.pi*f*2*k)
x=x*np.minimum(1,k/.08)*np.exp(-k/3.2)
if MUSIC: add(x,72.65,.07)
hit(72.65,.9)
# --- master ---
fade=np.ones(N); nf=int(1.2*SR); fade[-nf:]=np.linspace(1,0,nf)
M=np.stack([L,R],1)*fade[:,None]
M=np.tanh(M*1.4)/np.tanh(1.4)
M=M/np.max(np.abs(M))*0.89
pcm=(M*32767).astype('<i2')
w=wave.open(OUT,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('rms dB', 20*np.log10(np.sqrt(np.mean(M**2))))
