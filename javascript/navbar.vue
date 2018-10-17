
<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" id="mainNav">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="#">Home</a>
                </li>
            </ul>
        </div>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="#about">About</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Skills</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Projects</a>
                </li>

                <li class="nav-item">
                    <a class="nav-link" href="#">Contact</a>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
    $(function () {
    $(document).scroll(function () {
        var $nav = $("#mainNav");
        $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
        });
    });
</script>

<style scoped>
    #mainNav {
        /* display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-auto-rows: minmax(50px, auto); */

        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        z-index: 1030;
        margin-bottom: 0;
        text-transform: uppercase;
        background: transparent !important;
    }
    #mainNav.scrolled {
        background-color: #000 !important;
        transition: background-color 200ms linear;
        border-bottom: 2px solid #bf5700;
    }
    a.nav-link {
        font-weight: bold;
        color: white !important;
    }
    a.nav-link:hover {
        color: #bf5700 !important;
    }
</style>
