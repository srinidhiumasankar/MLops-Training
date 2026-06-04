async function sendQuestion(){

    const query =
        document.getElementById("question").value;

    const response =
        await fetch(
            "http://127.0.0.1:5000/chat",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    query:query
                })
            }
        );

    const data = await response.json();

    document.getElementById("response").innerHTML =
        data.answer.replace(/\n/g,"<br>");
}