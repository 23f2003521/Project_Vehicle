
<script>
export default {
    methods:{
        logout(){
                localStorage.clear();
                this.$router.push('/');
            }

    }
  }
</script>

<template>
  <div class="sidebar">
    <div class="logo">
        <ul class="menu">
            <li>
                <a href="http://" class="active">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </li>
            <li>
                <a href="/profile/{{user_id}}">
                    <i class="fas fa-user"></i>
                    <span>Profile</span>
                </a>
            </li>
            <li>
                <a href="http://">
                    <i class="fas fa-chart-bar"></i>
                    <span>Statistics</span>
                </a>
            </li>
            <li>
                <a href="http://">
                    <i class="fas fa-question-circle"></i>
                    <span>FAQ</span>
                </a>
            </li>
            <li>
                <a href="http://">
                    <i class="fas fa-star"></i>
                    <span>Testimonials</span>
                </a>
            </li>
            <li class="logout" @click="logout">
  <a href="#">
    <i class="fas fa-sign-out-alt" title="Logout"></i>
    <span class="logout-text">Logout</span>
  </a>
</li>

        </ul>
    </div>
</div>



</template>



<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    border: none;
    outline: none;
    font-family: 'Montserrat', sans-serif;
}


.sidebar{
    position: sticky;
    top:0;
    left:0;
    bottom:0;
    width:110px;
    height:100vh;
    padding: 0 1.7rem;
    color:#fff;
    overflow:hidden;
    transition:all 0.5s linear;
    background: rgba(113,99,186,255);

}
.sidebar:hover{
    width:240px;
    transition: 0.5s;
}
.logo{
    height:80px;
    padding:16px;
}

.menu{
    height:88%;
    position:relative;
    list-style: none;
    padding:0;
}
.menu li {
   padding:1rem;
   margin:8px 0;
   border-radius: 8px;
   transition: all 0.5s ease-in-out;
}

.menu li:hover,
.active{
 background: #e0e0e058;
}

.menu a{
    color: #fff;
    font-size:14px;
    text-decoration:none;
    display:flex;
    align-items:center;
    gap:1.5rem;

}

.menu a span{
    overflow: hidden;
}

.menu a i {
    font-size: 1.2rem;
}
/* .logout{
    position: absolute;
    bottom:0;
    left:0;
    width:100%;
} */

.logout-text {
  display: inline-block;
  white-space: nowrap;
  opacity: 0;
  transition: all 0.1s ease-in-out;
}

/* When sidebar is hovered, show the logout text */
.sidebar:hover .logout-text {
  opacity: 1;
}


</style>