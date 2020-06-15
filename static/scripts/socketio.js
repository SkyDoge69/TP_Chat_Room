document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    
    
    const username = document.querySelector('#get-username').innerHTML;
    let room = "Lounge";
    joinRoom("Lounge");
    
    //maybe leter heterosexualen tp
    
    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        let img = document.createElement("img");
        
        if (data.username == username) {
            p.setAttribute("class", "my-msg");
            span_username.setAttribute("class", "my-username");
            img.setAttribute("class", "my-img");
        }  else if (typeof data.username !== 'undefined') {
            p.setAttribute("class", "others-msg");    
            span_username.setAttribute("class", "other-username");
            img.setAttribute("class", "others-img");
        }
        else {
            printSysMsg(data.msg);
        }
        span_username.innerText = data.username;
        span_timestamp.setAttribute("class", "timestamp");
        span_timestamp.innerText = data.time_stamp;
        if (data.type == "TEXT") {
            p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        } else if(data.type == "IMAGE") {
            img.src = data.msg;
            document.querySelector('#display-message-section').append(img);
            document.querySelector('#display-message-section').append(br);
        }
        scrollDownChatWindow();
    });
    //send
    document.querySelector('#send_message').onclick = () => {
        msgCheck(document.querySelector('#user_message').value);        
    }

    //create
    document.querySelector('#create_room').onclick = () => {
        if (document.querySelector('#room_name').value != "") {
            socket.emit('create_room', {'name': document.querySelector('#room_name').value,
            'username': username});
            document.querySelector('#room_name').value = ''; 
        } else {
            printSysMsg("Room without name not possible!");
        }
    }

    document.querySelector('#create_private_room').onclick = () => {
        if (document.querySelector('#room_name').value != "") {
            printSysMsg("Room without name not possible!");
            socket.emit('create_private_room', {'name': document.querySelector('#room_name').value,
            'username': username});
            document.querySelector('#room_name').value = '';
        } else {
            printSysMsg("Room without name not possible!");
        }
    }


    //delete
    document.querySelector('#delete_room').onclick = () => {
        socket.emit('close_room', {'name': document.querySelector('#room_name').value,
        'username': username, 'room': room});
        document.querySelector('#room_name').value = '';
    }
    
    document.querySelector('#invite').onclick = () => {
        socket.emit('invite_user', {'invited_user': document.querySelector('#invite_name').value,
        'username': username, 'room': room});
        document.querySelector('#invite_name').value = '';
    }

  
    //gif
    document.getElementById("btnSearch").addEventListener("click", ev => {
        let APIKEY = "TtyDmfIxKqgeUJAmgzDpucrWJGH909ac";
        ev.preventDefault();
        let url = `https://api.giphy.com/v1/gifs/search?api_key=${APIKEY}&limit=1&q=`;
        let str = document.getElementById("search").value.trim();
        url = url.concat(str);
        console.log(url);
        fetch(url)
          .then(response => response.json())
          .then(content => {
            socket.emit('send_gif', {'gif_url': content.data[0].images.downsized.url, 'username': username, 'room': room});
          })
    });

    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = "You are already in ${room} room.";
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }     
    });
    
    function leaveRoom(room) {
        socket.emit('leave', {'username' : username, 'room': room});
    }
    
    function joinRoom(room) {
        socket.emit('join', {'username': username, 'room': room});
        document.querySelector('#display-message-section').innerHTML = '';
    }
    
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        document.querySelector("#user_message").focus();
    }

    function msgCheck(msg) {
        if (msg != "" && msg != "::love::" && msg != "::scared::" && msg != "::pussy::" &&
            msg != "::ugabuga::" && msg != "<3" && msg != "::depressed::") {
                socket.send({'msg': msg, 
                'username': username, 'room': room});
                document.querySelector('#user_message').value = '';        
        } 
        if (msg == "::love::" || msg == "<3") {
            socket.emit('send_gif', 
            {'gif_url': "https://media1.tenor.com/images/6d0ace5c4ae614d21854e9a455a089c3/tenor.gif?itemid=12933782", 'username': username, 'room': room});
            document.querySelector('#user_message').value = '';
        } else if (msg == "::scared::") {
            socket.emit('send_gif', 
            {'gif_url': "https://media3.giphy.com/media/QZOZIBLbFDHoEHIBiT/giphy.gif", 'username': username, 'room': room});
            document.querySelector('#user_message').value = '';
        }  else if (msg == "::depressed::") {
            socket.emit('send_gif', 
            {'gif_url': "https://media1.tenor.com/images/8f9b17c96ec7065798309a74162625a6/tenor.gif?itemid=14007788", 'username': username, 'room': room});
            document.querySelector('#user_message').value = '';
        } else if (msg == "::ugabuga::") {
            socket.emit('send_gif', 
            {'gif_url': "https://media1.tenor.com/images/75686e0e110e3a1a7366e9750ee1004b/tenor.gif?itemid=13749557", 'username': username, 'room': room});
            document.querySelector('#user_message').value = '';
        }
    }          
})

