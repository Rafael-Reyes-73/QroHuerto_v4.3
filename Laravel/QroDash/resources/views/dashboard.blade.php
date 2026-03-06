<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <link href='https://unpkg.com/boxicons@2.0.9/css/boxicons.min.css' rel='stylesheet'>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
  
  <link rel="stylesheet" href="{{ asset('static/CSS/das.css') }}">
  <link rel="stylesheet" href="{{ asset('static/CSS/sectiondash.css') }}">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <title>QroDash</title>
</head>
<body>

  <section id="sidebar">
    <a href="#" class="brand">
      <img src="{{ asset('static/Resourses/img/QH.png') }}" alt="Logo" class="logo">
      <img src="{{ asset('static/Resourses/img/QroDash.png') }}" alt="Logo" class="rect-logo">
    </a>

    <ul class="side-menu top">
      <li class="active" data-section="dashboard">
        <a href="#">
          <i class='bx bxs-dashboard'></i>
          <span class="text">QroDash</span>
        </a>
      </li>
      <li data-section="semillas">
        <a href="#">
          <i class='bx bxs-circle'></i>
          <span class="text">Semillas</span>
        </a>
      </li>
      <li data-section="usuarios">
        <a href="#">
          <i class='bx bxs-user'></i>
          <span class="text">Usuarios</span>
        </a>
      </li>
      <li data-section="contenido">
        <a href="#">
          <i class='bx bxs-book-content'></i>
          <span class="text">Contenido</span>
        </a>
      </li>
      <li data-section="moderadores">
        <a href="#">
          <i class='bx bxs-shield'></i>
          <span class="text">Moderadores</span>
        </a>
      </li>
    </ul>
  </section>
  <section id="content">
    <nav>
      <i class='bx bx-menu' id="menu-toggle"></i>
      <a href="#" class="nav-link">Categories</a>
      <form action="#">
        <div class="form-input">
          <input type="search" placeholder="Search...">
          <button type="submit" class="search-btn"><i class='bx bx-search'></i></button>
        </div>
      </form>
      <input type="checkbox" id="switch-mode" hidden>

      <div class="profile-container" id="profileMenuBtn">
        <img src="{{ asset('static/Resourses/user/user2.png') }}" class="profile-img">
        <span class="username">Rafael</span>
        <i class='bx bxs-check-circle verified-icon'></i>
      </div>

      <div class="profile-dropdown" id="profileDropdown">
        <a href="{{ url('/perfil') }}"><i class='bx bxs-user'></i> Ver perfil</a>
        <a href="{{ url('/logout') }}"><i class='bx bx-log-out'></i> Cerrar sesión</a>
      </div>
    </nav>
    <main>
      
      <section id="dashboard" class="active-section container-fluid mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h1 class="fw-bold">Home</h1>
            <nav aria-label="breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="#">Dashboard</a></li>
                <li class="breadcrumb-item active" aria-current="page">Home</li>
              </ol>
            </nav>
          </div>
        </div>

        <div class="row g-3 mb-4">
          <div class="col-12 col-md-4">
            <div class="card shadow-sm py-3 px-4 d-flex flex-row align-items-center">
              <i class='bx bxs-package fs-1 text-primary me-3'></i>
              <div>
                <h3 class="mb-0">36</h3>
                <p class="text-muted mb-0">Semillas Activas</p>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="card shadow-sm py-3 px-4 d-flex flex-row align-items-center">
              <i class='bx bxs-shield fs-1 text-success me-3'></i>
              <div>
                <h3 class="mb-0">2</h3>
                <p class="text-muted mb-0">Total Moderadores</p>
              </div>
            </div>
          </div>

          <div class="col-12 col-md-4">
            <div class="card shadow-sm py-3 px-4 d-flex flex-row align-items-center">
              <i class='bx bxs-user fs-1 text-warning me-3'></i>
              <div>
                <h3 class="mb-0">{{ $total ?? 0 }}</h3> 
                <p class="text-muted mb-0">Usuarios Totales</p>
              </div>
            </div>
          </div>
        </div>

        <div class="row g-4">
          <div class="col-12 col-md-4"><div class="card shadow-sm"><div class="card-body"><h6 class="card-title">Semillas Activas vs Inactivas</h6><div style="position:relative; height:240px;"><canvas id="chartSemillas"></canvas></div></div></div></div>
          <div class="col-12 col-md-4"><div class="card shadow-sm"><div class="card-body"><h6 class="card-title">Moderadores</h6><div style="position:relative; height:240px;"><canvas id="chartModeradores"></canvas></div></div></div></div>
          <div class="col-12 col-md-4"><div class="card shadow-sm"><div class="card-body"><h6 class="card-title">Usuarios registrados por mes</h6><div style="position:relative; height:240px;"><canvas id="chartUsuarios"></canvas></div></div></div></div>
        </div>

        <div class="card shadow-sm mt-5">
          <div class="card-body">
            <h3 class="mb-3">Top 10 Semillas más Cultivadas</h3>
            <div class="table-responsive">
              <table class="table table-bordered table-hover align-middle">
                <thead class="table-dark">
                  <tr><th>Posición</th><th>Imagen</th><th>Nombre</th><th>Veces Cultivada</th></tr>
                </thead>
                <tbody>
                  <tr class="table-warning fw-bold">
                    <td>🥇 1</td>
                    <td style="width:64px;"><img src="{{ asset('static/Resourses/FV Webp/Zanahoria.webp') }}" width="48" height="48" class="rounded-circle" style="object-fit:cover;"></td>
                    <td>Zanahoria</td>
                    <td>450</td>
                  </tr>
                  </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <section id="usuarios" class="hidden-section container-fluid py-3">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <div><h1 class="fw-bold">Usuarios</h1></div>
        </div>

        <div class="row row-cols-1 row-cols-md-3 g-3 mb-3">
          <div class="col"><div class="card h-100"><div class="card-body d-flex align-items-center gap-3"><i class="bx bxs-user fs-1 text-success"></i><div><h3 class="mb-0">{{ $total ?? 0 }}</h3><p class="mb-0 text-muted">Total de Usuarios</p></div></div></div></div>
          <div class="col"><div class="card h-100"><div class="card-body d-flex align-items-center gap-3"><i class="bx bxs-user-check fs-1 text-success"></i><div><h3 class="mb-0">{{ $total_activos ?? 0 }}</h3><p class="mb-0 text-muted">Usuarios Activos</p></div></div></div></div>
          <div class="col"><div class="card h-100"><div class="card-body d-flex align-items-center gap-3"><i class="bx bxs-user-x fs-1 text-danger"></i><div><h3 class="mb-0">{{ $total_inactivos ?? 0 }}</h3><p class="mb-0 text-muted">Usuarios Inactivos</p></div></div></div></div>
        </div>

        <div class="row g-4">
          <div class="col-12 col-lg-5">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Registrar Usuario</h5>
                <div id="alertas"></div>

                <form id="form-registro" class="row g-2" method="POST" action="{{ url('/usuarios/registrar') }}" enctype="multipart/form-data">
                  @csrf
                  <div class="col-12 col-md-6"><label class="form-label">Nombre</label><input type="text" name="nombre" class="form-control"></div>
                  <div class="col-12"><button type="submit" class="btn btn-success">Registrar</button></div>
                </form>
              </div>
            </div>

            <div class="card mt-3">
              <div class="card-body">
                <h5 class="card-title">Lista de Usuarios</h5>
                <div class="table-responsive">
                  <table class="table table-striped table-hover align-middle">
                    <thead class="table-light">
                      <tr><th>ID</th><th>Foto</th><th>Nombre</th><th>Municipio</th><th>Apodo</th><th>Acciones</th></tr>
                    </thead>
                    <tbody>
                      @if(isset($usuarios))
                          @foreach ($usuarios as $user)
                          <tr>
                            <td>{{ $user->id }}</td>
                            <td style="width:56px;">
                              @if ($user->foto_perfil)
                                <img src="{{ asset('static/uploads/' . $user->foto_perfil) }}" width="40" height="40" class="rounded-circle" style="object-fit:cover;">
                              @else
                                <img src="{{ asset('static/img/default-user.png') }}" width="40" height="40" class="rounded-circle" style="object-fit:cover;">
                              @endif
                            </td>
                            <td>{{ $user->nombre }} {{ $user->apellido_paterno }} {{ $user->apellido_materno }}</td>
                            <td>{{ $user->municipio }}</td>
                            <td>{{ $user->apodo }}</td>
                            <td>
                              <a href="{{ url('/usuarios/editar/' . $user->id) }}" class="btn btn-sm btn-outline-primary">Editar</a>
                              <form action="{{ url('/usuarios/eliminar/' . $user->id) }}" method="POST" style="display:inline;" onsubmit="return confirm('¿Seguro que quieres eliminar este usuario?');">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="btn btn-sm btn-danger">Eliminar</button>
                              </form>
                            </td>
                          </tr>
                          @endforeach
                      @endif
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-12 col-lg-7">...</div>
        </div>
      </section>

      <section id="contenido" class="hidden-section container-fluid mt-4">
        <form method="POST" action="{{ url('/contenido') }}" enctype="multipart/form-data">
            @csrf
            </form>

        <table class="table table-bordered table-hover align-middle">
          <tbody>
            @if(isset($contenidos))
                @foreach ($contenidos as $contenido)
                <tr>
                  <td>{{ $contenido->id }}</td>
                  <td>{{ $contenido->slider }}</td>
                  <td>{{ $contenido->titulo_inicial }} {{ $contenido->conector }} {{ $contenido->titulo_final }}</td>
                  <td>{{ $contenido->notas }}</td>
                  <td><img src="{{ asset('static/uploads/' . $contenido->imagen) }}" width="60" class="rounded"></td>
                  <td class="text-center">
                    <a href="{{ url('/contenido/editar/' . $contenido->id) }}" class="btn btn-sm btn-warning mb-1">Editar</a>
                    <form action="{{ url('/contenido/eliminar/' . $contenido->id) }}" method="POST" onsubmit="return confirm('¿Seguro que quieres eliminar este contenido?');">
                      @csrf
                      @method('DELETE')
                      <button type="submit" class="btn btn-sm btn-danger">Eliminar</button>
                    </form>
                  </td>
                </tr>
                @endforeach
            @endif
          </tbody>
        </table>
      </section>

    </main>
  </section>

  <script src="{{ asset('static/JS/dash.js') }}"></script>
  <script src="{{ asset('static/JS/graficas.js') }}"></script>

  <script>
    // Usamos @json() para pasar variables de PHP a JS de forma segura
    const TOTAL_ACTIVOS = @json($total_activos ?? 0);
    const TOTAL_INACTIVOS = @json($total_inactivos ?? 0);
  </script>
</body>
</html>