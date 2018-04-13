from Tkinter import *
import backend as backend
import tkMessageBox as tkMessageBox

global window
window = Tk()
window.resizable(width=True, height=True)


# window.minsize(width=600,height=800)

def search_parameter():
    try:
        title = (title_entry.get(), "title")
        id = (id_entry.get(), "id")
        genre = (genre_entry.get(), "genre")
        ans = backend.get_movie(title, id, genre)
        update_listbox(ans)
    except Exception:
        print(Exception.message)


# add movie to the data base
def add_movie():
    try:
        title = (title_entry.get(), "title")
        id = (id_entry.get(), "id")
        genre = (genre_entry.get(), "genre")
        if title[0] == "" or id[0] == "" or genre[0] == "":
            tkMessageBox._show("Error", "Please entry id title and genre", tkMessageBox.ERROR)
        else:
            if id[0].isdigit() is False:
                tkMessageBox._show("Error", "Please entry id contains from integers only", tkMessageBox.ERROR)
            else:
                backend.add_movie(title, id, genre)
                mesg = id[0] + " " + title[0] + " " + genre[0]
                tkMessageBox._show("Insert", 'The movie Was Insert  : \n ' + mesg, tkMessageBox.INFO)

    except Exception:
        tkMessageBox._show("Error", "insert movie was canceled, try again", tkMessageBox.ERROR)


# close the app
def close():
    global window
    window.quit()


# after click on movie from the listbox it will fill up the selected movie data into the Entry
def on_click(event):
    selection = movie_listbox.curselection()[0]
    global selected_movie
    selected_movie = movie_listbox.get(selection)
    selected_movie = backend.get_movie([selected_movie, "title"])[0]
    # clean Entry
    id_entry.delete(0, END)
    title_entry.delete(0, END)
    genre_entry.delete(0, END)
    id_entry.insert(0, selected_movie[0])
    title_entry.insert(0, selected_movie[1])
    genre_entry.insert(0, selected_movie[2])


# update movie from the frontend to the database
def update_movie():
    if selected_movie is not None:
        new_title = title_entry.get()
        new_id = id_entry.get()
        new_genre = genre_entry.get()
        id_was_changed = str(selected_movie[0]) != new_id
        if id_was_changed:  # wait for an answer if need to support it
            id_already_exist = backend.get_movie([new_id, "id"]) is not None
        else:
            backend.update_movie(selected_movie[0], new_id, new_title, new_genre)
            old_movie = str(selected_movie[0]) + " " + str(selected_movie[1]) + " " + str(selected_movie[2])
            new_movie = new_id + " " + new_title + " " + new_genre
            tkMessageBox._show("Update", 'The movie Was Update from : \n ' + old_movie + "\n" "to : \n " + new_movie,
                               tkMessageBox.INFO)
            view_all_cmd()

    else:
        tkMessageBox._show("Error", "No movie was selected.\n To update select a movie", tkMessageBox.ERROR)


def delete_movie():
    if selected_movie is not None:
        title = title_entry.get()
        id = id_entry.get()
        genre = genre_entry.get()
        movie_deleted = id + " " + title + " " + genre
        backend.delete_movie(id)
        view_all_cmd()
        tkMessageBox._show("Delete", 'The movie Was Deleted  : \n ' + movie_deleted, tkMessageBox.INFO)


    else:
        tkMessageBox._show("Error", "No movie was selected.\n To delete select a movie", tkMessageBox.ERROR)


def build_main_window():
    # search box and its lbl
    global title_entry, genre_entry, id_entry, selected_movie
    selected_movie = None
    title_lbl = Label(window, text="Title")
    title_lbl.grid(row=0, column=0)
    title_entry = Entry(window)
    title_entry.grid(row=0, column=1)
    year_lbl = Label(window, text="Genre")
    year_lbl.grid(row=0, column=2)
    genre_entry = Entry(window)
    genre_entry.grid(row=0, column=3)
    id_lbl = Label(window, text="ID")
    id_lbl.grid(row=1, column=0)
    id_entry = Entry(window)
    id_entry.grid(row=1, column=1)
    # display box
    global movie_listbox
    movie_listbox_scroll = Scrollbar(window)
    movie_listbox_scroll.grid(row=4, column=2, rowspan=5)
    movie_listbox = Listbox(window, yscrollcommand=movie_listbox_scroll, selectmode=SINGLE)
    movie_listbox.bind('<<ListboxSelect>>', on_click)
    movie_listbox.grid(row=4, column=0, columnspan=2, rowspan=5)
    movie_listbox_scroll.config(command=movie_listbox.yview)
    # all the  buttons
    view_all_btt = Button(window, width=15, text="View All", command=view_all_cmd)
    view_all_btt.grid(row=3, column=3)
    search_entry_btt = Button(window, width=15, text="Search Entry", command=search_parameter)
    search_entry_btt.grid(row=4, column=3)
    add_entry_btt = Button(window, width=15, text="Add Entry", command=add_movie)
    add_entry_btt.grid(row=5, column=3)
    update_selected_btt = Button(window, width=15, text="Update Selected", command=update_movie)
    update_selected_btt.grid(row=6, column=3)
    delete_selected_btt = Button(window, width=15, text="Delete Selected", command=delete_movie)
    delete_selected_btt.grid(row=7, column=3)
    close_btt = Button(window, width=15, text="Close", command=close)
    close_btt.grid(row=8, column=3)


# view all command after press on the view all button
def view_all_cmd():
    movies = backend.get_all_movies()
    update_listbox(movies)


def update_listbox(movies):
    movie_listbox.delete(0, END)
    movie_listbox.config(width=0)
    for movie in movies:
        movie_listbox.insert(END, movie[1])
    window.winfo_toplevel().wm_geometry("")


build_main_window()


# build the data base from the backend
def build_db1():
    backend.build_db()


# callback function for search after a movie , take the search parameter and send it to the backend


build_db1()

window = mainloop()
