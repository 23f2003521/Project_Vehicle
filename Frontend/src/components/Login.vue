<script setup>
import { onMounted, nextTick } from 'vue'

onMounted(() => {
  nextTick(() => {
    const container = document.getElementById('container');
    const registerBtn = document.getElementById('register');
    const loginBtn = document.getElementById('login');

    if (registerBtn && loginBtn && container) {
      registerBtn.addEventListener('click', () => {
        container.classList.add("active");
      });

      loginBtn.addEventListener('click', () => {
        container.classList.remove("active");
      });
    }
  });
});

</script>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            FormData:{
            email: '',
            password: '',
            vehicle_no: '',
            username:''
        },
        token : "",
        role:'',
        error:""
    }
          },
          methods:{
            login(){
                const response =axios.post('http://127.0.0.1:5000/api/login', JSON.stringify(this.FormData), {
                    headers:{"Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }

                } )
                response
                .then(res => {
                        console.log(res)
                        this.error=''
                        localStorage.setItem('token', res.data.access_token)
                        localStorage.setItem('role', res.data.role)
                        console.log(this.role)
                        this.$router.push('/dashboard').then(() => {
                        window.location.reload()
                    })
                        
                    }
                )
                .catch(err => {
                    console.log(err)
                    this.error=err.response.data.message;
                })
            },

            register: function() {
            const response = axios.post('http://127.0.0.1:5000/api/user_registration', JSON.stringify(this.FormData), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                }
            });
            response
                .then(res=>{
                    const container = document.getElementById('container');
                    container.classList.remove("active");  // shows login
                    console.log(res)
                }).catch(err => {
        console.log(err.response?.data?.message || "Registration failed");
        this.error = err.response?.data?.message || "Registration failed";
      });
}
            
          }
}

</script>



<template>
    <div class="container" id="container">
        <div class="form-container sign-up">
            <form id="reg" @submit.prevent="register">
                <h1>Create Account</h1>
                <div class="social-icons">
                    <a href="#" class="icon"><i class="fa-brands fa-google-plus-g"></i></a>
                    <a href="#" class="icon"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="#" class="icon"><i class="fa-brands fa-github"></i></a>
                    <a href="#" class="icon"><i class="fa-brands fa-linkedin-in"></i></a>
                </div>
                <input type="text" id="uname" v-model="FormData.username" placeholder="Enter your Name">
                <input type="email" id="uemail" v-model="FormData.email" placeholder="Enter your Email">
                <input type="password" id="pwd" v-model="FormData.password" placeholder="Enter Password">
                <input type="v-number" id="v-mn" v-model="FormData.vehicle_no" placeholder="Enter your vehicle-no">
                <button type="submit">Sign Up</button>
            </form>
        </div>
        <div class="form-container sign-in">
            <p  v-if="error">{{ error }}</p>
            <form id="sign-in" @submit.prevent="login">
                <h1>Sign In</h1>
                <div class="social-icons">
                    <a href="#" class="icon"><i class="fa-brands fa-google-plus-g"></i></a>
                    <a href="#" class="icon"><i class="fa-brands fa-facebook-f"></i></a>
                    <a href="#" class="icon"><i class="fa-brands fa-github"></i></a>
                    <a href="#" class="icon"><i class="fa-brands fa-linkedin-in"></i></a>
                </div>
                <span>or use your email password</span>
                <input type="email" id="email" v-model="FormData.email" placeholder="Email">
                <input type="password" id="password" v-model="FormData.password" placeholder="Password">
                <a href="/user_registration">New User? Create account now!!</a>
                <!-- <button @click="login">Sign In</button> -->
                <button type="submit">Sign In</button>
           
            </form>
        </div>
        <div class="toggle-container">
            <div class="toggle">
                <div class="toggle-panel toggle-left">
                    <h1>Welcome Back!</h1>
                    <p>Enter your personal details to use all of site features</p>
                    <button class="hidden" id="login">Sign In</button>
                </div>
                <div class="toggle-panel toggle-right">
                    <h1>Hello, Friend!</h1>
                    <p>Register with your personal details to use all of site features</p>
                    <button class="hidden" id="register">Sign Up</button>
                </div>
            </div>
        </div>
    </div>

   


</template>



<style scoped>
/* You can keep this empty for now or add your styles */
</style>