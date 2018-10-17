<template>
    <div id="app">
        <!-- <img src="./assets/austin.png"> -->
        <Navbar/>
        <Header/>
        <About/>
    </div>
</template>

<script>
    import Navbar from './components/Navbar'
    import Header from './components/Header'
    import About from './components/About'

    export default {
        name: 'App',
        components: {
            Navbar,
            Header,
            About
        }
    }
</script>

<style>
    html {
        scroll-behavior: smooth;
    }
    body {
        position: relative;
        /* background-image: url("https://images.pexels.com/photos/414491/pexels-photo-414491.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=380&w=940"); */
        background-image: url("https://images.pexels.com/photos/557782/pexels-photo-557782.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940");
        background-repeat: no-repeat;
        background-color: #000; /* fallback if image doesn't load */
    }
    img {
          -webkit-filter: grayscale(1);
    filter: grayscale(1);
    }
    #app {
        /* font-family: Cabin, 'Helvetica Neue', Helvetica, Arial, sans-serif;     */
        /* font-family: 'Avenir', Helvetica, Arial, sans-serif; */
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
    }
</style>
