update_valor_planejamento_categoria = (id) =>{
    input = document.getElementById('valores'+id);
    
    valor = input.value;

    fetch('/planejamento/update_valor_categoria/'+id,{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({novo_valor:valor})
    }).then(function(result){
        return result.json();
    }).then(function(data){
        return alert(data.status)
    })
}