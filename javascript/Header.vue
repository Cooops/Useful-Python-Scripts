<template>
    <section id="header">
        <h2>COOPER RIBB</h2>
        <h5>Full Stack Developer located in <span id="ATX">Austin, TX</span> 🤘.</h5>
        <!-- <a href="#about" class="btn"> -->
        <button type="button" class="btn btn-default btn-circle btn-lg">
            <a href="#about">
                <i class="fa fa-angle-double-down" aria-hidden="true"></i>
            </a>
            <!-- <i class="fa fa-long-arrow-down" aria-hidden="true"></i> -->
        </button>
    </section>
</template>

<script>
</script>

<style lang="scss" scoped>
    #header {
        padding-bottom: 480px;
    }
    h2 {
        margin-top: 15%;
        font-size: 3.5em;
        font-weight: bold;
        color: white;

    }
    h5 {
        font-size: 1em;
        color: white;
    }
    #ATX {
        color: #bf5700;
        // border-bottom: 2px solid white;
    }
    .btn {
        margin-top: 50px;
        border: 2px solid white;
        transition: all .3s ease-in-out;
        width: 50px;
        height: 50px;
        text-align: center;
        padding: 10px 0;
        line-height: 1.428571429;
        border-radius: 100%;
        background: transparent;

        -webkit-animation: bouncingButton 1s infinite  alternate;
        animation: bouncingButton 1s infinite  alternate;
    }
    i.fa.fa-angle-double-down {
        color: white;
        font-size: 1.5em;
    }

    .btn:hover {
        // background: lighten(#333, 5%);
        // background: rgb(191,0,103);
        background: #bf5700;
    }
    @-webkit-keyframes bouncingButton {
        0% { transform: translateY(0); }
        100% { transform: translateY(-10px); }
    }
    @keyframes bouncingButton {
        0% { transform: translateY(0); }
        100% { transform: translateY(-10px); }
    }
</style>
