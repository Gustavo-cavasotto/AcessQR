// Funcionalidade do menu responsivo
$(document).ready(function() {
    
    // Função para verificar o tamanho da tela e ajustar o menu
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            $('#hamburgerBtn').show();
            $('.sidebar').removeClass('show');
            $('.sidebar-overlay').removeClass('show');
        } else {
            $('#hamburgerBtn').hide();
            $('.sidebar').addClass('show');
            $('.sidebar-overlay').removeClass('show');
        }
    }

    // Verificar tamanho da tela ao carregar
    checkScreenSize();

    // Verificar tamanho da tela ao redimensionar
    $(window).resize(function() {
        checkScreenSize();
    });

    // Toggle do menu hambúrguer
    $('#hamburgerBtn').click(function() {
        $('.sidebar').toggleClass('show');
        $('.sidebar-overlay').toggleClass('show');
    });

    // Fechar menu ao clicar no overlay
    $('#sidebarOverlay').click(function() {
        $('.sidebar').removeClass('show');
        $('.sidebar-overlay').removeClass('show');
    });

    // Fechar menu ao clicar no botão X
    $('#closeSidebarBtn').click(function() {
        $('.sidebar').removeClass('show');
        $('.sidebar-overlay').removeClass('show');
    });

    // Fechar menu ao clicar em um link (apenas em mobile)
    $('.sidebar .nav-link').click(function() {
        if (window.innerWidth <= 768) {
            setTimeout(function() {
                $('.sidebar').removeClass('show');
                $('.sidebar-overlay').removeClass('show');
            }, 100);
        }
    });

    // Fechar menu ao pressionar ESC (apenas em mobile)
    $(document).keydown(function(e) {
        if (e.keyCode === 27 && window.innerWidth <= 768) {
            $('.sidebar').removeClass('show');
            $('.sidebar-overlay').removeClass('show');
        }
    });

    // Prevenir scroll do body quando o menu estiver aberto no mobile
    $('.sidebar').on('show.bs.collapse', function() {
        if (window.innerWidth <= 768) {
            $('body').addClass('no-scroll');
        }
    });

    $('.sidebar').on('hide.bs.collapse', function() {
        $('body').removeClass('no-scroll');
    });

    // Adicionar classe no body quando menu estiver aberto
    $('#hamburgerBtn').click(function() {
        if (window.innerWidth <= 768) {
            if ($('.sidebar').hasClass('show')) {
                $('body').addClass('no-scroll');
            } else {
                $('body').removeClass('no-scroll');
            }
        }
    });

    // Remover classe no body quando menu fechar
    $('#sidebarOverlay, #closeSidebarBtn').click(function() {
        $('body').removeClass('no-scroll');
    });

    // Swipe para fechar menu no mobile (opcional)
    let startX = 0;
    let currentX = 0;

    $('.sidebar').on('touchstart', function(e) {
        startX = e.originalEvent.touches[0].clientX;
    });

    $('.sidebar').on('touchmove', function(e) {
        currentX = e.originalEvent.touches[0].clientX;
    });

    $('.sidebar').on('touchend', function(e) {
        const diffX = startX - currentX;
        if (diffX > 50 && window.innerWidth <= 768) { // Swipe para esquerda
            $('.sidebar').removeClass('show');
            $('.sidebar-overlay').removeClass('show');
            $('body').removeClass('no-scroll');
        }
    });
}); 