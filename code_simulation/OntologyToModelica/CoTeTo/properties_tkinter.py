#Base code from https://codereview.stackexchange.com/questions/97332/tkinter-gui-for-making-very-simple-edits-to-pandas-dataframes

try: 
    import Tkinter as tk
except ImportError:
    import tkinter as tk
#import tkinter.font

import pandas

class EditorApp:

    def __init__(self, master, dataframe, edit_rows=[]):
        """ master    : tK parent widget
        dataframe : pandas.DataFrame object"""
        self.root = master
        self.root.minsize(width=600, height=400)
        self.root.title('Data Property File Editor')

        self.main = tk.Frame(self.root)
        self.main.pack(fill=tk.BOTH, expand=True)
        

        self.lab_opt = {'background': 'blue', 'foreground': 'white'}


#       the dataframe
        self.df = dataframe
        self.dat_cols = list(self.df)
        if edit_rows:
            self.dat_rows = edit_rows
        else:
            self.dat_rows = range(len(self.df))
        self.rowmap = {i: row for i, row in enumerate(self.dat_rows)}

#       subset the data and convert to giant list of strings (rows) for viewing
        
        #myformatter = lambda x: '{:>10}'.format(x)
        #formatters={'BUDO': myformatter, 'explanation': myformatter, 'parameter': myformatter, 'tag': myformatter, 'unit': myformatter, 'value': myformatter}
        
        self.sub_data = self.df.loc[self.dat_rows, self.dat_cols]
        #col_space=xxx
        self.sub_datstring = self.sub_data.to_string(
            index=False, col_space=100).split('\n')
        self.title_string = self.sub_datstring[0]

# save the format of the lines, so we can update them without re-running
# df.to_string()
        self._get_line_format(self.title_string)

#       fill in the main frame
        self._fill()

#       updater for tracking changes to the database
        self.update_history = []

##################
# ADDING WIDGETS #
##################
    def _fill(self):
        self.canvas = tk.Canvas(self.main)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self._init_scroll()
        self._init_lb()
        self._pack_config_scroll()
        self._pack_bind_lb()
        self._fill_listbox()
        self._make_editor_frame()
        self._sel_mode()

##############
# SCROLLBARS #
##############
    def _init_scroll(self):
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical")
        self.xscrollbar = tk.Scrollbar(self.canvas, orient="horizontal")

    def _pack_config_scroll(self):
        self.scrollbar.config(command=self.lb.yview)
        self.xscrollbar.config(command=self._xview)
        self.scrollbar.pack(side="right", fill="y")
        self.xscrollbar.pack(side="bottom", fill="x")

    def _onMouseWheel(self, event):
        self.title_lb.yview("scroll", event.delta, "units")
        self.lb.yview("scroll", event.delta, "units")
        return "break"

    def _xview(self, *args):
        """connect the yview action together"""
        self.lb.xview(*args)
        self.title_lb.xview(*args)

################
# MAIN LISTBOX #
################
    def _init_lb(self):
        self.title_lb = tk.Listbox(self.canvas, height=1,
                                   yscrollcommand=self.scrollbar.set,
                                   xscrollcommand=self.xscrollbar.set,
                                   exportselection=False)

        self.lb = tk.Listbox(self.canvas,
                             yscrollcommand=self.scrollbar.set,
                             xscrollcommand=self.xscrollbar.set,
                             exportselection=False,
                             selectmode=tk.EXTENDED)

    def _pack_bind_lb(self):
        self.title_lb.pack(fill=tk.X)
        self.lb.pack(fill="both", expand=True)
        self.title_lb.bind("<MouseWheel>", self._onMouseWheel)
        self.lb.bind("<MouseWheel>", self._onMouseWheel)

    def _fill_listbox(self):
        """ fill the listbox with rows from the dataframe"""
        self.title_lb.insert(tk.END, self.title_string)
        for line in self.sub_datstring[1:]:
            self.lb.insert(tk.END, line)
            self.lb.bind('<ButtonRelease-1>', self._listbox_callback)
        self.lb.select_set(0)


    def _listbox_callback(self, event):
        """ when a listbox item is selected"""
        items = self.lb.curselection()
        if items:
            new_item = items[-1]
            dataVal = str(
                self.df.loc[
                    self.rowmap[new_item],
                    self.opt_var.get()])
            self.entry_box_old.config(state=tk.NORMAL)
            self.entry_box_old.delete(0, tk.END)
            self.entry_box_old.insert(0, dataVal)
            self.entry_box_old.config(state=tk.DISABLED)

#####################
# FRAME FOR EDITING #
#####################
    def _make_editor_frame(self):
        """ make a frame for editing dataframe rows"""
        self.editorFrame = tk.Frame(
            self.main, bd=2, padx=2, pady=2, relief=tk.GROOVE)
        self.editorFrame.pack(fill=tk.BOTH, side=tk.LEFT)

#       column editor
        self.col_sel_lab = tk.Label(
            self.editorFrame,
            text='Select a cell to edit:',
            **self.lab_opt)
        self.col_sel_lab.grid(row=0, columnspan=2, sticky=tk.W + tk.E)

        self.opt_var = tk.StringVar()
        self.opt_var.set(self.dat_cols[0])
        self.opt = tk.OptionMenu(
            self.editorFrame,
            self.opt_var,
            *
            list(
                self.df))
        self.opt.grid(row=0, columnspan=2, column=2, sticky=tk.E + tk.W)

        self.old_val_lab = tk.Label(
            self.editorFrame,
            text='Old value:',
            **self.lab_opt)
        self.old_val_lab.grid(row=1, sticky=tk.W, column=0)
        self.entry_box_old = tk.Entry(
            self.editorFrame,
            state=tk.DISABLED,
            bd=2,
            relief=tk.GROOVE)
        self.entry_box_old.grid(row=1, column=1, sticky=tk.E)

#       entry widget
        self.new_val_lab = tk.Label(
            self.editorFrame,
            text='New value:',
            **self.lab_opt)
        self.new_val_lab.grid(row=1, sticky=tk.E, column=2)
        self.entry_box_new = tk.Entry(self.editorFrame, bd=2, relief=tk.GROOVE)
        self.entry_box_new.grid(row=1, column=3, sticky=tk.E + tk.W)

#       make update button
        self.update_b = tk.Button(
            self.editorFrame,
            text='Update value',
            relief=tk.RAISED,
            command=self._updateDF_multi)
        self.update_b.grid(row=2, columnspan=1, column=3, sticky=tk.W + tk.E)

#       make undo button
        self.undo_b = tk.Button(
            self.editorFrame,
            text='Undo',
            command=self._undo)
        self.undo_b.grid(row=2, columnspan=1, column=1, sticky=tk.W + tk.E)

################
# SELECT MODES #
################
    def _sel_mode(self):
        """ creates a frame for toggling between interaction modes wt"""
        self.mode_frame = tk.Frame(
            self.main, bd=2, padx=2, pady=2, relief=tk.GROOVE)
        self.mode_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        tk.Label(self.mode_frame, text='Selection mode', **
                 self.lab_opt).pack(fill=tk.BOTH, expand=tk.YES)

        self.mode_lb = tk.Listbox(
            self.mode_frame,
            height=2,
            width=16,
            exportselection=False)
        self.mode_lb.pack(fill=tk.BOTH, expand=tk.YES)
        self.mode_lb.insert(tk.END, 'Select by cell')
        self.mode_lb.bind('<ButtonRelease-1>', self._mode_lb_callback)
        self.mode_lb.insert(tk.END, 'Find and replace')
        self.mode_lb.bind('<ButtonRelease-1>', self._mode_lb_callback)
        self.mode_lb.select_set(0)

    def _mode_lb_callback(self, event):
        items = self.mode_lb.curselection()
        if items[0] == 0:
            self._swap_mode('multi')
        elif items[0] == 1:
            self._swap_mode('findrep')

    def _swap_mode(self, mode='multi'):
        """swap between modes of interaction with database"""
        self.lb.selection_clear(0, tk.END)
        self._swap_lab(mode)
        if mode == 'multi':
            self.lb.config(state=tk.NORMAL)
            self.entry_box_old.config(state=tk.DISABLED)
            self.update_b.config(
                command=self._updateDF_multi,
                text='Update multi selection')
        elif mode == 'findrep':
            self.lb.config(state=tk.DISABLED)
            self.entry_box_old.config(state=tk.NORMAL)
            self.update_b.config(
                command=self._updateDF_findrep,
                text='Find and replace')
        self.entry_box_new.delete(0, tk.END)
        self.entry_box_new.insert(0, "Enter new value")

    def _swap_lab(self, mode='multi'):
        """ alter the labels on the editor frame"""
        if mode == 'multi':
            self.old_val_lab.config(text='Old value:')
            self.new_val_lab.config(text='New value:')
        elif mode == 'findrep':
            self.old_val_lab.config(text='Find:')
            self.new_val_lab.config(text='Replace:')

#################
# EDIT COMMANDS #
#################
    def _updateDF_multi(self):
        """ command for updating via selection"""
        self.col = self.opt_var.get()
        items = self.lb.curselection()
        self._track_items(items)

    def _updateDF_findrep(self):
        """ command for updating via find/replace"""
        self.col = self.opt_var.get()
        old_val = self.entry_box_old.get()
        try:
            items = pandas.np.where(
                self.sub_data[
                    self.col].astype(str) == old_val)[0]
        except TypeError as err:
            self.errmsg(
                '%s: `%s` for column `%s`!' %
                (err, str(old_val), self.col))
            return
        if not items.size:
            self.errmsg(
                'Value`%s` not found in column `%s`!' %
                (str(old_val), self.col))
            return
        else:
            self._track_items(items)
            self.lb.config(state=tk.DISABLED)

    def _undo(self):
        if self.update_history:
            updated_vals = self.update_history.pop()
            for idx, val in updated_vals['vals'].items():
                self.row = self.rowmap[idx]
                self.idx = idx
                self.df.set_value(self.row, updated_vals['col'], val)
                self._rewrite()
            self.sync_subdata()

####################
# HISTORY TRACKING #
####################
    def _track_items(self, items):
        """ this strings several functions together,
        updates database, tracks changes, and updates database viewer"""
        self._init_hist_tracker()
        for i in items:
            self.idx = i
            self.row = self.rowmap[i]
            self._track()
            self._setval()
            self._rewrite()
        self._update_hist_tracker()
#       update sub_data used w find and replace
        self.sync_subdata()

    def _setval(self):
        """ update database"""
        try:
            self.df.set_value(self.row, self.col, self.entry_box_new.get())
        except ValueError:
            self.errmsg(
                'Invalid entry `%s` for column `%s`!' %
                (self.entry_box_new.get(), self.col))

    def _init_hist_tracker(self):
        """ prepare to track a changes to the database"""
        self.prev_vals = {}
        self.prev_vals['col'] = self.col
        self.prev_vals['vals'] = {}

    def _track(self):
        """record a change to the database"""
        self.prev_vals['vals'][self.idx] = str(self.df.loc[self.row, self.col])

    def _update_hist_tracker(self):
        """ record latest changes to database"""
        self.update_history.append(self.prev_vals)

    def sync_subdata(self):
        """ syncs subdata with data"""
        self.sub_data = self.df.loc[self.dat_rows, self.dat_cols]

#################
# ERROR MESSAGE #
#################
    def errmsg(self, message):
        """ opens a simple error message"""
        errWin = tk.Toplevel()
        tk.Label(
            errWin,
            text=message,
            foreground='white',
            background='red').pack()
        tk.Button(errWin, text='Ok', command=errWin.destroy).pack()

##################
# UPDATING LINES #
##################
    def _rewrite(self):
        """ re-writing the dataframe string in the listbox"""
        new_col_vals = self.df.loc[self.row, self.dat_cols].astype(str).tolist()
        new_line = self._make_line(new_col_vals)
        if self.lb.cget('state') == tk.DISABLED:
            self.lb.config(state=tk.NORMAL)
            self.lb.delete(self.idx)
            self.lb.insert(self.idx, new_line)
            self.lb.config(state=tk.DISABLED)
        else:
            self.lb.delete(self.idx)
            self.lb.insert(self.idx, new_line)

    def _get_line_format(self, line):
        """ save the format of the title string, stores positions
            of the column breaks"""
            
        list_chars=[]
        for line in self.sub_datstring[1:]:
            for n in self.dat_cols:
                list_chars.append(int(line.find(' ' + n) + len(n))) 
            pos=[max(list_chars)]
# #--------PRUEBAS  
#        df=edited_df
#        
#        dat_rows = range(len(df))
#        dat_cols = list(df)
#        sub_data = df.loc[dat_rows, dat_cols]
#        
#        myformatter = lambda x: '{:>10}'.format(x)
#        
#        
#        sub_datstring = sub_data.to_string(
#            index=False, formatters={'BUDO': myformatter, 'explanation': myformatter, 'parameter': myformatter, 'tag': myformatter, 'unit': myformatter, 'value': myformatter}).split('\n')
#        title_string = sub_datstring[0]
#         
#        list_chars=[]
#        for line in sub_datstring[1:]:
#            for n in dat_cols:
#                list_chars.append(int(line.find(' ' + n) + len(n))) 
#            pos=[max(list_chars)]
#            
#---------FIN PRUEBAS            
        pos = [1 + line.find(' ' + n) + len(n) for n in self.dat_cols]
        self.entry_length = [pos[0]] + \
                            [p2 - p1 for p1, p2 in zip(pos[:-1], pos[1:])]

    def _make_line(self, col_entries):
        """ add a new line to the database in the correct format"""
        new_line_entries = [('{:^50}' % self.entry_length[i]).format(entry)
                            for i, entry in enumerate(col_entries)]
#        new_line_entries=[('{0: >%d}' % self.[20]).format(entry)
#                       for entry in enumerate(col_entries)]
        new_line = "".join(new_line_entries)
        return new_line


#def main():
##    from pyld import jsonld
##
##    from ebc_jsonld_files.initial_jsonld import context
##    from ebc_jsonld_files.initial_jsonld import doc
##    jsonldfile = jsonld.compact(doc, {"@context": context})
##    from jsonld_budo_to_ontology import budo_to_graph
##    (g,df)=budo_to_graph(jsonldfile)
#
##   start
#    root = tk.Tk()
#    editor = EditorApp(root, df)
#    root.mainloop()  # until closes window
#
##   re-assign dataframe
#    new_df = editor.df
#
#    #print ("THIS IS THE NEW DATABASE:")
#    #print (new_df.to_string(index=False))
#    
#    return new_df
#
#if __name__ == '__main__':
#    main()
#    
#
#
##edited_df=main()
#
