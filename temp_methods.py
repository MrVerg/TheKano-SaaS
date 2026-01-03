    def agregar_docente(self, e):
        self.mostrar_dialogo_docente("Agregar Nuevo Docente")

    def editar_docente(self, docente):
        self.mostrar_dialogo_docente("Editar Docente", docente)

    def mostrar_dialogo_docente(self, titulo, docente=None):
        nombre_field = ft.TextField(label="Nombre Completo", value=docente['nombre'] if docente else "")
        titulo_field = ft.TextField(label="Título Académico", value=docente['titulo'] if docente else "")
        email_field = ft.TextField(label="Email", value=docente['email'] if docente else "")
        contrato_dd = ft.Dropdown(
            label="Tipo de Contrato",
            value=docente['contrato'] if docente else None,
            options=[ft.dropdown.Option("Planta"), ft.dropdown.Option("Honorarios"), ft.dropdown.Option("Reemplazo")]
        )
        horas_field = ft.TextField(label="Horas Contratadas", value=str(docente.get('horas_contratadas', '')) if docente else "", keyboard_type=ft.KeyboardType.NUMBER)
        evaluacion_field = ft.TextField(label="Evaluación (0.0 - 5.0)", value=str(docente.get('evaluacion', '')) if docente else "", keyboard_type=ft.KeyboardType.NUMBER)

        def guardar_docente_handler(e):
            try:
                nombre = nombre_field.value
                if not nombre:
                    self.mostrar_mensaje("El nombre es obligatorio.", 'error')
                    return

                docente_data = (
                    nombre,
                    titulo_field.value,
                    contrato_dd.value,
                    int(horas_field.value) if horas_field.value else 0,
                    email_field.value,
                    float(evaluacion_field.value) if evaluacion_field.value else 0.0
                )
                docente_id = docente['id'] if docente else None

                self.dao.guardar_docente(docente_data, docente_id)
                
                self.mostrar_mensaje(f"✅ Docente '{nombre}' guardado exitosamente.", 'success')
                self.cerrar_dialogo(dialogo)
                self._actualizar_vista_docentes()

            except Exception as ex:
                self.mostrar_mensaje(f"❌ Error al guardar docente: {ex}", 'error')

        dialogo = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Column([
                nombre_field,
                titulo_field,
                email_field,
                contrato_dd,
                horas_field,
                evaluacion_field
            ], scroll=ft.ScrollMode.AUTO, height=400, width=400),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dialogo)),
                ft.ElevatedButton("Guardar", on_click=guardar_docente_handler),
            ]
        )
        self.page.dialog = dialogo
        dialogo.open = True
        self.page.update()
