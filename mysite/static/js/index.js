$(document).ready(function () {
    // Filtro de búsqueda
    $("#searchInput").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#projectList .project-item").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
        });
    });

    // Animaciones de aparición al desplazarse
    $(window).on("scroll", function () {
        $(".project-item").each(function () {
            var elementTop = $(this).offset().top;
            var viewportBottom = $(window).scrollTop() + $(window).height();

            if (elementTop < viewportBottom - 100) {
                $(this).addClass("animate__animated animate__fadeInUp");
            }
        });
    });

    // Inicializa las animaciones para los elementos que ya están en vista
    $(window).trigger("scroll");
});