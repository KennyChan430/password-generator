import tkinter as tk
from tkinter import ttk, DISABLED, NORMAL
import ctypes
from tkinter.ttk import Style


class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)

        self.columnconfigure(list(range(6)), uniform="uniform", weight=1)
        self.rowconfigure(list(range(15)), weight=1, uniform="uniform")
        # Theme mode
        self.theme_mode = 'light'  # default theme mode

        # Create value lists
        self.generated_password = "rtmhkbst32@#%jeh"

        # Declare parameters
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        self.var_3 = tk.IntVar(value=2)
        self.password_length_min = 1
        self.password_length_max = 100
        self.password_length = tk.IntVar(value=12)  # default password length
        self.char_pool = tk.IntVar(value=0)
        self.char_type = {
            'value': {
                'upper': tk.IntVar(value=1),
                'lower': tk.IntVar(value=1),
                'number': tk.IntVar(value=1),
                'symbol': tk.IntVar(value=1)
            }
        }

        # Widgets
        self.change_theme_switch = None
        self.result_frame = None
        self.result_label = None

        # Create widgets :)
        self.setup_widgets()

    def setup_widgets(self):
        r = Style()
        r.configure('Red.TFrame', background='pink')
        b = Style()
        b.configure('Blue.TFrame', background='lightgreen')
        c = Style()
        c.configure('LBlue.TFrame', background='lightblue')

        self.frame_top_bar = ttk.Frame(self)
        self.frame_left = ttk.Frame(self)
        self.frame_center = ttk.Frame(self)
        self.frame_right = ttk.Frame(self)

        # grid
        self.frame_top_bar.grid(row=0, column=0, columnspan=6, sticky='nsew')
        self.frame_left.grid(row=1, rowspan=14, column=0, sticky='nsew')
        self.frame_center.grid(row=1, rowspan=14, column=1, columnspan=4, sticky='nsew')
        self.frame_right.grid(row=1, rowspan=14, column=5, sticky='nsew')

        self.change_theme_switch = ttk.Checkbutton(self.frame_top_bar, text="Dark Mode", style="Switch.TCheckbutton", command=self.change_theme)
        self.change_theme_switch.pack(side='right', padx=10)

        self.result_frame = ttk.LabelFrame(self.frame_center, text="Result", padding=(20, 10))
        self.result_frame.pack(fill='x')

        self.result_label = ttk.Label(self.result_frame, text=self.generated_password,
                                      font=("-size", 15, "-weight", "bold"))
        self.result_label.pack(side='left', padx=10)

        self.config_frame = ttk.Frame(self, style='LBlue.TFrame')
        self.config_frame.grid(row=3, rowspan=12, column=1, columnspan=4, sticky='nsew')

        self.config_frame.columnconfigure((0, 1, 2), weight=1)

        self.config_title = ttk.Label(self.config_frame, text='Customize Your Password',
                                      font=("-size", 24, "-weight", "bold", "-family", "Monotype Corsiva"))
        self.config_title.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.separator = ttk.Separator(self.config_frame)
        self.separator.grid(row=1, column=0, columnspan=5, padx=(20, 10), pady=10, sticky='nsew')

        self.config_left_pane = ttk.Frame(self.config_frame, style='Red.TFrame')
        self.config_left_pane.grid(row=2, column=0, sticky='nsew')
        self.config_left_pane.rowconfigure((0, 1, 2), weight=1)

        self.password_length_label = ttk.Label(self.config_left_pane, text='Password Length')
        self.password_length_label.grid(row=0, columnspan=2, sticky='w')

        vcmd = (self.register(self.callback))
        self.password_length_entry = ttk.Entry(self.config_left_pane, width=5,
                                               validate='all', validatecommand=(vcmd, '%P'))
        self.password_length_entry.insert(-1, self.password_length.get())

        self.password_length_entry.grid(row=1, column=0, sticky='ns', pady=5, padx=10)

        self.password_length_scale = ttk.Scale(
            self.config_left_pane,
            from_=self.password_length_min,
            to=self.password_length_max,
            variable=self.password_length,
            command=lambda event: self.password_length.set(self.password_length_scale.get()),
        )
        self.password_length_scale.grid(row=1, column=1, sticky='ew')

        self.config_center_pane = ttk.Frame(self.config_frame, style='Blue.TFrame')
        self.config_center_pane.grid(row=2, column=1, sticky='nsew')

        self.easy2read_radio_btn = ttk.Radiobutton(self.config_center_pane, text='Easy to Read', variable=self.char_pool, value=0)
        self.easy2read_radio_btn.grid(sticky='w')

        self.all_chars_radio_btn = ttk.Radiobutton(self.config_center_pane, text='All Characters', variable=self.char_pool, value=1)
        self.all_chars_radio_btn.grid(sticky='w')

        self.config_right_pane = ttk.Frame(self.config_frame, style='Red.TFrame')
        self.config_right_pane.grid(row=2, column=2, sticky='nsew')

        self.char_type['btn'] = {
            'upper': ttk.Checkbutton(self.config_right_pane, text='Uppercase',
                                     onvalue=1, offvalue=0,
                                     variable=self.char_type['value']['upper'],
                                     command=lambda: self.check_if_last_checkbox()),
            'lower': ttk.Checkbutton(self.config_right_pane, text='Lowercase',
                                     onvalue=1, offvalue=0,
                                     variable=self.char_type['value']['lower'],
                                     command=lambda: self.check_if_last_checkbox()),
            'number': ttk.Checkbutton(self.config_right_pane, text='Numbers',
                                      onvalue=1, offvalue=0,
                                      variable=self.char_type['value']['number'],
                                      command=lambda: self.check_if_last_checkbox()),
            'symbol': ttk.Checkbutton(self.config_right_pane, text='Symbols',
                                      onvalue=1, offvalue=0,
                                      variable=self.char_type['value']['symbol'],
                                      command=lambda: self.check_if_last_checkbox())
        }
        # grid all char_type button
        for x in self.char_type['btn'].values():
            x.grid(sticky='w')

    def change_theme(self):
        self.theme_mode = 'light' if self.tk.call("ttk::style", "theme", "use") == "azure-dark" \
            else 'dark'
        self.tk.call("set_theme", self.theme_mode)

    def callback(self, P):
        if P == "":
            return True
        else:
            if (str.isdigit(P) and
                    self.password_length_min <= int(float(P)) <= self.password_length_max):
                return True
            else:
                return False

    def check_if_last_checkbox(self):
        if sum([x.get() for x in self.char_type['value'].values()]) == 1:
            target_char_type = next((k for k, v in self.char_type['value'].items() if v.get() == 1), '')
            self.char_type['btn'][target_char_type].config(state=DISABLED)
        else:
            for x in self.char_type['btn'].values():
                x.config(state=NORMAL)


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("1600x1200")
    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

    root.mainloop()
