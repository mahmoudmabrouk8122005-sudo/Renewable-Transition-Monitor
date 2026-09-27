"""Renewable Transition Monitor — Tkinter sustainability dashboard."""
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sustainability Lens: forest green, warm cream, and calm evidence-first composition.
GREEN='#2E8B57'; DEEP='#173F35'; CREAM='#FBFAF2'; GOLD='#D9A441'; MUTED='#6E817B'
class RenewableMonitor(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('Renewable Transition Monitor'); self.geometry('1260x800'); self.configure(bg=CREAM)
        self.data=pd.read_csv(Path(__file__).parent/'data'/'renewable_transition_data.csv'); self.start_year=tk.StringVar(); self.end_year=tk.StringVar(); self.target_var=tk.StringVar(value='25'); self.build(); self.draw()
    def build(self):
        top=tk.Frame(self,bg=DEEP,padx=30,pady=18); top.pack(fill='x'); tk.Label(top,text='RENEWABLE TRANSITION MONITOR',bg=DEEP,fg='white',font=('Segoe UI',13,'bold')).pack(side='left'); tk.Label(top,text='SUSTAINABILITY INTELLIGENCE / 02',bg=DEEP,fg='#B9D2C5',font=('Consolas',9)).pack(side='right')
        hero=tk.Frame(self,bg=CREAM,padx=34,pady=28); hero.pack(fill='x'); tk.Label(hero,text='Make the shift visible.',bg=CREAM,fg=GREEN,font=('Georgia',34,'italic')).pack(anchor='w'); tk.Label(hero,text='A comparative view of renewable electricity share in Egypt and the world benchmark.',bg=CREAM,fg=DEEP,font=('Segoe UI',11)).pack(anchor='w',pady=6)
        self.cards=tk.Frame(self,bg=CREAM,padx=34); self.cards.pack(fill='x'); self.card_labels=[]
        for i in range(3):
            f=tk.Frame(self.cards,bg='white',highlightbackground='#D8E2DB',highlightthickness=1,padx=18,pady=14); f.pack(side='left',fill='both',expand=True,padx=(0 if i==0 else 10,0)); l=tk.Label(f,text='—',bg='white',fg=MUTED,font=('Consolas',8)); l.pack(anchor='w'); v=tk.Label(f,text='—',bg='white',fg=GREEN,font=('Georgia',23,'bold')); v.pack(anchor='w',pady=5); self.card_labels.append((l,v))
        controls=tk.Frame(self,bg=CREAM,padx=34,pady=18); controls.pack(fill='x'); tk.Label(controls,text='COMPARE YEARS',bg=CREAM,fg=MUTED,font=('Consolas',9)).pack(side='left'); years=[str(int(y)) for y in sorted(self.data.Year.unique())]; self.start_year.set(years[0]); self.end_year.set(years[-1]); ttk.Combobox(controls,textvariable=self.start_year,values=years,state='readonly',width=10).pack(side='left',padx=10); tk.Label(controls,text='to',bg=CREAM,fg=MUTED).pack(side='left'); ttk.Combobox(controls,textvariable=self.end_year,values=years,state='readonly',width=10).pack(side='left',padx=10); main=tk.Frame(self,bg=CREAM,padx=34,pady=20); main.pack(fill='both',expand=True); self.fig=Figure(figsize=(10,4),dpi=100,facecolor='white'); self.ax=self.fig.add_subplot(111); self.canvas=FigureCanvasTkAgg(self.fig,master=main); self.canvas.get_tk_widget().pack(fill='both',expand=True)
        self.res_frame=tk.Frame(self,bg='#EAF3EC',padx=34,pady=12); self.res_frame.pack(fill='x',padx=34); self.res_label=tk.Label(self.res_frame,text='Press RUN SCENARIO to compare growth rates.',bg='#EAF3EC',fg=DEEP,font=('Segoe UI',10,'bold')); self.res_label.pack(side='left'); tk.Button(self.res_frame,text='RUN SCENARIO',command=self.run_scenario,bg=GREEN,fg='white',relief='flat',font=('Segoe UI',9,'bold'),padx=12).pack(side='right'); target_bar=tk.Frame(self,bg=CREAM,padx=34,pady=8); target_bar.pack(fill='x'); tk.Label(target_bar,text='TARGET %',bg=CREAM,fg=MUTED,font=('Consolas',9)).pack(side='left'); tk.Entry(target_bar,textvariable=self.target_var,width=8).pack(side='left',padx=10); tk.Button(target_bar,text='CHECK TARGET',command=self.check_target,bg=GOLD,fg=DEEP,relief='flat',font=('Segoe UI',9,'bold'),padx=12).pack(side='left'); self.target_result=tk.Label(target_bar,text='Set a renewable-share target to find the first year Egypt reaches it.',bg=CREAM,fg=DEEP,font=('Segoe UI',10,'bold')); self.target_result.pack(side='left',padx=16); tk.Label(self,bg=CREAM,fg=MUTED,text='Decision note: compare the pace of the transition, then investigate the policy and investment context behind the curve.',font=('Segoe UI',10),pady=10).pack()
    def draw(self):
        egypt=self.data[self.data.Entity=='Egypt']; world=self.data[self.data.Entity=='World']; col=self.data.columns[-1]; last=egypt.iloc[-1]; first=egypt.iloc[0]
        vals=[('LATEST EGYPT YEAR',str(int(last.Year))),('EGYPT RENEWABLE SHARE',f'{last[col]:.1f}%'),('WORLD BENCHMARK',f'{world.iloc[-1][col]:.1f}%')]
        for pack,(a,b) in zip(self.card_labels,vals): pack[0].config(text=a); pack[1].config(text=b)
        self.ax.clear(); self.ax.set_facecolor('white'); self.ax.grid(alpha=.16,axis='y')
        self.ax.plot(egypt.Year,egypt[col],marker='o',lw=2.6,color=GREEN,label='Egypt'); self.ax.plot(world.Year,world[col],lw=2,color=GOLD,label='World benchmark'); self.ax.set_title('Renewables share of electricity',loc='left',fontdict={'fontsize':14,'fontweight':'bold','color':DEEP}); self.ax.set_ylabel('% of electricity'); self.ax.legend(frameon=False); self.ax.spines[['top','right']].set_visible(False); self.fig.tight_layout(); self.canvas.draw()
    def run_scenario(self):
        egypt=self.data[(self.data.Entity=='Egypt') & (self.data.Year.between(int(self.start_year.get()),int(self.end_year.get())))]; world=self.data[(self.data.Entity=='World') & (self.data.Year.between(int(self.start_year.get()),int(self.end_year.get())))]; col=self.data.columns[-1]
        e_growth=egypt.iloc[-1][col]-egypt.iloc[0][col]; w_growth=world.iloc[-1][col]-world.iloc[0][col]
        self.res_label.config(text=f'SCENARIO RESULT  →  Egypt moved {e_growth:.1f} points from {self.start_year.get()} to {self.end_year.get()}, versus {w_growth:.1f} points globally. The gap changed by {(e_growth-w_growth):.1f} points.')

    def check_target(self):
        col=self.data.columns[-1]; target=float(self.target_var.get()); egypt=self.data[self.data.Entity=='Egypt']; hit=egypt[egypt[col]>=target]
        if hit.empty: self.target_result.config(text=f'TARGET RESULT → Egypt has not reached {target:.0f}% in the available data.')
        else: self.target_result.config(text=f'TARGET RESULT → Egypt first reaches {target:.0f}% in {int(hit.iloc[0].Year)} at {hit.iloc[0][col]:.1f}%.')

if __name__=='__main__': RenewableMonitor().mainloop()
