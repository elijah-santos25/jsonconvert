import tkinter as tk
import jsonconvert as jc

class ConverterWindow (tk.Tk):
    _input_text: tk.Text
    _output_text: tk.Text
    _main_frame: tk.Frame

    def convert(self):
        json = self._input_text.get("1.0", "end")
        html = ""
        try:
            html = jc.convert_to_html(json)
        except:
            html = "An error occurred during conversion."
        self._output_text.delete("1.0", "end")
        self._output_text.insert("1.0", html)

    def mainloop(self) -> None:
        self.title("JSON to HTML Converter")
        f = tk.Frame(self)

        i = tk.Frame(f, relief=tk.GROOVE, borderwidth=2)
        in_label = tk.Label(i, text="JSON (Input):")
        in_text = tk.Text(i)

        o = tk.Frame(f, relief=tk.GROOVE, borderwidth=2)
        out_label = tk.Label(o, text="HTML (Output):")
        out_text = tk.Text(o)

        convert_btn = tk.Button(f, command=self.convert, text="Convert", default="active", padx=5, pady=5)

        self._main_frame = f
        self._input_text = in_text
        self._output_text = out_text

        f.grid(column=0, row=0)

        in_label.grid(column=0, row=0)
        in_text.grid(column=0, row=1)
        i.grid(column=0, row=0)

        out_label.grid(column=0, row=0)
        out_text.grid(column=0, row=1)
        o.grid(column=1, row=0)

        convert_btn.grid(column=0, row=1, columnspan=2)
        in_text.bind("<Control-Enter>", lambda e: convert_btn.invoke())
        in_text.bind("<Control-Return>", lambda e: convert_btn.invoke())
        return super().mainloop()

if __name__ == "__main__":
    w = ConverterWindow()
    w.mainloop()