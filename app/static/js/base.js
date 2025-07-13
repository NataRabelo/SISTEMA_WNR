document.addEventListener("DOMContentLoaded", function (){
    // Lógica do modal
    var modal = document.getElementById("ConfirmarSair");
    var confirmBtn = document.getElementById("confirmarSairBtn");
    modal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget;
        if (button) {
            confirmBtn.href = "/logout";
        }
    });
    // Lógica para remover as flash messages
    let flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = "opacity 0.5s ease";
                msg.style.opacity = "0";
                setTimeout(() => msg.remove(), 500);
            });
        }, 3000);
    }
})
