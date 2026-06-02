import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

from algorithms import *
from shapes import *
from transforms import *
from history import HistoryManager


class MiniPaint:

    def __init__(self, root):

        self.root = root

        self.root.title("Mini Paint 2D")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        self.current_tool = "Select"

        self.shapes = []

        self.selected_shape = None

        self.start_x = 0
        self.start_y = 0

        self.temp_points = []

        self.preview_id = None

        self.animating = False

        self.history = HistoryManager()

        self.stroke_color = "#000000"
        self.fill_color = ""

        self.line_width = 2

        self.line_style = "solid"

        self.create_menu()

        self.create_layout()

        self.create_toolbar()

        self.create_property_panel()

        self.create_canvas()

        self.create_statusbar()

        self.bind_events()

        self.draw_grid()

    def create_menu(self):

        menubar = tk.Menu(self.root)

        # FILE

        file_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        file_menu.add_command(
            label="New",
            command=self.new_canvas
        )

        file_menu.add_command(
            label="Clear Canvas",
            command=self.clear_canvas
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.root.destroy
        )

        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        edit_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        edit_menu.add_command(
            label="Undo",
            command=self.undo
        )

        edit_menu.add_command(
            label="Redo",
            command=self.redo
        )

        edit_menu.add_separator()

        edit_menu.add_command(
            label="Delete",
            command=self.delete_selected
        )

        menubar.add_cascade(
            label="Edit",
            menu=edit_menu
        )

        transform_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        transform_menu.add_command(
            label="Move Left",
            command=lambda: self.translate_selected(-20, 0)
        )

        transform_menu.add_command(
            label="Move Right",
            command=lambda: self.translate_selected(20, 0)
        )

        transform_menu.add_command(
            label="Move Up",
            command=lambda: self.translate_selected(0, -20)
        )

        transform_menu.add_command(
            label="Move Down",
            command=lambda: self.translate_selected(0, 20)
        )

        transform_menu.add_separator()

        transform_menu.add_command(
            label="Rotate 15°",
            command=lambda: self.rotate_selected(15)
        )

        transform_menu.add_command(
            label="Rotate 45°",
            command=lambda: self.rotate_selected(45)
        )

        transform_menu.add_command(
            label="Rotate 90°",
            command=lambda: self.rotate_selected(90)
        )

        transform_menu.add_separator()

        transform_menu.add_command(
            label="Scale Up",
            command=lambda: self.scale_selected(1.2)
        )

        transform_menu.add_command(
            label="Scale Down",
            command=lambda: self.scale_selected(0.8)
        )

        transform_menu.add_separator()

        transform_menu.add_command(
            label="Shear X",
            command=lambda: self.shear_x_selected(0.2)
        )

        transform_menu.add_command(
            label="Shear Y",
            command=lambda: self.shear_y_selected(0.2)
        )

        menubar.add_cascade(
            label="Transform",
            menu=transform_menu
        )

        # ANIMATION
        animation_menu = tk.Menu(
            menubar,
            tearoff=0
        )

        animation_menu.add_command(
            label="Start Rotation",
            command=self.start_rotation
        )

        animation_menu.add_command(
            label="Stop Rotation",
            command=self.stop_rotation
        )

        menubar.add_cascade(
            label="Animation",
            menu=animation_menu
        )

        self.root.config(menu=menubar)

    def create_layout(self):

        self.toolbar_frame = tk.Frame(
            self.root,
            bg="#252526",
            width=180
        )

        self.toolbar_frame.pack(
            side="left",
            fill="y"
        )

        self.property_frame = tk.Frame(
            self.root,
            bg="#252526",
            width=220
        )

        self.property_frame.pack(
            side="right",
            fill="y"
        )

        self.center_frame = tk.Frame(
            self.root,
            bg="#1e1e1e"
        )

        self.center_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

    def create_toolbar(self):

        tk.Label(
            self.toolbar_frame,
            text="TOOLS",
            bg="#252526",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=10
        )

        tools = [

            "Select",

            "Point",

            "Line",

            "Rectangle",

            "Circle",

            "Ellipse",

            "Triangle",

            "Polygon",

            "Rhombus",

            "Parallelogram"
        ]

        for tool in tools:

            btn = tk.Button(
                self.toolbar_frame,
                text=tool,
                bg="#3c3c3c",
                fg="white",
                relief="flat",
                command=lambda t=tool:
                self.set_tool(t)
            )

            btn.pack(
                fill="x",
                padx=10,
                pady=2
            )

    def create_property_panel(self):

        tk.Label(
            self.property_frame,
            text="PROPERTIES",
            bg="#252526",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=10
        )

        tk.Button(
            self.property_frame,
            text="Stroke Color",
            command=self.choose_stroke
        ).pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Button(
            self.property_frame,
            text="Fill Color",
            command=self.choose_fill
        ).pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Label(
            self.property_frame,
            text="Thickness",
            bg="#252526",
            fg="white"
        ).pack()

        self.width_var = tk.IntVar(
            value=2
        )

        ttk.Combobox(
            self.property_frame,
            textvariable=self.width_var,
            values=[1,2,3,5,8,10]
        ).pack(
            fill="x",
            padx=10
        )

        tk.Label(
            self.property_frame,
            text="Line Style",
            bg="#252526",
            fg="white"
        ).pack(
            pady=(10,0)
        )

        self.style_var = tk.StringVar(
            value="solid"
        )

        ttk.Combobox(
            self.property_frame,
            textvariable=self.style_var,
            values=[
                "solid",
                "dashed"
            ]
        ).pack(
            fill="x",
            padx=10
        )
        
    # Canvas
    def create_canvas(self):

        self.canvas = tk.Canvas(
            self.center_frame,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

    def create_statusbar(self):

        self.status_var = tk.StringVar()

        self.status_var.set("Ready")

        self.statusbar = tk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            bg="#252526",
            fg="white"
        )

        self.statusbar.pack(
            side="bottom",
            fill="x"
        )

    def bind_events(self):

        self.canvas.bind(
            "<Button-1>",
            self.mouse_down
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.mouse_drag
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.mouse_up
        )

        self.canvas.bind(
            "<Motion>",
            self.mouse_move
        )

        self.canvas.bind(
            "<Double-Button-1>",
            self.finish_polygon
        )

        self.root.bind(
            "<Control-z>",
            lambda e: self.undo()
        )

        self.root.bind(
            "<Control-y>",
            lambda e: self.redo()
        )

        self.root.bind(
            "<Delete>",
            lambda e: self.delete_selected()
        )

    def draw_grid(self):

        self.canvas.update()

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        for x in range(0, w, 20):

            self.canvas.create_line(
                x,
                0,
                x,
                h,
                fill="#eeeeee"
            )

        for y in range(0, h, 20):

            self.canvas.create_line(
                0,
                y,
                w,
                y,
                fill="#eeeeee"
            )

    def set_tool(self, tool):

        self.current_tool = tool

    def choose_stroke(self):

        color = colorchooser.askcolor()[1]

        if color:
            self.stroke_color = color

    def choose_fill(self):

        color = colorchooser.askcolor()[1]

        if color:
            self.fill_color = color

    def mouse_move(self, event):

        self.status_var.set(
            f"Tool: {self.current_tool} | "
            f"X:{event.x} Y:{event.y} | "
            f"Objects:{len(self.shapes)}"
        )

    def mouse_down(self, event):

        self.start_x = event.x
        self.start_y = event.y

        if self.current_tool == "Select":

            self.select_shape(
                event.x,
                event.y
            )

            return

        if self.current_tool == "Point":

            self.history.save_state(
                self.shapes
            )

            shape = create_point(
                event.x,
                event.y,
                self.stroke_color
            )

            self.shapes.append(
                shape
            )

            self.redraw()

            return

        if self.current_tool == "Polygon":

            self.temp_points.append(
                (
                    event.x,
                    event.y
                )
            )

            return

    def mouse_drag(self, event):

        if self.preview_id:

            self.canvas.delete(
                self.preview_id
            )

        dash = None

        if self.style_var.get() == "dashed":

            dash = (5, 5)

        tool = self.current_tool

        if tool == "Line":

            self.preview_id = self.canvas.create_line(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                fill=self.stroke_color,
                width=self.width_var.get(),
                dash=dash
            )

        elif tool == "Rectangle":

            self.preview_id = self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                outline=self.stroke_color,
                width=self.width_var.get(),
                dash=dash
            )

        elif tool == "Circle":

            self.preview_id = self.canvas.create_oval(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                outline=self.stroke_color,
                width=self.width_var.get(),
                dash=dash
            )

        elif tool == "Ellipse":

            self.preview_id = self.canvas.create_oval(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                outline=self.stroke_color,
                width=self.width_var.get(),
                dash=dash
            )

        elif tool == "Rhombus":

            x1 = self.start_x
            y1 = self.start_y

            x2 = event.x
            y2 = event.y

            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2

            pts = [
                cx, y1,
                x2, cy,
                cx, y2,
                x1, cy
            ]

            self.preview_id = self.canvas.create_polygon(
                pts,
                outline=self.stroke_color,
                fill="",
                width=self.width_var.get()
            )

        elif tool == "Parallelogram":

            x1 = self.start_x
            y1 = self.start_y

            x2 = event.x
            y2 = event.y

            offset = abs(x2 - x1) * 0.25

            pts = [

                x1 + offset, y1,

                x2 + offset, y1,

                x2, y2,

                x1, y2
            ]

            self.preview_id = self.canvas.create_polygon(
                pts,
                outline=self.stroke_color,
                fill="",
                width=self.width_var.get()
            )

    def mouse_up(self, event):

        if self.current_tool in [
            "Line",
            "Rectangle",
            "Circle",
            "Ellipse",
            "Triangle",
            "Rhombus",
            "Parallelogram"
        ]:

            self.history.save_state(
                self.shapes
            )

        if self.preview_id:

            self.canvas.delete(
                self.preview_id
            )

            self.preview_id = None

        x1 = self.start_x
        y1 = self.start_y

        x2 = event.x
        y2 = event.y

        tool = self.current_tool

        shape = None

        if tool == "Line":

            shape = create_line(
                (x1, y1),
                (x2, y2),
                self.stroke_color,
                self.width_var.get(),
                self.style_var.get()
            )

        elif tool == "Rectangle":

            shape = create_rectangle(
                (x1, y1),
                (x2, y2),
                self.stroke_color,
                self.fill_color,
                self.width_var.get(),
                self.style_var.get()
            )

        elif tool == "Circle":

            radius = int(
                distance(
                    x1,
                    y1,
                    x2,
                    y2
                )
            )

            shape = create_circle(
                (x1, y1),
                radius,
                self.stroke_color,
                self.fill_color,
                self.width_var.get(),
                self.style_var.get()
            )

        elif tool == "Ellipse":

            rx = abs(x2 - x1)
            ry = abs(y2 - y1)

            shape = create_ellipse(
                (x1, y1),
                rx,
                ry,
                self.stroke_color,
                self.fill_color,
                self.width_var.get(),
                self.style_var.get()
            )

        elif tool == "Triangle":

            p1 = (
                (x1 + x2) / 2,
                y1
            )

            p2 = (
                x1,
                y2
            )

            p3 = (
                x2,
                y2
            )

            shape = create_triangle(
                p1,
                p2,
                p3,
                self.stroke_color,
                self.fill_color,
                self.width_var.get(),
                self.style_var.get()
            )

        elif tool == "Rhombus":

            shape = create_rhombus(
                (x1, y1),
                (x2, y2),
                self.stroke_color,
                self.fill_color,
                self.width_var.get(),
                self.style_var.get()
            )

        elif tool == "Parallelogram":

            shape = create_parallelogram(
                (x1, y1),
                (x2, y2),
                self.stroke_color,
                self.fill_color,
                self.width_var.get(),
                self.style_var.get()
            )

        if shape:

            self.shapes.append(
                shape
            )

            self.redraw()

    def finish_polygon(self, event):

        if self.current_tool != "Polygon":
            return

        if len(self.temp_points) < 3:
            return

        self.history.save_state(
            self.shapes
        )

        poly = create_polygon(
            self.temp_points.copy(),
            self.stroke_color,
            self.fill_color,
            self.width_var.get(),
            self.style_var.get()
        )

        self.shapes.append(
            poly
        )

        self.temp_points.clear()

        self.redraw()

    def draw_pixel(
        self,
        x,
        y,
        color
    ):

        self.canvas.create_rectangle(
            x,
            y,
            x + 1,
            y + 1,
            outline=color,
            fill=color
        )

    def redraw(self):

        self.canvas.delete(
            "all"
        )

        self.draw_grid()

        for shape in self.shapes:

            self.draw_shape(shape)

        self.draw_selection()

    def draw_shape(self, shape):

        st = shape["stroke_color"]

        fill = shape.get(
            "fill_color",
            ""
        )

        width = shape.get(
            "line_width",
            2
        )

        dash = None

        if shape.get(
            "line_style"
        ) == "dashed":

            dash = (5, 5)

        t = shape["type"]

        if t == "point":

            x, y = shape["points"][0]

            self.canvas.create_oval(
                x - 2,
                y - 2,
                x + 2,
                y + 2,
                fill=st,
                outline=st
            )

        elif t == "line":

            p1, p2 = shape["points"]

            pts = bresenham_line(
                int(p1[0]),
                int(p1[1]),
                int(p2[0]),
                int(p2[1])
            )

            for px, py in pts:

                self.draw_pixel(
                    px,
                    py,
                    st
                )

        elif t == "rectangle":

            pts = []

            for p in shape["points"]:

                pts.extend(p)

            self.canvas.create_polygon(
                pts,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

        elif t == "circle":

            cx, cy = shape["center"]
            r = shape["radius"]

            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

        elif t == "ellipse":

            cx, cy = shape["center"]

            rx = shape["rx"]
            ry = shape["ry"]

            self.canvas.create_oval(
                cx - rx,
                cy - ry,
                cx + rx,
                cy + ry,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

        elif t == "triangle":

            pts = []

            for p in shape["points"]:
                pts.extend(p)

            self.canvas.create_polygon(
                pts,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

        elif t == "polygon":

            pts = []

            for p in shape["points"]:
                pts.extend(p)

            self.canvas.create_polygon(
                pts,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

        elif t == "rhombus":

            pts = []

            for p in shape["points"]:
                pts.extend(p)

            self.canvas.create_polygon(
                pts,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

        elif t == "parallelogram":

            pts = []

            for p in shape["points"]:
                pts.extend(p)

            self.canvas.create_polygon(
                pts,
                outline=st,
                fill=fill,
                width=width,
                dash=dash
            )

    def select_shape(self, x, y):

        self.selected_shape = None

        for shape in reversed(self.shapes):

            if contains_point(
                shape,
                x,
                y
            ):

                self.selected_shape = shape
                break

        self.redraw()

    def draw_selection(self):

        if not self.selected_shape:
            return

        x1, y1, x2, y2 = get_bounding_box(
            self.selected_shape
        )

        self.canvas.create_rectangle(
            x1 - 5,
            y1 - 5,
            x2 + 5,
            y2 + 5,
            outline="red",
            dash=(4, 4),
            width=2
        )

    def delete_selected(self):

        if not self.selected_shape:
            return

        self.history.save_state(
            self.shapes
        )

        self.shapes.remove(
            self.selected_shape
        )

        self.selected_shape = None

        self.redraw()

    def undo(self):

        self.shapes = self.history.undo(
            self.shapes
        )

        self.selected_shape = None

        self.redraw()

    def redo(self):

        self.shapes = self.history.redo(
            self.shapes
        )

        self.selected_shape = None

        self.redraw()

    def clear_canvas(self):

        self.history.save_state(
            self.shapes
        )

        self.shapes.clear()

        self.selected_shape = None

        self.redraw()

    def new_canvas(self):

        answer = messagebox.askyesno(
            "Mini Paint",
            "Clear current canvas?"
        )

        if answer:

            self.clear_canvas()
            
    def translate_selected(self, dx, dy):

        if not self.selected_shape:
            return

        self.history.save_state(
            self.shapes
        )

        idx = self.shapes.index(
            self.selected_shape
        )

        self.shapes[idx] = translate_shape(
            self.selected_shape,
            dx,
            dy
        )

        self.selected_shape = self.shapes[idx]

        self.redraw()

    def rotate_selected(self, angle):

        if not self.selected_shape:
            return

        self.history.save_state(
            self.shapes
        )

        idx = self.shapes.index(
            self.selected_shape
        )

        self.shapes[idx] = rotate_shape(
            self.selected_shape,
            angle
        )

        self.selected_shape = self.shapes[idx]

        self.redraw()

    def scale_selected(self, factor):

        if not self.selected_shape:
            return

        self.history.save_state(
            self.shapes
        )

        idx = self.shapes.index(
            self.selected_shape
        )

        self.shapes[idx] = scale_shape(
            self.selected_shape,
            factor
        )

        self.selected_shape = self.shapes[idx]

        self.redraw()

    def shear_x_selected(self, shx):

        if not self.selected_shape:
            return

        self.history.save_state(
            self.shapes
        )

        idx = self.shapes.index(
            self.selected_shape
        )

        self.shapes[idx] = shear_shape_x(
            self.selected_shape,
            shx
        )

        self.selected_shape = self.shapes[idx]

        self.redraw()

    def shear_y_selected(self, shy):

        if not self.selected_shape:
            return

        self.history.save_state(
            self.shapes
        )

        idx = self.shapes.index(
            self.selected_shape
        )

        self.shapes[idx] = shear_shape_y(
            self.selected_shape,
            shy
        )

        self.selected_shape = self.shapes[idx]

        self.redraw()

    def start_rotation(self):

        if not self.selected_shape:
            return

        self.animating = True

        self.animate()

    def stop_rotation(self):

        self.animating = False

    def animate(self):

        if not self.animating:
            return

        if self.selected_shape:

            idx = self.shapes.index(
                self.selected_shape
            )

            self.shapes[idx] = animation_rotate(
                self.selected_shape
            )

            self.selected_shape = self.shapes[idx]

            self.redraw()

        self.root.after(
            50,
            self.animate
        )

if __name__ == "__main__":

    root = tk.Tk()

    app = MiniPaint(root)

    root.mainloop()