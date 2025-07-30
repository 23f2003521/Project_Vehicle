<script>
import axios from 'axios'
export default{
    data(){
        return {
            FormData: {
                criteria:'',
                search:''
            },
            message:'',
            lotdata:[],
            username:'',
            userId:''
        
        };
    },

    mounted(){
        this.default_lot();

    },




    methods:{
        lot_search: function(){
            const response = axios.post('http://127.0.0.1:5000/api/user/lot_search',JSON.stringify(this.FormData),{ // No filter
    
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            });
            response
                .then(res=>{
                    this.lotdata=res.data.result
                    this.username=res.data.username
                    this.userId=res.data.user_id
                    this.message=""
                }).catch(err=> {
                    
                    console.log(err);
                    this.message=err.response.data.message;
                    this.lotdata = [];
                })
        },
        default_lot: function(){
            const response = axios.post('http://127.0.0.1:5000/api/user/lot_search', {} ,{
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            }); 
            response
                .then(res=>{
                    this.username=res.data.username
                    this.userId=res.data.user_id
                    
                    this.lotdata=res.data.result
                    this.message=''
                }).catch(err=> {
                    console.log(err);
                    this.message=err.response.data.message;
                    this.lotdata = [];
                })
        }
    }
}
</script>


<template>
<div class="main--content">
      <!-- Header -->
      <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome {{ this.username }}</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
             
            <div class="search--box">
            <form @submit.prevent="lot_search">
              <select v-model="FormData.criteria">
                <option value="">Select Category</option>
                <option value="address">Address</option>
                <option value="pincode">Pin code</option>
                <option value="primelocation">Prime Location</option>
              </select> 
              <input type="search" v-model="FormData.search" placeholder="Enter value here">
              <button type="submit" class="btn btn-success">Search</button>
            </form>
          </div>
          <router-link class="btn-export" :to="`/user/profile/${this.userId}`">
           <i class="fas fa-user-circle fs-4"></i>
          </router-link>
        </div>
      </div>

      <!-- Parking History Table -->
      <div class="tabular-wrapper">
        <h3 class="main-title">Lots Details</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th class="tcenter">ID</th>
                <th class="tcenter">Address</th>
                <th class="tcenter">Availability</th>
                <th class="tcenter">Action</th>
              </tr>
            </thead>
            <tbody>
                {{ message }}
              <tr v-for="entry in this.lotdata" :key="entry.id">
                <td class="tcenter">{{ entry.id }}</td>
                <td class="tcenter">{{ entry.address }}</td>
                <td class="tcenter">{{ entry.availability }}</td>
                <td class="tcenter">
                 <RouterLink :to="`/user/booking/${entry.id}`" class="btn btn-outline-primary fw-bold rounded px-4 py-2 flex-fill text-center">Book
                </RouterLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

</template>



<style>
</style>