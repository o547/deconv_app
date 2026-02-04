let algo_select=document.querySelector("#algorithm");
let input_number_2=document.querySelector(".input_number_2");

algo_select.addEventListener("change",(e)=>{
    if(e.target.value=="standard"){
        input_number_2.innerHTML='t=<input type="number" id="sigma" name="t" step="0.01" value="3" required>：1～16程度 (10の指数で入力)<br>'
    }else{
        input_number_2.innerHTML='ε=<input type="number" id="epsilon" name="epsilon" step="0.01" value="5" required>：1～10程度 (10の指数で入力)<br>'
    }
})