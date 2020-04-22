document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    let room = "Lounge";
    joinRoom("Lounge");
    //maybe leter heterosexualen tp

    socket.on('message', data => {
        const p = document.createElement('p');
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        const br = document.createElement('br');
        
        if (data.username) {
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
        } else {
            printSysMsg(data.msg);
        }
        
    });

    //send
    document.querySelector('#send_message').onclick = () => {
        if (document.querySelector('#user_message').value != "") { 
            socket.send({'msg': document.querySelector('#user_message').value, 
            'username': username, 'room': room});
            document.querySelector('#user_message').value = '';
        }
    }

    //create
    document.querySelector('#create_room').onclick = () => {
        socket.emit('create_room', {'name': document.querySelector('#room_name').value,
        'username': username});
        document.querySelector('#room_name').value = '';
    }

    document.querySelector('#create_private_room').onclick = () => {
        socket.emit('create_private_room', {'name': document.querySelector('#room_name').value,
        'username': username});
        document.querySelector('#room_name').value = '';
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
    
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }

})