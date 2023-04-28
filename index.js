import {config} from 'config.js'

api_key = config.arbiscan_api_key;
address_list = config.address_list;
now = parseInt(Date.now()/1000);
resultat = 0;

to_clip_button = document.getElementsByClassName("to_clipboard")

function add_token(address,name){
    var sound = new Audio('./notif.mp3');
    sound.play();
    var now = new Date();
    const contract = document.createElement("contract_address");
    contract.innerHTML = now.getHours() + ':' + now.getMinutes() +':' + now.getSeconds() +" "+ name + " <contract>"+address+"</contract>";

    const clipboard_b = document.createElement("input");
    clipboard_b.type = "button";
    clipboard_b.classList.add('to_clipboard');
    clipboard_b.onclick = function(){
        navigator.clipboard.writeText(address)
        console.log("'"+address+"'"+ " copied to clipboard")
    }
    contract.appendChild(clipboard_b)

    const dscreen_b = document.createElement("input");
    dscreen_b.type = "button";
    dscreen_b.classList.add('dscreen_b_c');
    dscreen_b.onclick = function(){
        window.focus();
        window.open('https://dexscreener.com/arbitrum/'+address,'_blank');
    }
    contract.appendChild(dscreen_b)
    document.getElementById("main").appendChild(contract)
}





async function get_tx(){
    tx_checked = []
    fetch("https://api.arbiscan.io/api?module=block&action=getblocknobytime&timestamp="+now+"&closest=before&apikey="+api_key)
    .then(function(res) {
        if (res.ok) {
            return(res.json());
        }
        else throw Error;
    })
    .then(function(value) {
        return(value.result)
    })
    .then(function(block_number){
        let nb_iter = 1
        const interval = 1200
        myInterval = setInterval( async function() {
            console.log(nb_iter)
            nb_iter++
            for (i=0;i<address_list.length;i++){
                setTimeout(function(i){
                    const a = address_list[i]
                    console.log("Checking "+a)
                    fetch("https://api.arbiscan.io/api?module=account&action=tokentx&address="+ a +"&startblock="+block_number+"&endblock=99999999&sort=asc&apikey=" + api_key)
                        .then(function(res){
                            if (res.ok) {
                                return(res.json());
                                }
                            else throw Error;
                        })
                        .then(function(value){
                            console.log("Checked "+a)
                            if(value.result.length >0) {
                                for (r = 0; r < value.result.length; r++){
                                    if(tx_checked.includes(value.result[r].hash+value.result[r].tokenSymbol) == false){ //si tx pas dans la liste des tx déjà check
                                        if(value.result[r].to.localeCompare(a, undefined, { sensitivity: 'base' }) == 0){ //si adresse qui reçoit les token est bien l'adresse trackée
                                            add_token(value.result[r].contractAddress,value.result[r].tokenName)
                                        }
                                        tx_checked.push(value.result[r].hash+value.result[r].tokenSymbol)
                                    }
                                }
                            }
                        })
                },interval*i,i);
            }
        },interval*(address_list.length+1));
        
    }
    )
}

const timer = ms => new Promise(res => setTimeout(res, ms))

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
get_tx();