document.getElementById('exportar').addEventListener('click',(event)=>{
    event.preventDefault();
   
    var minhaTabela = document.getElementById('card');

    var option = {
        margin:[10,10,10,10],
        filename:'extrato.pdf',
        html2canvas:{scale:2},
        jsPDF:{unit:'mm',format:'a4',orientation:'portrait'},
    };
    html2pdf().set(option).from(minhaTabela).save();
});




