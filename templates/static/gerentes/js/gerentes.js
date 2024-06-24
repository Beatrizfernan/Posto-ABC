

function add_abastecimentos() {
  // Obter o elemento container
  var container = document.getElementById('form-abastecimentos');

  // Criar o HTML para adicionar
  var html = `
    <br>
    <div class='row'>
      <div class='col-md'>
        <input type='text' placeholder='Abastecimento' class='form-control' name='abastecimento'>
      </div>
      <div class='col-md'>
        <select class='form-control' name='tanque'>
          <option value='gasolina'>Gasolina</option>
          <option value='oleo'>Óleo</option>
        </select>
      </div>
     <div class="col-md">
        <select class='form-control' name='bomba'>
             <option value='bomba1gasolina'>Bomba01 - Gasolina</option>
            <option value='bomba2gasolina'>Bomba02 -Gasolina</option>
            <option value='bomba1oleo'>Bomba01 - Oleo</option>
            <option value='bomba2oleo'>Bomba02 - Oleo</option>
        </select>
        </div>
        <div class="col-md">
         <input type='number' step='0.01' placeholder='Valor'
         class='form-control' name='valor'
         value="{{valor}}">
        </div>
        <div class="col-md">
        <input type='number' step='0.01' placeholder='Quantidade'
        class='form-control' name='quantidade'
        value="{{quantidade}}">
         </div>
    </div>`;

  container.innerHTML += html;
}


function exibir_form(tipo){

  add_gerente = document.getElementById('adicionar_gerente')
  att_gerente = document.getElementById('att_gerente')

  if(tipo == "1"){
      att_gerente.style.display = "none"
      add_gerente.style.display = "block"

  }else if(tipo == "2"){
      add_gerente.style.display = "none";
      att_gerente.style.display = "block"
  }

}

