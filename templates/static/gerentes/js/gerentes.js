function exibir_form(tipo) {
  const addGerente = document.getElementById("adicionar_gerente");
  const attGerente = document.getElementById("att_gerente");
  if (tipo === '1') {
    addGerente.style.display = "block";
    attGerente.style.display = "none";
  } else if (tipo === '2') {
    addGerente.style.display = "none";
    attGerente.style.display = "block";
  }
}

function add_abastecimentos() {
  const container = document.getElementById('form-abastecimentos');

  const html = `
      <br>
      <div class="row">
          <div class="col-md">
              <input type="text" placeholder="Abastecimento" class="form-control" name="abastecimento[]" value="{{ abastecimento.abastecimento }}">
          </div>
          <div class="col-md">
              <select class="form-control" name="tanque[]">
                  <option value="gasolina" {% if abastecimento.tanque == "gasolina" %}selected{% endif %}>Gasolina</option>
                  <option value="oleo" {% if abastecimento.tanque == "oleo" %}selected{% endif %}>Óleo</option>
              </select>
          </div>
          <div class="col-md">
              <select class="form-control" name="bomba[]">
                  <option value="bomba1gasolina" {% if abastecimento.bomba == "bomba1gasolina" %}selected{% endif %}>Bomba01 - Gasolina</option>
                  <option value="bomba2gasolina" {% if abastecimento.bomba == "bomba2gasolina" %}selected{% endif %}>Bomba02 - Gasolina</option>
                  <option value="bomba1oleo" {% if abastecimento.bomba == "bomba1oleo" %}selected{% endif %}>Bomba01 - Óleo</option>
                  <option value="bomba2oleo" {% if abastecimento.bomba == "bomba2oleo" %}selected{% endif %}>Bomba02 - Óleo</option>
              </select>
          </div>
          <div class="col-md">
              <input type="number" step="0.01" placeholder="Valor" class="form-control" name="valor[]" value="{{ abastecimento.valor }}">
          </div>
          <div class="col-md">
              <input type="number" step="0.01" placeholder="Quantidade" class="form-control" name="quantidade[]" value="{{ abastecimento.quantidade }}">
          </div>
      </div>
  `;

  container.innerHTML += html;
}


function dados_gerente() {
  gerente = document.getElementById("gerente-select");
  csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  idGerente = gerente.value;

  data = new FormData();
  data.append('id_gerente', idGerente);

  fetch('/gerentes/atualiza_gerente/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken
    },
    body: data
  })
    .then(function (result) {
      return result.json()
    })
    .then(function (data) {
      document.getElementById("form-att-gerente").style.display = 'block';

      id = document.getElementById('id')
      id.value = data['gerente_id']

      nome = document.getElementById('nome')
      nome.value = data['gerente']['nome']

      cpf = document.getElementById('cpf')
      cpf.value = data['gerente']['cpf']

      email = document.getElementById('email')
      email.value = data['gerente']['email']

      div_abastecimentos = document.getElementById('abastecimentos')


      for (i = 0; i < data['abastecimentos'].length; i++) {
        div_carros.innerHTML += "\<form action='/gerentes/update_abastecimento/" + data['abastecimentos'][i]['id'] + "' method='POST'>\
              <div class='row'>\
                        <div class='col-md'>\
                            <input class='form-control' name='abastecimento' type='text' value='" + data['abastecimentos'][i]['fields']['abastecimento'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' name='placa' type='text' value='" + data['abastecimentos'][i]['fields']['tanque'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='ano' value='" + data['abastecimentos'][i]['fields']['valor'] + "' >\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='ano' value='" + data['abastecimentos'][i]['fields']['quantidade'] + "' >\
                        </div>\
                        <div class='col-md'>\
                            <input class='btn btn-lg btn-success' type='submit'>\
                        </div>\
                    </form>\
                    <div class='col-md'>\
                        <a href='/gerentes/excluir_abastecimento/"+ data['abastecimentos'][i]['id'] + "' class='btn btn-lg btn-danger'>EXCLUIR</a>\
                    </div>\
                </div><br>"
      }

    })


}

function update_gerente() {
  const idGerente = document.getElementById('id').value;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const cpf = document.getElementById('cpf').value;

  const data = new FormData();
  data.append('id', idGerente);
  data.append('nome', nome);
  data.append('email', email);
  data.append('cpf', cpf);

  fetch('/gerentes/att_gerente/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken
    },
    body: data
  })
    .then(response => response.json())
    .then(data => {
      console.log('Update successful:', data);
      alert('Gerente updated successfully!');
    })
    .catch(error => console.error('Error updating gerente:', error));
}