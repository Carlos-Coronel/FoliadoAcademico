document.addEventListener("DOMContentLoaded", () => {
    const checkboxContainer = document.getElementById('checkboxContainer');
    const cboCarrera = document.getElementById('cboCarrera');

    const listarMaterias = async (codcarrera) => {
        try {
            const response = await fetch(`./materiasf/${codcarrera}`);
            const data = await response.json();
            checkboxContainer.innerHTML = "";

            if (data.message === "Success") {
                const semestreMap = {
                    1: "Primero",
                    2: "Segundo",
                    3: "Tercero",
                    4: "Cuarto",
                    5: "Quinto",
                    6: "Sexto",
                    7: "Séptimo",
                    8: "Octavo",
                    9: "Noveno",
                    10: "Décimo"
                };

                const materiasPorSemestre = {};

                data.materias.forEach(materia => {
                    if (materia.curso_id && materia.semestre_id) { // Verificar que tenga curso y semestre asignado
                        const cursoId = materia.curso_id;
                        const semestreCalculado1 = (cursoId * 2) - 1;
                        const semestreCalculado2 = cursoId * 2;

                        if (!materiasPorSemestre[semestreCalculado1]) {
                            materiasPorSemestre[semestreCalculado1] = [];
                        }
                        if (!materiasPorSemestre[semestreCalculado2]) {
                            materiasPorSemestre[semestreCalculado2] = [];
                        }

                        if (materia.semestre_id === 1) {
                            materiasPorSemestre[semestreCalculado1].push(materia);
                        } else if (materia.semestre_id === 2) {
                            materiasPorSemestre[semestreCalculado2].push(materia);
                        }
                    }
                });

                Object.entries(materiasPorSemestre).forEach(([semestreId, materias]) => {
                    const semestreName = semestreMap[semestreId];

                    let checkboxes = '';
                    materias.forEach(materia => {
                        checkboxes += `
                            <input type="checkbox" id="materia${materia.id}" name="pdf_id" value="${materia.id}">
                            <label for="materia${materia.id}">${materia.materia}</label><br>
                        `;
                    });

                    const divContenedor = document.createElement('div');
                    divContenedor.id = 'div-materias';

                    const fieldset = document.createElement('fieldset');
                    const legend = document.createElement('legend');
                    legend.textContent = `${semestreName} Semestre`;
                    fieldset.appendChild(legend);
                    fieldset.innerHTML += checkboxes;
                    divContenedor.appendChild(fieldset);

                    checkboxContainer.appendChild(divContenedor);
                });
            } else {
                alert("Materias no encontradas...");
            }
        } catch (error) {
            console.error(error);
        }
    };

    const cargaInicial = async () => {
        await listarMaterias('KTII');
        cboCarrera.addEventListener("change", (event) => {
            listarMaterias(event.target.value);
        });
    };

    window.addEventListener("load", async () => {
        await cargaInicial();
    });
});
