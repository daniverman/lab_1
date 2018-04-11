from Tkinter import *
import backend as backend

window = Tk()
window.resizable(width=True, height=True)


# window.minsize(width=600,height=800)

def build_main_window():
    # search box and its lbl
    title_lbl = Label(window, text="Title")
    title_lbl.grid(row=0, column=0)
    title_entry = Entry(window)
    title_entry.grid(row=0, column=1)
    year_lbl = Label(window, text="Year")
    year_lbl.grid(row=0, column=2)
    year_entry = Entry(window)
    year_entry.grid(row=0, column=3)
    id_lbl = Label(window, text="ID")
    id_lbl.grid(row=1, column=0)
    id_entry = Entry(window)
    id_entry.grid(row=1, column=1)
    # display box
    global movie_listbox
    movie_listbox_scroll = Scrollbar(window)
    movie_listbox_scroll.grid(row=4, column=2, rowspan=5)
    movie_listbox = Listbox(window,yscrollcommand=movie_listbox_scroll)
    movie_listbox.grid(row=4, column=0, columnspan=2, rowspan=5)
    movie_listbox_scroll.config(command=movie_listbox.yview)
    # all the  buttons
    view_all_btt = Button(window, width=15, text="View All", command=view_all_cmd)
    view_all_btt.grid(row=3, column=3)
    search_entry_btt = Button(window, width=15, text="Search Entry")
    search_entry_btt.grid(row=4, column=3)
    add_entry_btt = Button(window, width=15, text="Add Entry")
    add_entry_btt.grid(row=5, column=3)
    update_selected_btt = Button(window, width=15, text="Update Selected")
    update_selected_btt.grid(row=6, column=3)
    delete_selected_btt = Button(window, width=15, text="Delete Selected")
    delete_selected_btt.grid(row=7, column=3)
    close_btt = Button(window, width=15, text="Close")
    close_btt.grid(row=8, column=3)


# view all command after press on the view all button
def view_all_cmd():
    movies = backend.get_all_movies()
    movie_listbox.config(width=0)
    i = 1
    for movie in movies:
        movie_listbox.insert(i, movie[1])
        i += 1
    window.winfo_toplevel().wm_geometry("")
build_main_window()


def build_db1():
    backend.build_db()


build_db1()

window = mainloop()
