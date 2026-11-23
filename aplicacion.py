import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class App(tk.Tk):
    PALETA = {
        "fondo": "#0F1115",
        "superficie": "#181B21",
        "superficie_alt": "#22262E",
        "primario": "#F59E0B",
        "primario_hover": "#FBBF24",
        "texto": "#F9FAFB",
        "texto_secundario": "#9CA3AF",
        "error": "#EF4444",
        "exito": "#22C55E",
        "borde": "#2D313A",
    }

    EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    def __init__(self):
        super().__init__()

        self.title("🐧 Gestor de clientes · Tux")
        self.geometry("840x580")
        self.minsize(780, 540)

        self.clientes = []

        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        colores = self.PALETA

        self.configure(background=colores["fondo"])

        estilo.configure(
            "TFrame",
            background=colores["fondo"]
        )

        estilo.configure(
            "Card.TFrame",
            background=colores["superficie"]
        )

        estilo.configure(
            "Titulo.TLabel",
            background=colores["fondo"],
            foreground=colores["texto"],
            font=("Segoe UI", 20, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            background=colores["fondo"],
            foreground=colores["texto_secundario"],
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Campo.TLabel",
            background=colores["superficie"],
            foreground=colores["texto"],
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "Estado.TLabel",
            background=colores["fondo"],
            foreground=colores["texto_secundario"],
            font=("Segoe UI", 10)
        )

        estilo.configure(
            "TEntry",
            fieldbackground=colores["superficie_alt"],
            foreground=colores["texto"],
            insertcolor=colores["texto"],
            bordercolor=colores["borde"],
            lightcolor=colores["borde"],
            darkcolor=colores["borde"],
            padding=8
        )

        estilo.configure(
            "Card.TLabelframe",
            background=colores["superficie"],
            borderwidth=0
        )

        estilo.configure(
            "Card.TLabelframe.Label",
            background=colores["superficie"],
            foreground=colores["primario"],
            font=("Segoe UI", 10, "bold")
        )

        estilo.configure(
            "Primario.TButton",
            background=colores["primario"],
            foreground="#111111",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focusthickness=0,
            padding=(16, 10)
        )

        estilo.map(
            "Primario.TButton",
            background=[
                ("disabled", "#6B5A21"),
                ("active", colores["primario_hover"])
            ],
            foreground=[
                ("disabled", "#3B3B3B")
            ]
        )

        estilo.configure(
            "Secundario.TButton",
            background=colores["superficie_alt"],
            foreground=colores["texto"],
            font=("Segoe UI", 10),
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10)
        )

        estilo.map(
            "Secundario.TButton",
            background=[
                ("active", "#31363F")
            ]
        )

        estilo.configure(
            "Peligro.TButton",
            background="#3B1D1D",
            foreground=colores["error"],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10)
        )

        estilo.map(
            "Peligro.TButton",
            background=[
                ("active", "#4A2424")
            ]
        )

        estilo.configure(
            "Treeview",
            background=colores["superficie"],
            foreground=colores["texto"],
            fieldbackground=colores["superficie"],
            rowheight=34,
            borderwidth=0
        )

        estilo.configure(
            "Treeview.Heading",
            background=colores["superficie_alt"],
            foreground=colores["primario"],
            font=("Segoe UI", 10, "bold"),
            padding=(10, 8)
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", colores["primario"])
            ],
            foreground=[
                ("selected", "#111111")
            ]
        )

    def crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=24)
        contenedor.pack(fill="both", expand=True)

        cabecera = ttk.Frame(contenedor)
        cabecera.pack(fill="x", pady=(0, 20))

        titulo_frame = ttk.Frame(cabecera)
        titulo_frame.pack(anchor="w")

        ttk.Label(
            titulo_frame,
            text="🐧",
            font=("Segoe UI Emoji", 28)
        ).pack(side="left", padx=(0, 12))

        texto_cabecera = ttk.Frame(titulo_frame)
        texto_cabecera.pack(side="left")

        ttk.Label(
            texto_cabecera,
            text="Gestor de clientes",
            style="Titulo.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            texto_cabecera,
            text="Sistema Tux · Añade, busca y administra registros",
            style="Subtitulo.TLabel"
        ).pack(anchor="w")

        self.crear_formulario(contenedor)
        self.crear_busqueda(contenedor)
        self.crear_tabla(contenedor)
        self.crear_estado(contenedor)

        self.campo_nombre.focus()

    def crear_formulario(self, padre):
        formulario = ttk.LabelFrame(
            padre,
            text="Nuevo cliente",
            style="Card.TLabelframe",
            padding=18
        )
        formulario.pack(fill="x", pady=(0, 20))

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        ttk.Label(
            formulario,
            text="Nombre",
            style="Campo.TLabel"
        ).grid(
            row=0, column=0,
            sticky="w",
            padx=(0, 8),
            pady=(0, 10)
        )

        self.campo_nombre = ttk.Entry(formulario)
        self.campo_nombre.grid(
            row=0, column=1,
            sticky="ew",
            padx=(0, 20),
            pady=(0, 10)
        )

        ttk.Label(
            formulario,
            text="Email",
            style="Campo.TLabel"
        ).grid(
            row=0, column=2,
            sticky="w",
            padx=(0, 8),
            pady=(0, 10)
        )

        self.campo_email = ttk.Entry(formulario)
        self.campo_email.grid(
            row=0, column=3,
            sticky="ew",
            pady=(0, 10)
        )

        ttk.Label(
            formulario,
            text="Teléfono",
            style="Campo.TLabel"
        ).grid(row=1, column=0, sticky="w", padx=(0, 8))

        self.campo_telefono = ttk.Entry(formulario)
        self.campo_telefono.grid(
            row=1, column=1,
            sticky="ew",
            padx=(0, 20)
        )

        ttk.Label(
            formulario,
            text="Ciudad",
            style="Campo.TLabel"
        ).grid(row=1, column=2, sticky="w", padx=(0, 8))

        self.campo_ciudad = ttk.Entry(formulario)
        self.campo_ciudad.grid(row=1, column=3, sticky="ew")

        acciones = ttk.Frame(formulario, style="Card.TFrame")
        acciones.grid(
            row=2, column=0,
            columnspan=4,
            sticky="ew",
            pady=(18, 0)
        )

        ttk.Button(
            acciones,
            text="Guardar cliente",
            style="Primario.TButton",
            command=self.guardar_cliente
        ).pack(side="left")

        ttk.Button(
            acciones,
            text="Limpiar",
            style="Secundario.TButton",
            command=self.limpiar_campos
        ).pack(side="left", padx=(10, 0))

    def crear_busqueda(self, padre):
        busqueda = ttk.Frame(padre)
        busqueda.pack(fill="x", pady=(0, 12))

        self.campo_busqueda = ttk.Entry(busqueda)
        self.campo_busqueda.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=2
        )

        self.campo_busqueda.bind(
            "<KeyRelease>",
            lambda evento: self.actualizar_tabla()
        )

        ttk.Button(
            busqueda,
            text="Buscar",
            style="Secundario.TButton",
            command=self.actualizar_tabla
        ).pack(side="left", padx=(10, 0))

    def crear_tabla(self, padre):
        tabla_frame = ttk.Frame(padre)
        tabla_frame.pack(fill="both", expand=True)

        columnas = ("nombre", "email", "telefono", "ciudad")

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("email", text="Email")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("ciudad", text="Ciudad")

        self.tabla.column("nombre", width=190, anchor="w")
        self.tabla.column("email", width=250, anchor="w")
        self.tabla.column("telefono", width=150, anchor="w")
        self.tabla.column("ciudad", width=160, anchor="w")

        scrollbar = ttk.Scrollbar(
            tabla_frame,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def crear_estado(self, padre):
        acciones_tabla = ttk.Frame(padre)
        acciones_tabla.pack(fill="x", pady=(12, 0))

        ttk.Button(
            acciones_tabla,
            text="Eliminar seleccionado",
            style="Peligro.TButton",
            command=self.eliminar_cliente
        ).pack(side="left")

        self.estado = ttk.Label(
            acciones_tabla,
            text="0 clientes registrados",
            style="Estado.TLabel"
        )
        self.estado.pack(side="left", padx=(16, 0))

    def guardar_cliente(self):
        nombre = self.campo_nombre.get().strip()
        email = self.campo_email.get().strip()
        telefono = self.campo_telefono.get().strip()
        ciudad = self.campo_ciudad.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Campo obligatorio",
                "El nombre es obligatorio."
            )
            self.campo_nombre.focus()
            return

        if email and not re.fullmatch(self.EMAIL_REGEX, email):
            messagebox.showwarning(
                "Email inválido",
                "Introduce un email válido, por ejemplo: nombre@dominio.com"
            )
            self.campo_email.focus()
            return

        if email and self.email_duplicado(email):
            messagebox.showwarning(
                "Cliente duplicado",
                "Ya existe un cliente con ese email."
            )
            self.campo_email.focus()
            return

        self.clientes.append({
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "ciudad": ciudad
        })

        self.limpiar_campos()
        self.actualizar_tabla()

        self.estado.config(
            text=(
                f"Cliente añadido correctamente · "
                f"{len(self.clientes)} registros"
            ),
            foreground=self.PALETA["exito"]
        )

    def email_duplicado(self, email):
        return any(
            cliente["email"].lower() == email.lower()
            for cliente in self.clientes
        )

    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_email.delete(0, tk.END)
        self.campo_telefono.delete(0, tk.END)
        self.campo_ciudad.delete(0, tk.END)

        self.campo_nombre.focus()

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())

        filtro = self.campo_busqueda.get().strip().lower()

        for cliente in self.clientes:
            texto = " ".join(cliente.values()).lower()

            if filtro and filtro not in texto:
                continue

            self.tabla.insert(
                "",
                "end",
                values=(
                    cliente["nombre"],
                    cliente["email"],
                    cliente["telefono"],
                    cliente["ciudad"]
                )
            )

        total = len(self.tabla.get_children())

        self.estado.config(
            text=f"{total} clientes registrados",
            foreground=self.PALETA["texto_secundario"]
        )

    def eliminar_cliente(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            messagebox.showinfo(
                "Sin selección",
                "Selecciona un cliente para eliminarlo."
            )
            return

        valores = self.tabla.item(seleccion[0], "values")
        email = valores[1]

        self.clientes = [
            cliente for cliente in self.clientes
            if cliente["email"].lower() != email.lower()
        ]

        self.actualizar_tabla()

        self.estado.config(
            text=f"Cliente eliminado · {len(self.clientes)} registros",
            foreground=self.PALETA["error"]
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()