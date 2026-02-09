import tkinter as tk
import tkinter.font as tkfont


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.bg = "#f6f1df"
        self.root.title("todo list")
        self.root.configure(bg=self.bg)

        self.normal_font = tkfont.Font(family="Arial", size=11)
        self.done_font = tkfont.Font(family="Arial", size=11, overstrike=1)
        self.desc_font = tkfont.Font(family="Arial", size=9)
        self.desc_done_font = tkfont.Font(family="Arial", size=9, overstrike=1)

        main = tk.Frame(root, bg=self.bg, padx=20, pady=20)
        main.pack(fill="both", expand=True)

        title = tk.Label(
            main,
            text="todo list",
            bg=self.bg,
            font=tkfont.Font(family="Arial", size=14, weight="bold"),
        )
        title.pack(pady=(0, 10))

        entry_frame = tk.Frame(main, bg=self.bg)
        entry_frame.pack(fill="x", pady=(0, 6))

        self.todo_entry = tk.Entry(entry_frame, width=40)
        self.todo_entry.pack(side="left", fill="x", expand=True)
        self.todo_entry.bind("<Return>", lambda event: self.add_item())

        add_button = tk.Button(entry_frame, text="add", command=self.add_item)
        add_button.pack(side="left", padx=(6, 0))

        self.desc_text = tk.Text(main, height=3, width=45, wrap="word")
        self.desc_text.pack(fill="x", pady=(0, 10))
        self._set_description_placeholder()
        self.desc_text.bind("<FocusIn>", self._clear_description_placeholder)
        self.desc_text.bind("<FocusOut>", self._restore_description_placeholder)

        self.items_frame = tk.Frame(main, bg=self.bg)
        self.items_frame.pack(fill="both", expand=True)

    def _set_description_placeholder(self):
        self.desc_text.delete("1.0", "end")
        self.desc_text.insert("1.0", "description")
        self.desc_text.configure(fg="#999999")

    def _clear_description_placeholder(self, _event):
        if self.desc_text.get("1.0", "end-1c") == "description":
            self.desc_text.delete("1.0", "end")
            self.desc_text.configure(fg="#222222")

    def _restore_description_placeholder(self, _event):
        if not self.desc_text.get("1.0", "end-1c").strip():
            self._set_description_placeholder()

    def _read_description(self):
        text = self.desc_text.get("1.0", "end-1c").strip()
        if text == "description":
            return ""
        return text

    def add_item(self):
        title = self.todo_entry.get().strip()
        if not title:
            return
        desc = self._read_description()

        self._add_item_widget(title, desc)
        self.todo_entry.delete(0, "end")
        self._set_description_placeholder()

    def _add_item_widget(self, title, desc):
        row = tk.Frame(self.items_frame, bg=self.bg)
        row.pack(fill="x", pady=4)

        var = tk.BooleanVar(value=False)

        text_frame = tk.Frame(row, bg=self.bg)
        title_label = tk.Label(
            text_frame,
            text=title,
            bg=self.bg,
            anchor="w",
            font=self.normal_font,
            fg="#222222",
        )
        title_label.pack(anchor="w")

        desc_label = None
        if desc:
            desc_label = tk.Label(
                text_frame,
                text=desc,
                bg=self.bg,
                anchor="w",
                font=self.desc_font,
                fg="#666666",
            )
            desc_label.pack(anchor="w")

        check = tk.Checkbutton(
            row,
            variable=var,
            command=lambda v=var, t=title_label, d=desc_label: self._apply_style(v, t, d),
            bg=self.bg,
            activebackground=self.bg,
            selectcolor=self.bg,
        )
        check.pack(side="left", padx=(0, 8))

        text_frame.pack(side="left", fill="x", expand=True)

        delete_btn = tk.Button(
            row,
            text="delete",
            bg="#e25555",
            fg="white",
            activebackground="#d64b4b",
            activeforeground="white",
            borderwidth=0,
            command=row.destroy,
        )
        delete_btn.pack(side="right", padx=(8, 0))

        self._apply_style(var, title_label, desc_label)

    def _apply_style(self, var, title_label, desc_label):
        if var.get():
            title_label.configure(font=self.done_font, fg="#888888")
            if desc_label:
                desc_label.configure(font=self.desc_done_font, fg="#888888")
        else:
            title_label.configure(font=self.normal_font, fg="#222222")
            if desc_label:
                desc_label.configure(font=self.desc_font, fg="#666666")


def main():
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
