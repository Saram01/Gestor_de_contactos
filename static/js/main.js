document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('formulario-contacto');
    const listaContactos = document.getElementById('lista-contactos');

    const cargarContactos = () => {
        fetch('/api/contactos')
            .then(response => response.json())
            .then(contactos => {
                listaContactos.innerHTML = '';
                contactos.forEach(contacto => {
                    const li = document.createElement('li');
                    li.textContent = `${contacto.nombre} - ${contacto.telefono} - ${contacto.email} - ${contacto.categoria}`;
                    listaContactos.appendChild(li);
                });
            });
    };

    formulario.addEventListener('submit', (e) => {
        e.preventDefault();
        const datos = {
            nombre: formulario.nombre.value,
            telefono: formulario.telefono.value,
            email: formulario.email.value,
            categoria: formulario.categoria.value
        };

        fetch('/api/contactos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        })
        .then(response => response.json())
        .then(resultado => {
            if (resultado.error) {
                alert(`Error: ${resultado.error}`);
            } else {
                alert(resultado.mensaje);
                formulario.reset();
                cargarContactos();
            }
        });
    });

    cargarContactos();
});
