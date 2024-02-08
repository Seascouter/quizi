# Imports
import os
import random
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.constants import *
import quizi

# General Window Manager Class
class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("Quizi") # Window title


        container = tk.Frame(self, height=480, width=640) # container for all of the screens
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Every screen
        self.frames = {
            "HomeScreen": HomeScreen(container, self),
            "SetScreen": SetScreen(container, self),
            "FCScreen": FCScreen(container, self),
            "LearnScreen": LearnScreen(container, self),
        }
        # Load every screen
        for key in self.frames:
            self.frames[key].grid(row=0, column=0, sticky="nsew")

        # start on home screen
        self.show_frame("HomeScreen")

    # to change frames, refresh the frame and raise it to the window
    def show_frame(self, cont):
        if cont != "LearnScreen":
            self.frames[cont].refresh()
        else:
            self.frames[cont].ref()
        self.frames[cont].tkraise()

# Home Screen
class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        # Initialize the frame and label
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Quizi", font=("Arial", 18, 'bold', 'underline'))
        label.grid(row=0, column=2, sticky=EW)

        self.current_set = tk.StringVar() # Current Set


        self.current_set_label = ttk.Label( # displays the current set on the screen
            self,
            text=self.current_set.get()
        )
        self.current_set_label.grid(row=1, column=2, sticky=EW)

        self.set_cs() # set the current label to say the blank set upon load

        set_selection_button = ttk.Button(
            self,
            text="Set Selection",
            command=self.browse_sets,
            cursor="hand"
        ).grid(row=2, column=0, sticky=EW)

        new_edit_set_button = ttk.Button(
            self,
            text="New/Edit Set",
            command=lambda: controller.show_frame("SetScreen"),
            cursor="hand"
        ).grid(row=2, column=1, sticky=EW)

        learn_button = ttk.Button(
            self,
            text="Learn Set",
            command=lambda: controller.show_frame("LearnScreen"),
            cursor="hand"
        ).grid(row=2, column=3, sticky=EW)

        flashcard_button = ttk.Button(
            self,
            text="Flash Cards",
            command=lambda: controller.show_frame("FCScreen"),
            cursor="hand"
        ).grid(row=2, column=4, sticky=EW)

    def set_cs(self):
        # Sets the current set label to the current set name
        self.current_set.set(f"Current Set: {quizi.currentSet.get_name()}")
        self.current_set_label.configure(text=self.current_set.get())
        

    def browse_sets(self):
        # Opens a file dialog to return a path of a file
        filename = filedialog.askopenfilename(
            initialdir = "~/quizi/sets",
            title = "Choose a Set",
            filetypes = (("Set File", "*.set"), ("All Files", "*.*"))
        )
        quizi.loadSet(filename) # Quizi loads the set
        self.set_cs() # The set name label is reset

    def refresh(self):
        # Nothing function to not raise errors
        pass

class FCScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) # Initializes the frame

        self.current_fc_text = tk.StringVar() # Variable for the current question/answer

        # To check whether a valid set is loaded
        self.enabled = True
        if quizi.currentSet.get_name() == "N/A":
            self.enabled = False
            self.current_fc_text.set("Please load a study set\nto begin studying!")
        else:
            self.enabled = True
        
        self.set_index = 0
        self.qa = "q"

        self.swap = False
        self.is_random = False

        self.random_order = list(range(0, len(quizi.currentSet.contents)))

        # The label of the current set and position in the set
        self.label = tk.Label(self, text=f"Flash Cards: {quizi.currentSet.get_name()} | Term {self.set_index + 1}/{len(quizi.currentSet.contents)}")
        self.label.grid(row=0, column=1)

        home_button = ttk.Button(
            self,
            text="Home",
            command=lambda: controller.show_frame("HomeScreen"),
            cursor="hand"
        )
        home_button.grid(row=4, column=1)

        refresh_button = ttk.Button(
            self,
            text="Refresh",
            command=self.refresh,
            cursor="hand"
        )
        refresh_button.grid(row=4, column=0)

        info_canvas = tk.Canvas(self, bg="#3f3f3f")
        info_canvas.grid(row=1, column=0, rowspan=2, columnspan=3)
        info_canvas.pack_propagate(False)

        self.info_canvas_text = tk.Label(info_canvas, text=self.current_fc_text.get())
        self.info_canvas_text.pack(expand=True)

        back_button = ttk.Button(
            self,
            text="Back",
            command=self.back,
            cursor="hand"
        ).grid(row=3, column=0)

        flip_button = ttk.Button(
            self,
            text="Flip",
            command=self.flip,
            cursor="hand"
        ).grid(row=3, column=1)

        forward_button = ttk.Button(
            self,
            text="Forward",
            command=self.forward,
            cursor="hand"
        ).grid(row=3, column=2)

        self.q_a_swap_button = ttk.Button(
            self,
            text="Show Question",
            command=self.swap_qa,
            cursor="hand"
        )
        self.q_a_swap_button.grid(row=5, column=0)

        self.random_button = ttk.Button(
            self,
            text="Fixed Order",
            command=self.set_random_order,
            cursor="hand"
        )
        self.random_button.grid(row=5, column=2)
        
    def swap_qa(self):
        if self.swap:
            self.swap = False
            self.q_a_swap_button.configure(text="Show Question") # resets text on button to mean showing questions
        else:
            self.swap = True
            self.q_a_swap_button.configure(text="Show Answer") # resets text on button to mean showing answers
        self.print_fc(self.set_index)
        
    def set_random_order(self):
        if self.is_random:
            self.is_random = False
            self.random_button.configure(text="Fixed Order") # resets text on button to mean the order of the set
        else:
            self.is_random = True
            self.random_button.configure(text="Random Order") # resets text on button to mean the set will be asked in a random order
        self.print_fc(self.set_index)

    def print_fc(self, index):
        if self.enabled:
            if self.qa == "q":
                if self.swap:
                    if self.is_random:
                        self.current_fc_text.set(quizi.currentSet.contents[self.random_order[index]].get_a()) # Get a random answer
                    else:
                        self.current_fc_text.set(quizi.currentSet.contents[index].get_a()) # Get the position's answer
                else:
                    if self.is_random:
                        self.current_fc_text.set(quizi.currentSet.contents[self.random_order[index]].get_q()) # Get a random question
                    else:
                        self.current_fc_text.set(quizi.currentSet.contents[index].get_q()) # Get the position's question
            else:
                if self.swap:
                    if self.is_random:
                        self.current_fc_text.set(quizi.currentSet.contents[self.random_order[index]].get_q()) # Get the random answer's question
                    else:
                        self.current_fc_text.set(quizi.currentSet.contents[index].get_q()) # Get the position's question
                else:
                    if self.is_random:
                        self.current_fc_text.set(quizi.currentSet.contents[self.random_order[index]].get_a()) # Get the random question's answer
                    else:
                        self.current_fc_text.set(quizi.currentSet.contents[index].get_a()) # Get the position's answer
            
            self.info_canvas_text.configure(text=self.current_fc_text.get()) # Set the text on screen to the respective question/answer

    def forward(self):
        # reset the counter if gone too far
        if self.set_index == len(quizi.currentSet.contents) - 1:
            self.set_index = 0
            random.shuffle(self.random_order)
        # or just increment the counter
        else:
            self.set_index += 1
        # Go to the question and update the flash card and label
        self.qa = "q"
        self.print_fc(self.set_index)
        self.label.configure(text=f"Flash Cards: {quizi.currentSet.get_name()} | Term {self.set_index + 1}/{len(quizi.currentSet.contents)}")

    def back(self):
        # reset the counter if gone too far
        if self.set_index == 0:
            self.set_index = len(quizi.currentSet.contents) - 1
        # or just decrement the counter
        else:
            self.set_index += -1
        # Go to the question and update the flash card and label
        self.qa = "q"
        self.print_fc(self.set_index)
        self.label.configure(text=f"Flash Cards: {quizi.currentSet.get_name()} | Term {self.set_index + 1}/{len(quizi.currentSet.contents)}")
        
            
    def flip(self):
        # q -> a
        # a -> q
        # reprint the flash card
        if self.enabled:
            if self.qa == "q":
                self.qa = "a"
                self.print_fc(self.set_index)
            else:
                self.qa = "q"
                self.print_fc(self.set_index)

        
    def refresh(self):
        # If using the blank set
        if quizi.currentSet.get_name() == "N/A":
            # set enabled to false
            # display a message to load a set
            # lock down functionality of buttons
            self.enabled = False
            self.current_fc_text.set("Please load a study set\nto begin studying!")
        else:
            # otherwise set enabled to true
            # enable functionality of buttons
            self.enabled = True
        if self.enabled:
            # If an actual set is loaded
            self.current_fc_text.set(quizi.currentSet.contents[0].get_q()) # Set first term to the screen's flash card
            self.info_canvas_text.configure(text=self.current_fc_text.get())
            self.label.configure(text=f"Flash Cards: {quizi.currentSet.get_name()} | Term {self.set_index + 1}/{len(quizi.currentSet.contents)}") # Display name and term of set
            # Set starting variables for functionality: start on question, term 0, unswapped question/answer, and fixed order
            self.qa = "q"
            self.set_index = 0
            self.swap = False
            self.is_random = False
            # Prepare the random order
            self.random_order = list(range(0, len(quizi.currentSet.contents)))
            random.shuffle(self.random_order)
            
class LearnScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # mc for Multiple Choice | wr for Written Response
        self.mode = "mc"

        self.set_index = 0
        self.count = 0

        self.random_order = list(range(0, len(quizi.currentSet.contents)))
        self.random_index = 0

        self.rb_var = tk.IntVar()
        self.entry_var = tk.StringVar()
        self.current_learn_text = tk.StringVar()
        self.correct_rb = 1
        self.wrong_answer_text = tk.StringVar()

        self.swap = False
        self.is_random = False

        # To check whether a valid set is loaded
        self.enabled = True
        if quizi.currentSet.get_name() == "N/A":
            self.enabled = False
            self.current_learn_text.set("Please load a study set\nto begin studying!")
        else:
            self.enabled = True

        # Set the label to display the set name
        self.label = tk.Label(self, text=f"Learn Set: {quizi.currentSet.get_name()}")
        self.label.grid(row=0, column=1)

        info_canvas = tk.Canvas(self, bg="#3f3f3f")
        info_canvas.grid(row=1, column=0, rowspan=2, columnspan=3)
        info_canvas.pack_propagate(False)
        self.info_canvas_text = tk.Label(info_canvas, text=self.current_learn_text.get())
        self.info_canvas_text.pack(expand=True)

        self.incorrect_label = tk.Label(
            self,
            text=self.wrong_answer_text,
            fg="#f66"
        )

        self.op1 = tk.Radiobutton(self, variable=self.rb_var, value=1)
        self.op1.grid(row=4, column=0)
        self.op2 = tk.Radiobutton(self, variable=self.rb_var, value=2)
        self.op2.grid(row=4, column=2)
        self.op3 = tk.Radiobutton(self, variable=self.rb_var, value=3)
        self.op3.grid(row=5, column=0)
        self.op4 = tk.Radiobutton(self, variable=self.rb_var, value=4)
        self.op4.grid(row=5, column=2)
        
        self.entry = tk.Entry(
            self,
            textvariable=self.entry_var
        )
        self.entry.grid(row=6, column=0, columnspan=2)
        
        self.confirm = tk.Button(
            self,
            text="Confirm",
            command=self.answer,
            cursor="hand"
        ).grid(row=6, column=2)

        self.refresh = ttk.Button(
            self,
            text="Refresh",
            command=self.ref,
            cursor="hand"
        ).grid(row=7, column=0)
        
        self.home_button = ttk.Button(
            self,
            text="Home",
            command=lambda: controller.show_frame("HomeScreen"),
            cursor="hand"
        ).grid(row=7, column=1)

        self.q_a_swap_button = ttk.Button(
            self,
            text="Show Question",
            command=self.swap_qa,
            cursor="hand"
        )
        self.q_a_swap_button.grid(row=8, column=0)

        self.random_button = ttk.Button(
            self,
            text="Fixed Order",
            command=self.set_random_order,
            cursor="hand"
        )
        self.random_button.grid(row=8, column=2)

    # Swap whether it asks for the question or the answer.
    def swap_qa(self):
        if self.swap:
            self.swap = False
            self.q_a_swap_button.configure(text="Show Question")
        else:
            self.swap = True
            self.q_a_swap_button.configure(text="Show Answer")
        self.update_screen()

    # Swap whether questions are asked in the fixed order or a random order.
    def set_random_order(self):
        if self.is_random:
            self.is_random = False
            self.set_index = 0
            self.count = 0
            self.update_screen()
            self.random_button.configure(text="Fixed Order")
        else:
            self.is_random = True
            self.set_index = 0
            self.count = 0
            self.update_screen()
            self.random_button.configure(text="Random Order")

    def update_screen(self):
        # Reset count if it gets too high
        if self.count > 4:
            self.count = 0
        if self.count < 3:
            # Set multiple choice mode for 3 questions
            self.mode = "mc"
        else:
            # Then written response for 2 questions
            self.mode = "wr"
        if self.mode == "mc":
            # Get rid of the entrybox and add the radiobuttons
            self.entry.grid_remove()
            self.op1.grid(row=4, column=0)
            self.op2.grid(row=4, column=2)
            self.op3.grid(row=5, column=0)
            self.op4.grid(row=5, column=2)

            # if it is random, adjust the set_index accordingly to the random index
            if self.is_random:
                self.set_index = self.random_order[self.random_index]

            # if it is not swapped
            if not self.swap:
                # post the question and choose a random radiobutton to be correct
                self.current_learn_text.set(quizi.currentSet.contents[self.set_index].get_q())
                self.info_canvas_text.configure(text=self.current_learn_text.get())
                self.correct_rb = random.randint(1, 4)

                # post the correct (and incorrect) answers to the respective radiobuttons
                if self.correct_rb == 1:
                    self.op1.configure(text=quizi.currentSet.contents[self.set_index].get_a())

                    self.op2.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op3.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op4.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_a())
                elif self.correct_rb == 2:
                    self.op2.configure(text=quizi.currentSet.contents[self.set_index].get_a())

                    self.op1.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op3.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op4.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_a())
                elif self.correct_rb == 3:
                    self.op3.configure(text=quizi.currentSet.contents[self.set_index].get_a())

                    self.op2.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op1.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op4.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_a())
                elif self.correct_rb == 4:
                    self.op4.configure(text=quizi.currentSet.contents[self.set_index].get_a())

                    self.op2.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op3.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_a())
                    self.op1.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_a())
                    
            else:
                # if it is swapped, the same steps are taken, but the questions are put on the radiobuttons
                self.current_learn_text.set(quizi.currentSet.contents[self.set_index].get_a())
                self.info_canvas_text.configure(text=self.current_learn_text.get())
                self.correct_rb = random.randint(1, 4)
                
                if self.correct_rb == 1:
                    self.op1.configure(text=quizi.currentSet.contents[self.set_index].get_q())

                    self.op2.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op3.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op4.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_q())
                elif self.correct_rb == 2:
                    self.op2.configure(text=quizi.currentSet.contents[self.set_index].get_q())

                    self.op1.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op3.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op4.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_q())
                elif self.correct_rb == 3:
                    self.op3.configure(text=quizi.currentSet.contents[self.set_index].get_q())

                    self.op2.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op1.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op4.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_q())
                elif self.correct_rb == 4:
                    self.op4.configure(text=quizi.currentSet.contents[self.set_index].get_q())

                    self.op2.configure(text=quizi.currentSet.contents[(self.set_index + 1) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op3.configure(text=quizi.currentSet.contents[(self.set_index + 3) % (len(quizi.currentSet.contents) - 1)].get_q())
                    self.op1.configure(text=quizi.currentSet.contents[(self.set_index + 5) % (len(quizi.currentSet.contents) - 1)].get_q())
            
            
        elif self.mode == "wr":
            # if it is written response, the radiobuttons are removed and the entrybox is added
            self.op1.grid_remove()
            self.op2.grid_remove()
            self.op3.grid_remove()
            self.op4.grid_remove()
            self.entry.grid(row=6, column=0, columnspan=2)
            # if it is swapped, ask an answer, otherwise, ask a question
            if self.swap:
                if self.is_random:
                    self.set_index = self.random_order[self.random_index]
                self.current_learn_text.set(quizi.currentSet.contents[self.set_index].get_a())
                self.info_canvas_text.configure(text=self.current_learn_text.get())
            else:
                if self.is_random:
                    self.set_index = self.random_order[self.random_index]
                self.current_learn_text.set(quizi.currentSet.contents[self.set_index].get_q())
                self.info_canvas_text.configure(text=self.current_learn_text.get())
        

    def answer(self):
        # if functionality is enabled
        if self.enabled:
            # if multiple choice
            if self.mode == "mc":
                # if you chose the incorrect radiobutton
                if self.rb_var.get() != self.correct_rb:
                    # Displays the correct answer
                    if not self.swap:
                        self.wrong_answer_text.set(f"Incorrect. The correct answer was {quizi.currentSet.contents[self.set_index].get_a()}.")
                    else:
                        self.wrong_answer_text.set(f"Incorrect. The correct answer was {quizi.currentSet.contents[self.set_index].get_a()}.")
                    self.incorrect_label.configure(text=self.wrong_answer_text.get())
                    self.incorrect_label.grid(row=3, column=0, columnspan=3)
                else:
                    # Removes the incorrect label
                    self.incorrect_label.grid_remove()
            # if written response
            elif self.mode == "wr":
                if not self.swap:
                    # Displays the correct answer if wrong, otherwise, removes the incorrect label
                    if self.entry_var.get() != quizi.currentSet.contents[self.set_index].get_a():
                        self.wrong_answer_text.set(f"Incorrect. The correct answer was {quizi.currentSet.contents[self.set_index].get_a()}.")
                    else:
                        self.incorrect_label.grid_remove()
                else:
                    if self.entry_var.get() != quizi.currentSet.contents[self.set_index].get_q():
                        self.wrong_answer_text.set(f"Incorrect. The correct answer was {quizi.currentSet.contents[self.set_index].get_q()}.")
                    else:
                        self.incorrect_label.grid_remove()
                self.incorrect_label.configure(text=self.wrong_answer_text.get())
                self.incorrect_label.grid(row=3, column=0, columnspan=3)

            # Deselects all radio buttons and clears the entry
            self.op1.deselect()
            self.op2.deselect()
            self.op3.deselect()
            self.op4.deselect()
            self.entry.delete(0, "end")

            # increments the count
            self.count += 1

            # Adjusts the set index to another random number if random or increments it if fixed
            # Then updates the screen for the next question
            if not self.is_random:
                if self.set_index == len(quizi.currentSet.contents) - 1:
                    self.set_index = 0
                else:
                    self.set_index += 1
            else:
                if self.random_index == len(quizi.currentSet.contents) - 1:
                    random.shuffle(self.random_order)
                    self.random_index = 0
                else:
                    self.random_index += 1
            self.update_screen()

    def ref(self):
        # If no set is loaded, functionality is locked down
        if quizi.currentSet.get_name() == "N/A":
            self.enabled = False
            self.current_learn_text.set("Please load a study set\nto begin studying!")
        else:
            # Otherwise, buttons work
            self.enabled = True
            # The first question is loaded
            self.current_learn_text.set(quizi.currentSet.contents[0].get_q())
            self.info_canvas_text.configure(text=self.current_learn_text.get())
            # The set name is put at the top
            self.label.configure(text=f"Learn Set: {quizi.currentSet.get_name()}")
            self.incorrect_label.grid_remove()
            # Initial settings are reset
            self.mode = "mc"
            self.set_index = 0
            self.count = 0
            self.swap = False
            self.is_random = False
            self.random_order = list(range(0, len(quizi.currentSet.contents)))
            random.shuffle(self.random_order)
            self.random_index = 0
            # Screen is updated to show potential answers
            self.update_screen()
            
class SetScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.set_name_entry_var = tk.StringVar()

        self.current_row = 2

        self.question_vars = [0, 0]
        self.answer_vars = [0, 0]

        self.questions = [0, 0]
        self.answers = [0, 0]
                
        self.label = tk.Label(self, text=f"Set: ", justify=CENTER)
        self.label.grid(row=0, column=1)

        self.q_label = tk.Label(self, text="Question")
        self.q_label.grid(row=1, column=0)

        self.a_label = tk.Label(self, text="Answer")
        self.a_label.grid(row=1, column=2)

        self.open_set = ttk.Button(
            self,
            text="Open Set",
            command=self.browse_sets,
            cursor="hand"
        )
        self.open_set.grid(row=4, column=0)

        self.set_name_entry = tk.Entry(
            self,
            textvariable=self.set_name_entry_var
        )
        self.set_name_entry.grid(row=4, column=1)

        self.save_button = ttk.Button(
            self,
            text="Save Set",
            command=self.save_set,
            cursor="hand"
        )
        self.save_button.grid(row=4, column=2)

        self.home_button = ttk.Button(
            self,
            text="Home",
            command=lambda: controller.show_frame("HomeScreen"),
            cursor="hand"
        )
        self.home_button.grid(row=4, column=3)

        self.add_pair_button = tk.Button(
            self,
            text="Add New Q/A",
            command=self.add_pair,
            cursor="hand"
        )
        self.add_pair_button.grid(row=self.current_row, column=3)

        self.message = tk.Label(
            self,
            text="",
            fg="#37b027"
        )
        
    def add_pair(self):
        # Add a new variable slot for the question/answer
        self.question_vars.append(tk.StringVar())
        self.answer_vars.append(tk.StringVar())

        # Add the question entry box
        self.questions.append(0)
        self.questions[self.current_row] = tk.Entry(self, textvariable=self.question_vars[self.current_row], width=10)
        self.questions[self.current_row].grid(row=self.current_row, column=0)

        # Add the answer entry box
        self.answers.append(0)
        self.answers[self.current_row] = tk.Entry(self, textvariable=self.answer_vars[self.current_row], width=10)
        self.answers[self.current_row].grid(row=self.current_row, column=2)

        # Move the current row down and all the action buttons respectively
        self.current_row += 1
        self.add_pair_button.grid(row=self.current_row, column=3)
        self.open_set.grid(row=self.current_row + 2, column=0)
        self.set_name_entry.grid(row=self.current_row + 2, column=1)
        self.save_button.grid(row=self.current_row + 2, column=2)
        self.home_button.grid(row=self.current_row + 2, column=3)

    def save_set(self):
        # Save the set in the format:
        # Name
        # {[question]\:/[answer]}
        # ...
        # to the path given by the set name entry
        lines = []
        lines.append(self.set_name_entry_var.get())
        self.question_vars = self.question_vars[2:]
        self.answer_vars = self.answer_vars[2:]
        for i in range(len(self.question_vars)):
            lines.append("{["+self.question_vars[i].get()+"]\:/["+self.answer_vars[i].get()+"]}")
        try:
            with open(f"sets/{self.set_name_entry_var.get()}.set", "w") as f:
                for i in range(len(lines)):
                    f.write(lines[i]+"\n")
            # Write the success message
            self.message.configure(text=f"Set {self.set_name_entry_var.get()}.set successfully created!")
            self.message.grid(row=self.current_row + 3, column=1)
        except Exception as e:
            print(e)

    def reset_screen(self):
        # remove every entrybox
        self.questions = self.questions[2:]
        self.answers = self.answers[2:]
        for x in range(len(self.questions)):
            self.questions[x].destroy()
            self.answers[x].destroy()

        # Clear every entrybox holder and variable holder
        self.questions = [0, 0]
        self.answers = [0, 0]
        self.question_vars = [0, 0]
        self.answer_vars = [0, 0]

        # Reset the current row
        self.current_row = 2

        # Move all buttons back to the beginning
        self.open_set.grid(row=4, column=0)
        self.set_name_entry.grid(row=4, column=1)
        self.save_button.grid(row=4, column=2)
        self.add_pair_button.grid(row=self.current_row, column=3)
        self.home_button.grid(row=4, column=2)

        # Clear the name entry
        self.set_name_entry_var.set("")
        self.message.grid_remove()

    def browse_sets(self):
        # Open a file dialog to find a file path
        filename = filedialog.askopenfilename(
            initialdir = "~/quizi/sets",
            title = "Choose a Set",
            filetypes = (("Set File", "*.set"), ("All Files", "*.*"))
        )
        path = filename
        self.setup_edit(path)

    def setup_edit(self, path):
        # Clear the screen and reset everything
        self.reset_screen()
        # Open it like reading a set
        with open(path, "r") as f:
            for line in f:
                if line[0] != "{":
                    set_name = line.strip()
                    continue
                line = line.strip()
                line = line[1:-1]
                line = line.split("\:/")
                for item in range(len(line)):
                    # insert the questions into their variables and the answers into theirs
                    line[item] = line[item][1:-1]
                    q = tk.StringVar()
                    q.set(line[0])
                    a = tk.StringVar()
                    a.set(line[1])
                self.question_vars.append(q)
                self.answer_vars.append(a)

        # Put the set name in the set name entry
        self.set_name_entry_var.set(set_name)
        self.set_name_entry.configure(textvariable=self.set_name_entry_var)

        # Add all question entryboxes with their respective questions (and same for answers)
        for x in range(len(self.question_vars)):
            if self.question_vars[x] != 0:
                self.questions.append(0)
                self.questions[self.current_row] = tk.Entry(self, textvariable=self.question_vars[self.current_row], width=10)
                self.questions[self.current_row].grid(row=self.current_row, column=0)

                self.answers.append(0)
                self.answers[self.current_row] = tk.Entry(self, textvariable=self.answer_vars[self.current_row], width=10)
                self.answers[self.current_row].grid(row=self.current_row, column=2)

                # Move the buttons down and the current row to its correct spot
                self.current_row += 1
                self.add_pair_button.grid(row=self.current_row, column=3)
                self.open_set.grid(row=self.current_row + 2, column=0)
                self.set_name_entry.grid(row=self.current_row + 2, column=1)
                self.save_button.grid(row=self.current_row + 2, column=2)
                self.home_button.grid(row=self.current_row + 2, column=3)

    def refresh(self):
        # Clear the screen
        self.reset_screen()



if __name__ == "__main__":
    testObj = windows()
    testObj.geometry("640x480")
    testObj.mainloop()
