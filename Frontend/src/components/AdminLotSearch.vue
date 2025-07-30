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
            lotData:[]
        
        };
    },

    mounted(){
        this.default_lot();

    },




    methods:{
        lot_search: function(){
            const response = axios.post(
    'http://127.0.0.1:5000/api/admin/lot_search',JSON.stringify(this.FormData),{ // No filter
    
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            });
            response
                .then(res=>{
                    this.lotData=res.data.results
                    this.message=''
                }).catch(err=> {
                    console.log(err.response.data.message);
                    this.message=err.response.data.message;
                    this.lotData = [];
                })
        },
        default_lot: function(){
            const response = axios.post('http://127.0.0.1:5000/api/admin/lot_search', {} ,{
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem('token')}`
                }
            }); 
            response
                .then(res=>{
                    this.lotData=res.data.results
                    this.message=''
                }).catch(err=> {
                    console.log(err);
                    this.message=err.response.data.message;
                    this.lotData = [];
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
          <!-- <span>Welcome {{ userdata.username }}</span> -->
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
            <div class="search--box">
            <RouterLink to="/admin/user_search" class="btn-export">Users</RouterLink>
            </div>
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
          <router-link :to="`/user/profile/1`" class="btn-export">
           <i class="fas fa-user-circle fs-4"></i>
          </router-link>
        </div>
      </div>

      <!-- Parking History Table -->
      <!-- Lot Cards -->
    <div class="card-container mt-4">
      <h3 class="main-title">All Parking Lots</h3>
      <div class="d-flex flex-wrap">
        <div v-if="lotData.length === 0 && message">
            <p class="text-danger">{{ message }}</p>
        </div>
        <div
          v-for="(lot, index) in lotData"
          :key="lot.id"
          class="lot-card m-3 p-3 border rounded shadow-sm"
          style="width: 260px;"
        >
          <h5 class="fw-bold">{{ lot.prime_address }}</h5>

          <!-- Action Icons -->
          <RouterLink :to="`/admin/update_lot/${lot.id}`" class="text-warning me-2">
            <i class="fas fa-pencil-alt"></i>
          </RouterLink>
          <RouterLink :to="`/admin/delete_lot/${lot.id}`" class="text-danger">
            <i class="fas fa-trash-alt"></i>
          </RouterLink>

          <!-- Slot Grid -->
          <div class="slot-grid mt-2">
            <div class="slot-grid">
                  <router-link v-for="(slot, i) in lot.spots" :key="i" :to="`/admin/view_spot/${slot.id}`" class="slot-box"
                    :class="{
                              available: slot.status === 'A',
                              occupied: slot.status === 'O',
                              booked: slot.status === 'B'
                            }">{{ slot.status }}</router-link>
              </div>
          </div>
        </div>
      </div>
    </div>



    </div>

</template>



<style scoped>
/* Slot grid styling */
.slot-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  margin-top: 10px;
}

.slot-box {
  width: 30px;
  height: 30px;
  font-weight: bold;
  font-size: 14px;
  text-align: center;
  line-height: 30px;
  border-radius: 6px;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
}

.available {
  background-color: lightgreen;
  color: black;
}

.occupied {
  background-color: lightcoral;
  color: white;
}
.booked {
  background-color: rgb(244, 244, 116);
  color: black;
}
</style>

