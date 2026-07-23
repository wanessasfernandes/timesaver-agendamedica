document.addEventListener("DOMContentLoaded", function () {
    const mensagemVazio = document.getElementById("mensagem-vazio");
    const tableContainer = document.getElementById("agenda-table");

    const table = new Tabulator("#agenda-table", {
        layout: "fitColumns",
        responsiveLayout: "collapse",
        placeholder: "Carregando agendamentos...",
        columns: [
            { title: "Data", field: "data", sorter: "date", width: 110, minWidth: 90 },
            { title: "Horário", field: "horario", width: 90, minWidth: 70 },
            { title: "Paciente", field: "paciente", minWidth: 150, widthGrow: 2 },
            { title: "CPF", field: "cpf", width: 130, responsive: 2 },
            { title: "Médico", field: "medico", minWidth: 150, widthGrow: 2, responsive: 1 },
            { title: "Especialidade", field: "especialidade", minWidth: 120, responsive: 3 },
            { title: "Convênio", field: "convenio", minWidth: 120, responsive: 3 },
            {
                title: "Status",
                field: "status",
                width: 120,
                formatter: function (cell) {
                    const valor = cell.getValue();
                    return `<span class="status-badge ${valor}">${valor}</span>`;
                },
            },
        ],
        responsiveLayout: "collapse",
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