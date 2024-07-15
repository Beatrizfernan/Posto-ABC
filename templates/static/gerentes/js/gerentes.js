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
              <input type="text" placeholder="Abastecimento" class="form-control" name="abastecimento" ">
          </div>
          <div class="col-md">
              <select class="form-control" name="tanque">
                  <option value="gasolina" {% if abastecimento.tanque == "gasolina" %}selected{% endif %}>Gasolina</option>
                  <option value="oleo" {% if abastecimento.tanque == "oleo" %}selected{% endif %}>Óleo</option>
              </select>
          </div>
          <div class="col-md">
              <select class="form-control" name="bomba">
                  <option value="bomba1gasolina" {% if abastecimento.bomba == "bomba1gasolina" %}selected{% endif %}>Bomba01 - Gasolina</option>
                  <option value="bomba2gasolina" {% if abastecimento.bomba == "bomba2gasolina" %}selected{% endif %}>Bomba02 - Gasolina</option>
                  <option value="bomba1oleo" {% if abastecimento.bomba == "bomba1oleo" %}selected{% endif %}>Bomba01 - Óleo</option>
                  <option value="bomba2oleo" {% if abastecimento.bomba == "bomba2oleo" %}selected{% endif %}>Bomba02 - Óleo</option>
              </select>
          </div>
           <div class="col-md">
              <input type="number" step="0.01" placeholder="valor" class="form-control" name="valor_unitario" ">
          </div>
          <div class="col-md">
              <input type="number" step="0.01" placeholder="Quantidade" class="form-control" name="quantidade" ">
          </div>
      </div>
  `;

  container.innerHTML += html;
}


function dados_gerente() {
  const gerente = document.getElementById("gerente-select");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const idGerente = gerente.value;

  const data = new FormData();
  data.append('id_gerente', idGerente);

  fetch('/gerentes/atualiza_gerente/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken
    },
    body: data
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById("form-att-gerente").style.display = 'block';

      document.getElementById('id').value = data['gerente_id'];
      document.getElementById('nome').value = data['gerente']['nome'];
      document.getElementById('cpf').value = data['gerente']['cpf'];
      document.getElementById('email').value = data['gerente']['email'];

      const div_abastecimentos = document.getElementById('abastecimentos');
      div_abastecimentos.innerHTML = ''; // Limpa o conteúdo existente

      data['abastecimentos'].forEach(abastecimento => {
        div_abastecimentos.innerHTML += `
          <form action='/gerentes/update_abastecimento/${abastecimento['id']}' method='POST'>
            <div class='row'>
              <div class='col-md'>
                <input class='form-control' name='abastecimento' type='text' value='${abastecimento['fields']['abastecimento']}'>
              </div>
              <div class='col-md'>
                <input class='form-control' name='tanque' type='text' value='${abastecimento['fields']['tanque']}'>
              </div>
              <div class='col-md'>
                <input class='form-control' name='bomba' type='text' value='${abastecimento['fields']['bomba']}'>
              </div>
              <div class='col-md'>
                <input class='form-control' type='number' name='valor_unitario' value='${abastecimento['fields']['valor_unitario']}' step='0.01'>
              </div>
              <div class='col-md'>
                <input class='form-control' type='number' name='quantidade' value='${abastecimento['fields']['quantidade']}' step='0.01'>
              </div>
              <div class='col-md'>
                <input class='btn btn-lg btn-success' type='submit' value='Atualizar'>
              </div>
            </div>
          </form>
          <a href='/gerentes/excluir_abastecimento/${abastecimento['id']}' class='btn btn-lg btn-danger'>EXCLUIR</a>
          <br>
        `;
      });
    });
}

function update_gerente() {
  const idGerente = document.getElementById('id').value;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const nome = document.getElementById('nome').value;
  const email = document.getElementById('email').value;
  const cpf = document.getElementById('cpf').value;


  fetch('/gerentes/update_gerente/' + idGerente, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
      nome: nome,
      email: email,
      cpf: cpf
    })
  }).then(function(result){
    return result.json()
}).then(function(data){

    if(data['status'] == '200'){
        nome = data['nome']
        
        email = data['email']
        cpf = data['cpf']
        console.log('Dados alterado com sucesso')
    }else{
        console.log('Ocorreu algum erro')
    }

})
}