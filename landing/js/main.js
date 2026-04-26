document.addEventListener("DOMContentLoaded", () => {
    const botonesAcceso = ["#accederBtn", "#accederBtn2"];
    const urlDestino = "http://127.0.0.1:8550"; // Cambia si lo despliegas en producción

    botonesAcceso.forEach(selector => {
        const boton = document.querySelector(selector);
        if (boton) {
            boton.addEventListener("click", () => {
                window.open(urlDestino, "_blank");
            });
        }
    });
});