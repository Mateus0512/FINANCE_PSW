update_valor_planejamento_categoria = (id) =>{
    inputs = document.getElementsByTagName('input');
    console.log(inputs[id-1].value);
    valor = inputs[id-1].value;

    fetch('/planejamento/update_valor_categoria/'+id,{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({novo_valor:valor})
    }).then(function(result){
        return result.json();
    }).then(function(data){
        return alert(data);
    })
}