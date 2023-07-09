var dia_do_pagamento = document.getElementById('dia_do_pagamento');



dia_atual = () =>{
    let data = new Date();
    let hoje = data.getDate();
    let mes = data.getMonth()+1;
    let ano =  data.getFullYear();

    if(hoje<10){
        hoje = '0'+hoje;
    }
    if(mes<10){
        mes = '0'+mes;
    }
    dia_do_pagamento.value = ano+'-'+mes+'-'+hoje;
}
dia_atual();

adicionar_id = (id,titulo) =>{
    document.getElementById('id_conta').value = id;
    document.getElementById('exampleModalLabel').textContent = titulo;
    console.log(titulo);
}