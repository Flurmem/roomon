function getAllUsuariosKids() {
    const url = "/sidebar";

    return fetch(url)
      .then(response => {
        return response.json();
      })
      .then(usuarios => {
        return usuarios;
        console.log(usuarios)
      })
  }

  // {%if usuarios%}
  //       {%for u in usuarios%}
  //       <li class="d-flex align-items-center justify-content-center col-12 gap-3 position-relative">
  //         <button class="bg-transparent border-0">
  //           <div class="bg-info rounded-circle d-flex align-items-center justify-content-center position-relative"
  //             style="aspect-ratio: 1; width: 2rem;">
  //             <img src='../static/imagens/usuarios/avatar{{u.id|id_img}}.jpg' class="w-100 h-100 rounded-circle">
  //             <div class="p-1 position-absolute rounded-circle statusBall">
  //             </div>
  //           </div>
  //         </button>
  //         <div class="flex-column escondido me-auto">
  //           <p class="m-0 text-black fw-bolder dosis h6">
  //             @{{u.nomeUsuario}}
  //           </p>
  //           <p class="mb-0 text-black small opacity-75">
  //             Categoria
  //           </p>
  //         </div>


  //       </li>
  //       {%endfor%}
  //       {%endif%}

  async function showUsuarios() {
    const usuarios = await getAllUsuariosKids();

    const lista = document.getElementById("sidebar");

    // Assuming usuarios is an object with user data
      (usuarios.usuarios).forEach(usuario => {
      const item = document.createElement('li');
      item.classList.add('itemListaUsuarios');

      const avatar = document.createElement('img');
      avatar.src = `../static/imagens/usuarios/avatar${String(usuario.id).padStart(4, '0')}.jpg`;
      
      avatar.classList.add('avatarItemSidebar');

      const corpo = document.createElement('div');
      const usuarioNick = document.createElement('p');
      usuarioNick.appendChild(document.createTextNode('@'+usuario.nomeUsuario))
      corpo.classList.add('corpoItemSidebar', 'escondido');
      usuarioNick.classList.add('nickItemSidebar');

      corpo.appendChild(usuarioNick);
      item.appendChild(avatar);
      item.appendChild(corpo);

      // Append the item to the list
      lista.appendChild(item);
    });
  }
  document.addEventListener("DOMContentLoaded", function () {
    showUsuarios();
  })

