$(document).ready(() => {
    const removePlaceholders = () => {
        $('#sidebarPlaceholder').empty();
        $('#proyectosList').empty();
        $('#contentPanel .placeholder-glow').remove();
    };

    const fetchProjects = () => {
        fetch(`/API/users/${getUserID()}/proyectos/`, {
            method: 'GET'
        }).then(response => {
            if (!response.ok) {
                throw new Error(response.statusText);
            } else {
                return response.json();
            }
        }).then(data => {
            $('#proyectosList').html(proyectosLink(data));
            $('.panel-link').click(event => {
                const id = event.currentTarget.id.split('proyectoLink')[1];
                window.location.href = `/proyectos/${id}/edit/`;
            });

            removePlaceholders();
        }).catch(error => {
            console.error(error);
            $('#response').html(errorMessage(error.message));
        });
    };

    const proyectosLink = (proyectosData) => {
        let proyectos = '';
        if (proyectosData && proyectosData.length > 0) {
            proyectosData.forEach(data => {
                proyectos += `
                <a id="proyectoLink${data.id}" class="list-group-item list-group-item-action panel-link">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">${data.title}</h5>
                        <small>${data.subtitle || 'No subtitle'}</small>
                    </div>
                    <p class="mb-1">${data.description}</p>
                </a>
                `;
            });
            return `
            <div id="proyectosList" class="list-group">
                ${proyectos}
            </div>
            `;
        } else {
            return '<p>No projects found.</p>';
        }
    };

    const errorMessage = (message) => {
        return `
            <div class="alert alert-danger" role="alert">
                ${message}
            </div>
        `;
    };

    const getUserID = () => {
        // Implement this function based on your needs.
        return 1; // Example user ID
    };

    fetchProjects();
});