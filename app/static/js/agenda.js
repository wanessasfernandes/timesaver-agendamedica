document.addEventListener("DOMContentLoaded", function () {
    const mensagemVazio = document.getElementById("mensagem-vazio");
    const tableContainer = document.getElementById("agenda-table");

    const table = new Tabulator("#agenda-table", {
        layout: "fitColumns",
        placeholder: "Carregando agendamentos...",
        columns: [
            { title: "Data", field: "data", sorter: "date" },
            { title: "Horário", field: "horario" },
            { title: "Paciente", field: "paciente" },
            { title: "CPF", field: "cpf" },
            { title: "Médico", field: "medico" },
            { title: "Especialidade", field: "especialidade" },
            { title: "Convênio", field: "convenio" },
            { title: "Status", field: "status" },
        ],
    });

    function carregarAgendamentos(busca = "") {
        const url = busca
            ? `/api/agendamentos?busca=${encodeURIComponent(busca)}`
            : "/api/agendamentos";

        fetch(url)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Erro ao buscar agendamentos");
                }
                return response.json();
            })
            .then((dados) => {
                if (dados.erro) {
                    mensagemVazio.textContent = dados.erro;
                    mensagemVazio.style.display = "block";
                    tableContainer.style.display = "none";
                    return;
                }

                if (dados.length === 0) {
                    mensagemVazio.textContent = "Nenhum agendamento encontrado.";
                    mensagemVazio.style.display = "block";
                    tableContainer.style.display = "none";
                } else {
                    mensagemVazio.style.display = "none";
                    tableContainer.style.display = "block";
                    table.setData(dados);
                }
            })
            .catch((erro) => {
                mensagemVazio.textContent = "Não foi possível carregar os agendamentos no momento.";
                mensagemVazio.style.display = "block";
                tableContainer.style.display = "none";
                console.error(erro);
            });
    }

    let debounceTimer;
    document.getElementById("busca-input").addEventListener("input", function (e) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            carregarAgendamentos(e.target.value.trim());
        }, 300);
    });

    carregarAgendamentos();
});